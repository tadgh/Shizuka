import psutil
import logging
from Monitor import Monitor

## Polls PSUtil to get a percent value for RAM currently in use.
#
#
class RAMPercentMonitor(Monitor):

    def __init__(self):
        Monitor.__init__(self)
        logging.info("Initializing RAM Percent Monitor")
        logging.info("Minimum: {}, Current: {}, Maximum: {}".format(0.0, self.poll(), 100.0))

    ## Gets memory in use by using PSUtil's 'percent' attribute on virtual_memory()
    #  @return Float indicating the % of memory currently in use.
    def poll(self):
        memory_object = psutil.virtual_memory()
        return memory_object.percent

    def minimum(self):
        return 0.0

    def maximum(self):
        return 100.0









