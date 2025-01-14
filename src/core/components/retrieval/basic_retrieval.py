


from src.core.components.repository.vector_store.vector_store_interface import IVectorStore
from src.core.components.retrieval.interface.retrieval_inteface import RetrievalInterface



class BasicRetrieval(RetrievalInterface):
    
    def __init__(self, vector_store: IVectorStore) -> None:
        self.vector_store = vector_store
        
    
    def retriever(self, query_embedding: list):
        """Retrieve the top n_results most similar documents to the query embedding."""
        results = self.vector_store.retriever(query_embedding)
        return results