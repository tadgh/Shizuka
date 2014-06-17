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

    def test_purge_removes_all_data(self):
        self.server.notify({"Data": "somevalue"})
        self.server.purge_data()
        self.assertListEqual(self.server.get_all_data(), [])

    def test_purge_removes_all_messages(self):
        self.server.send_message({"Data": "somevalue"})
        self.server.purge_messages()
        self.assertListEqual(self.server.get_all_messages(), [])

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


    def test_execute_command_sends_to_client(self):
        import Constants
        client = Client.Client()
        self.server._clients["test"] = ["garbage_uri", client]#mocking a client
        self.server.execute_command("test", Constants.NETWORK_INFO_TAG)



if __name__ == "__main__":
    unittest.main()

