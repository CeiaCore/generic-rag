from src.core.components.input.basic_input import BasicInput
from src.core.components.memory.basic_memory import BasicMemory
from src.core.components.retrieval.basic_retrieval import BasicRetrieval
from src.core.patterns.interface.pattern_interface import PatternInterface
from src.core.patterns.naive.basic_naive import BasicNaive
from src.infra.components.memory.postgres.postgres_memory import PostgresMemory
from src.infra.components.prompts.basic_prompt import BasicPrompt
from src.infra.components.repository.vector_store.pgvector.pgvetor import PgvectoryVectorStore
from src.infra.components.tools.tokenizer.tokenizer_tiktoken import TokenizerTikToken
from src.infra.patterns.interfaces.factory_interface import FactoryInterface
from src.infra.components.embedding.vertexai.embedding import VertexEmbeddings
from src.infra.patterns.naive.vertexai_naive_config import VERTEXAI_NAIVE_CONFIG
from src.infra.components.llm.vertexai.llm import LLMVertexAi

class VertexNaiveFactory(FactoryInterface):
    
    @staticmethod
    def create(config: VERTEXAI_NAIVE_CONFIG) -> PatternInterface:
   
        tokenizer = TokenizerTikToken(
            model=config.TOKENIZER_MODEL
            )
        
        vector_store = PgvectoryVectorStore(
            db_host=config.DB_HOST,
            db_name=config.DB_NAME,
            top_k=config.TOP_K,
            db_password=config.DB_PASSWORD,
            db_port=config.DB_PORT,
            db_user=config.DB_USER,
            vector_table_name=config.VECTOR_TABLE_NAME,
            similarity_threshold=config.SIMILARITY_THRESHOLD,
        )
        
        
        
        memory_store = PostgresMemory(
            db_host=config.DB_HOST,
            db_name=config.DB_NAME,
            db_user=config.DB_USER,
            db_password=config.DB_PASSWORD,
            db_port=config.DB_PORT,
            memory_table_name=config.MEMORY_TABLE_NAME
        )
        
        
        
        input_component = BasicInput(
            MAX_TOKENS=config.LLM_MAX_TOKENS,
            tokenizer=tokenizer
        )
        
        
        embedding_component = VertexEmbeddings(
            model=config.EMBEDDING_MODEL,
            project=config.PROJECT
        )
        
        
        
        retrieval_component = BasicRetrieval(
            vector_store=vector_store
        )
        
        
        memory_component = BasicMemory(
            memory_store=memory_store
        ) 
        
        
        prompt_component = BasicPrompt()
        
        
        llm_component = LLMVertexAi(
            model=config.LLM_MODEL,
            temperature=None,
            max_tokens=None,
            project=config.PROJECT
            
        )
  
        return BasicNaive(
            input_component=input_component,
            retrieval_component=retrieval_component,
            memory_component=memory_component,
            llm_component=llm_component,
            prompt_component=prompt_component,
            embedding_component=embedding_component
        )