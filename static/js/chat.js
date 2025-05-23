const chatContainer = document.getElementById('chat-container');

function appendMessage(who, text) {
  const div = document.createElement('div');
  div.className = who;
  div.textContent = text;
  chatContainer.appendChild(div);
}

async function sendMessage(text) {
  appendMessage('user', text);
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({message: text})
  });
  const data = await res.json();
  const reply = data.choices[0].message.content;
  appendMessage('bot', reply);
}

// inicializa chat simples
appendMessage('bot', 'Olá! Como posso ajudar?');

chatContainer.addEventListener('click', () => {
  const text = prompt('Digite sua pergunta:');
  if (text) sendMessage(text);
});
