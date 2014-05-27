import logging
import threading
import Pyro4
import Notifier
import MonitorManager
import socket
import random
import DriveDiscovery
## The class that communicates with the server. This will need to be made into a Pyro4 Daemon, with a thread running the
# polling duties, and another simply for communicating to the server.
#
# Holds onto a monitor manager as well as the command executor and notifier. A facade class to the underlying objects.
class Client:
    def __init__(self, client_id=-1):
        logging.info("Initializing client with ID:{}".format(client_id))
        self._client_id = client_id
        self._monitor_manager = None
        self._command_executor = None
        self._local_name = None
        #TODO is there a better way to start a new notifier?
        self._notifier = Notifier.Notifier()


    ## Sets a list of monitors to be run on this client, via a monitor manager.
    def set_monitor_manager(self, monitor_manager):
        self._monitor_manager = monitor_manager

    ## Sets the process responsible for executing commands on the host computer.
    def set_command_executor(self, command_executor):
        self._command_executor = command_executor

    ## Delegates the gather of data off to the monitor manager, which in turn polls all the monitors.
    # @return A dictionary holding each monitor's ID as the key, and the minimum/current/maximum as a list for the values.
    # TODO NIX THIS ??? Do we even want the server to be able to do a manual Poll?
    def gather_data(self):
        if self._monitor_manager is not None:
            return self._monitor_manager.poll_all()
        else:
            logging.error("Could not gather data. No monitor manager is set.")
            return None

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

    def register_to_name_server(self):
        def register_internal():
            logging.info("Registering Client to nameserver.")
            hostname = socket.gethostname()
            ns = None
            while ns is None:
                try:
                    ns = Pyro4.locateNS()
                    daemon = Pyro4.Daemon()
                    client_uri = daemon.register(self)

                    ns.register("shizuka.client.{}.{}".format(hostname, self._client_id), client_uri)
                    logging.info("Found the following in the nameserver after registration of client:{}".format(ns.list()))
                    self._local_name = "shizuka.client.{}".format(hostname)
                    daemon.requestLoop()
                except Exception as e:
                    logging.error("Couldn't connect to nameserver to register the client. Re-trying.: {}".format(e))

        request_thread = threading.Thread(target=register_internal, name="request_waiting_thread")
        #request_thread.setDaemon(True)
        request_thread.start()


def main():
    import RamByteMonitor
    import RamPercentMonitor
    import BytesSentMonitor
    import BytesReceivedMonitor
    import StorageByteMonitor
    import StoragePercentMonitor
    cid = random.randint(0, 10000)
    logging.basicConfig(level=logging.INFO)
    client = Client(cid)
    monman1 = MonitorManager.MonitorManager()
    m1 = RamByteMonitor.RamByteMonitor(1)
    m2 = RamPercentMonitor.RAMPercentMonitor(2)
    m3 = BytesReceivedMonitor.BytesReceivedMonitor(3)
    m4 = BytesSentMonitor.BytesSentMonitor(4)
    i = 5
    for mount_point in DriveDiscovery.get_drive_mountpoints():
        monman1.add_monitor(StoragePercentMonitor.StoragePercentMonitor(i, mount_point))
        monman1.add_monitor(StorageByteMonitor.StorageByteMonitor(i+1, mount_point))
        i += 2
    monman1.add_monitor(m1)
    monman1.add_monitor(m2)
    monman1.add_monitor(m3)
    monman1.add_monitor(m4)
    client.set_monitor_manager(monman1)
    client.register_to_name_server()
    client.begin_monitoring()


if __name__=="__main__":
    main()
