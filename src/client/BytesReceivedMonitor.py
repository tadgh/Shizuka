import sys
import time
import logging
import Constants
from Monitor import Monitor
import psutil

logger = logging.getLogger("Monitor")
logger.setLevel(logging.INFO)

## Polls PSUtil to get a value for the amount of bytes received per second (B/s).
#
class BytesReceivedMonitor(Monitor):

    def __init__(self):
        Monitor.__init__(self, Constants.BYTES_RECEIVED_MONITOR)
        logger.info("Initializing Bytes Received Monitor")
        self._casual_name = "Network Received Monitor"
        self._minimum = 0.0
        self._maximum = sys.maxsize
        logger.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Gets the received bit rate of the monitor in bytes/sec.
    #  @return Float indicating how many bytes/sec are received.
    def poll(self):
        initial_bytes = psutil.net_io_counters()[1]
        time.sleep(1)
        final_bytes = psutil.net_io_counters()[1]
        return float(final_bytes - initial_bytes)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum