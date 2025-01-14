
import psycopg2
import os

# Dados de conexão ao banco de dados
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_USER = os.getenv("POSTGRES_USER", "myuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mypassword")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5433)

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Criação do cursor para executar comandos SQL
cur = conn.cursor()

# Comando SQL para criar a tabela
drop_table = f"""DROP TABLE IF EXISTS chat"""

create_table_query = """
CREATE TABLE IF NOT EXISTS chat (
    user_id VARCHAR(255) NOT NULL,
    chat_id VARCHAR(255) PRIMARY KEY,
    chat_label VARCHAR(255),
    messages JSONB,
    created_at TIMESTAMP
);
"""

# Executa o comando SQL
cur.execute(create_table_query)

# Confirma as alterações no banco
conn.commit()

# Fecha o cursor e a conexão
cur.close()
conn.close()

print("Tabela 'chat' criada com sucesso.")