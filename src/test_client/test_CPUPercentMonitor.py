import unittest
import CPUPercentMonitor


class TestRamByteMonitor(unittest.TestCase):

    def setUp(self):
        self.cpu_monitor = CPUPercentMonitor.CPUPercentMonitor()

    def test_monitor_not_paused(self):
        paused = self.cpu_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        percent_cpu = self.cpu_monitor.poll()
        self.assertIsInstance(percent_cpu, float)

    def test_ram_within_limits(self):
        percent_cpu = self.cpu_monitor.poll()
        minimum = self.cpu_monitor.minimum()
        maximum = self.cpu_monitor.maximum()
        self.assertTrue(percent_cpu >= minimum and percent_cpu <= maximum,
                        "CPU% is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     percent_cpu,
                                                                                                     maximum))






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
