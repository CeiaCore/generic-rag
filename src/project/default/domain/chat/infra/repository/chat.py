import psycopg2
from typing import List, Optional
from src.project.default.domain.chat.entity.chat import Chat
import os
import json

from src.project.default.domain.chat.repository.chat_repository import IChatRepository

class ChatRepository(IChatRepository):
    def __init__(self):
        self.db_name = os.getenv("POSTGRES_DB", "mydatabase")
        self.db_user = os.getenv("POSTGRES_USER", "myuser")
        self.db_password = os.getenv("POSTGRES_PASSWORD", "mypassword")
        self.db_host = os.getenv("POSTGRES_HOST", "localhost")
        self.db_port = os.getenv("POSTGRES_PORT", "5432")

    def _connect(self):
        """Estabelece a conexão com o banco de dados PostgreSQL."""
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )

    def insert(self, chat: Chat):
        """Insere um novo chat no banco de dados."""
        insert_query = """
        INSERT INTO chat (user_id, chat_id, chat_label, messages, created_at)
        VALUES (%s, %s, %s, %s, %s);
        """
        chat_data = (
            chat.user_id,
            chat.chat_id,
            chat.chat_label,
            json.dumps(chat.messages),  # Converte a lista de mensagens para JSON
            chat.create_at
        )

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, chat_data)
                conn.commit()

    def delete(self, chat_id: str):
        """Deleta um chat do banco de dados pelo chat_id."""
        delete_query = "DELETE FROM chat WHERE chat_id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_query, (chat_id,))
                conn.commit()

    def update(self, chat: Chat):
        """Atualiza um chat existente no banco de dados."""
        update_query = """
        UPDATE chat 
        SET chat_label = %s, messages = %s
        WHERE chat_id = %s;
        """
        chat_data = (
            chat.chat_label,
            json.dumps(chat.messages),  # Converte a lista de mensagens para JSON
            chat.chat_id
        )

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_query, chat_data)
                conn.commit()

    def get_by_id(self, chat_id: str) -> Optional[Chat]:
        """Obtém um chat pelo chat_id."""
        select_query = "SELECT user_id, chat_id, chat_label, messages, created_at FROM chat WHERE chat_id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_query, (chat_id,))
                result = cursor.fetchone()

                if result:
                    user_id, chat_id, chat_label, messages, created_at = result
                    return Chat(
                        user_id=user_id,
                        chat_id=chat_id,
                        chat_label=chat_label,
                        messages=messages,  
                        create_at=created_at
                    )
                return None

    def get_all(self, user_id: str) -> List[Chat]:
        """Obtém todos os chats de um usuário."""
        select_query = "SELECT user_id, chat_id, chat_label, messages, created_at FROM chat WHERE user_id = %s ORDER BY created_at DESC;"
        chats = []

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_query, (user_id,))
                results = cursor.fetchall()
  
                for row in results:
                    user_id, chat_id, chat_label, messages, created_at = row
                    chat = Chat(
                        user_id=user_id,
                        chat_id=chat_id,
                        chat_label=chat_label,
                        messages=messages,  # Converte JSON para lista
                        create_at=created_at
                    )
                    chats.append(chat)
        
        return chats
