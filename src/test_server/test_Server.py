import threading
import unittest
import Server
import Pyro4.naming
import Pyro4
import threading


logging.basicConfig(level=logging.INFO)


class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = Server.Server()
        self.ns = None
        def start_nameserver():
            self.ns = Pyro4.naming.NameServer()
        threading.Thread(target=start_nameserve).start()



    def test_adding_client_to_server(self):
        self.ns.list()

    def test_server_starts_with_no_clients(self):
        self.assertTrue(len(self.server._clients) == 0)




if __name__ == "__main__":
    unittest.main()

