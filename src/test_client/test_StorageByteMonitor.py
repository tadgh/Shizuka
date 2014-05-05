import unittest
import psutil
import StorageByteMonitor


class TestStorageByteMonitor(unittest.TestCase):


    def setUp(self):
        self._drive = psutil.disk_partitions()[0].device
        self.storage_byte_monitor = StorageByteMonitor.StorageByteMonitor(self._drive)

    def test_monitor_not_paused(self):
        paused = self.storage_byte_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        storage_in_use = self.storage_byte_monitor.poll()
        self.assertIsInstance(storage_in_use, float)

    def test_ram_within_limits(self):
        storage_in_use = self.storage_byte_monitor.poll()
        minimum = self.storage_byte_monitor.minimum()
        maximum = self.storage_byte_monitor.maximum()
        self.assertTrue(storage_in_use >= minimum and storage_in_use <= maximum,
                        "Storage Amount(bytes) is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     storage_in_use,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()