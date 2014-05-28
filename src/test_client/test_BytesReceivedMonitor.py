import unittest
import BytesReceivedMonitor


class TestBytesReceivedMonitor(unittest.TestCase):

    def setUp(self):
        self.bytes_received_monitor = BytesReceivedMonitor.BytesReceivedMonitor()

    def test_monitor_not_paused(self):
        paused = self.bytes_received_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        bytes_received = self.bytes_received_monitor.poll()
        self.assertIsInstance(bytes_received, float)

    def test_ram_within_limits(self):
        bytes_received = self.bytes_received_monitor.poll()
        minimum = self.bytes_received_monitor.minimum()
        maximum = self.bytes_received_monitor.maximum()
        self.assertTrue(bytes_received >= minimum and bytes_received <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     bytes_received,
                                                                                                     maximum))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
