import unittest
from jshell import jshell, commands  # Adjust import according to your project structure

Debug = True

class TestJShell(unittest.TestCase):
    def setUp(self):
        # Initialize the shell instance
        #self.jsh = jshell()
        Test = True
        
    def test_variable_assignment(self):
        # Test variable assignment and retrieval
        global jsh
        output = jsh.execute_command("echo Hello, World!")

        print("Output: ", output)
        self.assertEqual(output, "Hello, World!")
        
    '''
    def test_cd_command(self):
        # Assuming you have a method to execute commands and return output
        original_directory = self.jsh.directory
        self.jsh.execute_command("cd ..")
        self.assertNotEqual(self.jsh.directory, original_directory)
        # Reset directory for other tests
        self.jsh.execute_command(f"cd {original_directory}")

    def test_echo_command(self):
        # Test echo output
        output = self.jsh.execute_command("echo Hello, World!")
        self.assertEqual(output, "Hello, World!")
    '''

if __name__ == '__main__':
    unittest.main()