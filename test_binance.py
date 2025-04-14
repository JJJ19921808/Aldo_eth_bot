from binance.client import Client
import config
client = Client(config.API_KEY, config.API_SECRET)
def get_price(symbol):
    try:
        ticker=client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exeption as e:
    print (f"Ошибка при получении {symbol}: {e}")
    return None
eth_usdt = get_price("ETHUSDT")
btc_usdt = get_price("BTCUSDT")
eth_btc = get_price("ETHBTC")
if None in (eth_usdt, btc_usdt, eth_btc):
    print ( "Ошибка получения данных. Завершаем.")
    exit()
    eth_to_btc = eth_btc * (1 - config .FEE)
    btc_to_usdt = eth_to_btc * bto_usdt * (1 - config. FEE)
    usdt_to_eth = btc_to_usdt / eth_usdt * (1 - config. FEE)
    profit = (usdt_toeth - 1) * 100
    eth_to_btc = eth_btc * (1 - config. FEE)
    bc_to_usdt = eth_to_btc * btc_usdt * (1 - config.FEE)
    usdt_to_eth = btc_to_usdt / eth_usdt * (1 - config. FEE)
    profit2 = (usdt_to_eth - 1) * 100
    print(f" \nETH → USDT → BTC → ETH: {profit1:.4f}%")
    print (f"ETH → BTC → USDT → ETH: {profit2:.4f}%")
    if profit1 > 0:
        print（f"ВЫГОДНАЯ ВОЗМОЖНОСТЬ: {profit1:.4f}% (ETH → USDT → ВТС → ЕТН) ")
    if profit2 > 0:
       print（f"ВЫГОДНАЯ ВОЗМОЖНОСТЬ: {profit1:.4f}% (ETH → USDT → ВТС → ЕТН) ") 

    