import unittest
import Server
import Pyro4.naming
import Pyro4
import threading
import Client
import logging
import Constants

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
        self.assertEqual(res, [{"test": 1}, {"test2": 2}])

    def test_server_returns_nothing_on_no_data(self):
        res = self.server.get_all_data()
        self.assertListEqual(res, [])

    def test_notify_returns_true(self):
        res = self.server.notify("whatever")
        self.assertTrue(res)

    def test_send_message_adds_to_queue(self):
        self.server.send_message({"Data": "somevalue"})
        self.server.send_message({"Data": "somevalue2"})
        mes_list = self .server.get_all_messages()
        self.assertTrue(len(mes_list) == 2)

    def test_get_all_messages(self):
        msg = "test2"
        self.server.send_message(msg)
        msg_list = self.server.get_all_messages()
        self.assertIn(msg, msg_list)

    def test_get_all_data(self):
        data = "asdadasd"
        self.server.notify(data)
        data_list = self.server.get_all_data()
        self.assertIn(data, data_list)

    def test_execute_command_sends_to_client_on_fail(self):
        import Constants
        client = Client.Client()
        self.server._clients["test"] = ["garbage_uri", client]#mocking a client
        self.server.execute_command("test", Constants.NETWORK_INFO_TAG)

    def test_execute_command_sends_to_client_on_success(self):
        import Constants
        import CommandInterface
        client = Client.Client()
        ci = CommandInterface.CommandInterface()
        client.set_command_executor(ci)
        self.server._clients["test"] = ["garbage_uri", client]#mocking a client
        res = self.server.execute_command("test", Constants.NETWORK_INFO_TAG)
        self.assertRegexpMatches(res, "Ethernet")

if __name__ == "__main__":
    unittest.main()

