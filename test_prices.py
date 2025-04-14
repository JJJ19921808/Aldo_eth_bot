from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

symbols = ['ETHUSDT', 'BTCUSDT', 'BNBUSDT']

for symbol in symbols:
    ticker = client.get_symbol_ticker(symbol=symbol)
    print(f"{symbol}: {ticker['price']}")
