from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

account_info = client.get_account()
balances = account_info['balances']

for asset in balances:
    if asset['asset'] in ['ETH', 'BTC', 'USDT']:
        print(asset)
