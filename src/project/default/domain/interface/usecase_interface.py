

from abc import ABC, abstractmethod


class UsecaseInterface(ABC):
    
    @abstractmethod
    def execute(self, input):
        raise NotImplementedError