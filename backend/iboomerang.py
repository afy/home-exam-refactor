from abc import ABC, abstractmethod, abstractproperty

class IBoomerang(ABC):
    @abstractmethod
    def calculateScore(self): pass