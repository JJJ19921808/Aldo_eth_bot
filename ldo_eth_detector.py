from datetime import datetime, timedelta
from binance.client import Client
import requests
import time
import json
import os

# --- Telegram настройки ---
TELEGRAM_TOKEN = '7673652206:AAFs_DskOSnKbbyIVzrJaDbgDekGc6J-4fg'
TELEGRAM_CHAT_ID = '6752022543'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"[DEBUG] Ошибка отправки в Telegram: {e}")

# --- Настройки пользователя ---
API_KEY = 'hwuEm34PVxuPYpE6HR1vUvq5RM2AvMcXujKT9nOYCH7dOIZsAyvfC4Dgf2keunK2'
API_SECRET = '7gyJENr8oALGCE8xIQ7i6BeY9hbuQNTRNnrE5rE1hb4aEaQqLBa2BnZ3NI4tK1rC'
ETHERSCAN_API_KEY = 'HBN5MZNIDRI72CTXGEVU57X63RKWYQE2D9'
SYMBOL_LDO = 'LDOUSDT'
SYMBOL_ETH = 'ETHUSDT'
SYMBOL_BTC = 'BTCUSDT'
TIMEFRAME = Client.KLINE_INTERVAL_15MINUTE
THRESHOLD_LDO = 3
ALERT_THRESHOLD = 1.5
SLEEP_INTERVAL = 60 * 5

client = Client(API_KEY, API_SECRET)

# --- TVL Lido ---
def get_lido_tvl_change():
    try:
        url = "https://api.llama.fi/v2/historicalChainTvl/Ethereum?protocol=lido"
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) >= 2:
            tvl_today = data[-1]["totalLiquidityUSD"]
            tvl_yesterday = data[-2]["totalLiquidityUSD"]
            change = ((tvl_today - tvl_yesterday) / tvl_yesterday) * 100
            return round(change, 2)
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении TVL Lido: {e}")
    return None

# --- TVL Ethereum ---
def get_ethereum_tvl_change():
    try:
        url = "https://api.llama.fi/v2/historicalChainTvl/Ethereum"
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) >= 2:
            tvl_today = data[-1]["tvl"]
            tvl_yesterday = data[-2]["tvl"]
            change = ((tvl_today - tvl_yesterday) / tvl_yesterday) * 100
            return round(change, 2)
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении TVL Ethereum: {e}")
    return None

# --- Gas Oracle ---
def get_gas_oracle():
    try:
        url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        data = response.json()
        result = data["result"]
        safe = round(float(result["SafeGasPrice"]))
        propose = round(float(result["ProposeGasPrice"]))
        fast = round(float(result["FastGasPrice"]))
        return safe, propose, fast
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении gas oracle: {e}")
        return None, None, None

# --- Beaconcha.in - застейканный ETH ---
def get_staking_eth():
    try:
        url = "https://beaconcha.in/api/v1/epoch/latest"
        response = requests.get(url, timeout=10)
        data = response.json()
        balance_gwei = data["data"]["totalvalidatorbalance"]
        staked_eth = int(balance_gwei) / 1e9
        return round(staked_eth, 2)
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении данных стейкинга: {e}")
        return None

# --- Сравнение и сохранение staking ---
def compare_and_store_staking(staked_eth, filepath="staking_eth.json"):
    try:
        delta_text = ""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                prev_data = json.load(f)
                prev_value = prev_data.get("staked_eth")
                if prev_value is not None:
                    delta = round(staked_eth - prev_value, 2)
                    arrow = "↑" if delta > 0 else "↓" if delta < 0 else "→"
                    delta_text = f"Δ staking: {arrow} {abs(delta):,.2f} ETH"
        with open(filepath, "w") as f:
            json.dump({"staked_eth": staked_eth}, f)
        return delta_text
    except Exception as e:
        print(f"[DEBUG] Ошибка при сравнении staking ETH: {e}")
        return ""

# --- Основной цикл ---
def main_loop():
    prev_propose = None
    next_alert_time = datetime.now()
    next_heartbeat_time = datetime.now()

    while True:
        now = datetime.now()

        try:
            klines_ldo = client.get_klines(symbol=SYMBOL_LDO, interval=TIMEFRAME, limit=2)
            klines_eth = client.get_klines(symbol=SYMBOL_ETH, interval=TIMEFRAME, limit=2)

            open_ldo = float(klines_ldo[0][1])
            close_ldo = float(klines_ldo[-1][4])
            ldo_change = round(((close_ldo - open_ldo) / open_ldo) * 100, 2)

            open_eth = float(klines_eth[0][1])
            close_eth = float(klines_eth[-1][4])
            eth_change = round(((close_eth - open_eth) / open_eth) * 100, 2)

            eth_price = float(client.get_symbol_ticker(symbol=SYMBOL_ETH)['price'])
            btc_price = float(client.get_symbol_ticker(symbol=SYMBOL_BTC)['price'])
            eth_btc_ratio = round(eth_price / btc_price, 4)

            tvl_lido_change = get_lido_tvl_change()
            tvl_eth_change = get_ethereum_tvl_change()
            staked_eth = get_staking_eth()
            safe, propose, fast = get_gas_oracle()
            staking_delta = compare_and_store_staking(staked_eth) if staked_eth else ""

            # --- Heartbeat раз в час ---
            if now >= next_heartbeat_time:
                report = f"""<b>LDO/ETH Мониторинг</b>

LDO: {close_ldo:.4f} | ETH: ${close_eth:.2f}
LDO/ETH Δ: {ldo_change}% | ETH Δ: {eth_change}%
ETH/BTC: {eth_btc_ratio}

TVL Lido Δ (24h): {tvl_lido_change}%
TVL ETH Δ (24h): {tvl_eth_change}%

Staked ETH: {staked_eth} ETH
{staking_delta}

Gas: Safe={safe}, Propose={propose}, Fast={fast}"""
                send_telegram_message(report)
                next_heartbeat_time = now + timedelta(minutes=60)

            # --- Алерт не чаще 1 раза в 15 минут ---
            ldo_eth_ratio_delta = round(ldo_change - eth_change, 2)
            if ldo_eth_ratio_delta >= ALERT_THRESHOLD and now >= next_alert_time:
                send_telegram_message(f"⚠️ ALERT: LDO/ETH вырос на {ldo_eth_ratio_delta:.2f}% — возможен отрыв от ETH!")
                next_alert_time = now + timedelta(minutes=15)

        except Exception as e:
            print(f"[DEBUG] Ошибка в основном цикле: {e}")

        time.sleep(SLEEP_INTERVAL)

# --- Запуск ---
if __name__ == "__main__":
    send_telegram_message("Тестовая отправка: бот успешно подключён.")
    main_loop()
