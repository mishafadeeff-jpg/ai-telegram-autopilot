import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "@aipulse_daily_global")
WEB_APP_URL = "https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/"

def send_crowdfund_post():
    text = (
        "☦️ <b>У каждого свой крест...</b>\n\n"
        "<i>«Но с любовью, верой и поддержкой мы сможем донести его до самой вершины.»</i>\n\n"
        "🕊️ <b>Интерактивный путь веры:</b>\n"
        "Каждое доброе пожертвование оживляет историю, облегчает ношу путника и открывает слова личного благословения.\n\n"
        "⭐ <b>Поддержите сбор и откройте живой мультфильм по кнопке ниже:</b>"
    )
    
    reply_markup = {
        "inline_keyboard": [
            [
                {
                    "text": "☦️ Открыть путь веры и поддержать ⭐",
                    "url": WEB_APP_URL
                }
            ]
        ]
    }
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": reply_markup
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        res_json = resp.json()
        if res_json.get("ok"):
            print("Successfully published crowdfund post to Telegram channel!")
        else:
            print("Telegram API response:", res_json)
    except Exception as e:
        print("Error publishing:", e)

if __name__ == "__main__":
    send_crowdfund_post()
