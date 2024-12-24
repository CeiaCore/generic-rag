

from abc import ABC, abstractmethod
from typing import List


class InputBasicPromptDto:
    
    def __init__(self, query: str, context: List, memory:List = None):
        self.query = query
        self.context = context
        self.memory = memory


class PromptInterface(ABC):
    @abstractmethod
    def prompt(self, input: InputBasicPromptDto)-> str:
        raise NotImplementedError