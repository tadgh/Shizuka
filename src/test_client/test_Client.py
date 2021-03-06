import socket
import threading
import unittest
import Pyro4
import MonitorManager
import RamByteMonitor
import MessageHandler
import Client
import logging


logging.basicConfig(level=logging.INFO)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client.Client()
        self.manager = MonitorManager.MonitorManager()

    def test_adding_manager_to_client(self):
        monitor_1 = RamByteMonitor.RamByteMonitor()
        self.manager.add_monitor(monitor_1)
        self.client.set_monitor_manager(self.manager)
        self.assertIsNotNone(self.client.list_monitors())

    def test_empty_client_has_no_monitors(self):
        self.assertIsNone(self.client.list_monitors())

    def test_client_id_is_correct(self):
        client_id = "shizuka.client.{}".format(socket.gethostname())
        self.assertEqual(client_id, self.client._client_id)

    def test_client_discovery_works(self):
        mh = MessageHandler.MessageHandler(self.client._client_id, testing=True)
        self.client.set_message_queue(mh)
        self.client.send_discovery()
        test = mh.get_queue().get_nowait()
        self.assertTrue(test is not None)






if __name__ == "__main__":
    unittest.main()

