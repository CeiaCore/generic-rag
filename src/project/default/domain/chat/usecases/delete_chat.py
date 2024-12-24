


from src.project.default.domain.chat.repository.chat_repository import IChatRepository
from src.project.default.domain.interface.usecase_interface import UsecaseInterface



class InputDeleteChatDto:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        

class DeleteChat(UsecaseInterface):
    
    def __init__(self, repository: IChatRepository ):
        self.repository = repository
        
    def execute(self, input: InputDeleteChatDto):
        self.repository.delete(input.chat_id)
        