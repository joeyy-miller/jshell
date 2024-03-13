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
        self.version = "0240311d" # Example: 0230417e -> 023 (2023) 04 (April) 17 (17th) e (5th version of the day)
        self.directory = ""
        self.userkey = jsettings['UserString']
        self.output = ""
        self.key = "$"
        self.debug = False # Debug mode

# Define the color codes of the outputs     
class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)
    def style_text(code):
        return "\33[{code}m".format(code=code)
    def color_text(code):
        return "\33[{code}m".format(code=code)

''' Output Functions '''
# Printing the standard error output messages
def jerror(err):
    print(jsh.userkey + "jsh error: " + err)

# Most standard output message, with the 'UserString' defined in data.json
def jmsg(msg):
    print(jsh.userkey + "jsh: " + str(msg))

# Most standard output message, without the 'jsh:' prepended
def jout(msg):
    print(jsh.userkey + str(msg))

def msg(message):
    print(str(message))

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

''' Main Loop for the user commands'''
def commands(user_input):

    ''' First Replace Any Variables in User Input '''
    # Replace any variables
    # Relace $output with the output of the last command

    if (jsh.output != ""):
        user_input = user_input.replace("$output", str(jsh.output))

    ''' Break Up User Input '''
    
    # Split the string by spaces
    parts = user_input.split()

    # Initialize variables
    command = ""
    options = []
    arguments = []

    # Process each part
    for part in parts:
        if part.startswith('-') and not command:  # Assuming options only come after the command
            # Extract options and remove the dash, then convert to a list for individual access
            options.extend(list(part[1:]))
        elif not command:
            # The first non-option part is the command
            command = part
        else:
            # Everything else is considered an argument
            arguments.append(part)

    '''
    For future reference:
    for option in options: 
        print(f"Option: {option}")
    '''


    print("USER INTPUT: " + user_input)
    
    ## START COMMAND LIST ##
    # This is where we start checking user_input for commands
    ## A ##
    # ABOUT about prints the version of jshell
    if user_input == "about":
        jmsg("jshell version " + jsh.version)
    
    ## B ##
    ## C ##
    # Cat command: cat
    elif (re.match("cat (.*)", user_input)):
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
    elif (re.match("cd (.*)", user_input)):
        if user_input == "cd ..":
            os.chdir("..")
            jsh.directory = os.path.abspath(os.curdir)
            jmsg("Moved up to: " + jsh.directory)
        else:
            jsh.directory = user_input[3:]
            try:
                os.chdir(jsh.directory)
            except FileNotFoundError:
                jerror("not a valid directory: " + jsh.directory)
            except:
                jerror("unknown error: " + jsh.directory)

    # CLEAR (Clear the terminal screen)
    elif user_input == "clear" or user_input == "cls":
        clear = lambda: os.system('clear')
        clear()
    
    ## D ##
    # DEBUG debug (adds additonal infromation for debugging)
    elif user_input == "debug":
        if jsh.debug:
            jsh.debug = False
            jmsg("debug mode off")
        else:
            jsh.debug = True
            jmsg("debug mode on")
        

    
    # DELETE del
    elif (re.match("del (.*)", user_input) or re.match("rm (.*)", user_input) or command == "delete"):
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
    elif (re.match("echo (.*)", user_input)):
        echo = user_input[5:]
        jsh.ouput = echo
        print(echo)

    # EXIT exit
    elif user_input == "exit" or user_input == "quit" or user_input == "q" or user_input == "close" or user_input == "bye" or user_input == "goodbye" or user_input == "end" or user_input == "stop" or user_input == "halt" or user_input == "terminate" or user_input == "kill" or user_input == "destroy":
        sys.exit()

    ## F ##
        
    ## G ##
        
    ## H ##
    # HELP help
    elif user_input == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make...")
        msg("           rm, rmdir, echo, clear, man, key, output, perm, touch.")
        jmsg("use: man [command] for more information on a command.")
        jmsg("use $output to use the output of the last command in your current command.")
        jmsg("type 'exit' to exit jshell.")

    # KEY lets a user define which symbol appears before their command
    elif (re.match("key(.*)", user_input)):
        set_key = jsh.directory = user_input[4:]
        if (len(set_key) <= 0):
            set_key = input("Please enter the key you would like to set: ")
            
        # Set the key
        jsh.key = set_key
        jmsg("Key set to: " + jsh.key)
        
    ## I ##
    ## J ##
    ## K ##
    ## L ##

    # LIST FILES ls
    elif (re.match("ls (.*)", user_input) or user_input == "ls"):
        LOOP = 0 # Used to not add spacing to the first loop in the long flag list.
        # Check flags
        human_readable = False
        COLOR_OPTION = True
        SHOW_HIDDEN_FILES = False

        # Check long mode
        if (re.match("ls -(.*)l(.*)", user_input)):
            human_readable = True #-l flag is true, make long
        # Check color mode
        if (re.match("ls -(.*)c(.*)", user_input)):
            COLOR_OPTION = False #-l flag is true, make long
        if (re.match("ls -(.*)a(.*)", user_input) or re.match("ls -(.*).(.*)", user_input)):
            SHOW_HIDDEN_FILES = True #-a or h flag is true, show hidden files


        dir_list = os.listdir(os.getcwd()) 
        # prints all files
        if not human_readable:
            max_length = -1
            for directory in dir_list:
                if not SHOW_HIDDEN_FILES and directory.startswith('.'):
                    continue  # Skip hidden files if SHOW_HIDDEN_FILES is False
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
                    if COLOR_OPTION:
                        # Print in color
                        print(ANSI.color_text(35) + directory + ANSI.color_text(0), end=" ")
                    else:
                        # Print without color
                        print(directory, end=" ")
                else:
                    if COLOR_OPTION:
                        print(ANSI.color_text(34) + directory + ANSI.color_text(0), end=" ")
                    else:
                        # Print without color
                        print(directory, end=" ")
                # Adjust spacing
                for i in range(max_length - len(directory)):
                    print(" ", end="")
                    count += 1
            print(" ")
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

                if COLOR_OPTION:
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
    elif (re.match("make (.*)", user_input) or re.match("mk (.*)", user_input)):
        try:
            new_file = user_input[5:]
            open(new_file, 'w').close() 
            jmsg("made file: " + new_file)
        except:
            jerror("can't make file: " + new_file) 

    # COMMAND MANUAL man
    elif (re.match("man(.*)", user_input)):

        # LS Manual
        if user_input == "man ls":
            msg("ls: command to list files.")
            msg("  This command allows you to list all the files in a folder.")
            msg("  Colors: Files show up as PURPLE in color. Folders are BLUE in color.")
            msg("  flags:")
            msg("  | -l | This is the 'long' command flag, it shows you the date created, along with the permissions, and hidden files.")
            #msg("  | -h | This is the 'human readbale' flag, it makes it easier to understand file permissions, etc.") NOT IMPLEMENTED
            msg("  | -c | This is the 'colorless' flag, prints the file and folder names wihtout color.")
            msg("  | -a | This is the 'all' flag, it shows all files, including hidden files.")
            msg("  | -. | Alias for the 'all' flag, same as typing -a.")

        # PERM Manual
        elif user_input == "man perm":
            msg("perm: command to change the permissions of a file.")
            msg("  This command allows you to read or change the permissions of a file.")
            msg("  Reading Permissions: perm [file]")
            msg("  Changing Permissions: perm [file] [permissions]")
            msg("  Example: perm file.txt 777")
            msg("  This will set the file.txt to have full permissions.")
            msg("  flags:")
            msg("  | -o | Octal mode, shows the file permissions in octal.")

        # KEY Manual
        elif user_input == "man key":
            msg("key: command to set the key before the command.")
            msg("  This command allows you to set the key before the command.")
            msg("  Example: key >")
            msg("  This will set the key to '>'.")
            msg("  The key is the symbol that appears before the command.")
            msg("  The default key is '$'.")
            msg("  The key is used to show the user that the shell is ready for a command.")
            msg("  flags:")
            msg("   none")            

        # User did not specify which command to get a manaul for
        elif user_input == "man":
            jmsg("man error: Manual for commands. Enter a command after 'man' to read its manual.")
            msg("  Supported commands: ls, perm. key")

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
    elif user_input == "output" or user_input == "out":
        print(jsh.output)

    ## P ##
    # PRINT WORKING jsh.directory pwd
    elif user_input == "pwd":
        jsh.ouput = jsh.directory
        jmsg(jsh.directory)

    elif re.match("perm (.*)", user_input):

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

        if (word3 == None):
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
        else:
            # User is using the perm command to *change* the file permissions
            permissions = word3
            change_file_permissions(file_to_read, permissions)
            
    
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
    ## W ##
    ## X ##
    ## Y ##
    ## Z ##
        

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
        msg(f"Command: {command}")
        msg(f"Options: {options}")
        msg(f"Arguments: {arguments}")
        msg(f"User Input: {user_input}")
        msg(f"jshell Output: {jsh.output}")
        msg('') # extra line

''' Main '''
def main():
    os.system("clear")
    jsh.directory = os.path.abspath(os.curdir)
    while True:
        print(jsh.key + " ", end="")
        commands(input())

''' Start Up '''
# Define the data structure settings for the shell
usersettings = open("data.json", "r")
jsettings = json.load(usersettings)


# Creat the Jshell Object to store data about the perons shell
jsh = jshell()
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