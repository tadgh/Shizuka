from Command import Command
import subprocess
import Constants
import logging


## Command that executes a restart operation on the client computer.
#
#
class NetworkInfoCommand(Command):
    def __init__(self):
        Command.__init__(self, Constants.NETWORK_INFO_TAG)

    def windows_execute(self):
        logging.info("IPCONFIG called. ")
        results = subprocess.check_output(["ipconfig", "/all"]).decode('utf-8')
        return results

    def nix_execute(self):
        logging.info("IFCONFIG called. ")
        results = subprocess.check_output(["ifconfig"]).decode("utf-8")
        return results



if __name__ == "__main__":
    nic = NetworkInfoCommand()
    nic.execute()

