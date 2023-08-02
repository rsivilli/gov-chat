from splitandstore import get_chroma_client, split_and_load_docs
import chromadb


# client = chromadb.Client(settings=chromadb.Settings(persist_directory="chroma_store",is_persistent=True,anonymized_telemetry=False))
client = get_chroma_client()


print(client.list_collections())

