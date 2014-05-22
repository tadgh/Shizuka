import Pyro4
import threading
import logging
import time
import Pyro4.errors


logging.basicConfig(level=logging.INFO)

## Class responsible for the aggregation of all clients.
class Server:
    def __init__(self):
        try:
            self._ns = Pyro4.locateNS()
        except Pyro4.errors.NamingError:
                    logging.error("Could not find Name Server!")
        self._clients = {}

    ## Method that kicks off the client-polling using the nameserver found during initialization. Finds objects in the
    # naming server that start with "shizuka.client."
    def run(self):
        def poll_for_clients():
            while True:
                time.sleep(5)
                logging.info("Checking Name Server...")
                try:
                    for client_identifier, client_uri in self._ns.list(regex="shizuka\.client\.[A-Z0-9]{12}\.commandInterface").items():
                        logging.info("Found client with Identifier:{}".format(client_identifier))

                        if client_uri not in self._clients.keys():
                            logging.info("Added client {} to list".format(client_identifier))
                            client = Pyro4.Proxy(client_uri)
                            self._clients[client_uri] = client
                except Pyro4.errors.NamingError:
                    logging.error("Could not find Name Server!")


        polling_thread = threading.Thread(target=poll_for_clients)

        #will need to re-enable this once we hook pyro in. When true, the app will quit when daemon is the only thread alive.
        #polling_thread.setDaemon(True)
        polling_thread.start()


if __name__=="__main__":
    server = Server()
    server.run()