def get_ldo_dex_volume():
    try:
        # Получаем текущую цену
        url_price = "https://coins.llama.fi/prices/current/ethereum:0x5a98fcbea516cf06857215779fd812ca3bef1b32"
        response = requests.get(url_price)
        response.raise_for_status()
        price = response.json()['coins']['ethereum:0x5a98fcbea516cf06857215779fd812ca3bef1b32']['price']

        # Новый endpoint для объема
        url_vol = "https://coins.llama.fi/summary/ethereum:0x5a98fcbea516cf06857215779fd812ca3bef1b32"
        response_vol = requests.get(url_vol)
        response_vol.raise_for_status()
        data = response_vol.json()

        volume = data["24hVolume"]

        return round(volume, 2), round(price, 4)
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении объёма LDO с DefiLlama: {e}")
        return None, None
