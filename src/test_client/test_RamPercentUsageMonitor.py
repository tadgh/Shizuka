import unittest
import RamPercentUsageMonitor


class TestRamPercentUsageMonitor(unittest.TestCase):

    def setUp(self):
        self.ram_percent_monitor = RamPercentUsageMonitor.RAMPercentUsageMonitor()

    def test_monitor_not_paused(self):
        paused = self.ram_percent_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        percent_ram = self.ram_percent_monitor.poll()
        self.assertIsInstance(percent_ram, float)

    def test_ram_within_limits(self):
        percent_ram = self.ram_percent_monitor.poll()
        minimum = self.ram_percent_monitor.minimum()
        maximum = self.ram_percent_monitor.maximum()
        self.assertTrue(percent_ram >= minimum and percent_ram <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_ram,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()