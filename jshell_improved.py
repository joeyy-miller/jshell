import sys
import re
import os
import time
import json
from datetime import date, datetime
from typing import Dict, Any

class ANSI:
    @staticmethod
    def background(code: int) -> str:
        return f"\33[{code}m"

    @staticmethod
    def style_text(code: int) -> str:
        return f"\33[{code}m"

    @staticmethod
    def color_text(code: int) -> str:
        return f"\33[{code}m"

    PURPLE = 35
    BLUE = 34

class Variable:
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
        self.type = self.determine_type()

    def determine_type(self) -> str:
        if isinstance(self.value, str):
            return 'string'
        elif isinstance(self.value, (int, float)):
            return 'number'
        else:
            return 'unknown'

    def __str__(self) -> str:
        return str(self.value)

class JShell:
    def __init__(self):
        self.build = "0240314e"
        self.version = "0.5.1"
        self.release = "beta"
        self.directory = ""
        self.userkey = jsettings['UserString']
        self.username = jsettings['UserName']
        self.output = ""
        self.debug = jsettings['DebugMode']
        self.color = True
        self.MAX_OUTPUT_LENGTH = 150
        self.variables: Dict[str, Variable] = {}
        self.last_command_output = ""

    def save_settings(self):
        file_name = 'data.json'
        data = {}
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    pass
        data['UserName'] = self.username
        data['UserString'] = self.userkey
        data['DebugMode'] = self.debug
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def execute_command(self, command: str) -> str:
        input(command)
        return self.last_command_output

def jerror(err: str):
    err = str(err)
    loop_count = 0
    ERROR_STRING = "jsh error: "
    ELLIPSIS = "..."
    while len(err) > 0:
        if len(err) > jsh.MAX_OUTPUT_LENGTH:
            print(jsh.userkey + ERROR_STRING + err[:jsh.MAX_OUTPUT_LENGTH - (len(ERROR_STRING) + len(ELLIPSIS))] + ELLIPSIS)
        else:
            print(jsh.userkey + ERROR_STRING + err)
        err = err[jsh.MAX_OUTPUT_LENGTH:]
        loop_count += 1
        if loop_count >= 1:
            ERROR_STRING = ""

def jmsg(msg: str):
    msg = str(msg)
    jsh.last_command_output = str(msg)
    ELLIPSIS = "..."
    JSH_STRING = "jsh: "
    while len(msg) > 0:
        if len(msg) > jsh.MAX_OUTPUT_LENGTH:
            print(jsh.userkey + JSH_STRING + msg[:jsh.MAX_OUTPUT_LENGTH - (len(ELLIPSIS) + len(ELLIPSIS))] + "...")
        else:
            print(jsh.userkey + "jsh: " + msg)
        msg = msg[jsh.MAX_OUTPUT_LENGTH:]

def jout(msg: str):
    msg = str(msg)
    jsh.last_command_output = str(msg)
    ELLIPSIS = "..."
    while len(msg) > 0:
        if len(msg) > jsh.MAX_OUTPUT_LENGTH:
            print(msg[:jsh.MAX_OUTPUT_LENGTH - len(ELLIPSIS)] + ELLIPSIS)
        else:
            print(msg)
        msg = msg[jsh.MAX_OUTPUT_LENGTH:]

def rm_dir(rm_directory: str):
    try:
        os.rmdir(rm_directory)
    except FileNotFoundError:
        jerror(f"not a valid directory: {rm_directory}")
    except Exception:
        jerror(f"can't remove directory: {rm_directory}")
    else:
        jmsg(f"removed directory: {rm_directory}")

def change_file_permissions(file_path: str, permissions: str):
    mode = int(permissions, 8)
    os.chmod(file_path, mode)

def process_input(user_input: str, variables: Dict[str, Variable]) -> str:
    definition_pattern = r'\$(\w+)\s*=\s*"([^"]*)"|\$(\w+)\s*=\s*(\d+(?:\.\d+)?)'
    usage_pattern = r'\$(\w+)'
    for match in re.finditer(definition_pattern, user_input):
        name, string_value, number_name, number_value = match.groups()
        if name:
            variables[name] = Variable(name, string_value)
        elif number_name:
            number_value = float(number_value) if '.' in number_value else int(number_value)
            variables[number_name] = Variable(number_name, number_value)

    def replace_function(match: re.Match) -> str:
        variable_name = match.group(1)
        if variable_name in variables:
            return str(variables[variable_name])
        return match.group(0)

    modified_input = re.sub(usage_pattern, replace_function, user_input)
    return modified_input

def commands(user_input: str):
    if jsh.output != "":
        user_input = user_input.replace("$output", str(jsh.output))
    user_input_old = user_input
    user_input = process_input(user_input, jsh.variables)
    IF_VARIABLE = user_input != user_input_old

    parts = user_input.split()
    command = ""
    options = []
    arguments = []
    for part in parts:
        if part.startswith('-') and not command:
            options.extend(list(part[1:]))
        elif not command:
            command = part
        else:
            arguments.append(part)

    if user_input == "about":
        if jsh.debug:
            jmsg(f"jshell build: {jsh.build} build:{jsh.version}")
        jmsg(f"jshell build {jsh.version}")

    elif command == "cat":
        if len(arguments) >= 2 and arguments[1] == ">>":
            file_to_write = arguments[0]
            try:
                with open(file_to_write, 'a') as file:
                    cat_length = 3 + len(arguments[0] + arguments[1])
                    file.write(user_input[cat_length:])
                jmsg(f"wrote to file: {file_to_write}")
            except FileNotFoundError:
                jerror(f"not a valid file: {file_to_write}")
            except Exception:
                jerror(f"unknown error: {file_to_write}")
        else:
            file_to_read = user_input[4:]
            try:
                with open(file_to_read, 'r') as file:
                    jout(file.read())
            except FileNotFoundError:
                jerror(f"not a valid file: {file_to_read}")
            except Exception:
                jerror(f"unknown error: {file_to_read}")
        if user_input == "cat":
            jmsg("cat error: Please enter a file to print the contents of.")

    elif command in ["cd", "chdir"]:
        if arguments[0] == "..":
            os.chdir("..")
            jsh.directory = os.path.abspath(os.curdir)
            jmsg(f"Moved up to: {jsh.directory}")
        else:
            jsh.directory = arguments[0]
            try:
                os.chdir(jsh.directory)
            except FileNotFoundError:
                jerror(f"not a valid directory: {jsh.directory}")
            except Exception:
                jerror(f"unknown error: {jsh.directory}")

    elif command in ["cp", "copy"]:
        if re.match("cp (.*) (.*)", user_input):
            file_to_copy = arguments[0]
            new_file = arguments[1]
            try:
                with open(file_to_copy, 'r') as file:
                    with open(new_file, 'w') as new_file:
                        new_file.write(file.read())
                jmsg(f"copied file: {file_to_copy} to {new_file}")
            except FileNotFoundError:
                jerror(f"not a valid file: {file_to_copy}")
            except Exception:
                jerror(f"unknown error: {file_to_copy}")
        else:
            jerror("cp error: Please enter a file to copy and a new file to copy it to.")

    elif command in ["clear", "cls"]:
        os.system('clear')

    elif command == "color":
        jsh.color = not jsh.color
        jmsg("color mode " + ("on" if jsh.color else "off"))

    elif command == "debug":
        jsh.debug = not jsh.debug
        jmsg("debug mode " + ("on" if jsh.debug else "off"))
        jsh.save_settings()

    elif command in ["del", "rm", "delete"]:
        if re.match("del (.*)", user_input):
            remove_file = arguments[0]
        else:
            remove_file = arguments[0]
        jmsg(f"deleting file {remove_file}")
        try:
            os.remove(remove_file)
        except IsADirectoryError:
            rm_dir(remove_file)
        except FileNotFoundError:
            jerror(f"not a valid file: {remove_file}")
        except PermissionError:
            jerror(f"permission denied: {remove_file}")
        except Exception:
            jerror(f"unknown error: {remove_file}")

    elif user_input == "date":
        today = date.today()
        jsh.output = today
        jmsg(today)

    elif command == "echo":
        echo = user_input[5:]
        jsh.output = echo
        jout(echo)

    elif user_input in ["exit", "quit", "q", "close", "bye", "goodbye", "end", "stop", "halt", "terminate", "kill", "destroy"]:
        sys.exit()

    elif command == "help":
        jmsg("commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make...")
        jout(" rm, rmdir, echo, clear, man, key, output, perm, touch, whoami, color.")
        jout("use: man [command] for more information on a command. 'man jsh' for additional manual pages.")
        jout("use $output to use the output of the last command in your current command.")
        jout("type 'exit' to exit jshell.")

    elif command == "input":
        jout(f"Input: {user_input}")
        jout(f"Command: {command}")
        jout(f"Options: {options}")
        jout(f"Arguments: {arguments}")
        jout(f"User Input: {user_input}")
        jout(f"jshell Output: {jsh.output}")
        jout(f"jshell Last Output: {jsh.last_command_output}")
        jout('')

    elif command == "key":
        set_key = user_input[4:]
        if len(set_key) <= 0:
            set_key = input("Please enter the key you would like to set: ")
        jsh.userkey = str(set_key)
        jmsg(f"Key set to: {jsh.userkey}")
        jsh.save_settings()

    elif command in ["ls", "list"]:
        LOOP = 0
        human_readable = False
        COLOR_OPTION = True
        SHOW_HIDDEN_FILES = False
        if re.match("ls -(.*)l(.*)", user_input):
            human_readable = True
        if re.match("ls -(.*)c(.*)", user_input):
            COLOR_OPTION = False
        if re.match("ls -(.*)a(.*)", user_input) or re.match("ls -(.*).(.*)", user_input):
            SHOW_HIDDEN_FILES = True
        dir_list = os.listdir(os.getcwd())
        if not human_readable:
            max_length = -1
            for directory in dir_list:
                if not SHOW_HIDDEN_FILES and directory.startswith('.'):
                    continue
                if len(directory) > 0:
                    if len(directory) > max_length:
                        max_length = len(directory)
            line_len = 70
            count = 0
            for directory in dir_list:
                if not SHOW_HIDDEN_FILES and directory.startswith('.'):
                    continue
                count += len(directory)
                if count >= line_len:
                    print(" ")
                    count = 0
                isFile = os.path.isfile(directory)
                if isFile:
                    if COLOR_OPTION and jsh.color:
                        print(ANSI.color_text(ANSI.BLUE) + directory + ANSI.color_text(0), end=" ")
                    else:
                        print(directory, end=" ")
                else:
                    if COLOR_OPTION and jsh.color:
                        print(ANSI.color_text(ANSI.PURPLE) + "[" + directory + "]" + ANSI.color_text(0), end=" ")
                    else:
                        print(directory, end=" ")
                for i in range(max_length - len(directory)):
                    print(" ", end="")
                count += 1
            print(" ")
        else:
            max_length = -1
            count = 0
            for jsh.directory in dir_list:
                if LOOP == 0:
                    if len(jsh.directory) > max_length:
                        max_length = len(jsh.directory)
                    print(" ", end="")
                    LOOP += 1
            for jsh.directory in dir_list:
                file_to_read = jsh.directory
                file_modified = str(time.ctime(os.path.getmtime(file_to_read)))
                st = os.stat(file_to_read)
                mask = oct(os.stat(file_to_read).st_mode)[-3:]
                isFile = os.path.isfile(jsh.directory)
                if COLOR_OPTION and jsh.color:
                    if isFile:
                        print(f"r: {mask} m: {file_modified} f: {ANSI.color_text(35)}{jsh.directory}{ANSI.color_text(0)}")
                    else:
                        print(f"r: {mask} m: {file_modified} f: {ANSI.color_text(34)}{jsh.directory}{ANSI.color_text(0)}")
                else:
                    print(f"r:{mask} m:{file_modified} f:{jsh.directory}")

    elif command in ["make", "mk"]:
        try:
            new_file = user_input[5:]
            open(new_file, 'w').close()
            jmsg(f"made file: {new_file}")
        except Exception:
            jerror(f"can't make file: {new_file}")

    elif command in ["mkdir", "mkd", "makefolder", "folder", "makedir"]:
        try:
            jsh.directory = arguments[0]
            os.mkdir(jsh.directory)
        except FileExistsError:
            jerror(f"directory already exists: {jsh.directory}")
        except Exception:
            jerror(f"can't make directory: {jsh.directory}")
        else:
            jmsg(f"created directory: {jsh.directory}")

    elif command == "man":
        if user_input == "man ls":
            jout("ls: command to list files.")
            jout(" This command allows you to list all the files in a folder.")
            jout(" Colors: Files show up as BLUE in color. Folders are PURPLE in color, and surrounded in brackets.")
            jout(" flags:")
            jout(" | -l | This is the 'long' command flag, it shows you the date created, along with the permissions, and hidden files.")
            jout(" | -c | This is the 'colorless' flag, prints the file and folder names without color.")
            jout(" | -a | This is the 'all' flag, it shows all files, including hidden files.")
            jout(" | -. | Alias for the 'all' flag, same as typing -a.")
        elif user_input == "man perm":
            jout("perm: command to change the permissions of a file.")
            jout(" This command allows you to read or change the permissions of a file.")
            jout(" Reading Permissions: perm [file]")
            jout(" Changing Permissions: perm [file] [permissions]")
            jout(" Example: perm file.txt 777")
            jout(" This will set the file.txt to have full permissions.")
            jout(" flags:")
            jout(" | -o | Octal mode, shows the file permissions in octal.")
        elif user_input == "man key":
            jout("key: command to set the key before the command.")
            jout(" This command allows you to set the key before the command.")
            jout(" Example: key >")
            jout(" This will set the key to '>'.")
            jout(" The key is the symbol that appears before the command.")
            jout(" The default key is '$'.")
            jout(" The key is used to show the user that the shell is ready for a command.")
            jout(" flags:")
            jout(" none")
        elif user_input == "man jsh":
            jout("How to use jshell:")
            jout("Commands: about, help, pwd, ls, cd, date, time, del, exit, mk, mkdir, make, rm, rmdir, echo, clear, color, man, key, output, perm, touch.")
            jout("Color Mode: type 'color' to turn on/off color mode. This will show the output in color.")
            jout("Variables: You can use the $output variable to use the output of the last command that shows an output in your current command.")
            jout(" You can also create your own variables by typing '$[variable name] = [value]'")
            jout(" Example: $name = 'John'. Variables can be an integer or number. They cannot be assigned to each other.")
            jout(" See a list of made variables by typing 'variable' or 'var'. Variables can be used in the same way as $output.")
            jout("Debug Mode: type 'debug' to turn on/off debug mode. This will show additional information about the command.")
            jout("type 'exit' to exit jshell.")
        elif command == "man":
            jmsg("man error: Manual for commands. Enter a command after 'man' to read its manual.")
            jout(" Supported commands: ls, perm, key")

    elif command == "pwd":
        jsh.output = jsh.directory
        jmsg(jsh.directory)

    elif command == "perm":
        OCTAL_MODE = False
        if re.match("perm -(.*)o(.*)", user_input):
            OCTAL_MODE = True
            user_input = user_input.replace("-o", "")
        words = user_input.split()
        word1 = word2 = word3 = None
        if len(words) >= 1:
            word1 = words[0]
        if len(words) >= 2:
            word2 = words[1]
        if len(words) == 3:
            word3 = words[2]
        file_to_read = word2
        if word3 is None and word2 is not None:
            try:
                st = os.stat(file_to_read)
                if not OCTAL_MODE:
                    mask = oct(os.stat(file_to_read).st_mode)[-3:]
                    print(mask)
            except FileNotFoundError:
                jerror(f"not a valid file: {file_to_read}")
        elif word3 is not None and word2 is not None:
            permissions = word3
            change_file_permissions(file_to_read, permissions)
        else:
            jerror("perm error: Please enter a file to read or change the permissions of.")

    elif user_input == "time":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        jsh.output = current_time
        jmsg(f"Current Time: {current_time}")

    elif command == "touch":
        if len(arguments) != 0:
            FILE_NAME = arguments[0]
            try:
                file = open(FILE_NAME, "x")
                file.close()
            except FileExistsError:
                jerror(f"file already exists: {FILE_NAME}")
            except Exception:
                jerror(f"can't make file: {FILE_NAME}")
        else:
            jerror("no file specified.")

    elif command in ["var", "variable"]:
        jmsg("Variables:")
        for var in jsh.variables.values():
            jout(f"Name: {var.name}, Value: {var.value}, Type: {var.type}")

    elif command == "width":
        try:
            width = int(arguments[0])
            jsh.MAX_OUTPUT_LENGTH = width
        except Exception:
            jerror("width error: Please enter a number.")
        jout(f"Width: {jsh.MAX_OUTPUT_LENGTH}")

    elif command == "whoami":
        if len(arguments) >= 1:
            jsh.username = arguments[0]
            jout(f"Your new username is: {jsh.username}")
        else:
            if jsh.username:
                jout(f"Your username is {jsh.username}")
            else:
                jout("You do not have a username set.")
                jout("Type your username...")
                user_name = input()
                if user_name:
                    jsh.username = user_name
                    jsh.save_settings()
                else:
                    jerror("Unable to change username")

    elif IF_VARIABLE:
        pass

    elif user_input == "":
        jerror("no input.")

    else:
        jerror(f"command not found: '{user_input}'.")

    if jsh.debug:
        jout(f"Command: {command}")
        jout(f"Options: {options}")
        jout(f"Arguments: {arguments}")
        jout(f"User Input: {user_input}")
        jout(f"jshell Output: {jsh.output}")
        jout(f"jshell Last Output: {jsh.last_command_output}")
        jout('')

def main():
    os.system("clear")
    jsh.directory = os.path.abspath(os.curdir)
    while True:
        print(jsh.userkey + " ", end="")
        commands(input())

if __name__ == "__main__":
    usersettings = open("data.json", "r")
    jsettings = json.load(usersettings)
    global jsh
    jsh = JShell()
    usersettings.close()
    main()