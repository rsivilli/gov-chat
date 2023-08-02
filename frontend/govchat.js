/*** Govchat JS client
 * This file defines classes for the chatbot and surrounding messages to and from
 * the chatbot service
 */
class ChatMessage{
    constructor(message,role){
        this.message = message;
        this.role = role;
    }
}
class GovChat{
    chat_url = "localhost:8001/chat";
    session_id = self.crypto.randomUUID();
    site="localhost:8001/chat/894e5bb1-73d0-4b46-b89e-d8fc0c661b4f";
    constructor(chat_url,site, welcome_message, chatbot_id,customer){
        this.chat_url = chat_url;
        this.site = site
        this.messages = [];
        this.chatbot_id = chatbot_id;
        this.customer = customer
        this.messages.push(
            new ChatMessage(welcome_message,"agent")
        )
    }
    

    async chat(client_message){
        this.messages.push(new ChatMessage(client_message,"client"))
        const res = await fetch(this.chat_url+this.chatbot_id,  {
            body: JSON.stringify({
                question:client_message,
                collection:this.site,

        }),method: "POST",headers: {"Content-Type": "application/json",}});
        const out = await res.json();
        this.messages.push(out);

        return out; 


    }
    #dummy_chat(){
        const responses = [
            "Hello, how can I help you today? 😊",
            "I'm sorry, I didn't understand your question. Could you please rephrase it? 😕",
            "I'm here to assist you with any questions or concerns you may have. 📩",
            "I'm sorry, I'm not able to browse the internet or access external information. Is there anything else I can help with? 💻",
            "What would you like to know? 🤔",
            "I'm sorry, I'm not programmed to handle offensive or inappropriate language. Please refrain from using such language in our conversation. 🚫",
            "I'm here to assist you with any questions or problems you may have. How can I help you today? 🚀",
            "Is there anything specific you'd like to talk about? 💬",
            "I'm happy to help with any questions or concerns you may have. Just let me know how I can assist you. 😊",
            "I'm here to assist you with any questions or problems you may have. What can I help you with today? 🤗",
            "Is there anything specific you'd like to ask or talk about? I'm here to help with any questions or concerns you may have. 💬",
            "I'm here to assist you with any questions or problems you may have. How can I help you today? 💡",
          ];
          
          // Return a random response
        return responses[Math.floor(Math.random() * responses.length)];
    }
}

