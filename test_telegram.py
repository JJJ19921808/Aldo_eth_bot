import requests
import config

url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
params = {"chat_id": config.TELEGRAM_CHAT_ID, "text": "Test message from bot"}
response = requests.post(url, params=params)

print(response.json())  # Должен вернуть {"ok": true, "result": ...}
