import requests

def get_lido_tvl_change():
    try:
        url = "https://yields.llama.fi/chart/lido?duration=2"
        data = requests.get(url, timeout=10).json()["data"]
        tvl_yesterday = data[-2]["tvl"]
        tvl_today = data[-1]["tvl"]
        change = ((tvl_today - tvl_yesterday) / tvl_yesterday) * 100
        return round(change, 2)
    except Exception as e:
        print("[DEBUG] Ошибка TVL Lido:", e)
        return None

def get_ethereum_tvl_change():
    try:
        url = "https://api.llama.fi/chains"
        chains = requests.get(url, timeout=10).json()
        for chain in chains:
            if chain["name"].lower() == "ethereum":
                return round(chain["change_1d"], 2)
    except Exception as e:
        print("[DEBUG] Ошибка TVL Ethereum:", e)
        return None

print("TVL Lido Δ (24h):", get_lido_tvl_change(), "%")
print("TVL ETH Δ (24h):", get_ethereum_tvl_change(), "%")
