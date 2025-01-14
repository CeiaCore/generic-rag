import datetime
from typing import Dict, List
from uuid import uuid4



class InputChatDto:
    def __init__(self, user_id: str):
        self.user_id = user_id
        

class Chat:
    user_id: str
    chat_id: str
    chat_label: str
    messages: List
    created_at: datetime
    
    def __init__(self, user_id: str, chat_id: str, chat_label: str, messages: List, create_at: datetime) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self.chat_label = chat_label
        self.create_at = create_at
        self.messages = messages
    
    @staticmethod
    def create(input: InputChatDto):
        chat = Chat(chat_id=str(uuid4()), 
                    chat_label="Novo chat", 
                    create_at=datetime.datetime.now(), 
                    messages=[],
                    user_id=input.user_id
                    )
        return chat
    
    def get_user_id(self):
        return self.user_id
    
    def get_chat_id(self):
        return self.chat_id
    
    def get_chat_label(self):
        return self.chat_label
    
    def insert_message(self, message: dict):
        self.messages.append(message)
        
    def change_chat_label(self, label: str):
        if (len(label) > 2) and (self.chat_label == "Novo chat"):
            self.chat_label = label[:50]
    
    def to_json(self):
        return {
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "chat_label": self.chat_label,
            "create_at": self.create_at,
            "messages": self.messages,
        }
        
    def get_info(self):
        return {
            "chat_id": self.chat_id,
            "chat_label": self.chat_label,
            "create_at": self.create_at,
        }
        
    def __str__(self) -> str:
        return {
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "chat_label": self.chat_label,
            "create_at": self.create_at,
            "messages": self.messages,
        }