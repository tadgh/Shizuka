import Pyro4
import threading
import logging
import time
import Pyro4.errors
import Pyro4.naming


## Class responsible for the aggregation of all clients.
class Server:
    def __init__(self):
        try:
            self._ns = Pyro4.locateNS()
        except Pyro4.errors.NamingError:
                    logging.error("Could not find Name Server!")
        self._clients = {}

    def poll_for_clients_continuously(self):
        while True:
            self.poll_for_clients()
            time.sleep(10)

    def poll_for_clients(self):
        logging.info("Checking Name Server...")
        try:
            for client_identifier, client_uri in self._ns.list(regex="shizuka\.client\..*").items():
                if client_uri not in self._clients.keys():
                    client = Pyro4.Proxy(client_uri)
                    self._clients[client_uri] = client
                    logging.info("Added New Client: {}".format(client_identifier))
        except Pyro4.errors.NamingError:
            logging.error("Could not find Name Server!")

    ## Method that kicks off the client-polling using the nameserver found during initialization. Finds objects in the
    # naming server that start with "shizuka.client."
    def run(self):
        polling_thread = threading.Thread(target=self.poll_for_clients_continuously)
        #will need to re-enable this once we hook pyro in. When true, the app will quit when daemon is the only thread alive.
        #polling_thread.setDaemon(True)
        polling_thread.start()

    ## Uses the nameserver to register itself so that clients can find it.
    def register_to_name_server(self):
        if self._ns:
            def request_loop():
                if self._ns:
                    daemon = Pyro4.Daemon()
                    server_uri = daemon.register(self)
                    ##todo determine how to properly name server
                    try:
                        self._ns.register("shizuka.server.instance", server_uri)
                        logging.info("Registered Shizuka Server to the name server. ")
                        daemon.requestLoop()
                    except Exception as e:
                        logging.error("Registration error! Error Message: {}".format(str(e)))
            request_loop_thread = threading.Thread(target=request_loop)
            #request_loop_thread.setDaemon(True)
            request_loop_thread.start()

    #Called remotely by clients to pass dicts of data through.
    # @param data A dictionary containing all relevant polling data for the client.
    def notify(self, data):
        print("Received some data from client...\n{}".format(data))
        return True

    #Simple lightweight method that allows a client to verify its connection. This will only be called by clients.
    # @return True, indicating successful connection.
    def ping(self):
        logging.info("GOT PINGED!")
        return True


if __name__=="__main__":

    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.register_to_name_server()
    server.run()