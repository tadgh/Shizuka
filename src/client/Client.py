import logging
import Pyro4

## The class that communicates with the server. This will need to be made into a Pyro4 Daemon, with a thread running the
# polling duties, and another simply for communicating to the server.
#
# Holds onto a monitor manager as well as the command executor.
class Client:
    def __init__(self, client_id=-1):
        self._client_id = client_id
        self._monitor_manager = None

    ## Sets a list of monitors to be run on this client, via a monitor manager.
    def set_monitor_manager(self, monitor_manager):
        self._monitor_manager = monitor_manager

    ## Sets the process responsible for executing commands on the host computer.
    def set_command_executor(self, command_executor):
        #TODO work on this later. Irrelevant at the moment.
        pass

    ## Delegates the gather of data off to the monitor manager, which in turn polls all the monitors.
    # @return A dictionary holding each monitor's ID as the key, and the minimum/current/maximum as a list for the values.
    def gather_data(self):
        if self._monitor_manager is not None:
            return self._monitor_manager.poll_all()
        else:
            logging.error("Could not gather data. No monitor manager is set.")
            return None

    # Returns the monitor_list variable from the monitor_manager.
    def list_monitors(self):
        if self._monitor_manager is not None:
            return self._monitor_manager.list_monitors()
        else:
            logging.error("Could not gather data. No monitor manager is set.")
            return None

def main():
    client = Client()
    #todo Do some pyro stuff?


if __name__=="__main__":
    main()
