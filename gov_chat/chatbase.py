import requests

values = dict(
    captchaCode="hadsa",
    chatId="chatbase--1--pdf-p680fxvnm",
    conversationId= "x6DifMhAoYkoDV-NiHvEj-chatbase--1--pdf-p680fxvnm",
    messages =[{
        "role": "assistant", "content": "👋 Hi! I am ChatbaseAI, ask me anything about Chatbase!"

    },
    {"content": "What is Chatbase?", "role": "user"}
    ]
)
values = {"messages":[{"role":"assistant","content":"👋 Hi! I am ChatbaseAI, ask me anything about Chatbase!"},{"role":"assistant","content":"By the way, you can create a chatbot like me for your website! 😮"},{"content":"What is Chatbase?","role":"user"},{"content":"Chatbase is an AI chatbot builder that allows you to train ChatGPT on your data. It enables you to add a chat widget to your website or interact with the chatbot through the API. You can upload a document or provide a link to your website, and Chatbase will create a chatbot that can answer questions about the content. It's a powerful tool for enhancing user engagement and providing automated support.","role":"assistant"},{"content":"How do I add data to my chatbot?","role":"user"},{"content":"To add data to your chatbot, you have a few options. You can upload documents in formats like .pdf, .txt, .doc, or .docx. Alternatively, you can paste text directly into Chatbase or provide a link to your website. Chatbase will extract the data from these sources and use it to train the chatbot. Simply choose the method that is most convenient for you and let Chatbase handle the rest!","role":"assistant"},{"content":"how do I add chatbase to my website?","role":"user"}],"captchaCode":"hadsa","chatId":"chatbase--1--pdf-p680fxvnm","conversationId":"x6DifMhAoYkoDV-NiHvEj-chatbase--1--pdf-p680fxvnm"}
r = requests.get("https://www.chatbase.co/api/fe/chat",data=values,headers={"Content-Type":"application/json"})



print(r.json())