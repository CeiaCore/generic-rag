
import os
from typing import List
import psycopg2
from src.core.components.memory.interface.memory_interface import MemoryInterface

from psycopg2.extras import RealDictCursor

class PostgresMemory(MemoryInterface):
    
    def __init__(self, db_name, db_user, db_password, db_host, db_port, memory_table_name) -> None:
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.memory_table_name = memory_table_name
        
        
    def _connect(self):
        """Estabelece a conexão com o banco de dados PostgreSQL."""
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        
        
    def retrieve_memory(self, chat_id: str) -> List[str]:
        """
        Recupera uma lista de documentos da tabela memory para um chat_id específico.

        :param chat_id: O ID do chat para buscar memórias associadas.
        :return: Lista de strings contendo os documentos da memória.
        """
        
        query = f"""
        SELECT chat_id, content, query, response
        FROM {self.memory_table_name}
        WHERE chat_id = %s
        ORDER BY chat_id DESC
        LIMIT 5
        """

        conn = None
        memory_list = []

        try:
            conn = self._connect()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Executar consulta com parâmetros
            cursor.execute(query, (chat_id,))
            
            # Obter resultados
            results = cursor.fetchall()
            
            # Construir a lista de memórias
            for row in results:
                memory_list.append({
                    "chat_id": row["chat_id"],
                    "content": row["content"].split(",") if isinstance(row["content"], str) else row["content"],
                    "query": row["query"],
                    "response": row["response"],
                })
        
        except Exception as e:
            print(f"Erro ao recuperar memórias para chat_id {chat_id}: {e}")
        
        finally:
            # Fechar conexão apenas se ela foi criada
            if conn:
                cursor.close()
                conn.close()

        return memory_list
    
    def save_memory(self, chat_id: str, content: List[str], query: str, response: str):
        """
        Salva um novo documento na tabela memory para um chat_id específico.

        :param chat_id: O ID do chat ao qual a memória será associada.
        :param data: O conteúdo da memória a ser salvo.
        :param query: A query relacionada a essa memória.
        """


        conn = None

        try:
            conn = self._connect()
            cursor = conn.cursor()

            insert_query = f"""
            INSERT INTO {self.memory_table_name} (chat_id, content, query, response)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (chat_id, content, query, response))
            conn.commit()
        
        except Exception as e:
            print(f"Erro ao salvar memória para chat_id {chat_id}: {e}")
            if conn:
                conn.rollback()
        
        finally:
            if conn:
                cursor.close()
                conn.close()
