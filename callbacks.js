<script>
function openChatbot() { document.getElementById('chatbot-ui').style.display = 'block';
}
function sendMessage() {
const userInput = document.getElementById('user-input').value; if (userInput.trim() !== '') {
const chatMessages = document.getElementById('chat-messages'); chatMessages.innerHTML += `<div>You: ${userInput}</div>`;
fetch('/chatbot', { method: 'POST',
headers: {
Content-Type': 'application/json'
},
body: JSON.stringify({ query: userInput }) })
.then(response => response.json()) .then(data => {
chatMessages.innerHTML += `<div>Chatbot: ${data.response}</div>`; })
.catch(error => { console.error('Error:', error);
});
document.getElementById('user-input').value = ' ';
} }
</script>