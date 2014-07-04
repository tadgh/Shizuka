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
        self._monitor_1 = RamByteMonitor.RamByteMonitor()
        self._monitor_manager.add_monitor(self._monitor_1)

        self._notifier = Notifier.Notifier("shizuka.client.Mulder", testing=True)
        #self._server = Server.Server()

    def test_notifier_fails_to_send_when_server_is_not_associated(self):
        self._notifier.set_server(None, "simulate a dropped connection!")
        self.assertRaises(ServerNotFoundError, self._notifier.post_to_server, "some sample data!")

    def test_polled_data_comes_in_when_called(self):
        results = self._notifier.get_polled_data()
        self.assertIsInstance(results, dict)

    def test_data_is_received_when_server_is_associated(self):
        results = self._notifier.get_polled_data()
        transmission_result = self._notifier.post_to_server(results)
        self.assertTrue(transmission_result)

    def test_shutting_down_notifier(self):
        self._notifier.start()
        self.assertTrue(threading.active_count() == 2)
        self._notifier.stop_polling()

if __name__ == "__main__":
    unittest.main()

