from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

# Получаем актуальные цены
eth_btc = float(client.get_symbol_ticker(symbol="ETHBTC")['price'])
btc_usdt = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
usdt_eth = float(client.get_symbol_ticker(symbol="ETHUSDT")['price'])

# Рассчитываем разницу цен (спред)
price_diff_1 = eth_btc * btc_usdt - usdt_eth  # ETH → BTC → USDT → ETH

# Выводим результаты
print("Price Differences:")
print(f"ETH → BTC → USDT → ETH: {price_diff_1}")
