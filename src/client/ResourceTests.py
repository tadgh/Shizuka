import unittest
import psutil

import RAMMonitor

__author__ = 'Tadgh'


class TestResourceMonitors(unittest.TestCase):

    def setUp(self):
        self.ram_monitor = RAMMonitor.RAMMonitor()


    def test_ps_utils_exists(self):
        utils = None
        utils = psutil.cpu_count()
        self.assertIsNotNone(utils)

    def test_monitor_not_paused(self):
        paused = self.ram_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")


    def test_ram_reporting(self):
        percent_ram = self.ram_monitor.poll()
        self.assertIsInstance(percent_ram, float)
        print(percent_ram)



if __name__ == "__main__":
    unittest.main()