import threading
import unittest
import time
import subprocess
import Notifier
import Server
import Pyro4.naming
import Pyro4
import threading
import Client
import logging
import Pyro4.errors
import os

logging.basicConfig(level=logging.INFO)


class TestConnectivity(unittest.TestCase):

    def setUp(self):
        self.server = Server.Server()
        self.ns = Pyro4.locateNS()

    def tearDown(self):
        pass

    def test_server_starts_with_no_clients(self):
        self.assertTrue(len(self.server._clients) == 0)

    def test_server_registration_succeeds(self):
        self.server.register_to_name_server()
        server_instances = self.ns.list(prefix="shizuka.server.")
        self.assertGreater(len(server_instances), 0)

    def test_adding_client_to_server(self):
        client = Client.Client()
        client.register_to_name_server()
        logging.info(self.ns.list())
        self.server.locate_nameserver()
        self.server.poll_for_clients()
        self.assertTrue(len(self.server._clients) > 0)

    def test_client_registered_successfully(self):
        client = Client.Client()
        client.register_to_name_server()
        ns = Pyro4.locateNS()
        print(ns.list(prefix=client._client_id))

    def test_data_is_received_when_server_is_associated(self):
        self.server.register_to_name_server()
        notifier = Notifier.Notifier("shizuka.client.Mulder")
        results = notifier.get_polled_data()
        transmission_result = notifier.post_to_server(results)
        self.assertTrue(transmission_result)

    def test_registration_to_name_server_succeeds(self):
        client = Client.Client()
        client.register_to_name_server()
        print(threading.enumerate())
        #todo Not sure how to test this.... Waits on another thread?


if __name__ == "__main__":
    unittest.main()
