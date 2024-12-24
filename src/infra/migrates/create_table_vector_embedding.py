
import psycopg2
import os

# Dados de conexão ao banco de dados
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_USER = os.getenv("POSTGRES_USER", "myuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mypassword")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5433)
DB_TABLE_NAME = "vector_embeddings"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()



cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# cur.execute(f"DROP TABLE IF EXISTS {DB_TABLE_NAME}")

create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (
        conteudo TEXT,
        embedding VECTOR(1536)
    );
    """
    


cur.execute(create_table_query)
cur.execute(create_table_query)

# Confirma as alterações no banco
conn.commit()

# Fecha o cursor e a conexão
cur.close()
conn.close()

print(f"Tabela '{DB_TABLE_NAME}' criada com sucesso.")