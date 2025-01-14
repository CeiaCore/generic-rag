

from abc import ABC, abstractmethod
from typing import List


class MemoryInterface(ABC):

    @abstractmethod
    def retrieve_memory(self, chat_id: str):
        raise NotImplementedError
    

    @abstractmethod
    def save_memory(self, chat_id: str, content: List[str], query: str, response: str):
        raise NotImplementedError