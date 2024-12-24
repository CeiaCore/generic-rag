import pandas as pd
from typing import List

from src.infra.components.embedding.openai.embedding import AzureEmbeddings
from src.infra.components.repository.vector_store.pgvector.pgvetor import PgvectoryVectorStore
from src.infra.patterns.naive.basic_naive.basic_naive_config import BASIC_NAIVE_CONFIG


def data_compose() -> List:
    result = process_csv()
    chunks = chunk_generator_with_sessions(result)
    return chunks

def process_csv():
    caminho_do_arquivo = "src/data_ingestion/chunks_merged.csv"
    df = pd.read_csv(caminho_do_arquivo)
    return df

def chunk_generator_with_sessions(df):
    chunks = df["conteudo"].apply(lambda chunk: {"conteudo": chunk}).tolist()
    return chunks

chunks = data_compose()
embeddings = AzureEmbeddings("text-embedding-ada-002",azure_deployment="text-embedding-ada-002", dimensions=None).embedding_chunks(chunks=chunks)

repository = PgvectoryVectorStore(
    db_host=BASIC_NAIVE_CONFIG.DB_HOST,
    db_name=BASIC_NAIVE_CONFIG.DB_NAME,
    top_k=BASIC_NAIVE_CONFIG.TOP_K,
    db_password=BASIC_NAIVE_CONFIG.DB_PASSWORD,
    db_port=BASIC_NAIVE_CONFIG.DB_PORT,
    db_user=BASIC_NAIVE_CONFIG.DB_USER,
    similarity_threshold=0.3,
    vector_table_name="vector_embeddings"
)

repository.indexer(embeddings)