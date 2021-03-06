import logging
import MonitorManager

logger = logging.getLogger("DataManager")
logger.setLevel(logging.INFO)
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
            class_._instance._message_queue = None
            class_._instance._monitor_lock = None
        return class_._instance

    def __init__(self):
        self._instance._state = "Unimplemented"

    # For accessing the monitors. The lock ensures that we don't
    def set_lock(self, lock):
        self._instance._monitor_lock = lock

    # Sets the handler for outgoing messages to the server.
    def set_message_queue(self, handler):
        self._instance._message_queue = handler.get_queue()

    ## Polls all monitors held by the monitor manager.
    #  @return A dict that has Key values of the Monitor IDs, and a list containing [minimum, current, maximum] for the
    # particular monitor.
    #
    def poll_all(self):
        self._instance._monitor_lock.acquire()
        all_results = {}

        for monitor_id, monitor in MonitorManager.MonitorManager().list_monitors().items():
            all_results[monitor.get_type()] = [monitor.minimum(), monitor.poll(), monitor.maximum()]

        logger.info("Forthcoming Are all results from the Monitor Manager: \n***\n" +
                     "\n".join([str(key) + str(value) for key, value in all_results.items()]) + "\n***")
        self._instance._monitor_lock.release()
        return all_results
