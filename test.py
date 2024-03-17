from unittest.mock import patch
import unittest
import jshell  # Import your main application script here

class TestApplication(unittest.TestCase):

    @patch('builtins.input', side_effect=['command1', 'command2', 'exit'])
    @patch('sys.exit')
    def test_application_loop(self, mock_exit, mock_input):
        """
        Test the application loop by simulating user inputs.
        `side_effect` list ends with 'exit' to simulate exiting the application.
        """
        jshell.main()  # Assuming your main loop is in a function called `main`
        mock_exit.assert_called_once()  # Check that sys.exit() was called, indicating loop exit