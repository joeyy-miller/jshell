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
def print_err(err):
    print(jsh.userkey + "jsh error: " + err)

# Most standard output message, with the 'UserString' defined in data.json
def jmsg(msg):
    print(jsh.userkey + "jsh: " + str(msg))

# Most standard output message, without the 'jsh:' prepended
def jout(msg):
    print(jsh.userkey + str(msg))

''' Utilities '''
# Utility to remove a directory specified
def rm_dir(rm_directory):
    try:
        os.rmdir(rm_directory)
        jmsg("removed directory: " + rm_directory)
    except FileNotFoundError:
        print_err("not a valid directory: " + rm_directory)
    except:
        print_err("can't remove directory: " + rm_directory)

''' Main Loop for the user commands'''
def commands(user_input):

    # Replace any variables
    # Relace $output with the output of the last command
    if re.match("^(.*?)$output", user_input):
        output_index = user_input.index("$output")
        new_str = user_input[:output_index] + str(jsh.output) + user_input[output_index + 6:]
        user_input = new_str
    
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
            print_err("not a valid file: " + file_to_read)
        except:
            print_err("unknown error: " + file_to_read)
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
                print_err("not a valid directory: " + jsh.directory)
            except:
                print_err("unknown error: " + jsh.directory)

    # CLEAR (Clear the terminal screen)
    elif user_input == "clear" or user_input == "cls":
        clear = lambda: os.system('clear')
        clear()
    
    ## D ##
    # DELETE del
    elif (re.match("del (.*)", user_input) or re.match("rm (.*)", user_input)):
        if re.match("del (.*)", user_input):
            remove_file = user_input[4:]
        else:
            remove_file = user_input[3:]
        jmsg("deleting file" + remove_file)
        try:
            os.remove(remove_file)
        except IsADirectoryError:
            rm_dir(remove_file)
        except FileNotFoundError:
            print_err("not a valid file: " + remove_file)
        except PermissionError:
            print_err("permission denied: " + remove_file)
        except:
            print_err("unknown error: " + remove_file)

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
    elif user_input == "exit":
        sys.exit()

    ## F ##
        
    ## G ##
        
    ## H ##
    # HELP help
    elif user_input == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make, rm, rmdir, echo, clear")
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

        # Check long mode
        if (re.match("ls -(.*)l(.*)", user_input)):
            human_readable = True #-l flag is true, make long
        # Check color mode
        if (re.match("ls -(.*)c(.*)", user_input)):
            COLOR_OPTION = False #-l flag is true, make long

        dir_list = os.listdir(os.getcwd()) 
        # prints all files
        if not human_readable:
            max_length = -1;
            for jsh.directory in dir_list:
                if len(jsh.directory) > max_length:
                    max_length = len(jsh.directory)
            
            line_len = 70 # Max items per line
            count = 0 # Count the number of items printed
            for jsh.directory in dir_list:
                count += len(jsh.directory)
                if count >= line_len:
                    print(" ")
                    count = 0
                isFile = os.path.isfile(jsh.directory)
                if isFile:
                    if COLOR_OPTION:
                        # Print in color
                        print(ANSI.color_text(35) + jsh.directory + ANSI.color_text(0), end=" ")
                    else:
                        # Print without color
                        print(jsh.directory, end=" ")
                else:
                    if COLOR_OPTION:
                        print(ANSI.color_text(34) + jsh.directory + ANSI.color_text(0), end=" ")
                    else:
                        # Print without color
                        print(jsh.directory, end=" ")
                # print(jsh.directory + "  ", end=" ")
                for i in range(max_length - len(jsh.directory)):
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
            print_err("can't make file: " + new_file) 

    # COMMAND MANUAL man
    elif (re.match("man(.*)", user_input)):

        # LS Manual
        if user_input == "man ls":
            jmsg("ls: command to list files.")
            jmsg("  This command allows you to list all the files in a folder.")
            jmsg("  Colors: Files show up as PURPLE in color. Folders are BLUE in color.")
            jmsg("  flags:")
            jmsg("  -l This is the 'long' command flag, it shows you the date created, along with the permissions.")
            jmsg("  -h This is the 'human readbale' flag, it makes it easier to understand file permissions, etc.")
            jmsg("  -c This is the 'colorless' flag, prints the file and folder names wihtout color.")

        # KEY Manual
        if user_input == "man key":
            jmsg("key: command to set the key before the command.")
            jmsg("  This command allows you to set the key before the command.")
            jmsg("  Example: key >")
            jmsg("  This will set the key to '>'.")
            jmsg("  The key is the symbol that appears before the command.")
            jmsg("  The default key is '$'.")
            jmsg("  The key is used to show the user that the shell is ready for a command.")
            jmsg("  flags:")
            jmsg("   none")            

        # User did not specify which command to get a manaul for
        elif user_input == "man":
            jmsg("man error: Manual for commands. Enter a command after 'man' to read its manual.")
            jmsg("  Supported commands: ls")

    # MAKE jsh.directory mkdir or mkd
    elif (re.match("mkdir (.*)", user_input) or re.match("mkd (.*)", user_input)):
        try:
            jsh.directory = user_input[6:]
            os.mkdir(jsh.directory)
        except:
            print_err("can't make jsh.directory: " + jsh.directory)

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
        file_to_read = user_input[5:]
        st = os.stat(file_to_read)
        oct_perm = oct(st.st_mode)
        mask = oct(os.stat(file_to_read).st_mode)[-3:]
        print(mask)
        print(oct_perm)
    
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

    ## U ##
    ## V ##
    ## W ##
    ## X ##
    ## Y ##
    ## Z ##
        

    # ERRORS
    # NO INPUT
    elif user_input == "":
        print_err("no input.")

    # UNKOWN COMMAND
    else:
        print_err("command not found: '" + user_input + "'.")

    ## END COMMAND LIST ##

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