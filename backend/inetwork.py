from abc import ABC, abstractmethod

# Interface
# Necessary methods for GameLogic-to-Server communication
class INetwork(ABC):
    @abstractmethod
    def onPlayerConnect(self): pass

    @abstractmethod
    def runRound(self): pass