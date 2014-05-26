import unittest
import BytesSentMonitor


class TestBytesSentMonitor(unittest.TestCase):

    def setUp(self):
        self.bytes_sent_monitor = BytesSentMonitor.BytesSentMonitor(1)

    def test_monitor_not_paused(self):
        paused = self.bytes_sent_monitor.is_paused()
        self.assertFalse(paused, "Monitors are starting Paused?")

    def test_ram_reporting(self):
        bytes_sent = self.bytes_sent_monitor.poll()
        self.assertIsInstance(bytes_sent, float)

    def test_ram_within_limits(self):
        bytes_sent = self.bytes_sent_monitor.poll()
        minimum = self.bytes_sent_monitor.minimum()
        maximum = self.bytes_sent_monitor.maximum()
        self.assertTrue(bytes_sent >= minimum and bytes_sent <= maximum,
                        "RAM is not within upper and lower bound limits: {} <= {} <= {}".format(minimum,
                                                                                                     bytes_sent,
                                                                                                     maximum))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
