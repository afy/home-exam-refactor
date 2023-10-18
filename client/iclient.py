from abc import ABC, abstractmethod

# Interface:
# Middleman between server and "Client" (Players/Bots)
class IClient(ABC):
    @abstractmethod
    def initSocket(self): pass

    @abstractmethod
    def startListening(self): pass

    @abstractmethod 
    def makeChoice(self): pass
