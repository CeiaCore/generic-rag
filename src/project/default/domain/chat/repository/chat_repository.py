from abc import ABC, abstractmethod
from typing import List

from src.project.default.domain.chat.entity.chat import Chat


class IChatRepository(ABC):
    
    
    @abstractmethod
    def insert(self, chat: Chat):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, chat_id: str):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, chat: Chat):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, chat_id: str) -> Chat:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self, user_id: str) -> List[Chat]:
        raise NotImplementedError