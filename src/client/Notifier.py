import DataManager
from ClientErrors import ServerNotFoundError
import logging
import threading

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
            data_was_received = self._reporting_server.notify(polled_data)
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
                accepted = self.post_to_server(results)
                time.sleep(10)
        poll_and_notify_thread = threading.Thread(target=poll_and_post)
        #TODO will need to uncomment next line once we set up the Pyro object on the client.
        #poll_and_notify_thread.setDaemon(True)
        poll_and_notify_thread.start()

