import unittest
import logging
import CommandInterface
import Constants

logging.basicConfig(level=logging.INFO)

class TestCommandInterface(unittest.TestCase):

    def setUp(self):
        self.commandInterface = CommandInterface.CommandInterface()

    def test_command_executor_raises_KeyError_on_illegal_command(self):
        self.assertRaises(KeyError, self.commandInterface.execute_command("SOME_FAKE_COMMAND"))

    def test_some_command_returns_successfully(self):
        results = self.commandInterface.execute_command(Constants.NETWORK_INFO_TAG)
        self.assertTrue(isinstance(results, str))


if __name__ == "__main__":
    unittest.main()

