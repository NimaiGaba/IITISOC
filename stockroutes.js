require('dotenv').config();
const express = require('express');
const axios = require('axios');
const router = express.Router();

const API_KEY = process.env.V58TM3U6VLJ5H4PM;

router.get('/stock/:symbol', async (req, res) => {
  const symbol = req.params.symbol;

  try {
    const [candle, sma, ema, macd, rsi] = await Promise.all([
      axios.get(`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&apikey=${API_KEY}`),
      axios.get(`https://www.alphavantage.co/query?function=SMA&symbol=${symbol}&interval=daily&time_period=20&series_type=close&apikey=${API_KEY}`),
      axios.get(`https://www.alphavantage.co/query?function=EMA&symbol=${symbol}&interval=daily&time_period=20&series_type=close&apikey=${API_KEY}`),
      axios.get(`https://www.alphavantage.co/query?function=MACD&symbol=${symbol}&interval=daily&series_type=close&apikey=${API_KEY}`),
      axios.get(`https://www.alphavantage.co/query?function=RSI&symbol=${symbol}&interval=daily&time_period=14&series_type=close&apikey=${API_KEY}`),
    ]);

    res.json({
      candle: candle.data,
      sma: sma.data,
      ema: ema.data,
      macd: macd.data,
      rsi: rsi.data
    });
  } catch (err) {
    res.status(500).json({ error: 'Something went wrong!', details: err.message });
  }
});

module.exports = router;
