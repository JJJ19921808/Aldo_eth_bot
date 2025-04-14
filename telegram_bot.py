import requests
import config

TOKEN = "7801328841: AAGqAhfQ20UP5NrP_dCsoVphzbIQMp4cjsI"
URL = "https://api.telegram.org/bot" + TOKEN + "/"


CHAT_ID = "6752022543"


def send_message(text):
    url = URL + "sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, params=params)
    return response.json()
