


from abc import ABC, abstractmethod


class IVectorStoreLabed(ABC):
    
    @abstractmethod
    def retriever(self, query_embedding: list, id: str):
        raise NotImplementedError
    
    
    @abstractmethod
    def indexer(self, documents_embedded: list, label: str):
        raise NotImplementedError