import psutil
import abc

class Monitor:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.paused = False

    def togglePause(self):
        self.paused = not self.paused

    def is_paused(self):
        return self.paused

    @abc.abstractmethod
    def poll(self):
        """
        Abstract method, makes a single psutil call to return whichever parameter this monitor is polling for.

        :return: Float value of the resource being monitored
        """
        return

    @abc.abstractmethod
    def minimum(self):
        """
        Abstract method, returns the minimum possible value achievable by poll(), for the particular client.


        :return: Float value of the minimum returnable value.
        """
        return

    @abc.abstractmethod
    def maximum(self):
        """
        Abstract method, returns the maximum possible value achievable by poll(), for the particular client.


        :return: Float value of the maximum returnable value.
        """
        return




