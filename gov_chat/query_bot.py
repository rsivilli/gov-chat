# Build prompt
from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All, OpenAI
from langchain.llms.base import LLM
from langchain.vectorstores import Chroma

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
import chromadb
from pydantic import BaseModel
from .splitandstore import get_chroma_client

from enum import Enum

model_path = "./models/ggml-model-gpt4all-falcon-q4_0.bin"

class ChatBotBackend(str,Enum):
    LOCAL_GPT4ALL = "GPT4ALL"
    CHATGPT = "CHATGPT"
class ChatBot:
    
    db:Chroma
    llm:LLM
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible. 
    Always say "thanks for asking!" at the end of the answer. 
    {context}
    Question: {question}
    Helpful Answer:"""
    def __init__(self, backend_type:ChatBotBackend ) -> None:
        self.QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=self.template,)
        callbacks =  [StreamingStdOutCallbackHandler()]
        self.backend_type = backend_type
        if backend_type == ChatBotBackend.LOCAL_GPT4ALL:
            print(f"Loading from {model_path}")
            self.llm = GPT4All(model=model_path, callbacks=callbacks, verbose=False)
        elif backend_type == ChatBotBackend.CHATGPT:
            self.llm = OpenAI()
        else:
            raise ValueError(f"{backend_type} is not a supported backend type for chatbot")
            
        self.db = Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client())
        
        self.qa_chain = RetrievalQA.from_chain_type(self.llm,
                                        retriever=self.db.as_retriever(),
                                        chain_type_kwargs={"prompt":self.QA_CHAIN_PROMPT},return_source_documents=True)
    def ask_bot(self,query:str, history:list):
    
        result = self.qa_chain({"query": query})
        print(result)
        return result["result"], set([doc.metadata["source"] for doc in result["source_documents"] ])
    def select_collection(self,collection:str):
        chrome_client = get_chroma_client()
        chrome_client.get_collection(collection)
        self.db =  Chroma(embedding_function=HuggingFaceEmbeddings(),client=get_chroma_client(),collection_name=collection)
        self.qa_chain = RetrievalQA.from_chain_type(self.llm,
                                        retriever=self.db.as_retriever(),
                                        chain_type_kwargs={"prompt": self.QA_CHAIN_PROMPT},return_source_documents=True)
        
    def get_collections(self):
        client=get_chroma_client()
        return [col.name for col in client.list_collections()]
    def set_template(self,template:str):
        self.template = template
        self.QA_CHAIN_PROMPT =PromptTemplate(input_variables=["context", "question"],template=self.template,)
        self.qa_chain = RetrievalQA.from_chain_type(self.llm,
                                        retriever=self.db.as_retriever(),
                                        chain_type_kwargs={"prompt":self.QA_CHAIN_PROMPT},return_source_documents=True)

    # Run chain

   
    

class ChatMessage(BaseModel):
    message:str
    role:str
    sources:list[str]= []


