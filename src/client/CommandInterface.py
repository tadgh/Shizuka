from RestartCommand import RestartCommand
from ShutdownCommand import ShutdownCommand
from NetworkInfoCommand import NetworkInfoCommand
import Constants
import logging

logger = logging.getLogger("CommandInterface")
logger.setLevel(logging.INFO)
## Receives commands from the server and executes them.
#
class CommandInterface():

    def __init__(self):
        self._state = "Unimplemented"
        self._message_queue = None
        restart_command = RestartCommand()
        shutdown_command = ShutdownCommand()
        network_info_command = NetworkInfoCommand()

        self._allowed_commands = {restart_command.get_tag(): restart_command,
                                  shutdown_command.get_tag(): shutdown_command,
                                  network_info_command.get_tag(): network_info_command}

    ## Every class that needs to send messages has this method. Gives the CommandInterface a place to put outgoing messages.
    # @param handler The MessageHandler you would like to send messages through.
    def set_message_queue(self, handler):
        logger.info("Setting the outgoing message queue for the CommandInterface.")
        self._message_queue = handler.get_queue()

    ## Executes a command passed from the server.
    #  @param command_object The command object to be executed.
    #  @return The results from the call(if any). None is returned if the call is not allowed.
    def execute_command(self, command_tag):
        try:
            logger.info("Executing Command: {}".format(command_tag))
            results = self._allowed_commands[command_tag].execute()
            return results
        except KeyError:
            logger.error("""Command {} not found in the client's list of allowed commands.
                           Here is what is allowed: {}""".format(command_tag, self._allowed_commands.keys()))
            return None
        except Exception as e:
            logger.error("Unknown error while executing Command: {}".format(e))


if __name__ == "__main__":
    ci = CommandInterface()
    res = ci.execute_command(Constants.NETWORK_INFO_TAG)
    print(res)
