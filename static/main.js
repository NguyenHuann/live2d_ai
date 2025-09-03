const $msg = document.getElementById('msg');
const $send = document.getElementById('send');
const $list = document.getElementById('messages');
const $voice = document.getElementById('voice');

function pushMessage(text, who) {
  const div = document.createElement('div');
  div.className = `msg ${who}`;
  div.textContent = text;
  $list.appendChild(div);
  $list.scrollTop = $list.scrollHeight;
}

async function send() {
  const text = $msg.value.trim();
  if (!text) return;
  $msg.value = '';
  pushMessage(text, 'user');

  $send.disabled = true;
  try {
    const res = await fetch(`${window.location.origin}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || res.statusText);

    pushMessage(data.text, 'ai');
    $voice.src = data.audio_url; // mp3
    await $voice.play().catch(()=>{});
  } catch(e) {
    pushMessage('Lỗi: '+e.message, 'ai');
  } finally {
    $send.disabled = false;
    $msg.focus();
  }
}

$send.addEventListener('click', send);
$msg.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
