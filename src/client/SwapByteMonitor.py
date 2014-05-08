import psutil
import logging
from Monitor import Monitor

## Polls PSUtil to get a byte value for the amount of SWAP memory currently in use.
#
#
class SwapByteMonitor(Monitor):


    def __init__(self, identifier):
        Monitor.__init__(self, identifier)
        logging.info("Initializing Swap MB Usage Monitor")
        memory_object = psutil.swap_memory()
        self._minimum = 0.0
        self._maximum = memory_object.total
        logging.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Gets Bytes of Swap Memory in use by means of PSUtil's swap_memory() method.
    #  @return Float indicating the bytes of memory currently in SWAP.
    def poll(self):
        memory_object = psutil.swap_memory()
        in_use = memory_object.total - memory_object.free
        return float(in_use)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum







