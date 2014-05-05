import psutil
import logging
from Monitor import Monitor

## Polls PSUtil to get a percent value for swap memory in use.
#
#
class SwapPercentMonitor(Monitor):

    def __init__(self):
        Monitor.__init__(self)
        logging.info("Initializing SWAP Percent Monitor")
        logging.info("Minimum: {}, Current: {}, Maximum: {}".format(0.0, self.poll(), 100.0))

    ## Gets % of Swap Memory in use by means of PSUtil's swap_memory() method.
    #  @return Float indicating the % of memory currently used in SWAP.
    def poll(self):
        memory_object = psutil.swap_memory()
        return memory_object.percent

    def minimum(self):
        return 0.0

    def maximum(self):
        return 100.0


