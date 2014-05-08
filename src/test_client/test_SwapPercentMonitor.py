import unittest
import SwapPercentMonitor


class TestSwapPercentMonitor(unittest.TestCase):

    def setUp(self):
        self.swap_percent_monitor = SwapPercentMonitor.SwapPercentMonitor(1)

    def test_monitor_not_paused(self):
        paused = self.swap_percent_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_swap_reporting(self):
        percent_ram = self.swap_percent_monitor.poll()
        self.assertIsInstance(percent_ram, float)

    def test_swap_within_limits(self):
        percent_swap = self.swap_percent_monitor.poll()
        minimum = self.swap_percent_monitor.minimum()
        maximum = self.swap_percent_monitor.maximum()
        self.assertTrue(percent_swap >= minimum and percent_swap <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_swap,
                                                                                                     maximum))






if __name__ == "__main__":
    unittest.main()
