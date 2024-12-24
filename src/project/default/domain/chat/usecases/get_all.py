


from typing import List
from src.project.default.domain.chat.repository.chat_repository import IChatRepository
from src.project.default.domain.interface.usecase_interface import UsecaseInterface



class InputGetAllChatDto:
    def __init__(self, user_id: str):
        self.user_id = user_id
    

class OutputGetAllChatDto:
    def __init__(self, chats: List):
        self.chats = chats

class GetAllChat(UsecaseInterface):
    
    def __init__(self, repository: IChatRepository ):
        self.repository = repository
        
    def execute(self, input: InputGetAllChatDto) -> OutputGetAllChatDto:
        user_id = input.user_id
        chats = self.repository.get_all(user_id)
        
        output = OutputGetAllChatDto(
            chats = [chat.get_info() for chat in chats]
        )
        return output
        