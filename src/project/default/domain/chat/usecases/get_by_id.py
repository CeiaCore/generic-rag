
from typing import List
from src.project.default.domain.chat.repository.chat_repository import IChatRepository
from src.project.default.domain.interface.usecase_interface import UsecaseInterface



class InputGetBydIdChatDto:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
    

class OutputGetBydIdChatDto:
    def __init__(self, chat: List):
        self.chat = chat

class GetBydIdChat(UsecaseInterface):
    
    def __init__(self, repository: IChatRepository ):
        self.repository = repository
        
    def execute(self, input: InputGetBydIdChatDto) -> OutputGetBydIdChatDto:
        chat_id = input.chat_id
        chat = self.repository.get_by_id(chat_id)
        
        output = OutputGetBydIdChatDto(
            chat=chat.to_json()
        )
        return output
        