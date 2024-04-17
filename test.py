import unittest
import io
import os
import sys
import time
from jshell import jshell, commands

unittest.TestLoader.sortTestMethodsUsing = None

class TestJShell(unittest.TestCase):
    def setUp(self):
        self.jsh = jshell()

    def test_pwd_command(self):
        # Redirect stdout to a buffer
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer

        # Store the current directory
        current_dir = os.getcwd()

        # Execute the 'pwd' command
        commands("pwd")

        # Get the printed output from the buffer
        output = stdout_buffer.getvalue().strip()

        # Assert the expected output
        self.assertIn(current_dir, output)

        # Restore stdout
        sys.stdout = sys.__stdout__

    def test_about_command(self):
        # Redirect stdout to a buffer
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer

        # Execute the 'about' command
        commands("about")

        # Get the printed output from the buffer
        output = stdout_buffer.getvalue().strip()

        # Assert the expected output
        self.assertIn("jshell build", output)
        self.assertIn(self.jsh.version, output)

        # Restore stdout
        sys.stdout = sys.__stdout__

    def test_help_command(self):
        # Redirect stdout to a buffer
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer

        # Execute the 'help' command
        commands("help")

        # Get the printed output from the buffer
        output = stdout_buffer.getvalue().strip()

        # Assert the expected output
        self.assertIn("commands:", output)
        self.assertIn("about", output)
        self.assertIn("help", output)
        self.assertIn("pwd", output)
        # Add more assertions for other expected commands

        # Restore stdout
        sys.stdout = sys.__stdout__

    def test_unknown_command(self):
        # Redirect stdout to a buffer
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer

        # Execute an unknown command
        commands("unknown_command")

        # Get the printed output from the buffer
        output = stdout_buffer.getvalue().strip()

        # Assert the expected output
        self.assertIn("command not found: 'unknown_command'", output)

        # Restore stdout
        sys.stdout = sys.__stdout__


    def test_cd_command(self):
        # Store the current directory
        current_dir = os.getcwd()

        # Execute the 'cd' command to change directory
        commands("cd ..")

        # Assert the directory has changed
        self.assertNotEqual(os.getcwd(), current_dir)

        # Change back to the original directory
        os.chdir(current_dir)

    def test_mkdir_command(self):
        # Generate a unique directory name
        test_dir = "test_dir_" + str(int(time.time()))

        # Execute the 'mkdir' command to create a directory
        commands(f"mkdir {test_dir}")

        # Assert the directory was created
        self.assertTrue(os.path.exists(test_dir))

        # Clean up the created directory
        os.rmdir(test_dir)

    def test_touch_command(self):
        # Execute the 'touch' command to create a file
        commands("touch test_file.txt")

        # Assert the file was created
        self.assertTrue(os.path.exists("test_file.txt"))

        # Clean up the created file
        os.remove("test_file.txt")

    def test_rm_command(self):
        # Create a temporary file
        open("temp_file.txt", "w").close()

        # Execute the 'rm' command to remove the file
        commands("rm temp_file.txt")

        # Assert the file was removed
        self.assertFalse(os.path.exists("temp_file.txt"))

    def test_echo_command(self):
        # Redirect stdout to a buffer
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer

        # Execute the 'echo' command
        commands("echo Hello, World!")

        # Get the printed output from the buffer
        output = stdout_buffer.getvalue().strip()

        # Assert the expected output
        self.assertEqual(output, "Hello, World!")

        # Restore stdout
        sys.stdout = sys.__stdout__

    # Add more test methods for other commands and scenarios

if __name__ == '__main__':
    unittest.main()