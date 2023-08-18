from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain.docstore.document import Document
from json import load

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from os import environ
import chromadb

from tqdm import tqdm


def get_chroma_client():
    return chromadb.HttpClient(
        host=environ.get("VECTOR_STORE_HOST","localhost"),
        port=environ.get("VECTOR_STORE_PORT", "8000")

    )

def split_and_load_docs(document_dir:str = " ./outputs/docs", chunk_size=500, chunk_overlap=0,collection_name=None, clean_collection=True)->list[Document]:
    if Path(document_dir).exists is False:
        raise NameError(f"The specified directory {document_dir} does not exist")

    if clean_collection:
        if isinstance(collection_name,list):
            for name in collection_name:
                db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=name or Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME)
                db.delete_collection()
        else:
            db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=collection_name or Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME)
            db.delete_collection()

    for f in tqdm(Path(document_dir).glob("*.json")):
        with open(f,"r") as fp:
            tmp = load(fp)
            doc = Document.parse_raw(tmp)
            print(f"Indexing {doc.metadata.get('source')}")
    

            text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
            page = doc.metadata.get("page")
            all_splits = text_splitter.split_documents([doc])
            if page is not None:
                ids = [f"{doc.metadata.get('source')}-{page}-{i}" for i in range(len(all_splits))]
            else:
                ids = [f"{doc.metadata.get('source')}-{i}" for i in range(len(all_splits))]

            # Store 
            if isinstance(collection_name,list):
                for name in collection_name:
                    db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=name or Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME)
                    db.add_documents(all_splits,ids=ids)


            else:
                db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=collection_name or Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME)
                db.add_documents(all_splits,ids=ids)

if __name__ == "__main__":
    split_and_load_docs()