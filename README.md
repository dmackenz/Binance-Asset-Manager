# Binance-Automated-Trading-Client
This is an extension of binance-python library to automatically calculate Binance API filter restrictions and trade any trading pair. Given an API key and API secret, this library will automatically move all of your holdings in one currency to another currency on Binance. This library does all of the complex filters required for the Binance API in the background and boils the code down to a simple buy() and sell() method.

```python
from keys import api_key, api_secret
base_currency = 'USDT'
coin_currency = 'BTC'

bh = BinanceHelper.BinanceHelper(api_key, api_secret, base_currency, coin_currency)

# Automatically calculate step size, tick size, float precision and balance to work with API filters.

# Decide to sell.
if SELL:
  
  # Sell entire holding of coin_currency into base_currency.
  bh.sell()

# Decide to buy.
else:

  # transfer entire holding of base_currency into coin_currency.
  bh.buy()
```
