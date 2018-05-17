import math
from binance.client import Client

class BinanceHelper(object):
    def __init__(self, api_key, api_secret, base_currency, coin_currency):
        self.client = Client(api_key, api_secret)
        self.base_currency = base_currency
        self.coin_currency = coin_currency
        self.symbol = coin_currency + base_currency

    def float_precision(self, f, n):
        n = int(math.log10(1 / float(n)))
        f = math.floor(float(f) * 10 ** n) / 10 ** n
        f = "{:0.0{}f}".format(float(f), n)
        return str(int(f)) if int(n) == 0 else f

    def get_price(self):
        price = None
        tickers = self.client.get_all_tickers()
        for ticker in tickers:
            if ticker['symbol'] == self.symbol:
                price = float(ticker['price'])
        return price

    def get_tick_and_step_size(self):
        tick_size = None
        step_size = None
        symbol_info = self.client.get_symbol_info(self.symbol)
        for filt in symbol_info['filters']:
            if filt['filterType'] == 'PRICE_FILTER':
                tick_size = float(filt['tickSize'])
            elif filt['filterType'] == 'LOT_SIZE':
                step_size = float(filt['stepSize'])
        return tick_size, step_size

    def get_balance(self, currency):
        return float(self.client.get_asset_balance(asset=currency)['free'])

    def get_buy_info(self):
        tick_size, step_size = self.get_tick_and_step_size()
        price = float(self.float_precision(self.get_price(), tick_size))
        coin_currency_quantity = float(self.float_precision(self.get_balance(self.base_currency) / price, step_size))
        return price, coin_currency_quantity

    def get_sell_info(self):
        tick_size, step_size = self.get_tick_and_step_size()
        price = float(self.float_precision(self.get_price(), tick_size))
        coin_currency_quantity = float(self.float_precision(self.get_balance(self.coin_currency), step_size))
        return price, coin_currency_quantity

    def buy(self):
        price, quantity = self.get_buy_info()
        self.client.order_market_buy(symbol=self.symbol, quantity=quantity)

    def sell(self):
        price, quantity = self.get_sell_info()
        self.client.order_market_sell(symbol=self.symbol, quantity=quantity)

