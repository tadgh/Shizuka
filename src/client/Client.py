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


## The class that communicates with the server. This will need to be made into a Pyro4 Daemon, with a thread running the
# polling duties, and another simply for communicating to the server.
#
# Holds onto a monitor manager as well as the command executor and notifier. A facade class to the underlying objects.
class Client:
    def __init__(self):
        self._client_id = "shizuka.client.{}".format(socket.gethostname())
        logging.info("Initializing client with ID:{}".format(self._client_id))
        self._monitor_manager = None
        self._command_executor = None
        self._message_queue = None
        #TODO is there a better way to start a new notifier?
        self._notifier = None


    ## Sets a list of monitors to be run on this client, via a monitor manager.
    def set_monitor_manager(self, monitor_manager):
        self._monitor_manager = monitor_manager

    ## Sets the data notifier for the client
    def set_notifier(self, notifier):
        self._notifier = notifier


    ## Sets the process responsible for executing commands on the host computer.
    #
    # @param command_executor the CommandInterface object for receiving command objects.
    def set_command_executor(self, command_executor):
        self._command_executor = command_executor

    ## Sets the message handler for the client.
    def set_message_queue(self, message_handler):
        self._message_queue = message_handler.get_queue()

    ## Fires off the command to the notifier to start polling the hardware and sending the data to the server.
    #
    #
    def begin_monitoring(self):
        logging.info("Client has started the notifier's loop.")
        self._notifier.start()

    ## Returns the monitor_list variable from the monitor_manager.
    #
    # @return list of monitors that have been added.
    def list_monitors(self):
        if self._monitor_manager is not None:
            return self._monitor_manager.list_monitors()
        else:
            logging.error("Could not gather data. No monitor manager is set.")
            return None

    def execute_command(self, command):
        logging.info("Passing command: '{}' off to command executor".format(command))
        return self._command_executor.execute_command(command)
        
    #Starts a new thread that continuously attempts to find the nameserver. Once found, it registers the client with its
    #hostname, which is shizuka.client.[hostname] . It then begins the request loop waiting for requests.
    def register_to_name_server(self):
        def register_internal():
            logging.info("Registering Client to nameserver.")
            ns = None
            while ns is None:
                try:
                    ns = Pyro4.locateNS()
                    daemon = Pyro4.Daemon()
                    client_uri = daemon.register(self)
                    ns.register(self._client_id, client_uri)
                    logging.info("Found the following in the nameserver after registration of client:{}".format(ns.list()))
                    daemon.requestLoop()
                except Exception as e:
                    logging.error("Couldn't connect to nameserver to register the client. Re-trying.: {}".format(e))

        request_thread = threading.Thread(target=register_internal, name="request_waiting_thread")
        #request_thread.setDaemon(True)
        request_thread.start()

    def send_discovery(self):
        message = {}
        message["type"] = "Discovery"
        message["data"] = Utils.discover()
        self._message_queue.put(message)



def main():
    import MessageHandler
    import Notifier
    import queue

    logging.basicConfig(level=logging.INFO)

    client = Client()
    monman = MonitorManager.MonitorManager()
    cexec = CommandInterface.CommandInterface()
    notifier = Notifier.Notifier("shizuka.client.Aristotle")
    messagehandler = MessageHandler.MessageHandler("shizuka.client.Testerino")

    #config dictionary for starting monitors.
    #monitor_dict = {
    #    "add": [Constants.RAM_BYTE_MONITOR, Constants.BYTES_RECEIVED_MONITOR, Constants.CPU_PERCENT_MONITOR]
    #}
    #for mount_point in Utils.get_drive_mountpoints():
    #    monitor_dict["add"].append(Constants.STORAGE_BYTE_MONITOR + mount_point)

    #monman.handle_config(monitor_dict)
    client.set_message_queue(messagehandler)
    client.set_monitor_manager(monman)
    client.set_command_executor(cexec)
    client.set_notifier(notifier)
    client.register_to_name_server()
    client.send_discovery()
    messagehandler.start()#OOPS FORGOT TO START THE HANDLER.
    client.begin_monitoring()


if __name__=="__main__":
    main()
