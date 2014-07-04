import logging
import threading
import Pyro4
import CommandInterface
import Constants
import MonitorManager
import Notifier
import socket
import random
import Utils
logger = logging.getLogger("Client")

## The class that serves to start up all necessary services on the client.
#  Does the following:
#  1. Creates a Monitor Manager(empty)
#  2. Creates a CommandInterface(with default allowable commands)
#  3. Creates a Notifier
#  4. Creates a MessageHandler
#  5. Connects them all
#  6. Sends a discovery message to the server.
#  7. Begins the monitoring loop.
class Client:
    def __init__(self):
        self._client_id = self.input_unique_id()
        logger.info("Initializing client with ID:{}".format(self._client_id))
        self._monitor_manager = None
        self._command_executor = None
        self._message_queue = None
        #TODO is there a better way to start a new notifier?
        self._notifier = None

    def get_client_id(self):
        return self._client_id

    ## Sets a list of monitors to be run on this client, via a monitor manager.
    def set_monitor_manager(self, monitor_manager):
        self._monitor_manager = monitor_manager

    ## Sets the data notifier for the client
    def set_notifier(self, notifier):
        self._notifier = notifier

    ## Allows the user to set a unique identifier for this client. If input is '', sets it to the FQDN of the client.
    # @return the new unique ID.
    def input_unique_id(self):
        unique_id = input("Enter a unique name for this client(Just pressing enter will use the FQDN): ")
        if unique_id.strip() == '':
            unique_id = socket.getfqdn()
        return unique_id

    ## Sets the process responsible for executing commands on the host computer.
    #
    # @param command_executor the CommandInterface object for receiving command objects.
    def set_command_executor(self, command_executor):
        self._command_executor = command_executor

    ## Sets the message Queue for the client. Internally, requires calls the get_queue() of the handler.
    #
    # @param message_handler The MessageHandler that is used for the messages.
    def set_message_queue(self, message_handler):
        self._message_queue = message_handler.get_queue()

    ## Fires off the command to the notifier to start polling the hardware and sending the data to the server.
    #
    #
    def begin_monitoring(self):
        logger.info("Client has started the notifier's loop.")
        self._notifier.start()

    ## Returns the monitor_list variable from the monitor_manager.
    #
    # @return list of monitors that have been added.
    def list_monitors(self):
        if self._monitor_manager is not None:
            return self._monitor_manager.list_monitors()
        else:
            logger.error("Could not gather data. No monitor manager is set.")
            return None

    ## sends command off to the CommandInterface , which will then process whether it is allowed, and execute it.
    #
    # @param command The command tag(See Constants) indicating which command is to be executed.
    # @return the result of the command execution. Passed up from CommandInterface
    def execute_command(self, command):
        logger.info("Client Attempting to send command to CommandInterface")
        if self._command_executor is not None:
            logger.info("Passing command: '{}' off to command executor".format(command))
            return self._command_executor.execute_command(command)
        else:
            logger.error("Can not execute command. No command executor is set!")
            return "Can not execute command. No command executor is set!"

    ## A special type of command, changes the monitor configuration on the client. Adds or removes based on the contents
    # of the dictionary. No return value as the Monitor Manager puts a results message in the queue.
    # @param config_dict The dictionary containing the Information. See MonitorManager for implementation details.
    def configure_monitors(self, config_dict):

        if self._monitor_manager is not None:
            logger.info("Sending configuration dictionary to MonitorManager.")
            self._monitor_manager.handle_config(config_dict)
            return True
        else:
            logger.error("Could not pass monitoring message ")
            return False

    #Starts a new thread that continuously attempts to find the nameserver. Once found, it registers the client with its
    #hostname, which is shizuka.client.[hostname] . It then begins the request loop waiting for requests.
    def register_to_name_server(self):
        def register_internal():
            logger.info("Registering Client to nameserver.")
            ns = None
            while ns is None:
                try:
                    ns = Pyro4.locateNS()
                    daemon = Pyro4.Daemon()
                    client_uri = daemon.register(self)
                    ns.register("shizuka.client." + self._client_id, client_uri)
                    logger.info("Found the following in the nameserver after registration of client:{}".format(ns.list()))
                    daemon.requestLoop()
                except Exception as e:
                    logger.error("Couldn't connect to nameserver to register the client. Re-trying.: {}".format(e))

        request_thread = threading.Thread(target=register_internal, name="request_waiting_thread")
        request_thread.start()

    ## Adds a discovery Message to the message Queue. You can see the content of the discovery message in the Utils file.
    # This is how the webserver prefers to identify new clients.
    def send_discovery(self):
        message = {}
        message["type"] = "Discovery"
        message["data"] = Utils.discover()
        message["data"]["CLIENT_ID"] = self._client_id
        self._message_queue.put(message)


def main():
    import MessageHandler
    import Notifier
    import threading
    logger.setLevel(logging.INFO)
    logger.info("Instantiating the different components we need.")


    #Instantiating the different components we need.
    client = Client()
    monman = MonitorManager.MonitorManager()
    cexec = CommandInterface.CommandInterface()
    notifier = Notifier.Notifier(client.get_client_id())
    messagehandler = MessageHandler.MessageHandler(client.get_client_id())

    logger.info("Setting the outgoing message queue.")
    #Setting the outgoing message queue
    client.set_message_queue(messagehandler)
    monman.set_message_queue(messagehandler)

    ##TODO THIS SHIT IS TEMPORARY. MAKE A LOCK FACTORY CLASS OR SOMETHING.
    ##SETTING LOCKS FOR THE MONITORS SO WHEN THEY ARE BEING MODIFIED THEY CANT BE POLLED.
    lock = threading.RLock()
    monman.set_lock(lock)
    notifier._data_manager.set_lock(lock)

    logger.info("Giving client access to crucial components")
    #Giving client access to crucial components
    client.set_monitor_manager(monman)
    client.set_command_executor(cexec)
    client.set_notifier(notifier)

    #making the client visible on the nameserver
    client.register_to_name_server()

    #Sending a "Hey I"m here!" message to the server.
    client.send_discovery()

    #Starting the outgoing message queue
    messagehandler.start()

    #Beginning the monitoring cycle.
    client.begin_monitoring()


if __name__=="__main__":
    main()
