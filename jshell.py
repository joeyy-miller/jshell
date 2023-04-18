import sys
import re
import os
from datetime import date
from datetime import datetime

VERSION = "0230417e"
DIRECTORY = ""

def commands(input):

    global DIRECTORY
    
    # ABOUT about
    if input == "about":
        jmsg("jshell version " + VERSION)
    
    # CHANGE DIRECTORY cd
    elif (re.match("cd (.*)", input)):
        if input == "cd ..":
            os.chdir("..")
            DIRECTORY = os.path.abspath(os.curdir)
            jmsg("Moved up to: " + DIRECTORY)
        else:
            directory = input[3:]
            try:
                os.chdir(directory)
            except FileNotFoundError:
                print_err("not a valid directory: " + directory)
            except:
                print_err("Unkown: " + directory)
        
    # ECHO DATE date    
    elif input == "date":
        today = date.today()
        jmsg(today)

    # DELETE del
    elif (re.match("del (.*)", input) or re.match("rm (.*)", input)):
        if re.match("del (.*)", input):
            remove_file = input[4:]
        else:
            remove_file = input[3:]
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
            print_err("Unkown: " + remove_file)

    # ECHO echo
    elif (re.match("echo (.*)", input)):
        echo = input[5:]
        print(echo)

    # EXIT exit
    elif input == "exit":
        sys.exit()
    
    # HELP help
    elif input == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make, rm, rmdir, echo")

    # LIST FILES ls
    elif input == "ls":
        dir_list = os.listdir(os.getcwd()) 
        # prints all files
        max_length = -1;
        for directory in dir_list:
            if len(directory) > max_length:
                max_length = len(directory)
        
        line_len = 70 # Max items per line
        count = 0 # Count the number of items printed
        for directory in dir_list:
            count += len(directory)
            if count >= line_len:
                print(" ")
                count = 0
            isFile = os.path.isfile(directory)
            if isFile:
                print(ANSI.color_text(35) + directory + ANSI.color_text(0), end=" ")
            else:
                print(ANSI.color_text(34) + directory + ANSI.color_text(0), end=" ")
            # print(directory + "  ", end=" ")
            for i in range(max_length - len(directory)):
                print(" ", end="")
                count += 1
            
        print(" ")

    # MAKE FILE make or mk
    elif (re.match("make (.*)", input) or re.match("mk (.*)", input)):
        try:
            new_file = input[5:]
            open(new_file, 'w').close() 
            jmsg("made file: " + new_file)
        except:
            print_err("can't make file: " + new_file) 

    # MAKE DIRECTORY mkdir or mkd
    elif (re.match("mkdir (.*)", input) or re.match("mkd (.*)", input)):
        try:
            new_directory = input[6:]
            os.mkdir(new_directory)
        except:
            print_err("can't make directory: " + new_directory)

    # PRINT WORKING DIRECTORY pwd
    elif input == "pwd":
        jmsg(DIRECTORY)
    
    # ECHO TIME time
    elif input == "time":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        jmsg("Current Time =", current_time)

    # UNKOWN COMMAND
    else:
        print_err("command not found: " + input)
    

def print_err(err):
    print(">jsh error: " + err)

def jmsg(msg):
    print(">jsh: " + msg)

def rm_dir(directory):
    try:
        os.rmdir(directory)
        jmsg("removed directory: " + directory)
    except FileNotFoundError:
        print_err("not a valid directory: " + directory)
    except:
        print_err("can't remove directory: " + directory)
    

def main():
    os.system("clear")
    global DIRECTORY
    DIRECTORY = os.path.abspath(os.curdir)
    while True:
        print("$ ", end="")
        commands(input())
class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)
 
    def style_text(code):
        return "\33[{code}m".format(code=code)
 
    def color_text(code):
        return "\33[{code}m".format(code=code)

#example_ansi = ANSI.background(97) + ANSI.color_text(35) + ANSI.style_text(4) + " TESTE ANSI ESCAPE CODE"
#print(example_ansi)

main()