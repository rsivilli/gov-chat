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

import os

if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE']= 'gov_chat_management.settings'
    django.setup()

from customer_management.models import ChatbotConfig

server_chatbot_id = UUID(os.environ.get("CHATBOT_ID","e813ff23-7935-4dbe-8a79-5c1596154d5a"))
collection = ""


chatbot = ChatBot()


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

@app.post("/chat/{chatbot_id}")
async def generate_chat_response( 
    question:str = Body(), 
    chatbot_id:UUID= Path(), 
    chat_history:list[ChatMessage]=Body(default=[]),
    site:str=Body(),customer:str=Body()
    )->ChatMessage:
    if chatbot_id != server_chatbot_id:
        raise HTTPException(HTTP_404_NOT_FOUND, f"Could not find chatbot with id {chatbot_id}")
    try:
        chatbot.select_collection(site)
    except ValueError as e:
        raise HTTPException(HTTP_404_NOT_FOUND, f"Site {site} is not supported by this bot")

    message = chatbot.ask_bot(question,chat_history)
    return ChatMessage(message=message,role = "agent")

def initialize_chatbot():
    chat_config = ChatbotConfig.objects.get(pk=server_chatbot_id)
    if chat_config is None:
        raise ValueError(f"Could not find config for chatbot id {server_chatbot_id}")
    





