import os
from typing import List
import psycopg2
from src.core.components.repository.vector_store.vector_store_interface import IVectorStore
from psycopg2.extras import RealDictCursor
from psycopg2.extras import execute_values



class PgvectoryVectorStore(IVectorStore):
    
    def __init__(self ,db_name: str, db_port: int, db_user: str, db_password: str, db_host: str, vector_table_name: str, similarity_threshold: float, top_k: int) -> None:
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.vector_table_name = vector_table_name
        self.similarity_threshold: float = similarity_threshold
        self.top_k: int = top_k
        
    def _connect(self):
        """Estabelece a conexão com o banco de dados PostgreSQL."""
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        
    def retriever(self, query_embedding: list) -> List[str]:
        """
        Recupera conteúdos do banco de dados com base na similaridade do embedding.

        :param query_embedding: Vetor de consulta (embedding).
        :param similarity_threshold: Limiar mínimo de similaridade (float entre 0 e 1).
        :param num_matches: Número máximo de correspondências desejadas.
        :return: Lista de dicionários contendo os conteúdos correspondentes.
        """
        
        query = f"""
        WITH vector_matches AS (
            SELECT conteudo, 1 - (embedding <=> %s::vector) AS similarity
            FROM {self.vector_table_name}
            WHERE 1 - (embedding <=> %s::vector) > %s
            ORDER BY similarity DESC
            LIMIT %s
        )
        SELECT conteudo FROM vector_matches
        """

        conn = None
        matches = []

        try:
            conn = self._connect()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Executar consulta com parâmetros
            cursor.execute(query, (query_embedding, query_embedding, self.similarity_threshold, self.top_k))
            
            # Obter resultados
            results = cursor.fetchall()
            
            if len(results) == 0:
                raise Exception("Did not find any results. Adjust the query parameters.")
            # Construir a lista de correspondências
            for r in results:
                matches.append(r["conteudo"])
        
        except Exception as e:
            print(f"Erro ao recuperar documentos: {e}")
        
        finally:
            # Fechar conexão apenas se ela foi criada
            if conn:
                cursor.close()
                conn.close()

        return matches
    
    def indexer(self, documents_embedded: list):
        """
        Insere múltiplos documentos e seus embeddings na tabela PostgreSQL.

        :param documents_embedded: Lista de dicionários, onde cada dicionário tem:
            - "conteudo": Texto do documento.
            - "embedding": Lista ou vetor representando o embedding do documento.
        """
        
        
        insert_query = f"""
        INSERT INTO {self.vector_table_name} (conteudo, embedding)
        VALUES %s
        """
        
        values = [
            (doc["conteudo"], doc["embedding"])
            for doc in documents_embedded
        ]

        try:
            conn = self._connect()
            cursor = conn.cursor()
            execute_values(cursor, insert_query, values)
            conn.commit()
            print(f"registros inseridos com sucesso na tabela {self.vector_table_name}.")
        
        except Exception as e:
            print(f"Erro ao inserir documentos: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
