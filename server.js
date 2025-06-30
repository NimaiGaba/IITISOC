const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));


dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());

// Add this route:
app.get('/stock', async (req, res) => {
    const symbol = req.query.symbol;
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${process.env.API_KEY}`;
  
    try {
      const response = await fetch(url);
      const data = await response.json();
      res.json(data);
    } catch (err) {
      res.status(500).json({ error: 'Something went wrong' });
    }
  });  

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
