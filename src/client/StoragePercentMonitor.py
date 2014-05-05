import psutil
import logging
from Monitor import Monitor

## Polls PSUtil to get a percent value for used storage  on a particular drive.
#
#
class StoragePercentMonitor(Monitor):

    def __init__(self, drive_root):
        Monitor.__init__(self)
        logging.info("Initializing Storage Percent Monitor")
        self._drive_root = drive_root
        self._minimum = 0.0
        self._maximum = 100.0
        logging.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Gets Storage % in use by means of PSUtil's disk_usage() method.
    #  @return Float indicating the % of storage currently in use
    def poll(self):
        storage_object = psutil.disk_usage(self._drive_root)
        in_use = storage_object.percent
        return float(in_use)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum


