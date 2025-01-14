import pandas as pd
from typing import List

from src.infra.components.embedding.vertexai.embedding import VertexEmbeddings
from src.infra.components.repository.vector_store.pgvector.pgvetor import PgvectoryVectorStore


def data_compose() -> List:
    result = process_csv()
    chunks = chunk_generator_with_sessions(result)
    return chunks

def process_csv():
    caminho_do_arquivo = "/workspaces/generic-rag/src/data_ingestion/juridico_datasets.csv"
    df = pd.read_csv(caminho_do_arquivo)
    return df

def chunk_generator_with_sessions(df):
    chunks = df["conteudo"].apply(lambda chunk: {"conteudo": chunk}).tolist()
    return chunks

chunks = data_compose()
embeddings = VertexEmbeddings(model="text-multilingual-embedding-002", project="energygpt-421317").embedding_chunks(chunks=chunks)

 
# repository = PgvectoryVectorStore(
#     db_host=BASIC_NAIVE_CONFIG.DB_HOST,
#     db_name=BASIC_NAIVE_CONFIG.DB_NAME,
#     top_k=BASIC_NAIVE_CONFIG.TOP_K,
#     db_password=BASIC_NAIVE_CONFIG.DB_PASSWORD,
#     db_port=BASIC_NAIVE_CONFIG.DB_PORT,
#     db_user=BASIC_NAIVE_CONFIG.DB_USER,
#     similarity_threshold=0.3,
#     vector_table_name="vector_embeddings"
# )

repository = PgvectoryVectorStore(
    db_host="35.222.142.95",
    db_name="postgres",
    top_k=10,
    db_password="pipeline-rag",
    db_port=5432,
    db_user="postgres",
    similarity_threshold=0.3,
    vector_table_name="case_juridico"
)

repository.indexer(embeddings)