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

    ## Method that simply continues to poll, is started on a thread, typically.
    def poll_for_clients_continuously(self):
        while True:
            self.poll_for_clients()
            time.sleep(10)

    ## In case the nameserver goes offline, we attempt to reconnect to it.
    def locate_nameserver(self):


    def poll_for_clients(self):
        logging.info("Checking Name Server...")
        try:
            for client_identifier, client_uri in self._ns.list(regex="shizuka\.client\..*").items():
                #this is the case where we've never seen this client before.
                if client_identifier not in self._clients.keys():
                    client = Pyro4.Proxy(client_uri)
                    self._clients[client_identifier] = [client_uri, client]
                    logging.info("Added New Client: {} --> {}".format(client_identifier, client_uri))
                #this down here is the case where the client has disconnected, reconnected, and gotten a new URI.
                #This requires us to change the associated proxy as well as URI.
                elif self._clients[client_identifier][0] != client_uri:
                    client = Pyro4.Proxy(client_uri)
                    self._clients[client_identifier] = [client_uri, client]
                    logging.info("Client has shown up under a new URI. Modified our "
                                 "dictionary to reflect it: {} --> {}".format(client_identifier, client_uri))

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

    ## Attempts to perform some shell command on a remote client.
    # @param target_client The given name of a client, i.e; shizuka.client.myfancyclient
    # @param command_tag The command tag associated with the command object that you want to execute. See Constants for the different tags.
    def execute_command(self, target_client, command_tag):
        try:
            results = self._clients[target_client][1].execute_command(command_tag)
        except KeyError as e:
            logging.error("Could not find target client in the list. Are you sure it's been registered? Error: {}".format(e))
            return "Could not find target client in the list. Are you sure it's been registered?"
        except AttributeError as e1:
            logging.error("Found client in list: {} , but could not execute command remotely. It is",
                          " possible the URI has changed, or the client has gone offline. ".format(self._clients[target_client]))
            return "Couldn't execute remote method on target. Is it offline?"
        if results is None:
            print("Call did not return any results. ")
        else:
            print("Returned information: {}".format(results))




if __name__=="__main__":

    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.register_to_name_server()
    server.run()