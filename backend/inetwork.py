from abc import ABC, abstractmethod

# Interface
# Defines necessary methods for GameLogic-to-Server communication
# Used in the base class backend.boomerang.BoomerangGame
class INetwork(ABC):
    @abstractmethod
    def onPlayerConnect(self): pass

    @abstractmethod
    def runRound(self): pass