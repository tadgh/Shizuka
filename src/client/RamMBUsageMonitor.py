import psutil
import logging
from Monitor import Monitor


class RamMBUsageMonitor(Monitor):
    """
    This class handles RAM MegaByte Resource monitoring. All values returned in MB.
    """

    def __init__(self):
        Monitor.__init__(self)
        logging.info("Initializing RAM MB Usage Monitor")
        memory_object = psutil.virtual_memory()
        self._minimum = 0.0
        self._megabyte_divisor = 1024 * 1024
        self._maximum = memory_object.total / self._megabyte_divisor
        logging.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    def poll(self):
        memory_object = psutil.virtual_memory()
        in_use = memory_object.total - memory_object.available
        return in_use / self._megabyte_divisor

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum







