from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain.docstore.document import Document
from json import load

from langchain.embeddings import HuggingFaceEmbeddings
document_dir = "./outputs/docs"
docs = []
for f in Path(document_dir).glob("*.json"):
    with open(f,"r") as fp:
        doc = Document.parse_raw(load(fp))
        docs.append(doc)



text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(docs)


# Store 
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
vectorstore = Chroma.from_documents(documents=all_splits,embedding=HuggingFaceEmbeddings(),persist_directory="./chroma_store")
vectorstore.persist()