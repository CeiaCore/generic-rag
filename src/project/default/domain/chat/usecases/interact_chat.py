from src.core.patterns.interface.pattern_interface import PatternInterface
from src.core.patterns.naive.basic_naive import InputBasicNaiveDto
from src.project.default.domain.chat.repository.chat_repository import IChatRepository
from src.project.default.domain.interface.usecase_interface import UsecaseInterface


class InputInteractChatDto:
    def __init__(self, query: str,  chat_id: str, file: any = None):
        self.query = query
        self.chat_id = chat_id
        self.file = file


class InteractChat(UsecaseInterface):
    
    def __init__(self, repository: IChatRepository, pattern_service: PatternInterface):
        self.repository = repository
        self.pattern_service = pattern_service
        
    def execute(self, input: InputInteractChatDto):
        chat = self.repository.get_by_id(input.chat_id)
        user_message = {"rule": "user", "message": input.query}
        
        chat.change_chat_label(input.query)
        chat.insert_message(user_message)
        message = ""
        input_pattern = InputBasicNaiveDto(
            chat_id=input.chat_id,
            file=input.file,
            query=input.query,
        )
        for chunk in self.pattern_service.execute(input_pattern):
            message += chunk
            yield chunk
        
        bot_message = {"rule": "bot", "message": message}
        chat.insert_message(bot_message)
        chat.change_chat_label(input.query)
        self.repository.update(chat=chat)
        