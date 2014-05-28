import socket
import threading
import unittest
import Pyro4
import MonitorManager
import RamByteMonitor
import Client
import logging


logging.basicConfig(level=logging.INFO)


class TestClient(unittest.TestCase):

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

    def test_client_id_is_correct(self):
        client_id = "shizuka.client.{}".format(socket.gethostname())
        self.assertEqual(client_id, self.client._client_id)

    def test_client_registered_successfully(self):
        self.client.register_to_name_server()
        ns = Pyro4.locateNS()
        print(ns.list(prefix=self.client._client_id))

    #TODO move this to connectivity Tests
    def test_registration_to_name_server_succeeds(self):
        self.client.register_to_name_server()
        print(threading.enumerate())
        #todo Not sure how to test this.... Waits on another thread?







if __name__ == "__main__":
    unittest.main()

