from Command import Command
import Constants
import subprocess


## Command that executes a shutdown operation on the client computer.
#
#
class ShutdownCommand(Command):
    def __init__(self):
        Command.__init__(self, Constants.SHUTDOWN_TAG)

    def windows_execute(self):
        logging.info("Shutdown Command Called. Shutting Down in 15!")
        subprocess.call(["shutdown.exe", "/s", "/t", "15"])

    def nix_execute(self):
        logging.info("Shutdown Command Called. Shutting Down in 15!")
        subprocess.call(["shutdown", "-h", "15"])





if __name__=="__main__":
    sc = ShutdownCommand()
    sc.execute()

