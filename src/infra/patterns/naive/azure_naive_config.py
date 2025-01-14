import os

class AZURE_NAIVE_CONFIG:
    
    
    #POSTGRES CONFIG
    DB_NAME = os.getenv("POSTGRES_DB", "postgres")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pipeline-rag")
    DB_HOST = os.getenv("POSTGRES_HOST", "35.222.142.95")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    
    
    #RETRIEVAL CONFIG
    VECTOR_TABLE_NAME = "vector_embeddings"
    SIMILARITY_THRESHOLD: float = 0.3
    TOP_K: int = 5
    
    
    #TOKENIZER
    TOKENIZER_MODEL = "o200k_base"
    
    
    #LLM CONFIG
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: int = 1
    LLM_MAX_TOKENS: int = 10000
    LLM_MAX_TOKENS: int = 10000
    
    
    
    LLM_AZURE_DEPLOYMENT = "gpt-4o-mini"
    
    
    #EMBEDDING CONFIG
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_AZURE_DEPLOYMENT = "text-embedding-ada-002"
    DIMENSIONS: int = None
    
    
    #MEMORY CONFIG
    MEMORY_TABLE_NAME: str = "memory"


