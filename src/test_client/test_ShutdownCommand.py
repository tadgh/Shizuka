import unittest
import ShutdownCommand


class TestShutdownCommand(unittest.TestCase):

    def setUp(self):
        self.command = ShutdownCommand.ShutdownCommand()

    def test_shutdown_works(self):
        #This seems like a bad idea.
        #return True haha
        pass



if __name__ == "__main__":
    unittest.main()
