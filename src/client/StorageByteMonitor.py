import psutil
import logging
import Constants
from Monitor import Monitor

## Polls PSUtil to get a byte value for used storage on a particular drive.
#
#
class StorageByteMonitor(Monitor):

    def __init__(self, drive_root):
        Monitor.__init__(self, "{0} {1}".format(Constants.STORAGE_BYTE_MONITOR, str(drive_root)))
        logging.info("Initializing Storage Byte Monitor")
        self._drive_root = drive_root
        self._minimum = 0.0
        storage_object = psutil.disk_usage(self._drive_root)
        self._maximum = float(storage_object.total)
        logging.info("Minimum: {}, Current: {}, Maximum: {} ".format(self._minimum, self.poll(), self._maximum))

    ## Gets Storage % in use by means of PSUtil's disk_usage() method.
    #  @return Float indicating the bytes of storage currently in use
    def poll(self):
        storage_object = psutil.disk_usage(self._drive_root)
        in_use = storage_object.used
        return float(in_use)

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum