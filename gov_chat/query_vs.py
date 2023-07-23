from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings



def interregate_vs(query:str,history:list):
    db = Chroma(embedding_function=HuggingFaceEmbeddings(),persist_directory="./chroma_store")
    docs = db.similarity_search(query)
    sources = "\n".join([doc.metadata.get("source") for doc in docs])
    return f"I would have fed these into chatbot:\n {sources}"
