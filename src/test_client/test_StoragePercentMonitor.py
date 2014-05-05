import unittest
import psutil
import StoragePercentMonitor


class TestStoragePercentMonitor(unittest.TestCase):


    def setUp(self):
        self._drive = psutil.disk_partitions()[0].device
        self.storage_percent_monitor = StoragePercentMonitor.StoragePercentMonitor(self._drive)

    def test_monitor_not_paused(self):
        paused = self.storage_percent_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        storage_percent = self.storage_percent_monitor.poll()
        self.assertIsInstance(storage_percent, float)

    def test_ram_within_limits(self):
        percent_ram = self.storage_percent_monitor.poll()
        minimum = self.storage_percent_monitor.minimum()
        maximum = self.storage_percent_monitor.maximum()
        self.assertTrue(percent_ram >= minimum and percent_ram <= maximum,
                        "Storage Percent is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_ram,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()