## Receives commands from the server and executes them.
#
class CommandInterface():

    def __init__(self):
        self._state = "Unimplemented"

    ## Executes a command passed from the server.
    #  @param command_object The command object to be executed.
    #
    def execute_command(self, command_object):
        raise NotImplementedError()

    ## Server request to add a monitor object
    #  @param monitor The monitor to be added
    #
    def add_monitor(self, monitor):
        raise NotImplementedError()