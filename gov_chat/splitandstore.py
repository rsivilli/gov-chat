from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain.docstore.document import Document
from json import load

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def split_and_load_docs(document_dir:str = " ./outputs/docs", chunk_size=500, chunk_overlap=0)->list[Document]:
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
    vectorstore = Chroma.from_documents(documents=all_splits,embedding=HuggingFaceEmbeddings(),persist_directory="./chroma_store")
    vectorstore.persist()

if __name__ == "__main__":
    split_and_load_docs()