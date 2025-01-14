
import psycopg2
import os

# Dados de conexão ao banco de dados
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "pipeline-rag"
DB_HOST = "35.222.142.95"
DB_PORT = 5432
DB_TABLE_NAME = "case_juridico"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

drop_table = f"""DROP TABLE IF EXISTS {DB_TABLE_NAME}"""
cur.execute(drop_table)

cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# cur.execute(f"DROP TABLE IF EXISTS {DB_TABLE_NAME}")

create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (
        conteudo TEXT,
        embedding VECTOR(768)
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