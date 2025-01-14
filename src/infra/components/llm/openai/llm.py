
from src.core.components.llm.interface.llm_interface import LLMInterface
from langchain_openai import ChatOpenAI


class LLMOpenai(LLMInterface):
    
    def __init__(self, model: str, temperature: int, max_tokens: int) -> None:
        
        self.instance = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        
    def batch(self, prompt: str):
        return self.instance.invoke(prompt)

    def stream(self, prompt: str):
        for chunk in self.instance.stream(prompt):
            yield chunk.content
        