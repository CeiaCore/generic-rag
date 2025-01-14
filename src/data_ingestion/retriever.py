from src.infra.components.embedding.azure_openai.embedding import Embeddings

from src.infra.components.repository.vector_store.pgvector.pgvetor import PgvectoryRepository

query = "o que diz a A Companhia Energética de Minas Gerais (“Companhia” ou “Cemig”) submete à apreciação?"

embedding = Embeddings(
    dimensions=768,
    model="text-embedding-3-small"
)

query_embed = embedding.embedding_query(query=query)

retrieval = PgvectoryRepository()
result = retrieval.retriever(query_embedding=query_embed)
print(result)