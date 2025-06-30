async function fetchData(symbol) {
    const res = await fetch(`http://localhost:5000/stock?symbol=${symbol}`);
    const data = await res.json();
    return data;
  }
  
  function renderChart(candleData) {
    const chart = LightweightCharts.createChart(document.getElementById('chart'), {
      width: 800,
      height: 400,
    });
    const candleSeries = chart.addCandlestickSeries();
    const seriesData = Object.entries(candleData['Time Series (Daily)']).map(([date, values]) => ({
      time: date,
      open: parseFloat(values['1. open']),
      high: parseFloat(values['2. high']),
      low: parseFloat(values['3. low']),
      close: parseFloat(values['4. close'])
    })).reverse();
    candleSeries.setData(seriesData);
  }
  
  (async () => {
    const data = await fetchData('AAPL');
    renderChart(data);
  })();
  