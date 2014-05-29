import abc

## Superclass for all commands that can be executed on the terminals.
#
#
class Command:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    ## Abstract Method to be implemented in subclasses. Contains the actual code to be executed on the terminal.
    #
    # @return Returns whatever the shell returns(if anything) upon completion of the command. returns None if nothing is found.
    @abc.abstractmethod
    def execute(self):
        return


