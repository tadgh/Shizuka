import logging

## Singleton class that handles all monitors on the client.
#
# This class handles the addition and removal of monitors.
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
            logging.info("Created a new Monitor Manager singleton...")
        return class_._instance

    ## Does nothing, Singleton pattern. Otherwise, __init__ is called each time
    #  the singleton is accessed, which is not desired behaviour.
    #
    #
    def __init__(self):
        return

    ## Adds a monitor object to the dictionary of monitors running on the client
    #
    #
    def add_monitor(self, monitor):
        logging.info("Adding monitor: {}".format(monitor.get_id()))
        self._instance.monitor_list[monitor.get_id()] = monitor

    ## Removes a monitor object from the dictionary of monitors running on the client.
    #  @param monitor_id The specific ID of the monitor that needs to be removed.
    #
    def remove_monitor_by_id(self, monitor_id):
        try:
            logging.info("Deleting Monitor: {}".format(monitor_id) )
            del self._instance.monitor_list[monitor_id]
        except KeyError:
            logging.error("Could not find Monitor with id: {}. Has it already been removed?".format(monitor_id))

    ## Removes a monitor object from the dictionary of monitors running on the client.
    #  @param monitor The specific monitor object that needs to be removed.
    #
    def remove_monitor(self, monitor):
        try:
            logging.info("Deleting Monitor: {}".format(monitor))
            del self._instance.monitor_list[monitor.get_id()]
        except KeyError:
            logging.error("Could not find Monitor:{} in the monitor list. Has it already been removed?".format(monitor))

    def list_monitors(self):
        return self._instance.monitor_list

