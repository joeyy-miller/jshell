# jshell Quick Start Guide

This guide will help you quickly get started with jshell and explore its basic features.

## Installation

1. Clone the repository:
`git clone https://github.com/your-username/jshell.git`

2. Navigate to the project directory:
`cd jshell`

3. Run the jshell program:
`python jshell.py`
(note replace `python` with your Python interpretor. As of 2024 on macOS that is `python3`)
## Basic Commands

Here are some basic commands to get you started:

- `ls`: List files and directories in the current directory.
- `cd <directory>`: Change the current directory.
- `mkdir <directory>`: Create a new directory.
- `rm <file>`: Remove a file.
- `cat <file>`: Display the contents of a file.
- `touch <file>`: Create a new empty file.
- `date`: Display the current date.
- `time`: Display the current time.
- `whoami`: Display the current username.
- `help`: Show a list of available commands.
- `exit`: Exit jshell.

## Customization

You can customize various settings in jshell, such as:

- Username: Set your username using the `whoami` command.
- Command prompt: Change the command prompt symbol using the `key` command.
- Color mode: Enable or disable color output using the `color` command.

## Variables

jshell supports variables for command output and user-defined variables:

- `$output`: Refers to the output of the last command.
- `$<variable> = <value>`: Assign a value to a user-defined variable.

You can use these variables in subsequent commands.

## Debug Mode

Enable debug mode using the `debug` command to display detailed information about command execution, including the command, options, arguments, and output.

## Manual Pages

Access manual pages for commands using the `man <command>` command. For example, `man ls` will display the manual page for the `ls` command.

For more detailed information and advanced features, refer to the [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md) document.
