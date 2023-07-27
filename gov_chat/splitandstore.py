from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain.docstore.document import Document
from json import load

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from os import environ
import chromadb


def get_chroma_client():
    return chromadb.HttpClient(
        host=environ.get("VECTOR_STORE_HOST","localhost"),
        port=environ.get("VECTOR_STORE_PORT", "8000")

    )

def split_and_load_docs(document_dir:str = " ./outputs/docs", chunk_size=500, chunk_overlap=0,collection_name=None, clean_collection=True)->list[Document]:
    if Path(document_dir).exists is False:
        raise NameError(f"The specified directory {document_dir} does not exist")
    docs = []
    for f in Path(document_dir).glob("*.json"):
        with open(f,"r") as fp:
            tmp = load(fp)
            print(tmp)
            doc = Document.parse_raw(tmp)
            docs.append(doc)
    

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    all_splits = text_splitter.split_documents(docs)


    # Store 
    
    db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=collection_name or Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME)

    if clean_collection:
        db.delete_collection()
        db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=collection_name or Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME)
    db.add_documents(all_splits)
    db.persist()

if __name__ == "__main__":
    split_and_load_docs()