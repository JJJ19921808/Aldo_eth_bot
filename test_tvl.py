import requests

# --- LIDO TVL ---
def get_lido_tvl_change():
    try:
        url = "https://api.llama.fi/protocol/lido"
        response = requests.get(url, timeout=10)
        data = response.json()
        tvl_data = data.get('tvl', [])

        if len(tvl_data) >= 2:
            tvl_today = tvl_data[-1]['totalLiquidityUSD']
            tvl_yesterday = tvl_data[-2]['totalLiquidityUSD']
            change = ((tvl_today - tvl_yesterday) / tvl_yesterday) * 100
            return round(change, 2)
        else:
            print("[DEBUG] Недостаточно данных для расчёта TVL Lido.")
            return None
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении TVL Lido: {e}")
        return None

# --- ETHEREUM TVL ---
def get_ethereum_tvl_change():
    try:
        url = "https://api.llama.fi/v2/historicalChainTvl/Ethereum"
        response = requests.get(url, timeout=10)
        data = response.json()

        if len(data) >= 2:
            tvl_today = data[-1]['tvl']
            tvl_yesterday = data[-2]['tvl']
            change = ((tvl_today - tvl_yesterday) / tvl_yesterday) * 100
            return round(change, 2)
        else:
            print("[DEBUG] Недостаточно данных для расчёта TVL Ethereum.")
            return None
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении TVL Ethereum: {e}")
        return None

# --- Тестовый вывод ---
print("TVL Lido Δ (24h):", get_lido_tvl_change(), "%")
print("TVL Ethereum Δ (24h):", get_ethereum_tvl_change(), "%")
