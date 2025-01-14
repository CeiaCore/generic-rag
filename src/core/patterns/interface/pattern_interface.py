

from abc import ABC, abstractmethod



class PatternInterface(ABC):

    @abstractmethod
    def execute(input):
        raise NotImplementedError