#############################
#    jshell                 #
# light weight macOS shell  #
#  in the style of bash     #
#############################


# Imports
import sys
import re
import os
import time
import json
from datetime import date
from datetime import datetime

''' Jshell Classes '''
# Information about jshell, system and user settings
class jshell:
    key = ">" # Key to start a command
    def __init__(self):
        self.build = "0240314e" # Example: 0230417e -> 023 (2023) 04 (April) 17 (17th) e (5th build of the day)
        self.version = "0.5.1" # Main version number
        self.release = "beta" # Alpha, Beta, Release
        self.directory = "" # Stores the current directory the terminal is modifying
        self.userkey = jsettings['UserString']
        self.username = jsettings['UserName']
        self.output = "" # Stores the output of the last command
        self.debug = False # Debug mode, default False
        self.color = True # Color mode, default True
        self.MAX_OUTOUT_LENGTH = 150 # The maximum length of the output of a command
        self.variables = {} # A dictionary to store variables
        self.last_command_output = "" # A string that stores what was sent to jmsg last

    @staticmethod
    def save_settings():
        """
        Save the user settings UserName and UserString to the data.json file.
        """
        file_name = 'data.json'
        
        # Check if the file exists
        if os.path.exists(file_name):
            # File exists, read it
            with open(file_name, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    # File is empty or corrupt; start with an empty dict
                    data = {}
        else:
            # File does not exist; start with an empty dict
            data = {}
        
        # Update settings
        data['UserName'] = jsh.username
        data['UserString'] = jsh.userkey
        
        # Write updated settings back to the file
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

    # Used for testing to execute a command
    def execute_command(self, command):
        input(command)
        return self.last_command_output


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.type = self.determine_type()

    def determine_type(self):
        if isinstance(self.value, str):
            return 'string'
        elif isinstance(self.value, (int, float)):
            return 'number'
        else:
            return 'unknown'
    
    def __str__(self):
        return f"{self.value}"

# Define the color codes of the outputs     
class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code) # Background color
    def style_text(code):
        return "\33[{code}m".format(code=code) # Style of the text
    def color_text(code):
        return "\33[{code}m".format(code=code) # Color of the text
    
# Color Codes
PURPLE = 35
BLUE = 34
Debug = False

''' Output Functions '''
# Printing the standard error output messages
def jerror(err):

    err = str(err)
    loop_count = 0
    ERROR_STRING = "jsh error: "
    ELIPSE = "..."

    while len(err) > 0:
        if (len(err) > jsh.MAX_OUTOUT_LENGTH):
            print(jsh.userkey + ERROR_STRING + err[:jsh.MAX_OUTOUT_LENGTH - (len(ERROR_STRING) + len(ELIPSE))] + ELIPSE) # We know we are going to print another line below this one, so add elipses
        else:
            print(jsh.userkey + ERROR_STRING + err) # not going to print an addtional line.
        err = err[jsh.MAX_OUTOUT_LENGTH:] # Remove the first 100 characters from the string that we just printed
        loop_count += 1
        if (loop_count >= 1):
            # Only show error string on the first line
            ERROR_STRING = ""
        
# Most standard output message, with the 'UserString' defined in data.json
def jmsg(msg):

    msg = str(msg)
    jsh.last_command_output = str(msg)
    ELIPSE = "..."
    JSH_STRING = "jsh: "

    while len(msg) > 0:
        if (len(msg) > jsh.MAX_OUTOUT_LENGTH):
            print(jsh.userkey + JSH_STRING + msg[:jsh.MAX_OUTOUT_LENGTH - (len(ELIPSE) + len(ELIPSE))] + "...") 
        else:
            print(jsh.userkey + "jsh: " + msg) 
        msg = msg[jsh.MAX_OUTOUT_LENGTH:] 

# Most standard output message, without the 'jsh:' prepended
def jout(msg):

    msg = str(msg)
    jsh.last_command_output = str(msg)
    ELIPSE = "..."

    while len(msg) > 0:
        if (len(msg) > jsh.MAX_OUTOUT_LENGTH):
            print(msg[:jsh.MAX_OUTOUT_LENGTH - len(ELIPSE)] + ELIPSE) # We know we are going to print another line below this one, so add elipses
        else:
            print(msg) # not going to print an addtional line.
        msg = msg[jsh.MAX_OUTOUT_LENGTH:] # Remove the first 100 characters from the string that we just printed


''' Utilities '''
# Utility to remove a directory specified
def rm_dir(rm_directory):
    try:
        os.rmdir(rm_directory)
        jmsg("removed directory: " + rm_directory)
    except FileNotFoundError:
        jerror("not a valid directory: " + rm_directory)
    except:
        jerror("can't remove directory: " + rm_directory)

def change_file_permissions(file_path, permissions):
    # Convert the string permissions to an octal number
    mode = int(permissions, 8)
    
    # Change the file permissions
    os.chmod(file_path, mode)

def process_input(user_input, variables):
    """
    Process variable redefinitions in user_input, updating or adding to the variables structure.
    Replace variable uses in the text with their values, excluding redefinitions.

    :param user_input: String potentially containing variable redefinitions and uses.
    :param variables: Dictionary mapping variable names to their Variable instances.
    :return: Modified user_input with variable uses replaced by their values.
    """
    # Regex patterns for variable definition and usage
    definition_pattern = r'\$(\w+)\s*=\s*"([^"]*)"|\$(\w+)\s*=\s*(\d+(?:\.\d+)?)'
    usage_pattern = r'\$(\w+)'

    # Update variables with any definitions found
    for match in re.finditer(definition_pattern, user_input):
        name, string_value, number_name, number_value = match.groups()
        if name:  # String variable
            variables[name] = Variable(name, string_value)
        elif number_name:  # Number variable
            number_value = float(number_value) if '.' in number_value else int(number_value)
            variables[number_name] = Variable(number_name, number_value)

    # Function to replace matches with their values
    def replace_function(match):
        variable_name = match.group(1)
        if variable_name in variables:
            return str(variables[variable_name])
        return match.group(0)  # Return the original string if no variable found

    # Replace variable uses in the input
    modified_input = re.sub(usage_pattern, replace_function, user_input)

    return modified_input



''' Main Loop for the user commands'''
def commands(user_input):

    ''' First Replace Any Variables in User Input '''
    # Replace stock variable, $output, with the output of the last command
    # Relace $output with the output of the last command
    if (jsh.output != ""):
        ser_input = user_input.replace("$output", str(jsh.output))

    # Replace any other variables
    IF_VARIABLE = False # Used in input to check if the user is creating a variable
    user_input_old = user_input
    user_input = process_input(user_input, jsh.variables)

    if user_input != user_input_old:
        IF_VARIABLE = True

    ''' Create any new variables 
    # Regex pattern to match variable definitions
    # This pattern assumes variable names are alphanumeric + underscore, and values are in double quotes
    pattern = r'\$(\w+)\s*=\s*"([^"]*)"'
    # Find all matches in the user input
    matches = re.findall(pattern, user_input)
    
    IF_VARIABLE = False # Used in input to check if the user is creating a variable
    # Iterate over matches and assign to dictionary
    for match in matches:
        variable_name, variable_value = match
        jsh.variables[variable_name] = variable_value
        jmsg(f"Created variable '{variable_name}' with value '{variable_value}'")
        IF_VARIABLE = True # The user created a variable
    '''

    ''' Break Up User Input '''
    # Split the string by spaces
    parts = user_input.split()
    # Initialize variables
    command = ""
    options = []
    arguments = []
    # Process each option
    for part in parts:
        if part.startswith('-') and not command:  # Assuming options only come after the command
            # Extract options and remove the dash, then convert to a list for individual access
            options.extend(list(part[1:]))
        elif not command:
            # The first non-option option is the command
            command = part
        else:
            # Everything else is considered an argument
            arguments.append(part)
    '''
    For future reference:
    for option in options: 
        print(f"Option: {option}")
    '''

    ## START COMMAND LIST ##
    # This is where we start checking user_input for commands
    ## A ##
    # ABOUT about prints the build of jshell
    if user_input == "about":
        if jsh.debug:
            jmsg("jshell build: " + jsh.build + " build:" + jsh.version)
        jmsg("jshell build " + jsh.version)
    
    ## B ##
    ## C ##
    # Cat command: cat
    elif command == "cat":
        if (arguments[1] == ">>"):
            file_to_write = arguments[0]
            try:
                with open(file_to_write, 'a') as file:
                    cat_length = 3 + len(arguments[0] + arguments[1])
                    file.write(user_input[cat_length:])
                    jmsg("wrote to file: " + file_to_write)
            except FileNotFoundError:
                jerror("not a valid file: " + file_to_write)
            except:
                jerror("unknown error: " + file_to_write)
        else:
            file_to_read = user_input[4:]
            try:
                with open(file_to_read, 'r') as file:
                    jout(file.read())
            except FileNotFoundError:
                jerror("not a valid file: " + file_to_read)
            except:
                jerror("unknown error: " + file_to_read)
    elif user_input == "cat":
        jmsg("cat error: Please enter a file to print the contents of.")
    
    # (Change Directory) command: cd
    elif command == "cd" or command == "chdir":
        if arguments[0] == "..":
            os.chdir("..")
            jsh.directory = os.path.abspath(os.curdir)
            jmsg("Moved up to: " + jsh.directory)
        else:
            jsh.directory = arguments[0]
            try:
                os.chdir(jsh.directory)
            except FileNotFoundError:
                jerror("not a valid directory: " + jsh.directory)
            except:
                jerror("unknown error: " + jsh.directory)

    elif command == "cp" or command == "copy":
        if re.match("cp (.*) (.*)", user_input):
            file_to_copy = arguments[0]
            new_file = arguments[1]
            try:
                with open(file_to_copy, 'r') as file:
                    with open(new_file, 'w') as new_file:
                        new_file.write(file.read())
                jmsg("copied file: " + file_to_copy + " to " + new_file)
            except FileNotFoundError:
                jerror("not a valid file: " + file_to_copy)
            except:
                jerror("unknown error: " + file_to_copy)
        else:
            jerror("cp error: Please enter a file to copy and a new file to copy it to.")

    # CLEAR (Clear the terminal screen)
    elif command == "clear" or command == "cls":
        clear = lambda: os.system('clear')
        clear()
    
    # COLOR (Toggle color mode)
    elif command == "color":
        if jsh.color:
            jsh.color = False
            jmsg("color mode off")
        else:
            jsh.color = True
            jmsg("color mode on")
    
    ## D ##
    # DEBUG debug (adds additonal infromation for debugging)
    elif command == "debug":
        if jsh.debug:
            jsh.debug = False
            jmsg("debug mode off")
        else:
            jsh.debug = True
            jmsg("debug mode on")
        

    
    # DELETE del
    elif command == "del" or command == "rm" or command == "delete":
        if re.match("del (.*)", user_input):
            remove_file = arguments[0]
        else:
            remove_file = arguments[0]
        jmsg("deleting file " + remove_file)
        try:
            os.remove(remove_file)
        except IsADirectoryError:
            rm_dir(remove_file)
        except FileNotFoundError:
            jerror("not a valid file: " + remove_file)
        except PermissionError:
            jerror("permission denied: " + remove_file)
        except:
            jerror("unknown error: " + remove_file)

    ## E ##
    # ECHO DATE date    
    elif user_input == "date":
        today = date.today()
        jsh.output = today
        jmsg(today)

    # ECHO echo
    elif command == "echo":
        echo = user_input[5:]
        jsh.ouput = echo
        jout(echo)

    # EXIT exit
    elif user_input == "exit" or user_input == "quit" or user_input == "q" or user_input == "close" or user_input == "bye" or user_input == "goodbye" or user_input == "end" or user_input == "stop" or user_input == "halt" or user_input == "terminate" or user_input == "kill" or user_input == "destroy":
        sys.exit()

    ## F ##
    ## G ##
    
    ## H ##
    # HELP help
    elif command == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make...")
        jout("           rm, rmdir, echo, clear, man, key, output, perm, touch, whoami, color.")
        jout("use: man [command] for more information on a command. 'man jsh' for additional manual pages.")
        jout("use $output to use the output of the last command in your current command.")
        jout("type 'exit' to exit jshell.")

    # KEY lets a user define which symbol appears before their command
    elif command == "key":
        set_key = user_input[4:]
        if (len(set_key) <= 0):
            set_key = input("Please enter the key you would like to set: ")
            
        # Set the key
        jsh.userkey = str(set_key)
        jmsg("Key set to: " + jsh.userkey)

        # Save the key to data.json
        jsh.save_settings()
        
    ## I ##
    ## J ##
    ## K ##
    ## L ##

    # LIST FILES ls
    elif command == "ls" or command == "list":
        LOOP = 0 # Used to not add spacing to the first loop in the long flag list.
        # Check flags
        human_readable = False
        COLOR_OPTION = True
        SHOW_HIDDEN_FILES = False

        # Check long/list mode, display in list
        if (re.match("ls -(.*)l(.*)", user_input)):
            human_readable = True #-l flag is true, make long
        # Check color mode, display color
        if (re.match("ls -(.*)c(.*)", user_input)):
            COLOR_OPTION = False #-l flag is true, make long
        # Check for all mode, show hidden files
        if (re.match("ls -(.*)a(.*)", user_input) or re.match("ls -(.*).(.*)", user_input)):
            SHOW_HIDDEN_FILES = True #-a or h flag is true, show hidden files


        dir_list = os.listdir(os.getcwd()) 

        # Normal LS usage. Not with the -l flag
        if not human_readable:
            max_length = -1
            for directory in dir_list:
                if not SHOW_HIDDEN_FILES and directory.startswith('.'):
                    continue  # Skip hidden files if SHOW_HIDDEN_FILES is False
            
                if len(directory) > 0:
                    if len(directory) > max_length:
                        max_length = len(directory)

            line_len = 70  # Max items per line
            count = 0  # Count the number of items printed
            for directory in dir_list:
                if not SHOW_HIDDEN_FILES and directory.startswith('.'):
                    continue  # Skip hidden files if SHOW_HIDDEN_FILES is False
                count += len(directory)
                if count >= line_len:
                    print(" ")
                    count = 0
                isFile = os.path.isfile(directory)
                if isFile:
                    if COLOR_OPTION and jsh.color:
                        # Print in color
                        print(ANSI.color_text(BLUE) + directory + ANSI.color_text(0), end=" ")
                    else:
                        # Print without color
                        print(directory, end=" ")
                else: # It's a folder
                    if COLOR_OPTION and jsh.color:
                        print(ANSI.color_text(PURPLE) + "[" + directory + "]" + ANSI.color_text(0), end=" ")
                    else:
                        # Print without color
                        print(directory, end=" ")
                # Adjust spacing
                for i in range(max_length - len(directory)):
                    print(" ", end="")
                    count += 1
            print(" ")
        # Print in long mode, with the -l flag
        else:
            max_length = -1;
            count = 0
            for jsh.directory in dir_list:
                if (LOOP == 0):
                    if len(jsh.directory) > max_length:
                        max_length = len(jsh.directory)
                    print(" ", end="")
                LOOP += 1

            for jsh.directory in dir_list:
                # Give us the current file
                file_to_read = jsh.directory

                # Get the file modifed date
                file_modifed = str(time.ctime(os.path.getmtime(file_to_read)))

                # Get the file's permissions
                st = os.stat(file_to_read)
                oct_perm = oct(st.st_mode)
                mask = oct(os.stat(file_to_read).st_mode)[-3:] # convert the permissions 
                isFile = os.path.isfile(jsh.directory)

                if COLOR_OPTION and jsh.color:
                    # Print in color
                    if isFile:
                        print("r: " + mask + " m: " + file_modifed + " f: " + ANSI.color_text(35) + jsh.directory + ANSI.color_text(0))
                    else:
                        print("r: " + mask + " m: " + file_modifed + " f: " + ANSI.color_text(34) + jsh.directory + ANSI.color_text(0))
                else:
                    # Print with no color.
                    print("r:" + mask + " m:" + file_modifed + " f:" + jsh.directory)

    ## M ##
                    
    # MAKE FILE make or mk
    elif command == "make" or command == "mk":
        try:
            new_file = user_input[5:]
            open(new_file, 'w').close() 
            jmsg("made file: " + new_file)
        except:
            jerror("can't make file: " + new_file) 

    # MAKE DIRECTORY mkdir or mkd
    elif (command == "mkdir" or command == "mkd" or command == "makefolder" or command == "folder" or command == "makedir"):
        try:
            jsh.directory = arguments[0]
            os.mkdir(jsh.directory)
        except FileExistsError:
            jerror("directory already exists: " + jsh.directory)
        except:
            jerror("can't make jsh.directory: " + jsh.directory)
        else:
            jmsg("created directory: " + jsh.directory)
        finally:
            # Just wanted to show the use of the this keyword in Pyhton.
            created = False

    # COMMAND MANUAL man
    elif command == "man":

        # LS Manual
        if user_input == "man ls":
           jout("ls: command to list files.")
           jout("  This command allows you to list all the files in a folder.")
           jout("  Colors: Files show up as BLUE in color. Folders are PURPLE in color, and sorounded in brackets.")
           jout("  flags:")
           jout("  | -l | This is the 'long' command flag, it shows you the date created, along with the permissions, and hidden files.")
           #msg("  | -h | This is the 'human readbale' flag, it makes it easier to understand file permissions, etc.") NOT IMPLEMENTED
           jout("  | -c | This is the 'colorless' flag, prints the file and folder names wihtout color.")
           jout("  | -a | This is the 'all' flag, it shows all files, including hidden files.")
           jout("  | -. | Alias for the 'all' flag, same as typing -a.")

        # PERM Manual
        elif user_input == "man perm":
           jout("perm: command to change the permissions of a file.")
           jout("  This command allows you to read or change the permissions of a file.")
           jout("  Reading Permissions: perm [file]")
           jout("  Changing Permissions: perm [file] [permissions]")
           jout("  Example: perm file.txt 777")
           jout("  This will set the file.txt to have full permissions.")
           jout("  flags:")
           jout("  | -o | Octal mode, shows the file permissions in octal.")

        # KEY Manual
        elif user_input == "man key":
           jout("key: command to set the key before the command.")
           jout("  This command allows you to set the key before the command.")
           jout("  Example: key >")
           jout("  This will set the key to '>'.")
           jout("  The key is the symbol that appears before the command.")
           jout("  The default key is '$'.")
           jout("  The key is used to show the user that the shell is ready for a command.")
           jout("  flags:")
           jout("   none")

        # JShell Manual
        elif user_input == "man jsh":
            jout("How to use jshell:")
            jout("Commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make, rm, rmdir, echo, clear, color, man, key, output, perm, touch.")
            jout("Color Mode: type 'color' to turn on/off color mode. This will show the output in color.")
            jout("Variables: You can use the $output variable to use the output of the last command that shows an output in your current command.")
            jout("           You can also create your own variables by typing '$[variable name] = [value]'")
            jout("           Example: $name = 'John'. Variables can be an integer or number. They cannot be assigned to eachother.")
            jout("           See a list of made variables by typing 'variable' or 'var. Variables can be used in the same way as $output.")
            jout("Debug Mode: type 'debug' to turn on/off debug mode. This will show additional information about the command.")
            jout("type 'exit' to exit jshell.")

        # User did not specify which command to get a manaul for
        elif command == "man":
            jmsg("man error: Manual for commands. Enter a command after 'man' to read its manual.")
            jout("  Supported commands: ls, perm. key")

    # MAKE jsh.directory mkdir or mkd
    elif (re.match("mkdir (.*)", user_input) or re.match("mkd (.*)", user_input)):
        try:
            jsh.directory = user_input[6:]
            os.mkdir(jsh.directory)
        except:
            jerror("can't make jsh.directory: " + jsh.directory)

    ## N ##
    ## O ##
            
    # OUTPUT output or out
    elif command == "output" or command == "out":
        print(jsh.output)

    ## P ##
    # PRINT WORKING jsh.directory pwd
    elif command == "pwd":
        jsh.ouput = jsh.directory
        jmsg(jsh.directory)

    elif command == "perm":

        OCTAL_MODE = False
        # Check octal mode
        if (re.match("perm -(.*)o(.*)", user_input)):
            OCTAL_MODE = True #-o flag is true, show the octal file permission
            user_input = user_input.replace("-o", "")

        # Splitting the string into a list of words
        words = user_input.split()       
        # Initializing variables to None
        word1 = word2 = word3 = None        

        # Assigning each word to a separate variable based on the number of words present
        if len(words) >= 1:
            word1 = words[0]
        if len(words) >= 2:
            word2 = words[1]
        if len(words) == 3:
            word3 = words[2]

        file_to_read = word2

        if (word3 == None) and (word2 != None):
            # User is using the perm command to *output* the file permissions
            try:
                # Get the stat information on the file
                st = os.stat(file_to_read)
                # Get permissions in octal of the file
                oct_perm = oct(st.st_mode)

                if (OCTAL_MODE == False):
                    # Don't convert from octal to decimal
                    mask = oct(os.stat(file_to_read).st_mode)[-3:]

                print(mask)
                #print(oct_perm)
            except FileNotFoundError:
                jerror("not a valid file: " + file_to_read)
        elif (word3 != None) and (word2 != None):
            # User is using the perm command to *change* the file permissions
            permissions = word3
            change_file_permissions(file_to_read, permissions)
        else:
            jerror("perm error: Please enter a file to read or change the permissions of.")
            
    
    ## Q ##
    ## R ##
    ## S ##
    ## T ##
        
    # TIME Echos the current time to the terminal
    elif user_input == "time":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        jsh.output = current_time
        jmsg("Current Time: " + current_time)

    # TOUCH Creates a new file
    elif command == "touch":
        # Come back to this later
        if len(arguments) != 0:
            FILE_NAME = arguments[0]
            try:
                file = open(FILE_NAME, "x")
                file.close()
            except FileExistsError:
                jerror("file already exists: " + FILE_NAME)
            except:
                jerror("can't make file: " + FILE_NAME)
        else:
            jerror("no file specified.")
       

    ## U ##
    ## V ##
    elif command == "var" or command == "variable":
        jmsg("Variables:")
        for var in jsh.variables.values():
            jout(f"Name: {var.name}, Value: {var.value}, Type: {var.type}")
    ## W ##
    elif command == "width":
        try:
            width = int(arguments[0])
            jsh.MAX_OUTOUT_LENGTH = width
        except:
            jerror("width error: Please enter a number.")
        jout("Width: " + str(jsh.MAX_OUTOUT_LENGTH))
        #jout("Width: " + str(os.get_terminal_size().columns))

    elif command == "whoami":
        if len(arguments) >= 1:
            jsh.username = arguments[0]
            jout("Your newusername is: " + jsh.username)
        else:
            if (jsh.username):
                jout("Your username is " + jsh.username)
            else:
                jout("You do not have a username set.")
                jout("Type your username...")
                user_name = input()
                if (user_name):
                    jsh.username = user_name
                    # Save changes to username..
                    jsh.save_settings()
                else:
                    jerror("Unable to change username")
        

    ## X ##
    ## Y ##
    ## Z ##
            
    elif IF_VARIABLE:
        # If the user created a variable, let them know it was created, without causing a no input error.
        test = 0
        

    # ERRORS
    # NO INPUT
    elif user_input == "":
        jerror("no input.")

    # UNKOWN COMMAND
    else:
        jerror("command not found: '" + user_input + "'.")
        

    ## END COMMAND LIST ##
        
    # If the user is in debug mode, print addtion information at the end of the command
    if jsh.debug:
       jout(f"Command: {command}")
       jout(f"Options: {options}")
       jout(f"Arguments: {arguments}")
       jout(f"User Input: {user_input}")
       jout(f"jshell Output: {jsh.output}")
       jout(f"jshell Last Output: {jsh.last_command_output}")
       jout('') # extra line

''' Main '''
def main():
    os.system("clear")
    jsh.directory = os.path.abspath(os.curdir)
    while True:
        print(jsh.userkey + " ", end="")
        commands(input())

''' Start Up '''
# Define the data structure settings for the shell
usersettings = open("data.json", "r")
jsettings = json.load(usersettings)


# Creat the Jshell Object to store data about the perons shell

global jsh
jsh = jshell()
usersettings.close()
if __name__ == "__main__":
    main()

# TODO:
# Add -a to LS to show the hidden files (currently it always shows the hidden files)
# Fix the extra space at the begining of the -l flag in ls.
# Add more commands to the manual command.
# Add a way to peak in and see the first couple lines of a file aka peak command

# Change the way that user input works... split it up like this:
# Have a flag array flag[1] = "-l" flag[2] = "-h" flag[3] = "-c"
# Have a arguments array command = "ls" arguments[1] = "file.txt" arguments[2] = "777"
# Have one variable for the command itself. command = "ls"