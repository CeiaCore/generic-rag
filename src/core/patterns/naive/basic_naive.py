from src.core.components.embedding.interfaces.embedding_interface import EmbeddingInteface
from src.core.components.input.interface.InputInterface import InputInterface
from src.core.components.llm.interface.llm_interface import LLMInterface
from src.core.components.memory.interface.memory_interface import MemoryInterface
from src.core.components.prompt.interface.prompt_interface import InputBasicPromptDto, PromptInterface
from src.core.components.retrieval.interface.retrieval_inteface import RetrievalInterface
from src.core.patterns.interface.pattern_interface import PatternInterface


class InputBasicNaiveDto:

    def __init__(self, query: str, chat_id: str, file = None):
        self.query = query
        self.chat_id = chat_id
        self.file = file
        


class BasicNaive(PatternInterface):

    def __init__(self, input_component: InputInterface, retrieval_component: RetrievalInterface, embedding_component: EmbeddingInteface, memory_component: MemoryInterface, llm_component: LLMInterface, prompt_component: PromptInterface):
        self.input_component = input_component
        self.retrieval_component = retrieval_component
        self.memory_component = memory_component
        self.llm_component = llm_component
        self.prompt_component = prompt_component
        self.embedding_component = embedding_component

    def execute(self, input: InputBasicNaiveDto):
        self.input_component.validate(query=input.query, file=input.file)
        query_embed = self.embedding_component.embedding_query(input.query)
        
        documents = self.retrieval_component.retriever(query_embedding=query_embed)
        
        memory = self.memory_component.retrieve_memory(input.chat_id)
        input_prompt = InputBasicPromptDto(
            context=documents,
            memory=memory,
            query=input.query
        )
        prompt = self.prompt_component.prompt(input=input_prompt)
        
        response_generated = ""
        response = self.llm_component.stream(prompt=prompt)
        for chunk in response:
            response_generated += chunk
            yield chunk
            
        self.memory_component.save_memory(chat_id=input.chat_id, content=documents, query=input.query, response=response_generated)
        
        



