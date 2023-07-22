from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

db = Chroma(embedding_function=HuggingFaceEmbeddings(),persist_directory="./chroma_store")
query = "Do I need a fishing license?"
docs = db.similarity_search(query)

for doc in docs:
    print(doc.metadata)
    print(len(doc.page_content))
