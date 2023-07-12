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
        self.version = "0230417e"
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
    if re.match("^(.*?)output", user_input):
        output_index = user_input.index("output")
        new_str = user_input[:output_index] + str(jsh.output) + user_input[output_index + 6:]
        user_input = new_str
    
    # Start checking user_input for commands
    # ABOUT about
    if user_input == "about":
        jmsg("jshell version " + jsh.version)
    
    # CHANGE jsh.directory cd
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
        
    # ECHO DATE date    
    elif user_input == "date":
        today = date.today()
        jsh.output = today
        jmsg(today)

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

    # ECHO echo
    elif (re.match("echo (.*)", user_input)):
        echo = user_input[5:]
        jsh.ouput = echo
        print(echo)

    # EXIT exit
    elif user_input == "exit":
        sys.exit()
    
    # HELP help
    elif user_input == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make, rm, rmdir, echo")

    # KEY lets a user define which symbol appears before their command
    elif (re.match("key(.*)", user_input)):
        key = jsh.directory = user_input[4:]
        if (len(key) <= 0):
            key_str = input("Please enter the key you would like to set: ")
            
        # Set the key
        jsettings["UserKey"] = key_str
        jmsg("Key set to: " + jsettings["UserKey"])
        
        


    # LIST FILES ls
    elif (re.match("ls (.*)", user_input) or user_input == "ls"):
        human_readable = False
        if (re.match("ls -l(.*)", user_input)):
            human_readable = True

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
                    print(ANSI.color_text(35) + jsh.directory + ANSI.color_text(0), end=" ")
                else:
                    print(ANSI.color_text(34) + jsh.directory + ANSI.color_text(0), end=" ")
                # print(jsh.directory + "  ", end=" ")
                for i in range(max_length - len(jsh.directory)):
                    print(" ", end="")
                    count += 1
            print(" ")
        else:
            max_length = -1;
            count = 0
            for jsh.directory in dir_list:
                if len(jsh.directory) > max_length:
                    max_length = len(jsh.directory)
                print(" ", end="")

            for jsh.directory in dir_list:
                # Give us the current file
                file_to_read = jsh.directory

                # Get the file modifed date
                file_modifed = str(time.ctime(os.path.getmtime(file_to_read)))

                # Get the file's permissions
                st = os.stat(file_to_read)
                oct_perm = oct(st.st_mode)
                mask = oct(os.stat(file_to_read).st_mode)[-3:] # convert the permissions 

                print("r:" + mask + "m:" + file_modifed + "f:" + jsh.directory)

    # MAKE FILE make or mk
    elif (re.match("make (.*)", user_input) or re.match("mk (.*)", user_input)):
        try:
            new_file = user_input[5:]
            open(new_file, 'w').close() 
            jmsg("made file: " + new_file)
        except:
            print_err("can't make file: " + new_file) 

    # MAKE jsh.directory mkdir or mkd
    elif (re.match("mkdir (.*)", user_input) or re.match("mkd (.*)", user_input)):
        try:
            jsh.directory = user_input[6:]
            os.mkdir(jsh.directory)
        except:
            print_err("can't make jsh.directory: " + jsh.directory)

    # OUTPUT output or out
    elif user_input == "output" or user_input == "out":
        print(jsh.output)

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
    
    # ECHO TIME time
    elif user_input == "time":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        jsh.output = current_time
        jmsg("Current Time: " + current_time)

    # UNKOWN COMMAND
    else:
        print_err("command not found: " + user_input)

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