from dotenv import load_dotenv


from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.llms import GPT4All
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import os


load_dotenv()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
callbacks =  [StreamingStdOutCallbackHandler()]
# search = SerpAPIWrapper()
tools = [
    # Tool(
    #     name = "Current Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current events or the current state of the world"
    # ),
]


memory = ConversationBufferMemory(memory_key="chat_history")

# llm=OpenAI(temperature=0)
llm = GPT4All(model=model_path, backend="gptj", callbacks=callbacks, verbose=False)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory,callbacks=callbacks)

print(agent_chain.run(input="hi, i am bob"))

