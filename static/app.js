const form = document.getElementById('chatForm');
const input = document.getElementById('messageInput');
const chat = document.getElementById('chat');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

function addMessage(role, text) {
  const article = document.createElement('article');
  article.className = `message ${role}`;

  if (role === 'assistant') {
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = 'N';
    article.appendChild(avatar);
  }

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  article.appendChild(bubble);
  chat.appendChild(article);
  chat.scrollTop = chat.scrollHeight;
  return article;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage('user', message);
  input.value = '';
  sendBtn.disabled = true;
  const loading = addMessage('assistant', 'Thinking...');

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    loading.remove();
    addMessage('assistant', response.ok ? data.reply : data.error || 'Something went wrong.');
  } catch {
    loading.remove();
    addMessage('assistant', 'I could not connect to the server.');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});

resetBtn.addEventListener('click', async () => {
  await fetch('/api/reset', { method: 'POST' });
  chat.innerHTML = '';
  addMessage('assistant', 'New chat started. What would you like help with?');
});

input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
});
