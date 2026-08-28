import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk")
PRIMARY_CHANNEL = os.getenv("TELEGRAM_CHANNEL_ID", "@aipulse_daily_global")
JOBS_CHANNEL = os.getenv("JOBS_CHANNEL_ID", "")
WEB_APP_URL = "https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/"

CHANNELS_TO_BROADCAST = [PRIMARY_CHANNEL]
if JOBS_CHANNEL and JOBS_CHANNEL.strip():
    CHANNELS_TO_BROADCAST.append(JOBS_CHANNEL.strip())

POST_TEXT = (
    "☦️ <b>У каждого свой крест...</b>\n\n"
    "<i>«Но с любовью, верой и поддержкой мы сможем донести его до самой вершины.»</i>\n\n"
    "🕊️ <b>Интерактивный путь веры:</b>\n"
    "Каждое доброе пожертвование в Telegram Stars оживляет историю, облегчает ношу путника и открывает слова личного благословения батюшки.\n\n"
    "⭐ <b>Поддержите сбор и откройте живую игру прямо в Telegram:</b>"
)

REPLY_MARKUP = {
    "inline_keyboard": [
        [
            {
                "text": "☦️ Открыть путь веры и поддержать ⭐",
                "url": WEB_APP_URL
            }
        ]
    ]
}

def broadcast():
    print(f"Starting broadcast to {len(CHANNELS_TO_BROADCAST)} channel(s)...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    for ch in CHANNELS_TO_BROADCAST:
        payload = {
            "chat_id": ch,
            "text": POST_TEXT,
            "parse_mode": "HTML",
            "reply_markup": REPLY_MARKUP
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            res_json = resp.json()
            if res_json.get("ok"):
                print(f"✅ Successfully sent to channel: {ch}")
            else:
                print(f"❌ Failed to send to {ch}: {res_json.get('description')}")
        except Exception as e:
            print(f"⚠️ Network error while sending to {ch}: {e}")

if __name__ == "__main__":
    broadcast()
