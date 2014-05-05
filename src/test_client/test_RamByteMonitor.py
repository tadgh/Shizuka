import unittest
import RamByteMonitor


class TestRamByteMonitor(unittest.TestCase):

    def setUp(self):
        self.ram_mb_monitor = RamByteMonitor.RamByteMonitor()

    def test_monitor_not_paused(self):
        paused = self.ram_mb_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        percent_ram = self.ram_mb_monitor.poll()
        self.assertIsInstance(percent_ram, float)

    def test_ram_within_limits(self):
        percent_ram = self.ram_mb_monitor.poll()
        minimum = self.ram_mb_monitor.minimum()
        maximum = self.ram_mb_monitor.maximum()
        self.assertTrue(percent_ram >= minimum and percent_ram <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_ram,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()
