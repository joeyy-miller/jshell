import sys
import re
import os
from datetime import date

DIR = os.getcwd()
VERSION = "041023a"

def commands(input):

    # Version
    if input == "about":
        print("jshell version " + VERSION)

    if input == "help":
        print("commands: about, help, pwd, ls, cd, cd ..")

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

    if (re.match("cd(.*)", input)):
        print("you cd'd")
            

def main():
    os.system("clear")
    while True:
        print("$ ", end="")
        commands(input())

main()