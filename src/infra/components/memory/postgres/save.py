


from src.infra.components.memory.postgres.postgres_memory import PostgresMemory



memory = PostgresMemory()
documents = ["Document1",
             "Document2",
             "Document3",
             "Document4"]

# memory.save_memory(chat_id="chat_id", data=documents)

print(memory.retrieve_memory(chat_id="chat_id"))