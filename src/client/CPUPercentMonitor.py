import psutil
import logging
import Constants
from Monitor import Monitor

logger = logging.getLogger("Monitor")
logger.setLevel(logging.INFO)
## Polls PSUtil to get a percent value for CPU currently in use.
#
#
class CPUPercentMonitor(Monitor):

    def __init__(self):
        Monitor.__init__(self, Constants.CPU_PERCENT_MONITOR)
        logger.info("Initializing CPU % Usage Monitor")
        self._minimum = 0.0
        self._maximum = 100
        logger.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Calculates CPU in use from PSutil.
    def poll(self):
        percent_used = psutil.cpu_percent(interval=0.5)
        return percent_used

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum



if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    cpumon = CPUPercentMonitor()
    print(cpumon.poll())






