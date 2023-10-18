from abc import ABC, abstractmethod

class IClient(ABC):
    @abstractmethod
    def initSocket(self): pass

    @abstractmethod
    def startListening(self): pass

    @abstractmethod 
    def makeChoice(self): pass
