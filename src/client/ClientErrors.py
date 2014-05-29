
## A class that handles client side errors where the server is unreachable.
#
# This error gets raised whenever we are unable to execute commands on the reporting server.
class ServerNotFoundError(Exception):
    def __init__(self):
        pass