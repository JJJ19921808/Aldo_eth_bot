from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

print(client.get_system_status())

balance = client.get_asset_balance(asset="USDT")
print("Баланс USDT:", balance)

eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
print("ETH/USDT:", eth_price["price"])
