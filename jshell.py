import sys
import re
import os

DIR = os.getcwd()
VERSION = "041023a"

def commands(input):
    match input:
        case "about":
        case "help":
            print("jshell version " + VERSION)

        case "pwd":
            print(DIR)

        case "ls":
            print("ls")
            dir_list = os.listdir(os.getcwd()) 
            # prints all files
            print(dir_list)
    
        case "cd ..":
            os.chdir("..")
            DIR = os.path.abspath(os.curdir)
            print ("Moved up to: " + DIR)

    if (re.match("cd(.*)", input)):
        print("you cd'd")
            

def main():
    os.system("clear")
    while True:
        print("$ ", end="")
        commands(input())

main()