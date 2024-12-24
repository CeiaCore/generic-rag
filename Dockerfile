FROM python:3.12.4


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/home/python/app:/home/python/app"

ENV POSTGRES_DB "mydatabase"
ENV POSTGRES_USER "myuser"
ENV POSTGRES_PASSWORD "mypassword"
ENV POSTGRES_HOST "host.docker.internal"
ENV POSTGRES_PORT 5433

ENV KEYCLOAK_SERVER_URL "https://sso.sandbox.enap.gov.br"
ENV KEYCLOAK_REALM "enap"
ENV KEYCLOAK_CLIENT_ID "chat-secretaria-backend"
ENV KEYCLOAK_CLIENT_SECRET "wj0aKlPHR852h9oyy5qt41VrHc70UPK6"
ENV KEYCLOAK_PUBLIC_KEY_URL "https://sso.enap.gov.br/realms/enap/protocol/openid-connect/certs"
ENV EXPECTED_AUDIENCES ["master-realm", "account"]  



WORKDIR /home/python/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


COPY src/data_ingestion/chunks_merged.csv /app/src/data_ingestion/chunks_merged.csv


EXPOSE 8000

CMD ["sh", "-c", "python src/infra/migrates/create_table_chat.py && python src/infra/migrates/create_table_memory.py && python src/infra/migrates/create_table_vector_embedding.py  && uvicorn src.project.default.fastapi.main:app --host 0.0.0.0 --port 8000"]
# CMD ["sh", "-c", "python src/migrates/create_table_chat.py && python src/migrates/create_table_memory.py && python src/migrates/create_table_vector_embedding.py && python src/data_ingestion/extract_chunks.py && uvicorn src.templates.default.fastapi.main:app --host 0.0.0.0 --port 8000"]
