/**
 * This is an example of using the javascript client
 */

var govchat;
const chatbot = document.getElementById('chatbot');
const conversation = document.getElementById('conversation');
const inputForm = document.getElementById('input-form');
const inputField = document.getElementById('input-field');

const siteField = document.getElementById("site-field");
const customerField = document.getElementById("customer-field");
const chatbotField = document.getElementById("chatbot-field");


document.addEventListener('DOMContentLoaded', function(){
    govchat = new GovChat("http://localhost:8001/chat/");
   
    inputForm.addEventListener('submit', async function(event) {
        // Prevent form submission
        event.preventDefault();
      
        // Get user input
        const input = inputField.value;
        const site = siteField.value;
        const customer = customerField.value;
        const chatbot_id = chatbotField.value;

        govchat.site = site;
        govchat.customer = customer;
        govchat.chatbot_id = chatbot_id;
      
        // Clear input field
        inputField.value = '';
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });
      
        // Add user input to conversation
        let message = document.createElement('div');
        message.classList.add('chatbot-message', 'user-message');
        message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${input}</p>`;
        conversation.appendChild(message);
      
        // Generate chatbot response
    
        const response = await govchat.chat(input);
      
        
      
        // Add chatbot response to conversation
        message = document.createElement('div');
        message.classList.add('chatbot-message','chatbot');
        message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${response.message}</p>`;
        conversation.appendChild(message);
        message.scrollIntoView({behavior: "smooth"});
      });
})

window.addEventListener('load',function(event){

});

