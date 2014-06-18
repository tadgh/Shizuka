from Command import Command
import subprocess
import Constants
import logging

logger = logging.getLogger("Command")
logger.setLevel(logging.INFO)
## Command that executes a restart operation on the client computer. IPCONFIG on windows, IFCONFIG on unix.
#
#
class NetworkInfoCommand(Command):
    def __init__(self):
        Command.__init__(self, Constants.NETWORK_INFO_TAG)

    def windows_execute(self):
        logger.info("IPCONFIG called. ")
        results = subprocess.check_output(["ipconfig", "/all"]).decode('utf-8')
        return results

    def nix_execute(self):
        logger.info("IFCONFIG called. ")
        results = subprocess.check_output(["ifconfig"]).decode("utf-8")
        return results



if __name__ == "__main__":
    nic = NetworkInfoCommand()
    nic.execute()

