import logging
import threading
import Pyro4
import Notifier
import MonitorManager
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
        #TODO is there a better way to start a new notifier?
        self._notifier = Notifier.Notifier(self._client_id)


    ## Sets a list of monitors to be run on this client, via a monitor manager.
    def set_monitor_manager(self, monitor_manager):
        self._monitor_manager = monitor_manager

    ## Sets the process responsible for executing commands on the host computer.
    def set_command_executor(self, command_executor):
        self._command_executor = command_executor

    #Fires off the command to the notifier to start polling the hardware and sending the data to the server.
    def begin_monitoring(self):
        logging.info("Client has started the notifier's loop.")
        self._notifier.run()

    # Returns the monitor_list variable from the monitor_manager.
    def list_monitors(self):
        if self._monitor_manager is not None:
            return self._monitor_manager.list_monitors()
        else:
            logging.error("Could not gather data. No monitor manager is set.")
            return None
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


def main():
    import RamByteMonitor
    import BytesSentMonitor
    import BytesReceivedMonitor
    import StorageByteMonitor

    cid = random.randint(0, 10000)
    logging.basicConfig(level=logging.INFO)
    client = Client()
    monman1 = MonitorManager.MonitorManager()
    m1 = RamByteMonitor.RamByteMonitor(1)
    m3 = BytesReceivedMonitor.BytesReceivedMonitor(3)
    m4 = BytesSentMonitor.BytesSentMonitor(4)
    i = 5
    for index, mount_point in enumerate(Utils.get_drive_mountpoints()):
        monman1.add_monitor(StorageByteMonitor.StorageByteMonitor(i +index, mount_point))
    monman1.add_monitor(m1)
    monman1.add_monitor(m3)
    monman1.add_monitor(m4)
    client.set_monitor_manager(monman1)
    client.register_to_name_server()
    client.begin_monitoring()


if __name__=="__main__":
    main()
