


from src.project.default.domain.chat.entity.chat import Chat, InputChatDto
from src.project.default.domain.chat.repository.chat_repository import IChatRepository
from src.project.default.domain.interface.usecase_interface import UsecaseInterface



class InputCreateChatDto:
    def __init__(self, user_id: str):
        self.user_id = user_id
        

class CreateChat(UsecaseInterface):
    
    def __init__(self, repository: IChatRepository ):
        self.repository = repository
        
        
    def execute(self, input: InputCreateChatDto):
        input_chat = InputChatDto(
            user_id=input.user_id
        )
        chat = Chat.create(input_chat)
        self.repository.insert(chat)
        
        output = chat.to_json()
        return output
        