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
     document.getElementById('userInput').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
          event.preventDefault(); // Prevents default behavior like adding a new line
          sendMessage();
        }
      });

      async function loadPortfolio() {
        try {
          const res = await fetch('https://api.https://s3.tradingview.com/tv.js.com/portfolio'); // Replace with your real API URL
          const data = await res.json();

          const table = document.getElementById('portfolioTable');
          const totalBalanceElem = document.getElementById('totalBalance');
          const totalPnLElem = document.getElementById('totalPnL');

          let totalBalance = 0;
          let totalPnL = 0;

          table.innerHTML = ""; // Clear previous rows

          data.forEach((item, index) => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-gray-700 transition';

            const profitLoss = (item.livePrice - item.priceAtTransaction) * item.quantity;
            totalBalance += item.livePrice * item.quantity;
            totalPnL += profitLoss;

            row.innerHTML = `
              <td class="p-3">${index + 1}</td>
              <td class="p-3 text-blue-400">${item.symbol}</td>
              <td class="p-3">${item.name}</td>
              <td class="p-3">${item.orderType}</td>
              <td class="p-3">${item.orderMode}</td>
              <td class="p-3">${item.quantity}</td>
              <td class="p-3">$${item.priceAtTransaction.toFixed(2)}</td>
              <td class="p-3 text-green-400">$${item.livePrice.toFixed(2)}</td>
              <td class="p-3 text-${profitLoss >= 0 ? 'green' : 'red'}-400">$${profitLoss.toFixed(2)}</td>
              <td class="p-3">${item.datetime}</td>
            `;

            table.appendChild(row);
          });

          totalBalanceElem.textContent = `$${totalBalance.toFixed(2)}`;
          totalPnLElem.textContent = `$${totalPnL.toFixed(2)}`;
          totalPnLElem.className = totalPnL >= 0 ? 'text-green-400' : 'text-red-400';
        } catch (err) {
          console.error('Error loading portfolio data:', err);
        }
      }

      function showSection(sectionId) {
        const sections = ['charting', 'portfolio', 'screener', 'technical', 'stories'];
        sections.forEach(id => {
          document.getElementById(id).classList.add('hidden');
        });
        document.getElementById(sectionId).classList.remove('hidden');

        if (sectionId === 'portfolio') loadPortfolio();
        if (sectionId === 'charting') loadTradingViewWidget();
      }    