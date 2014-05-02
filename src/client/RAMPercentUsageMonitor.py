import psutil
import logging
from Monitor import Monitor


class RAMPercentUsageMonitor(Monitor):
    """
    This class handles RAM Percent Resource monitoring.
    """

    def __init__(self):
        Monitor.__init__(self)
        logging.info("Initializing RAM Percent Monitor")
        logging.info("Minimum: {}, Current: {}, Maximum: {}".format(0.0, self.poll(), 100.0))

    def poll(self):
        memory_object = psutil.virtual_memory()
        return memory_object.percent

    def minimum(self):
        return 0.0

    def maximum(self):
        return 100.0









