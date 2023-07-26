import chromadb


# client = chromadb.Client(settings=chromadb.Settings(persist_directory="chroma_store",is_persistent=True,anonymized_telemetry=False))
client = chromadb.HttpClient()


print(client.list_collections())