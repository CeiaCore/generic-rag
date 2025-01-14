from src.core.components.llm.interface.llm_interface import LLMInterface
from langchain_google_vertexai import VertexAI


class LLMVertexAi(LLMInterface):
    
    def __init__(self, model: str, project: str, temperature: int, max_tokens: int,  *args, **kwargs) -> None:
        self.instance = VertexAI(model_name=model,temperature=temperature, max_tokens=max_tokens, project=project)
        
 
    def batch(self, prompt: str):
        return self.instance.invoke(prompt)

    def stream(self, prompt: str):
        for chunk in self.instance.stream(prompt):
            yield chunk
        
        
        

