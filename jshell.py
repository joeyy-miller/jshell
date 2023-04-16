import sys
import re
import os
from datetime import date
from datetime import datetime

DIR = os.getcwd()
VERSION = "041023a"

def commands(input):

    # Version
    if input == "about":
        print("jshell version " + VERSION)

    if input == "help":
        print("commands: about, help, pwd, ls, cd, date, time")

    if input == "pwd":
        print(DIR)

    if input == "ls":
        print("ls")
        dir_list = os.listdir(os.getcwd()) 
        # prints all files
        print(dir_list)

    if input == "cd .."
        os.chdir("..")
        DIR = os.path.abspath(os.curdir)
        print ("Moved up to: " + DIR)
    
    if input == "date":
        today = date.today()
        print(today)
    
    if input == "time":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

    if (re.match("cd(.*)", input)):
        print("you cd'd")
            

def main():
    os.system("clear")
    while True:
        print("$ ", end="")
        commands(input())

main()