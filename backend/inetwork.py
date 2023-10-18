from abc import ABC, abstractmethod

class INetwork(ABC):
    @abstractmethod
    def onPlayerConnect(self): pass

    @abstractmethod
    def runRound(self): pass