

from abc import ABC, abstractmethod


class LLMInterface(ABC):
    
    
    @abstractmethod
    def batch(self, prompt):
        raise NotImplementedError
    
    @abstractmethod
    def stream(self,prompt):
        raise NotImplementedError