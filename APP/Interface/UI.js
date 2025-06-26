function toggleChat() {
      const chat = document.getElementById('chatWindow');
      chat.style.display = chat.style.display === 'flex' ? 'none' : 'flex';
    }

    function sendMessage() {
      const input = document.getElementById('userInput');
      const chatBody = document.getElementById('chatBody');
      const typingIndicator = document.getElementById('typingIndicator');

      const message = input.value.trim();
      if (message === '') return;

      const userMsg = document.createElement('p');
      userMsg.innerHTML = `<strong>You:</strong> ${message}`;
      chatBody.appendChild(userMsg);
      input.value = '';
      chatBody.scrollTop = chatBody.scrollHeight;

      typingIndicator.style.display = 'block';

      setTimeout(() => {
        typingIndicator.style.display = 'none';
        const botMsg = document.createElement('p');
        botMsg.innerHTML = `<strong>Bot:</strong> Sorry, I'm currently unable to respond.`;
        chatBody.appendChild(botMsg);
        chatBody.scrollTop = chatBody.scrollHeight;
      }, 1500);
    }

    function showSection(sectionId) {
      const sections = ['charting', 'portfolio', 'screener', 'technical', 'stories'];
      sections.forEach(id => {
        document.getElementById(id).classList.add('hidden');
      });
      document.getElementById(sectionId).classList.remove('hidden');
      document.getElementById('stockTable').classList.add('hidden');
    }