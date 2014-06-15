import Pyro4
import threading
import logging
import time
import Pyro4.errors
import Pyro4.naming


## Class responsible for the aggregation of all clients.
class Server:
    def __init__(self):
        self._ns = None
        self._all_data = []
        self._all_messages = []
        self._clients = {}

    def get_all_data(self):
        logging.info("get_all_data() called. Returning data and clearing the local list.")
        to_return = list(self._all_data)
        self.purge_data()
        return to_return

    def get_all_messages(self):
        logging.info("get_all_messages() called. Returning messages and clearing the local list.")
        to_return = list(self._all_messages)
        self.purge_messages()
        return to_return

    ## Removes all data received from clients.
    def purge_data(self):
        logging.info("clearing all_data in the server... ")
        self._all_data.clear()
    ## Removes all messages received from clients.
    def purge_messages(self):
        logging.info("clearing all_messages in the server... ")
        self._all_messages.clear()

    ## In case the nameserver goes offline, we attempt to reconnect to it.
    def locate_nameserver(self):
        while True:
            try:
                name_server = Pyro4.locateNS()
                self._ns = name_server
                return name_server
            except Pyro4.errors.NamingError as e:
                logging.error("Unable to find NameServer for Pyro4. Is it running? Error message: {}".format(str(e)))
            except Exception as e:
                logging.error("Unknown error occurred attempting to reconnect to ns. Error Message : {}".format(e))
            time.sleep(5)

    ## Method that simply continues to poll, is started on a thread, typically.
    def poll_for_clients_continuously(self):
        while True:
            self.poll_for_clients()
            time.sleep(10)

    ## Method meant for message communication from clients. Success reports/ Status reports, what have you.
    # @param message The dictionary containing the message.
    def send_message(self, message):
        logging.info("Received message from client: {}".format(message))
        self._all_messages.append(message)

    ## Checks the nameserver for instances of shizuka.client.CLIENT_NAME. If they are unknonw, adds them to client list.
    # If they are known, and the URI has changed, re-establish a new proxy with the new URI.
    def poll_for_clients(self):
        logging.info("Checking Name Server...")
        if self._ns:
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
                logging.error("Could not find Name Server! Attempting Reconnect...")
                self.locate_nameserver()
        else:
            self.locate_nameserver()

    ## Method that kicks off the client-polling using the nameserver found during initialization. Finds objects in the
    # naming server that start with "shizuka.client."
    def run(self):
        polling_thread = threading.Thread(target=self.poll_for_clients_continuously)
        #will need to re-enable this once we hook pyro in. When true, the app will quit when daemon is the only thread alive.
        #polling_thread.setDaemon(True)
        polling_thread.start()

    ## Uses the nameserver to register itself so that clients can find it.
    #TODO need to switch this to retry after a failed registration.
    def register_to_name_server(self):
        logging.info("Trying to register to nameserver...")
        self._ns = self.locate_nameserver()
        if self._ns:
            def request_loop():
                logging.info("In registration thread...")
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
                else:
                    logging.error("No Nameserver Found!")
            request_loop_thread = threading.Thread(target=request_loop)
            #request_loop_thread.setDaemon(True)
            request_loop_thread.start()
        else:
            logging.error("Failed to register to nameserver!!")

    #Called remotely by clients to pass dicts of data through.
    # @param data A dictionary containing all relevant polling data for the client.
    def notify(self, data):
        logging.info("Received some data from client. Appending to ALL list.\n{}".format(data))
        self._all_data.append(data)
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