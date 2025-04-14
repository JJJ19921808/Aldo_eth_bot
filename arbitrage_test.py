import sys
sys.path.insert(0, '/Users/user/Desktop/Arbitrage_Test')

import config
from binance.client import Client
import time
import requests

client = Client(config.API_KEY_BTC, config.API_SECRET_BTC)

def get_prices():
    """ Retrieve current market price for ETH/BTC -> BTC/USDT -> USDT/ETH """
    btc_eth = float(client.get_symbol_ticker(symbol="ETHBTC")['price'])
    btc_usdt = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
    usdt_eth = float(client.get_symbol_ticker(symbol="ETHUSDT")['price'])
    return btc_eth, btc_usdt, usdt_eth

def calculate_arbitrage(eth_btc, btc_usdt, eth_usdt):
    """ Calculate arbitrage potential for ETH -> BTC -> USDT -> ETH """
    start_eth = 1
    fee = 0.001

    btc = start_eth * eth_btc * (1 - fee) # ✅ ETH -> BTC
    usdt = btc * btc_usdt * (1 - fee) # ✅ BTC -> USDT
    final_eth = usdt / eth_usdt * (1 - fee) # ✅ USDT -> ETH
    
    profitability = (final_eth - start_eth) * 100

    print(f"DEBUG: USDT = {usdt:.6f}, BTC = {btc:.6f}, Final ETH = {final_eth:.6f}")

    if final_eth == 0:
        print(" ERROR: Final ETH is 0! Skiping this calculation.")
        return "Error: Final ETH is 0"
    
    return final_eth, profitability

def send_telegram_message(message):
    """ Send a message to Telegram """
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message}
    
    response = requests.post(url, params=params)

    if response.status_code == 200:
        print(f"✅ Message sent to Telegram")
    else:
        print(f"❌ Failed to send message: {response.text}")

def main():
    print("🚀 Arbitrage bot started!")

    while True:
        btc_eth, btc_usdt, usdt_eth = get_prices()
        final_eth, profitability = calculate_arbitrage(btc_eth, btc_usdt, usdt_eth)

        start_eth = 1


        if abs(final_eth - start_eth) /start_eth > 2:
            print(f"⚠️ Anomaly detected! Skipping message.")
            print(f"Expected ~1 ETH, but got {final_eth:.6f} ETH ({profitability:.4f}%)")
            time.sleep(120)
            continue

        send_telegram_message(f"✅ Arbitrage opportunity detected! Profitability: {profitability:.2f}%")
        time.sleep(60)


main()
