import os

class VERTEXAI_NAIVE_CONFIG:
    
    #VERTEXAI
    PROJECT = "energygpt-421317"
    
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
    LLM_MODEL: str = "gemini-2.0-flash-exp"
    LLM_TEMPERATURE: int = 1
    LLM_MAX_TOKENS: int = 10000
    
    
    
    #EMBEDDING CONFIG
    EMBEDDING_MODEL: str = "text-multilingual-embedding-002"
    
    
    #MEMORY CONFIG
    MEMORY_TABLE_NAME: str = "memory"


