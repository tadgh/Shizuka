import threading
import unittest
import Server
import Pyro4.naming
import Pyro4
import threading
import Client
import logging

logging.basicConfig(level=logging.INFO)


class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = Server.Server()

    def tearDown(self):
        pass

    def test_server_starts_with_no_clients(self):
        self.assertTrue(len(self.server._clients) == 0)

    def test_get_all_data_returns_all_data(self):
        self.server.notify({"test": 1})
        self.server.notify({"test2": 2})
        res = self.server.get_all_data()
        self.assertEqual(res, [{"test": 1},{"test2": 2}])

    def test_server_returns_nothing_on_no_data(self):
        res = self.server.get_all_data()
        self.assertListEqual(res, [])

    def test_message_passes_to_server_from_client(self):









if __name__ == "__main__":
    unittest.main()

