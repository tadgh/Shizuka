import threading
import Pyro4
import logging
import time
import Pyro4.errors
import queue
from ClientErrors import ServerNotFoundError

logger = logging.getLogger("MessageHandler")
logger.setLevel(logging.INFO)

## Class that handles any outgoing messages. Uses a Queue to hold any messages. Classes can call get_queue() to get a
# reference to the outgoing queue. This is a threaded class, whos sole purpose is to consume the queue and send it to
# the server.
class MessageHandler(threading.Thread):
    def __init__(self, client_identifier, testing=False):
        threading.Thread.__init__(self)
        self._client_identifier = client_identifier
        self._reporting_server = None
        self._message_queue = queue.Queue()
        self._stop_processing = threading.Event()

        #just a quick hack to allow me to run tests without using the connectivity aspect
        if testing:
            import Utils
            logger.info("Since we are testing, creating a mock server...")
            self._reporting_server = Utils.mock_server()
        else:
            logger.info("Since we are not testing, attempting to connect to server...")
            self.reconnect_to_server()

    ## A check for whether the _stop_processing Event has been set.
    # @ return A boolean indicating whether or not the Event is set.
    def stop_requested(self):
        return self._stop_processing.is_set()

    ## Sets a flag to stop processing once the queue is done.
    def request_stop(self):
        logger.info("Requesting stop in DataManager thread.")
        self._stop_processing.set()

    ##The method available to other modules that would like to send messages to the server through this handler.
    # @return the queue that holds the messages. Allows clients to put new messages into it.
    def get_queue(self):
        return self._message_queue

    ## Checks the queue after three seconds for new messages. When it finds a new message, it processes it and checks
    # again.
    def post_all_to_server(self):
        time.sleep(3)
        while not self._message_queue.empty():
            self.post_to_server(self._message_queue.get())

    ## The method called when the thread's .start() is called. Currently, continuously sends messages that are in the queue.
    # Terminates only when self._stop_processing is set using a call to self.request_stop()
    def run(self):
        while not self.stop_requested():
            self.post_all_to_server()

    ## Notifies the server object (A pyro proxy) of any new messages.
    # @param message The dictionary(or anything) that is to be sent to the server.
    # @return A boolean indicating whether or not data was received on the server end.
    def post_to_server(self, message):
        if self._reporting_server is not None:
            try:
                logger.info("Throwing message to server: {}".format(message))
                outgoing_message = {"client_id": self._client_identifier, "message": message}
                data_was_received = self._reporting_server.send_message(outgoing_message)
            except AttributeError as e:
                logger.error("Appears as though calling the remote notify() method on the server has failed attempting to reconnect.: {}".format(e))
                raise ServerNotFoundError
        else:
            logger.error("NO ASSOCIATED SERVER FOUND")
            raise ServerNotFoundError
        return data_was_received

    ## Associate a reporting server here. Without one, no data is reported to the server.
    # @param reporting_server the pyro proxy object indicating the server to be associated.
    def set_server(self, reporting_server, server_name):
        if self._reporting_server is None:
            logger.info("Initializing server for the first time --> Found Server : {} ".format(server_name))
        else:
            logger.warning("Server being re-assigned. : {} ".format(server_name))
        self._reporting_server = reporting_server

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
                    logger.info("Found Server named: {} . Joining...".format(server_name))
                    reporting_server = Pyro4.Proxy(server_uri)
                    self.set_server(reporting_server, server_name)
                try:
                    self._reporting_server.ping()
                    logger.info("Ping succeeded on server. Returning control to polling thread.")
                    disconnected = False
                except AttributeError as e:
                    logger.error("Unable to ping server: Error message: {}".format(str(e)))
            except KeyError as e:
                logger.error("Found Nameserver, but couldn't find Server Object. Error Message: {}".format(str(e)))
            except Pyro4.errors.NamingError as e:
                logger.error("Unable to find NameServer for Pyro4. Is it running? Error message: {}".format(str(e)))
            except Exception as e:
                logger.error("Unknown error occurred attempting to reconnect to server. Error Message : {}".format(e))
            time.sleep(5)


def main():
    import MonitorManager
    import Constants


    mm = MonitorManager.MonitorManager()
    mh = MessageHandler("shizuka.client.Mulder", testing=True)

    mm.set_message_handler(mh)

    config_dict = {
        "add": [Constants.CPU_PERCENT_MONITOR, Constants.BYTES_RECEIVED_MONITOR],
        "remove": [Constants.RAM_BYTE_MONITOR]
    }

    mm.handle_config(config_dict)
    mm.handle_config(config_dict)
    mm.handle_config(config_dict)
    mm.handle_config(config_dict)

    mh.start()
    mm.handle_config(config_dict)
    mm.handle_config(config_dict)
    mm.handle_config(config_dict)
    mm.handle_config(config_dict)
    mm.handle_config(config_dict)




if __name__=="__main__":
    main()