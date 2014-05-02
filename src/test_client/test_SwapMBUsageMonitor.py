import unittest
import SwapMBUsageMonitor


class TestSwapMBUsageMonitor(unittest.TestCase):

    def setUp(self):
        self.swap_mb_monitor = SwapMBUsageMonitor.SwapMBUsageMonitor()

    def test_monitor_not_paused(self):
        paused = self.swap_mb_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_swap_reporting(self):
        current_swap = self.swap_mb_monitor.poll()
        self.assertIsInstance(current_swap, float)

    def test_swap_within_limits(self):
        current_swap = self.swap_mb_monitor.poll()
        minimum = self.swap_mb_monitor.minimum()
        maximum = self.swap_mb_monitor.maximum()
        self.assertTrue(current_swap >= minimum and current_swap <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     current_swap,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()
