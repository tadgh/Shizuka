import Pyro4
import threading
import logging
import time
import Pyro4.errors
import Pyro4.naming
import queue

logger = logging.getLogger("Server")
logger.setLevel(logging.INFO)
## Class responsible for the aggregation of all clients.
class Server:
    def __init__(self):
        self._ns = None
        self._all_data = queue.Queue()
        self._all_messages = queue.Queue()
        self._clients = {}

    ## returns and clears all data in the _all_data list.
    # @return list containing _all_data
    def get_all_data(self):
        logger.info("get_all_data() called. Returning data and clearing the local list.")
        to_return = []
        while not self._all_data.empty():
            to_return.append(self._all_data.get())
            self._all_data.task_done()
        return to_return

    ## returns and clears all messages in  the _all_messages list.
    # @return list containing _all_messages
    def get_all_messages(self):
        logger.info("get_all_messages() called. Returning messages and clearing the local list.")
        to_return = []
        while not self._all_messages.empty():
            to_return.append(self._all_messages.get())
            self._all_messages.task_done()
        return to_return

    ## In case the nameserver goes offline, we attempt to reconnect to it.
    def locate_nameserver(self):
        while True:
            try:
                name_server = Pyro4.locateNS()
                self._ns = name_server
                return name_server
            except Pyro4.errors.NamingError as e:
                logger.error("Unable to find NameServer for Pyro4. Is it running? Error message: {}".format(str(e)))
            except Exception as e:
                logger.error("Unknown error occurred attempting to reconnect to ns. Error Message : {}".format(e))
            time.sleep(5)

    ## Method that simply continues to poll, is started on a thread, typically.
    def poll_for_clients_continuously(self):
        while True:
            self.poll_for_clients()
            time.sleep(10)

    ## Checks the nameserver for instances of shizuka.client.CLIENT_NAME. If they are unknonw, adds them to client list.
    # If they are known, and the URI has changed, re-establish a new proxy with the new URI.
    def poll_for_clients(self):
        logger.info("Checking Name Server...")
        if self._ns:
            try:
                for client_identifier, client_uri in self._ns.list(regex="shizuka\.client\..*").items():
                    #this is the case where we've never seen this client before.
                    proper_client_id = client_identifier.replace("shizuka.client.", "")
                    if proper_client_id not in self._clients.keys():
                        client = Pyro4.Proxy(client_uri)
                        self._clients[proper_client_id] = [client_uri, client]
                        logger.info("Added New Client: {} --> {}".format(proper_client_id, client_uri))
                    #this down here is the case where the client has disconnected, reconnected, and gotten a new URI.
                    #This requires us to change the associated proxy as well as URI.
                    elif self._clients[proper_client_id][0] != client_uri:
                        client = Pyro4.Proxy(client_uri)
                        self._clients[proper_client_id] = [client_uri, client]
                        logger.info("Client has shown up under a new URI. Modified our "
                                     "dictionary to reflect it: {} --> {}".format(proper_client_id, client_uri))
            except Pyro4.errors.NamingError:
                logger.error("Could not find Name Server! Attempting Reconnect...")
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
        logger.info("Trying to register to nameserver...")
        self._ns = self.locate_nameserver()
        if self._ns:
            def request_loop():
                logger.info("In registration thread...")
                if self._ns:
                    daemon = Pyro4.Daemon()
                    server_uri = daemon.register(self)
                    ##todo determine how to properly name server
                    try:
                        self._ns.register("shizuka.server.instance", server_uri)
                        logger.info("Registered Shizuka Server to the name server. ")
                        daemon.requestLoop()
                    except Exception as e:
                        logger.error("Registration error! Error Message: {}".format(str(e)))
                else:
                    logger.error("No Nameserver Found!")
            request_loop_thread = threading.Thread(target=request_loop)
            #request_loop_thread.setDaemon(True)
            request_loop_thread.start()
        else:
            logger.error("Failed to register to nameserver!!")

    #Called remotely by clients to pass dicts of data through.
    # @param data A dictionary containing all relevant polling data for the client.
    def notify(self, data):
        logger.info("Received some data from client. Appending to ALL list.\n{}".format(data))
        self._all_data.put(data)
        return True

    ## Method meant for message communication from clients. Success reports/ Status reports, what have you.
    # @param message The dictionary containing the message.
    def send_message(self, message):
        logger.info("Received message from client: {}".format(message))
        self._all_messages.put(message)
        return True

    #Simple lightweight method that allows a client to verify its connection. This will only be called by clients.
    # @return True, indicating successful connection.
    def ping(self):
        logger.info("GOT PINGED!")
        return True

    ## Attempts to perform some shell command on a remote client.
    # @param target_client The given name of a client, i.e; shizuka.client.myfancyclient
    # @param command_tag The command tag associated with the command object that you want to execute. See Constants for the different tags.
    def execute_command(self, target_client, command_tag):
        try:
            results = self._clients[target_client][1].execute_command(command_tag)
        except KeyError as e:
            logger.error("Could not find target client in the list. Are you sure it's been registered? Error: {}".format(e))
            logger.error("These are current clients: ", self._clients)
            return "Could not find target client in the list. Are you sure it's been registered?"
        except AttributeError as e1:
            logger.error("Found client in list: {} , but could not execute command remotely. It is",
                          " possible the URI has changed, or the client has gone offline. ".format(self._clients[target_client]))
            return "Couldn't execute remote method on target. Is it offline?"
        return results

    def configure_monitors(self, target_client, config_dict):
        logger.info("Attempting to send monitor configuration dictionary...")
        try:
            results = self._clients[target_client][1].configure_monitors(config_dict)
        except KeyError as e:
            logger.error("Could not find target client in the list. Are you sure it's been registered? Error: {}".format(e))
            logger.error("These are current clients: " + str(self._clients))
            return "Could not find target client in the list. Are you sure it's been registered?"
        except AttributeError as e1:
            logger.error("Found client in list: {} , but could not execute command remotely. It is",
                          " possible the URI has changed, or the client has gone offline. ".format(self._clients[target_client]))
            return "Couldn't execute remote method on target. Is it offline?"
        return results



if __name__=="__main__":

    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.register_to_name_server()
    server.run()