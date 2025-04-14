from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

try:
    account_info = client.get_account()
    print(account_info)
except Exception as e:
    print(f"Error: {e}")
