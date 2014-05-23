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
        self.ns = Pyro4.locateNS()

    def tearDown(self):
        pass

    def test_server_starts_with_no_clients(self):
        self.assertTrue(len(self.server._clients) == 0)


    def test_adding_client_to_server(self):
        self.ns.list()
        client = Client.Client()
        client.run()




if __name__ == "__main__":
    unittest.main()

