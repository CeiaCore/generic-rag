import psycopg2
import os

def create_memory_table():
    """
    Cria a tabela 'memory' no banco de dados PostgreSQL.
    """
    db_name = os.getenv("POSTGRES_DB", "mydatabase")
    db_user = os.getenv("POSTGRES_USER", "myuser")
    db_password = os.getenv("POSTGRES_PASSWORD", "mypassword")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", 5433)
    table_name = "memory"

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        chat_id TEXT NOT NULL,
        content TEXT[],
        query TEXT,
        response TEXT
    );
    """
    
    drop_table = f"""DROP TABLE IF EXISTS {table_name}"""

    conn = None
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = conn.cursor()
        
        cursor.execute(drop_table)
        # Criar a tabela
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabela 'memory' criada com sucesso.")
    
    except Exception as e:
        print(f"Erro ao criar a tabela 'memory': {e}")
    
    finally:
        # Fechar conexão
        if conn:
            cursor.close()
            conn.close()

# Executar a função
if __name__ == "__main__":
    create_memory_table()
