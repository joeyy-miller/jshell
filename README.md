# jshell! easy terminal-ing
A very simple command line shell in the style of Bash. Completely change, and *maybe* exipidite, your command line experience, today!

![Example image of jshell running on Mac OS X](/jsh_example.png)

## About
I developed in Python for personal use, and can use it to completely replace Bash, Zsh, or Fish for *non-complex* daily use!
It is encouraged to branch the code and create your own version and add your own commands!

## Features

- Basic file and directory management commands (ls, cd, mkdir, rm, etc.)
- File manipulation commands (cat, touch, cp, etc.)
- System information commands (date, time, whoami, etc.)
- Customizable user settings (username, command prompt, color mode, etc.)
- Variable support for command output and user-defined variables
- Debug mode for detailed command execution information
- Built-in help and manual pages for commands

## Getting Started

1. Clone the repository: `git clone https://github.com/your-username/jshell.git`
2. Navigate to the project directory: `cd jshell`
3. Run the jshell program: `python jshell.py`

For more detailed instructions, refer to the [QUICKSTART.md](QUICKSTART.md) guide.

## Documentation

For a comprehensive guide on jshell's features, commands, and technical details, please refer to the [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md) document.

## Commands:
jshell is built around commands, learn how to use them below. Commands are entered one at a time, and they usualy give an expected output, or change something on your system

### Anatomy of a Command:
`command -flags argument argument2`
"command" is the command you're typing.
Any single letter after the `-` is called an option, or flag. Use these to change the behavior of a command in certain ways. Such as using the -`.` flag to show hidden files when using the `ls` command.
Any words after that are taken as 'arguments' to the command. Such as using `..` as an argument to tell the `cd` command you wish to navigate up one  directory.

### Supported Commands:
+ `about`: Get infromation about jshell.
+ `help`: Get help on how to use jshell.
+ `pwd`: Get your current working directory.
+ `cat`: This command lets you read the contents of a file. Type `cat {filename}` to get an output of the file's contents printed in your terminal.
+ `ls`: List the files in your current working directory (see ls)
+ `cd`: Change directory. Use `cd ..` to move up a directory.
+ `date`: Get the current date, and set that to the `$output` variable.
+ `time`: Get the current time, and set that to the `$output` variable.
+ `del` or `rm`: Delete a file or folder.
+ `exit`: Exit the terminal.
+ `mk` or `touch`: Make a file! Use `touch file_name.txt` to create a file named `file_name.txt`.
+ `mkdir`: Make a directory in your current working directory.
+ `rmdir`: Remove a directory.
+ `echo`: Echo whatever you type as aguments to the terminal.
+ `output`: Tell you the value of the standard $output variable.
+ `perm`: Change the permissions of a folder or file. Type `perm filename.txt` by itself to retreive the permissions, or type `perm filename.txt 777` to change an example file called `filename.txt` to have full read, write, and access permissions (777 in shorthand). 
+ `clear`: Clear the screen.
+ `width`: Set your screen width. The first arugment is an int with the new with.
+ `man`: Get manaul pages for certain commands.
+ `color`: Turn on/off color mode.
+ `debug`: Turn on/off debug mode.
+ `version`: Get verison, build, and release information.
+ `history`: Get a list of commands that were run. 
+ `!`: Used to rerun comamnds. Type `![NUM]` with `[num]` being the number from the `history` command that you want to rerun.
+ `curl`: Retreive data from a URL. Type the url after the curl command, and it will be output in your terminal. Use the `-o` flag to download the response to a file. Example: `curl -o output.txt https://www.example.com/`

## Variables:
Jshell can use variables.

You can use the $output variable (a default variable in jshell) to use the output of the last command that shows an output in your current command, if supported. The `date` and `time` commands will change the value of `$output` to their own output.
You can also create your own variables by typing `$[variable name] = [value]`.
Example: `$name = 'John'`. Variables can be an integer or number. They cannot be assigned to eachother. Variables in jshell come in two flavors, `Int` for numbers, and `String` for text.
See a list of made variables by typing `variable` or `var`. Variables can be used in the same way as the default `$output` variable.

## Manuals:
Jshell offers manual pages built in to the termianl. 
Type `man {command}` to read that command's manual.
Commands with a manual right now are: jsh, ls, perm, and key.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

version: `0.5.3 beta`. build: `0240412b`

*jshell* (**c**) 2024 Joey Miller.