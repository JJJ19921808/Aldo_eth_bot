from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

symbols = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT']

prices = {}

for symbol in symbols:
    ticker = client.get_symbol_ticker(symbol=symbol)
    prices[symbol] = float(ticker['price'])

print("Price Differences:")
print(f"ETH - BTC: {prices['ETHUSDT'] - prices['BTCUSDT']}")
print(f"BTC - BNB: {prices['BTCUSDT'] - prices['BNBUSDT']}")
print(f"BNB - ETH: {prices['BNBUSDT'] - prices['ETHUSDT']}")
