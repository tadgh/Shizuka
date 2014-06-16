import psutil
import abc


## @brief An Abstract class used as a base to create different monitors.
#
# Has three methods that must be overriden:
#
#       1) poll(), the function that returns the current value of whatever resource you're looking at.
#       2) minimum(), which must return the lowest value that the resource could take on.
#       3) maximum(), which must return the largest value that the resource could take on.
class Monitor:
    __metaclass__ = abc.ABCMeta

    def __init__(self, type):
        self.paused = False
        self._type = type

    ## Negates the current value of paused.
    def togglePause(self):
        self.paused = not self.paused

    ## Self-evident.
    def is_paused(self):
        return self.paused

    ## Returns the name that the monitor holds as a key when passing data to the server.
    # @return self._id
    def get_type(self):
        return self._type

    ## Abstract method, makes a single psutil call to return whichever parameter this monitor is polling for.
    #
    # @return Float value of the resource being monitored
    @abc.abstractmethod
    def poll(self):
        return

    ##Abstract method, returns the minimum possible value achievable by poll(), for the particular client.
    #
    # @return Float value of the minimum returnable value.
    @abc.abstractmethod
    def minimum(self):
        return

    ## Abstract method, returns the maximum possible value achievable by poll(), for the particular client.
    #
    # @return Float value of the maximum returnable value.
    @abc.abstractmethod
    def maximum(self):
        return




