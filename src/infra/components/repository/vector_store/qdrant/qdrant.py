from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from src.core.components.repository.vector_store.vector_store_labed_interface import IVectorStoreLabed

class QdrantVectorStore(IVectorStoreLabed):
    def __init__(self, host="localhost", port=6333):
        """
        Inicializa o cliente Qdrant.

        :param host: Endereço do servidor Qdrant.
        :param port: Porta do servidor Qdrant.
        """
        self.client = QdrantClient(host=host, port=port)

    def retriever(self):
        """
        Método de recuperação (a ser implementado posteriormente).
        """
        pass

    def indexer(self, documents_embedded, label):
        """
        Indexa documentos no Qdrant.

        :param documents_embedded: Um dicionário contendo `content`, `embeddings` e metadados.
        :param label: Nome da collection onde os documentos serão armazenados.
        """
        # Cria uma coleção se ela ainda não existir
        if not self.client.get_collection(label):
            self.client.recreate_collection(
                collection_name=label,
                vector_size=len(documents_embedded["embeddings"][0]),
                distance="Cosine"  # Escolha o tipo de métrica: Cosine, Euclidean, etc.
            )

        # Construa os pontos para indexação
        points = []
        for idx, embedding in enumerate(documents_embedded["embeddings"]):
            point = PointStruct(
                id=idx,  # ID único para o ponto (pode ser um hash ou contador)
                vector=embedding,
                payload={
                    "content": documents_embedded["content"][idx]
                }
            )
            points.append(point)

        # Envia os pontos para o Qdrant
        self.client.upsert(
            collection_name=label,
            points=points
        )

        print(f"{len(points)} documentos indexados na coleção '{label}' com sucesso.")
