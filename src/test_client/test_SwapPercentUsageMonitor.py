import unittest
import SwapPercentUsageMonitor


class TestSwapPercentUsageMonitor(unittest.TestCase):

    def setUp(self):
        self.swap_mb_monitor = SwapPercentUsageMonitor.SwapPercentUsageMonitor()

    def test_monitor_not_paused(self):
        paused = self.swap_mb_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_swap_reporting(self):
        percent_ram = self.swap_mb_monitor.poll()
        self.assertIsInstance(percent_ram, float)

    def test_swap_within_limits(self):
        percent_swap = self.swap_mb_monitor.poll()
        minimum = self.swap_mb_monitor.minimum()
        maximum = self.swap_mb_monitor.maximum()
        self.assertTrue(percent_swap >= minimum and percent_swap <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_swap,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()
