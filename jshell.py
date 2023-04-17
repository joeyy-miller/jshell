import sys
import re
import os
from datetime import date
from datetime import datetime

VERSION = "0230417e"
DIRECTORY = ""

def commands(input):

    global DIRECTORY
    # Version
    if input == "about":
        jmsg("jshell version " + VERSION)
    
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
        
    elif input == "date":
        today = date.today()
        jmsg(today)

    elif (re.match("del (.*)", input)):
        remove_file = input[4:]
        jmsg("deleting file" + remove_file)
        try:
            os.remove(remove_file)
        except FileNotFoundError:
            print_err("not a valid file: " + remove_file)
        except:
            print_err("Unkown: " + remove_file)
    
    elif input == "exit":
        sys.exit()
    

    elif input == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit")

    elif input == "ls":
        dir_list = os.listdir(os.getcwd()) 
        # prints all files
        print(">", end=" ")
        for directory in dir_list:
            print(directory + "  ", end=" ")
        print(" ")

    elif input == "pwd":
        jmsg(DIRECTORY)
    
    elif input == "time":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        jmsg("Current Time =", current_time)

    else:
        print_err("command not found: " + input)
    

def print_err(err):
    print(">jsh error: " + err)

def jmsg(msg):
    print(">jsh: " + msg)

def main():
    os.system("clear")
    global DIRECTORY
    DIRECTORY = os.path.abspath(os.curdir)
    while True:
        print("$ ", end="")
        commands(input())

main()