import pexpect
import unittest

class TestJShellIntegration(unittest.TestCase):
    def test_about_command(self):
        """Test the 'about' command produces the expected output."""
        # Start the jshell application
        child = pexpect.spawn('python3 jshell.py')
        
        # Set a timeout for each interaction (adjust as necessary)
        child.timeout = 4

        # Wait for the shell to start and show its prompt
        child.expect_exact('$ ')
        
        # Send the 'about' command
        child.sendline('about')
        
        # Expect the output that contains version information, adjust as needed
        expected_output_part = 'about\r\n>jsh: jshell build 0.5.1'
        child.expect_exact(expected_output_part)
        
         
        # Capture the output
        output = child.before.decode('utf-8')

        # Check that the output contains the expected part
        self.assertIn(expected_output_part, output)
        
        # Close the jshell application
        child.sendline('exit')
        child.expect(pexpect.EOF)

if __name__ == '__main__':
    unittest.main()