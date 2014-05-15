import unittest
import MonitorManager
import DataManager
import Client
from ClientErrors import ServerNotFoundError
import RamByteMonitor
import logging
import Notifier
import threading

logging.basicConfig(level=logging.INFO)


class TestNotifier(unittest.TestCase):

    def setUp(self):
        self._data_manager = DataManager.DataManager()
        self._monitor_manager = MonitorManager.MonitorManager()
        self._monitor_1 = RamByteMonitor.RamByteMonitor(1)
        self._monitor_manager.add_monitor(self._monitor_1)

        self._notifier = Notifier.Notifier()
        #self._server = Server.Server()

    def test_notifier_fails_to_send_when_server_is_not_associated(self):
        self.assertRaises(ServerNotFoundError, self._notifier.post_to_server, "some sample data!")

    def test_polled_data_comes_in_when_called(self):
        results = self._notifier.get_polled_data()
        self.assertIsInstance(results, dict)

    def test_thread_starts_correctly(self):
        self._notifier.run()
        self.assertEquals(2, threading.active_count())






if __name__ == "__main__":
    unittest.main()

