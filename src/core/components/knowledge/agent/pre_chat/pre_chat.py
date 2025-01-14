
from pydantic import BaseModel
from src.core.components.embedding.interfaces.embedding_interface import EmbeddingInteface
from src.core.components.input.interface.input_knowledge_interface import InputFileKnowledgeInterface
from src.core.components.repository.vector_store.vector_store_interface import IVectorStore

class InputPreChatDto(BaseModel):
    prompt: str
    files: any


class PreChat:
    
    def __init__(self, embedding_component: EmbeddingInteface, input_file_component: InputFileKnowledgeInterface, vector_store_component: IVectorStore):
        self.embedding_component = embedding_component
        self.input_file_component = input_file_component
        self.vector_store_component = vector_store_component
        
    
    def execute(self, input: InputPreChatDto):
        chunks = self.input_file_component.extract(files=input.files)
        chunks_embeded = self.embedding_component.embedding_chunks(chunks=chunks)
        self.vector_store_component.indexer(documents_embedded=chunks_embeded)
            
            
    
        
        
    