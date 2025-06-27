const getStockData = async (symbol) => {
    const apiKey = 'V58TM3U6VLJ5H4PM'; 
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${apiKey}`;
  
    try {
      const res = await fetch(url);
      const data = await res.json();
  
      if (data['Time Series (Daily)']) {
        const latestDate = Object.keys(data['Time Series (Daily)'])[0];
        const latestData = data['Time Series (Daily)'][latestDate];
        document.getElementById('stock-output').textContent =
          ` ${symbol.toUpperCase()}: ₹${latestData['4. close']}`;
      } else {
        document.getElementById('stock-output').textContent =
          'Symbol not found or API limit exceeded ';
      }
    } catch (err) {
      console.error(err);
      alert("Error fetching stock data ");
    }
  };

  document.getElementById('get-stock-btn').addEventListener('click', () => {
    console.log("Button clicked!");
    const symbol = document.getElementById('symbol-input').value.trim().toUpperCase();
    if (symbol) {
      getStockData(symbol);
    } else {
      alert('Enter a stock symbol!');
    }
  });
  