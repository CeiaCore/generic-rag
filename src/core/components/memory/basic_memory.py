

from typing import List
from src.core.components.memory.interface.memory_interface import MemoryInterface


class BasicMemory(MemoryInterface):
    
    def __init__(self, memory_store: MemoryInterface) -> None:
        self.memory_store = memory_store
                
    def save_memory(self, chat_id: str, content: List[str], query: str, response: str):
        self.memory_store.save_memory(chat_id=chat_id, content=content, query=query, response=response)
    
    def retrieve_memory(self, chat_id: str) -> List[str]:
        response = self.memory_store.retrieve_memory(chat_id=chat_id)
        response = response[len(response)-7:]
        return response