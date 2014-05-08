import unittest
import psutil
import StoragePercentMonitor


class TestStoragePercentMonitor(unittest.TestCase):


    def setUp(self):
        self._drive = psutil.disk_partitions()[0].device
        self.storage_percent_monitor = StoragePercentMonitor.StoragePercentMonitor(1, self._drive)

    def test_monitor_not_paused(self):
        paused = self.storage_percent_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        storage_percent = self.storage_percent_monitor.poll()
        self.assertIsInstance(storage_percent, float)

    def test_ram_within_limits(self):
        percent_storage = self.storage_percent_monitor.poll()
        minimum = self.storage_percent_monitor.minimum()
        maximum = self.storage_percent_monitor.maximum()
        self.assertTrue(percent_storage > minimum and percent_storage <= maximum,
                        "Storage Percent is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_storage,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()