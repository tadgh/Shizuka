import psutil
from Monitor import Monitor


class RAMMonitor(Monitor):
    """
    This class handles RAM Resource monitoring.
    """

    def __init__(self):
        Monitor.__init__(self)
        print("Initializing RAM Monitor")

    def poll(self):
        """
        This function returns the ram usage as a float from 0.0 to 100.0.
        """
        memory_object = psutil.virtual_memory()
        return memory_object.percent








