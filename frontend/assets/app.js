async function fetchSignals() {
  try {
    const res = await fetch('/api/signals');
    const data = await res.json();
    const box = document.getElementById('signals');
    box.innerHTML = '';
    data.signals.forEach(s => {
      const el = document.createElement('div');
      el.className = 'p-2 border rounded';
      el.innerHTML = `<div class="font-medium">${s.symbol} – ${s.direction}</div>
                      <div>Confidence: ${s.confidence}, Price: ${s.price}</div>`;
      box.appendChild(el);
    });
  } catch (e) {
    console.error(e);
  }
}

async function sendMessage(message) {
  const chat = document.getElementById('chat');
  chat.insertAdjacentHTML('beforeend', `<div class="mb-2"><b>Du:</b> ${message}</div>`);
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message})
    });
    const data = await res.json();
    chat.insertAdjacentHTML('beforeend', `<div class="mb-2"><b>KI:</b> ${data.reply}</div>`);
    chat.scrollTop = chat.scrollHeight;
  } catch (e) {
    chat.insertAdjacentHTML('beforeend', `<div class="mb-2 text-red-600"><b>Fehler:</b> ${e}</div>`);
  }
}

document.getElementById('chatForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  sendMessage(msg);
});

// initial load and refresh every 30s
fetchSignals();
setInterval(fetchSignals, 30000);
