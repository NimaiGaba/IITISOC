 document.querySelectorAll('nav a').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        window.scrollTo({
          top: targetSection.offsetTop,
          behavior: 'smooth'
        });
      });
    });
    
   
    document.querySelectorAll('.feature-card').forEach((card, index) => {
      card.style.transitionDelay = `${index * 0.1}s`;
    });
    
    
    function resizeVideo() {
      const video = document.querySelector('.video-bg');
      const aspectRatio = 16/9;
      
      if (window.innerWidth / window.innerHeight > aspectRatio) {
        video.style.width = '100%';
        video.style.height = 'auto';
      } else {
        video.style.width = 'auto';
        video.style.height = '100%';
      }
    }
    
     function toggleChat() {
      const chat = document.getElementById('chatWindow');
      chat.style.display = chat.style.display === 'flex' ? 'none' : 'flex';
    }

    async function sendMessage() {
  const input = document.getElementById('userInput');
  const chatBody = document.getElementById('chatBody');
  const typingIndicator = document.getElementById('typingIndicator');

  const message = input.value.trim();
  if (message === '') return;

  // Show user message
  const userMsg = document.createElement('p');
  userMsg.innerHTML = `<strong>You:</strong> ${message}`;
  chatBody.appendChild(userMsg);
  input.value = '';
  chatBody.scrollTop = chatBody.scrollHeight;

  // Show typing indicator
  typingIndicator.style.display = 'block';

  try {
    const response = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    console.log("✅ Server response:", data); // Add this line for debugging

    typingIndicator.style.display = 'none';

    const botMsg = document.createElement('p');
    if (data.reply) {
      botMsg.innerHTML = `<strong>Bot:</strong> ${data.reply}`;
    } else {
      botMsg.innerHTML = `<strong>Bot:</strong> ⚠️ Unexpected server response.`;
    }

    chatBody.appendChild(botMsg);
    chatBody.scrollTop = chatBody.scrollHeight;

  } catch (error) {
    typingIndicator.style.display = 'none';
    const errorMsg = document.createElement('p');
    errorMsg.innerHTML = `<strong>Bot:</strong> ❌ Server error. Try again later.`;
    chatBody.appendChild(errorMsg);
    chatBody.scrollTop = chatBody.scrollHeight;
    console.error('❌ Fetch error:', error);
  }
}


    window.addEventListener('load', resizeVideo);
    window.addEventListener('resize', resizeVideo);