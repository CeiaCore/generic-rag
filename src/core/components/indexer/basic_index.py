



from src.core.components.indexer.interface.indexer_interface import IIndexer
from src.core.components.repository.vector_store.vector_store_interface import IVectorStore


class BasicIndexer(IIndexer):
    
    
    def __init__(self, vector_store:IVectorStore) -> None:
        self.vector_store = vector_store
        
        
    def indexer(self, input):
        
        self.vector_store.indexer()
