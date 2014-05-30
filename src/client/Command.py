import abc
import platform
## Superclass for all commands that can be executed on the terminals.
#
# Subclasses must override the execute() method. This is the single method contained in a command object. Support for
# undoing is not being considered at this time. The call_tag is used to quickly check if a command is allowed to be executed.
class Command:
    __metaclass__ = abc.ABCMeta

    def __init__(self, call_tag):
        self._call_tag = call_tag
        self._platform = platform.system()
    def get_tag(self):
        return self._call_tag
    ## Abstract Method to be implemented in subclasses. Contains the actual code to be executed on the terminal.
    #
    # @return Returns whatever the shell returns(if anything) upon completion of the command. returns None if nothing is found.
    def execute(self):
        if self._platform == "Windows":
            return self.windows_execute()
        else:
            return self.nix_execute()

    @abc.abstractmethod
    def windows_execute(self):
        return

    @abc.abstractmethod
    def nix_execute(self):
        return





