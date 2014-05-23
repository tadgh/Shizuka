import unittest
import MonitorManager
import RamByteMonitor
import RamPercentMonitor
import Client
import logging


logging.basicConfig(level=logging.INFO)


class TestMonitorManager(unittest.TestCase):

    def setUp(self):
        self.client = Client.Client()
        self.manager = MonitorManager.MonitorManager()


    def test_adding_manager_to_client(self):
        monitor_1 = RamByteMonitor.RamByteMonitor(1)
        self.manager.add_monitor(monitor_1)
        self.client.set_monitor_manager(self.manager)
        self.assertIsNotNone(self.client.list_monitors())

    def test_empty_client_has_no_monitors(self):
        self.assertIsNone(self.client.list_monitors())



if __name__ == "__main__":
    unittest.main()

