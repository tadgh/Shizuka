import psutil
import sys
import time
import logging
from Monitor import Monitor

## Polls PSUtil to get a value for the amount of bytes sent per second (B/s).
#
logging.basicConfig(level=logging.INFO)
class BytesSentMonitor(Monitor):


    def __init__(self, identifier):
        Monitor.__init__(self, identifier)
        logging.info("Initializing Bytes Sent Monitor")
        self._minimum = 0.0
        self._maximum = sys.maxsize
        logging.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Gets the output rate of the monitor in bytes/sec.
    #  @return Float indicating how many bytes/sec.
    def poll(self):
        initial_bytes = psutil.net_io_counters()[0]
        time.sleep(1)
        final_bytes = psutil.net_io_counters()[0]
        return float(final_bytes - initial_bytes)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

