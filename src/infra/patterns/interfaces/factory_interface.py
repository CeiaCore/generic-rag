

from abc import ABC, abstractmethod


class FactoryInterface(ABC):
    
    @abstractmethod
    def create(input):
        raise NotImplementedError