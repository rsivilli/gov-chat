# Build prompt
from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All
from langchain.llms.base import LLM
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

model_path = "./models/ggml-gpt4all-j-v1.3-groovy.bin"
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
    def __init__(self) -> None:
        QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=self.template,)
        callbacks =  [StreamingStdOutCallbackHandler()]
        print(f"Loading from {model_path}")
    
        self.llm = GPT4All(model=model_path, callbacks=callbacks, verbose=False)
        self.db = Chroma(embedding_function=HuggingFaceEmbeddings(),persist_directory="./chroma_store")
        self.qa_chain = RetrievalQA.from_chain_type(self.llm,
                                        retriever=self.db.as_retriever(),
                                        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    def ask_bot(self,query:str, history:list):
    
        result = self.qa_chain({"query": query})
        return result["result"]
        
    # Run chain

   
    

    