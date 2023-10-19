from abc import ABC, abstractmethod

# <<Interface>>
# Defines necessary methods for GameLogic-to-Server communication
# Used in the base class backend.boomerang.BoomerangGame
class INetwork(ABC):
    @abstractmethod
    def onPlayerConnect(self) -> None: pass

    @abstractmethod
    def onAllClientInputLogged(self, clientInput : str) -> dict: pass

    @abstractmethod
    def getInitialValues(self, playerId : int) -> dict: pass

    @abstractmethod
    def validateClientInput(self, input : str) -> bool: pass

    @abstractmethod
    def startGame(self) -> None: pass

    @abstractmethod
    def addBot(self, id) -> None: pass