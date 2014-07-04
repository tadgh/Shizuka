import logging
import Constants
import RamByteMonitor
import StorageByteMonitor
import CPUPercentMonitor
import BytesReceivedMonitor
import BytesSentMonitor
import SwapByteMonitor

logger = logging.getLogger("Monitor Manager")
logger.setLevel(logging.INFO)
## Singleton class that handles all monitors on the client.
#
# This class handles the addition and removal of monitors. Contains the factory
#
class MonitorManager():
    _instance = None
    ## Create a MonitorManager singleton.
    #
    #
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_._instance.monitor_list = {}
            class_._instance._message_queue = None
            class_._instance._monitor_lock = None
            logger.info("Created a new Monitor Manager singleton...")
        return class_._instance

    ## Does nothing, Singleton pattern. Otherwise, __init__ is called each time
    #  the singleton is accessed, which is not desired behaviour.
    #
    #
    def __init__(self):
        return

    def set_lock(self, lock):
        self._instance._monitor_lock = lock

    ## Sets the message handler, and grabs the relevant queue.
    def set_message_queue(self, handler):
        self._instance._message_queue = handler.get_queue()

    ## Queues the message to be sent back to the server.
    def send_message_to_server(self, message):
        message['type'] = "Monitor Report"
        if self._instance._message_queue is not None:
            logger.info("Sending message off to the queue.")
            self._instance._message_queue.put(message)
        else:
            logger.warning("No message queue is set in the monitor manager. Cannot send message: {}".format(message))

    ## Adds a monitor object to the dictionary of monitors running on the client
    #
    #
    def add_monitor(self, monitor):
        logger.info("Adding monitor: {}".format(monitor.get_type()))
        self._instance.monitor_list[monitor.get_type()] = monitor

    ## Removes a monitor object from the dictionary of monitors running on the client.
    #  @param monitor_id The specific ID of the monitor that needs to be removed.
    #
    def remove_monitor_by_type(self, monitor_type):
        try:
            logger.info("Deleting Monitor: {}".format(monitor_type) )
            del self._instance.monitor_list[monitor_type]
        except KeyError:
            logger.error("Could not find Monitor with type: {}. Has it already been removed?".format(monitor_type))

    ## Removes a monitor object from the dictionary of monitors running on the client.
    #  @param monitor The specific monitor object that needs to be removed.
    #
    def remove_monitor(self, monitor):
        try:
            logger.info("Deleting Monitor: {}".format(monitor))
            del self._instance.monitor_list[monitor.get_type()]
        except KeyError:
            logger.error("Could not find Monitor:{} in the monitor list. Has it already been removed?".format(monitor))

    #Empty out all monitors.
    def clear_monitors(self):
        self._instance.monitor_list.clear()

    ## Returns list of monitors currently held, otherwise Empty List.
    def list_monitors(self):
        return self._instance.monitor_list

    ## Handles a monitor configuration dictionary and delegates creation and deletion of monitors as necessary.
    ## TODO maybe don't have the result set built here. Keep separate?
    def handle_config(self, config_dict):
        self._instance._monitor_lock.acquire()
        logger.info("Attempting to handle the configuration dictionary...")
        results = {}
        try:
            for monitor_type in config_dict["add"]:
                self.add_monitor(self.create_monitor(monitor_type))
                if monitor_type in self.list_monitors().keys():
                    results["Added"] = monitor_type
                else:
                    results["Failed"] = monitor_type + " failed to add."
            for monitor_type in config_dict["remove"]:
                self.remove_monitor_by_type(monitor_type)
                if monitor_type not in self.list_monitors().keys():
                    results["Removed"] = monitor_type
                else:
                    results["Failed"] = monitor_type + " failed to remove."
        except Exception as e:
            print("Unknown Error Occurred Modifying the monitor list!: {}".format(e))

        self.send_message_to_server(results)
        self._instance._monitor_lock.release()

    ## Monitor factory based on type.
    # @param monitor_type the TYPE of the monitor, can be found in Constants.py
    # @return the correct subclass of monitor based on the type passed in
    @staticmethod
    def create_monitor(monitor_type):
        if monitor_type == Constants.RAM_BYTE_MONITOR:
            return RamByteMonitor.RamByteMonitor()
        elif monitor_type == Constants.BYTES_RECEIVED_MONITOR:
            return BytesReceivedMonitor.BytesReceivedMonitor()
        elif monitor_type == Constants.BYTES_SENT_MONITOR:
            return BytesSentMonitor.BytesSentMonitor()
        elif monitor_type == Constants.SWAP_BYTE_MONITOR:
            return SwapByteMonitor.SwapByteMonitor()
        elif monitor_type == Constants.CPU_PERCENT_MONITOR:
            return CPUPercentMonitor.CPUPercentMonitor()
        elif monitor_type.startswith(Constants.STORAGE_BYTE_MONITOR):
            logger.info("create_monitor() -> Found storage monitor request. ")
            #parse out the mount point that the storage monitor will attempt to monitor.
            #Element 2 of the tuple is the part after the separator: i.e; Storage Monitor: C:\
            mount_point = monitor_type.partition(Constants.STORAGE_BYTE_MONITOR)[2].strip()
            logger.info("create_monitor() -> Requested Mount point is: {}. ".format(mount_point))
            if mount_point != '':
                try:
                    return StorageByteMonitor.StorageByteMonitor(mount_point)
                except OSError: #The mount point doesn't exist.
                    logger.error("create_monitor() -> Mount point doesn't seem to exist!")
                    return None #for now. Will have to determine what to do later.
        else: #The type didn't match anything we know of.
            logger.error("create_monitor() -> Unable to match the requested type.")
            raise ValueError

