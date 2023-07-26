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
    chat_url = 0;
    session_id = self.crypto.randomUUID();
    site="localhost:8080/chat";
    constructor(chat_url,site, welcome_message){
        this.chat_url = chat_url;
        this.site = site
        this.messages = [];
        this.messages.push(
            new ChatMessage(welcome_message,"agent")
        )
    }

    chat(client_message){
        this.messages.push(new ChatMessage(client_message,"client"))
        // const res = await fetch("",  {body: JSON.stringify(this.messages)});
        const res = this.#dummy_chat();
        const out = new ChatMessage(res,"agent");
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

