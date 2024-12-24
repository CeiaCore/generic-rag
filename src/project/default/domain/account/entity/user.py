from src.project.default.domain.account.value_object.Email import Email


class InputUserDto:
    def __init__(self, email: Email, user_name: str, user_id: str):
        self.email = email
        self.user_name = user_name
        self.user_id = user_id
        

class User:
    
    def __init__(self, email:str, user_name: str, user_id: str) -> None:
        self.email = email
        self.user_name = user_name
        self.user_id = user_id
    
    def create(self, input: InputUserDto):
        email = Email.create(input.email)
        return User(user_id=input.user_id, email=email, user_name=input.user_name)
    