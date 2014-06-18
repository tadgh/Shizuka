from Command import Command
import subprocess
import Constants
import logging

logger = logging.getLogger("Command")
logger.setLevel(logging.INFO)


## Command that executes a restart operation on the client computer.
#
#
class RestartCommand(Command):
    def __init__(self):
        Command.__init__(self, Constants.RESTART_TAG)

    def windows_execute(self):
        logger.info("Restart Command Called. Restarting in 15!")
        subprocess.call(["shutdown.exe", "/r", "/t", "15"])

    def nix_execute(self):
        logger.info("Restart Command Called. Restarting in 15!")
        subprocess.call(["shutdown", "-r", "15"])




if __name__ == "__main__":
    rc = RestartCommand()
    rc.execute()

