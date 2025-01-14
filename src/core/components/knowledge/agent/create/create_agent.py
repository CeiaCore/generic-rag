from pydantic import BaseModel


class InputCreateAgentDto(BaseModel):
    name: str
    description: str
    prompt: str
    files: any



class CreateAgent:
    
    def __init__(self):
        pass
    
    def create(input: InputCreateAgentDto) -> OutputCreateAgenteDto:
        
        return OutputCreateAgenteDto()