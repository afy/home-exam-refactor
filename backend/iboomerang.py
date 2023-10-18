from abc import ABC, abstractmethod, abstractproperty

# Interface
# Methods implemented in the boomerang class
class IBoomerang(ABC):
    @abstractmethod
    def calculateScore(self): pass