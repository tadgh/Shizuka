import DataManager
from ClientErrors import ServerNotFoundError
import logging
import threading
import Pyro4
import Pyro4.errors
import time


## Class for handling notification of any observers, when new data is polled.
#
# The notifier will be running on a seperate thread, and polling for new data on a defined interval.
class Notifier:
    def __init__(self, client_identifier):
        self._data_manager = DataManager.DataManager()
        self._reporting_server = None
        self._client_identifier = client_identifier

    ## Associate a reporting server here. Without one, no data is reported to the server.
    # @param reporting_server the pyro proxy object indicating the server to be associated.
    def set_server(self, reporting_server, server_name):
        if self._reporting_server is None:
            logging.info("Initializing server for the first time --> Found Server : {} ".format(server_name))
        else:
            logging.warning("Server being re-assigned. : {} ".format(server_name))
        self._reporting_server = reporting_server

    # Gets new data from the DataManager Singleton
    # @return a dictionary of all polled results from the local computer.
    def get_polled_data(self):
        return self._data_manager.poll_all()

    ## Notifies the server object (A pyro proxy) of any new data.
    # @param polled_data A dictionary of data to be passed to the server.
    # @return A boolean indicating whether the server accepted our transmission.
    # @exception ServerNotFoundError if the server is not associated, raises this error.
    def post_to_server(self, polled_data):
        if self._reporting_server is not None:
            try:
                #todo gotta figure out best way to get the client ID in there.
                outgoing_message = {"client_id": self._client_identifier, "polled_data": polled_data}
                data_was_received = self._reporting_server.notify(outgoing_message)
            except AttributeError as e:
                logging.error("Appears as though calling the remote notify() method on the server has failed attempting to reconnect.: {}".format(e))
                raise ServerNotFoundError
        else:
            logging.error("NO ASSOCIATED SERVER FOUND")
            raise ServerNotFoundError
        return data_was_received

    ## The method invoked in a new thread. This is the working loop that polls data, and returns it to the server.
    def run(self):
        def poll_and_post():
            while True:
                logging.info("Notifier initiating Data Poll...")
                results = self.get_polled_data()
                logging.info("Notifier posting Data to Server...")
                try:
                    self.post_to_server(results)
                except ServerNotFoundError as e:
                    logging.error("Giving control to reconnection method. Posting to server failed...")
                    self.reconnect_to_server()
                time.sleep(10)

        poll_and_notify_thread = threading.Thread(target=poll_and_post, name="hardware_polling_thread")
        poll_and_notify_thread.setDaemon(True)
        poll_and_notify_thread.start()

    ## Called when unable to execute methods on remote server. Continuously attempts re-connection to Server and attempts
    # ping. When it succeeds, it sets the server and returns control to where it was called.
    def reconnect_to_server(self):
        disconnected = True
        while disconnected:
            try:
                name_server = Pyro4.locateNS()
                server_dict = name_server.list(prefix="shizuka.server.")
                server_name, server_uri = server_dict.popitem()

                if server_uri:
                    logging.info("Found Server named: {} . Joining...".format(server_name))
                    reporting_server = Pyro4.Proxy(server_uri)
                    self.set_server(reporting_server, server_name)
                try:
                    self._reporting_server.ping()
                    logging.info("Ping succeeded on server. Returning control to polling thread.")
                    disconnected = False
                except AttributeError as e:
                    logging.error("Unable to ping server: Error message: {}".format(str(e)))
            except KeyError as e:
                logging.error("Found Nameserver, but couldn't find Server Object. Error Message: {}".format(str(e)))
            except Pyro4.errors.NamingError as e:
                logging.error("Unable to find NameServer for Pyro4. Is it running? Error message: {}".format(str(e)))
            except Exception as e:
                logging.error("Unknown error occurred attempting to reconnect to server. Error Message : {}".format(e))
            time.sleep(5)



