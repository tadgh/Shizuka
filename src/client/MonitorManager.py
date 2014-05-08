import logging


## Class that handles all monitors on the client.
#
# This class is responsible for getting all data returned from all the monitors, and passing it along to the networking
# section of the program, for sending to the server. This class also handles addition and removal of particular monitors.
#
class MonitorManager():
    ## Sets an empty monitor list.
    #
    #
    def __init__(self):
        logging.info("Started up new Monitor Manager...")
        self.monitor_list = {}
        pass

    ## Adds a monitor object to the dictionary of monitors running on the client
    #
    #
    def add_monitor(self, monitor):
        logging.info("Adding monitor: {}".format(monitor.get_id()))
        self.monitor_list[monitor.get_id()] = monitor

    ## Removes a monitor object from the dictionary of monitors running on the client.
    #  @param monitor_id The specific ID of the monitor that needs to be removed.
    #
    def remove_monitor_by_id(self, monitor_id):
        try:
            logging.info("Deleting Monitor: {}".format(monitor_id) )
            del self.monitor_list[monitor_id]
        except KeyError:
            logging.error("Could not find Monitor with id: {}. Has it already been removed?".format(monitor_id))

    ## Removes a monitor object from the dictionary of monitors running on the client.
    #  @param monitor The specific monitor object that needs to be removed.
    #
    def remove_monitor(self, monitor):
        try:
            logging.info("Deleting Monitor: {}".format(monitor))
            del self.monitor_list[monitor.get_id()]
        except KeyError:
            logging.error("Could not find Monitor:{} in the monitor list. Has it already been removed?".format(monitor))