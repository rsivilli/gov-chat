import chromadb


client = chromadb.Client(settings=chromadb.Settings(persist_directory="test_dir",is_persistent=True))

client.get_or_create_collection("first-collection")

client.get_or_create_collection("second-collection")

client.get_or_create_collection("second-collection")

print(client.list_collections())