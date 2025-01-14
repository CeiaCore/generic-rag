

from abc import ABC, abstractmethod
from typing import List


class EmbeddingInteface(ABC):
    
    @abstractmethod
    def embedding_query(self, query: str) -> List:
        raise NotImplementedError
    
    @abstractmethod
    def embedding_documents(self, documents: List[str], chunk_size: int | None = None) -> List[List[float]]:
        raise NotImplementedError
    
    @abstractmethod
    def embedding_chunks(self, chunks) -> List[dict]:
        raise NotImplementedError