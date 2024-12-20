const axios = require('axios');
const { SERVER_URL, SYMBOL, LOT } = require('./config');

// Fungsi untuk mengirim sinyal trading
async function trade(action) {
  try {
    const response = await axios.post(`${SERVER_URL}/trade`, {
      action: action,
      symbol: SYMBOL,
      lot: LOT,
    });
    console.log(response.data);
  } catch (error) {
    console.error('Trade failed:', error.response ? error.response.data : error.message);
  }
}

// Contoh penggunaan
(async () => {
  console.log('Mengirim sinyal beli...');
  await trade('buy');

  console.log('Mengirim sinyal jual...');
  await trade('sell');
})();
