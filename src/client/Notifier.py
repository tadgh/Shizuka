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
    def __init__(self):
        self._data_manager = DataManager.DataManager()
        self._reporting_server = None

    ## Associate a reporting server here. Without one, no data is reported to the server.
    # @param reporting_server the pyro proxy object indicating the server to be associated.
    def set_server(self, reporting_server):
        if self._reporting_server is None:
            logging.info("Initializing server for the first time --> Found Server : {} ".format(reporting_server))
        else:
            logging.warning("Server being re-assigned. : {} ".format(reporting_server))
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
                data_was_received = self._reporting_server.notify(polled_data)
            except AttributeError as e:
                logging.error("Appears as though calling the remote notify() method on the server has failed",
                              "attempting to reconnect.")
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
        poll_and_notify_thread = threading.Thread(target=poll_and_post)
        #TODO will need to uncomment next line once we set up the Pyro object on the client.
        #poll_and_notify_thread.setDaemon(True)
        poll_and_notify_thread.start()

    def reconnect_to_server(self):
        while True:
            try:
                name_server = Pyro4.locateNS()
                if len(name_server.list(prefix="shizuka.server.")) > 0:
                    reporting_server = Pyro4.Proxy(server_proxy_uri)
                    self.set_server(reporting_server)
                if self._reporting_server.ping():
                    logging.info("Ping succeeded on server. Returning control to polling thread.")
                    return True
            except AttributeError as e:
                logging.error("Found Nameserver, but couldn't find Server Object. Error Message: {}".format(str(e)))
            except Pyro4.errors.NamingError as e:
                logging.error("Unable to find NameServer for Pyro4. Is it running? Error message: {}".format(str(e)))
            time.sleep(5)




