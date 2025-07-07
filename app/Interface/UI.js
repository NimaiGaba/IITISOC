let currentNewsPage = 1;
const newsPerPage = 10; // Number of news items to load per request

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
          const res = await fetch('https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&outputsize=30&apikey=1901c3f6f2a547989034900aa84a2aa6 '); // Replace with your real API URL
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
// Update the loadTopStories function
async function loadTopStories(page = 1, limit = 10) {
  try {
    const response = await fetch(`http://localhost:5000/api/news?page=${page}&limit=${limit}`);
    const stories = await response.json();
    
    const storiesContainer = document.getElementById('storiesContent');
    
    if (page === 1) {
      storiesContainer.innerHTML = '';
    }
    
    stories.forEach(story => {
      const timeAgo = formatTimeAgo(new Date(story.publishedAt));
      const ticker = story.ticker || 'GEN';
      
      const storyEl = document.createElement('div');
      storyEl.className = 'story-card p-4 mb-4 rounded-lg bg-gray-800 hover:bg-gray-700 transition cursor-pointer';
      storyEl.innerHTML = `
        <div class="flex flex-col sm:flex-row gap-4">
          <img src="${story.imageUrl || 'https://via.placeholder.com/150'}"
              alt="news image"
              class="w-full sm:w-48 h-32 object-cover rounded-lg mb-2 sm:mb-0">
          <div class="flex flex-col justify-between">
            <div>
              <div class="flex justify-between items-start mb-2">
                <span class="text-xs text-gray-400">${timeAgo}</span>
                <span class="text-xs font-semibold bg-blue-500 px-2 py-1 rounded">${ticker}</span>
              </div>
              <h3 class="text-lg font-semibold mb-2">${story.title}</h3>
              <p class="text-sm text-gray-300 mb-2">${story.description || ''}</p>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-xs text-gray-400">${story.source}</span>
              <a href="${story.url}" target="_blank" class="text-xs text-blue-400 hover:underline">Read more</a>
            </div>
          </div>
        </div>
      `;
      storiesContainer.appendChild(storyEl);
    });

    // Hide load more button if we've reached the end
    if (stories.length < limit) {
      document.getElementById('loadMoreStoriesBtn').style.display = 'none';
    }
  } catch (error) {
    console.error('Error loading stories:', error);
  }
}
  function formatTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) return `${interval} year${interval === 1 ? '' : 's'} ago`;
    
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) return `${interval} month${interval === 1 ? '' : 's'} ago`;
    
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) return `${interval} day${interval === 1 ? '' : 's'} ago`;
    
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) return `${interval} hour${interval === 1 ? '' : 's'} ago`;
    
    interval = Math.floor(seconds / 60);
    if (interval >= 1) return `${interval} minute${interval === 1 ? '' : 's'} ago`;
    
    return `${Math.floor(seconds)} second${seconds === 1 ? '' : 's'} ago`;
  }

  function extractTicker(title) {
    const tickerPattern = /[A-Z]{2,5}/g;
    const matches = title.match(tickerPattern);
    return matches ? matches[0] : null;
  }

  // Update showSection function
  function showSection(sectionId) {
    const sections = ['charting', 'portfolio', 'screener', 'technical', 'stories'];
    sections.forEach(id => {
      document.getElementById(id).classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');

    if (sectionId === 'portfolio') loadPortfolio();
    if (sectionId === 'charting') loadTradingViewWidget();
    if (sectionId === 'stories') loadTopStories();
  }
  
  document.getElementById('loadMoreStoriesBtn').addEventListener('click', () => {
  currentNewsPage++;
  loadTopStories(currentNewsPage);
});
