import psutil
import logging
import Constants
from Monitor import Monitor

logger = logging.getLogger("Monitor")
logger.setLevel(logging.INFO)

## Polls PSUtil to get a byte value for RAM currently in use.
#
#
class RamByteMonitor(Monitor):

    def __init__(self):
        Monitor.__init__(self, Constants.RAM_BYTE_MONITOR)
        logger.info("Initializing RAM MB Usage Monitor")
        memory_object = psutil.virtual_memory()
        self._minimum = 0.0
        self._maximum = memory_object.total
        logger.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Calculates memory in use by subtracting total memory from available memory.
    #  @return Float indicating the amount of bytes currently in use in memory.
    def poll(self):
        memory_object = psutil.virtual_memory()
        in_use = memory_object.total - memory_object.available
        return float(in_use)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum







