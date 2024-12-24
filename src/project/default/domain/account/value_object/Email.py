

class Email:
    email: str
    
    def __init__(self, email: str):
        self.email = email
    
    @staticmethod
    def create(email: str):
        Email.validate(email)
        return Email(email)
    
    @staticmethod
    def validate(email: str):
        if not isinstance(email, str):
            raise Exception("email must be type string")