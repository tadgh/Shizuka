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



