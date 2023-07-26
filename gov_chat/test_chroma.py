import chromadb


client = chromadb.Client(settings=chromadb.Settings(persist_directory="chroma_store",is_persistent=True))



print(client.list_collections())