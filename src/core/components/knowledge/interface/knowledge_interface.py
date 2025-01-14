
from abc import ABC, abstractmethod

class KnowledgeInterface(ABC):
    
    @abstractmethod
    def create_gpt():
        raise NotImplementedError
    
    @abstractmethod
    def delete_gpt():
        raise NotImplementedError
    
    @abstractmethod
    def edit_gpt():
        raise NotImplementedError