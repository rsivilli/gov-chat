from fastapi import FastAPI
from gov_chat.query_bot import ChatBot, ChatMessage
from uuid import UUID

from gov_chat_management import settings as app_settings
from django.conf import settings
import django
from pydantic import BaseSettings
from starlette.status import HTTP_404_NOT_FOUND
from fastapi import HTTPException, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from asgiref.sync import sync_to_async

import os

if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE']= 'gov_chat_management.settings'
    django.setup()

from customer_management.models import ChatbotConfig

server_chatbot_id = UUID(os.environ.get("CHATBOT_ID","318bd757-6c01-4f9b-b4a9-5128541dcf7a"))
collection = ""


def initialize_chatbot():
    chat_config = ChatbotConfig.objects.get(pk=server_chatbot_id)
    if chat_config is None:
        raise ValueError(f"Could not find config for chatbot id {server_chatbot_id}")
    return chat_config


chatbot = ChatBot(backend_type=os.getenv("MODEL_TYPE"))


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# chat_config = initialize_chatbot()
# chatbot.set_template(chat_config.prompt_template)


@app.post("/chat/{chatbot_id}")
async def generate_chat_response( 
    question:str = Body(), 
    chatbot_id:UUID= Path(), 
    chat_history:list[ChatMessage]=Body(default=[]),
    collection:str=Body(default=None)
    )->ChatMessage:
    try:
        #TODO need to verify that chatbot has permission to this collection 
        chatbot.select_collection(collection )
    except ValueError as e:
        raise HTTPException(HTTP_404_NOT_FOUND, f"Site {collection} is not supported by this bot")

    message, sources = chatbot.ask_bot(question,chat_history)
    return ChatMessage(message=message,role = "agent",sources=sources)





