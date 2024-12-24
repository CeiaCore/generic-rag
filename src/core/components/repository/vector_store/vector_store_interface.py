


from abc import ABC, abstractmethod


class IVectorStore(ABC):
    
    @abstractmethod
    def retriever(self, query_embedding: list):
        raise NotImplementedError
    
    
    @abstractmethod
    def indexer(self, documents_embedded: list):
        raise NotImplementedError