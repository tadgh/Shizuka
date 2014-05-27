import logging
import MonitorManager
## Singleton Class that handles all data on the client.
#
# This class is responsible for getting all data returned from all the monitors, and passing it along to the networking
# section of the program, for sending to the server.
#
class DataManager():
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self._instance._state = "Unimplemented"

    ## Polls all monitors held by the monitor manager.
    #  @return A dict that has Key values of the Monitor IDs, and a list containing [minimum, current, maximum] for the
    # particular monitor.
    #
    def poll_all(self):
        all_results = {}

        for monitor_id, monitor in MonitorManager.MonitorManager().list_monitors().items():
            all_results[monitor_id] = [monitor.get_name(),monitor.minimum(), monitor.poll(), monitor.maximum()]

        logging.info("Forthcoming Are all results from the Monitor Manager: \n***\n" +
                     "\n".join([str(key) + str(value) for key,value in  all_results.items()]) + "\n***")
        return all_results

    ## Polls a specific monitor held by the monitor manager.
    # @return Float value of the resource being monitored.
    #
    def poll_monitor_by_id(self, monitor_id):
        try:
            monitor = MonitorManager.MonitorManager().list_monitors()[monitor_id]
            return monitor.poll()
        except KeyError:
            logging.error("Could not poll monitor with ID:{} as it was not found in the monitor list".format(monitor_id))
            return None