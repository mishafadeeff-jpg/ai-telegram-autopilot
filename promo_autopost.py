import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk")
WEB_APP_URL = "https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/"
BANNER_PATH = os.path.join(os.path.dirname(__file__), "promo_banner.jpg")

TARGETS = [
    {"id": -1003717035094, "name": "AI Pulse Daily (@aipulse_daily_global)"},
    {"id": -1004485345052, "name": "Remote Tech Jobs Daily (@remotetech_jobs_global)"},
    {"id": 860392517, "name": "Misha (@MigOdin) Личные сообщения"}
]

CAPTION = (
    "🎰 <b>ГРАНДИОЗНЫЙ РОЗЫГРЫШ: КОЛЕСО ФОРТУНЫ!</b> 🎡🔥\n\n"
    "Не упустите шанс забрать ценные призы прямо в Telegram:\n\n"
    "👑 <b>Telegram Premium на 3 месяца</b>\n"
    "🌟 <b>Золотой Джекпот +1,000 Telegram Stars ⭐</b>\n"
    "🎟️ <b>Золотые Билеты на Еженедельный Супер-Куш</b>\n"
    "💎 <b>Секретные Боксы и Моментальные Звёзды</b>\n\n"
    "🎁 <b>1-я БЕСПЛАТНАЯ КРУТКА ДОСТУПНА ВСЕМ!</b>\n"
    "Нажмите на кнопку ниже и крутите прямо сейчас 👇"
)

REPLY_MARKUP = {
    "inline_keyboard": [
        [
            {
                "text": "🎰 Испытать удачу (Крутить Бесплатно) 🎡",
                "url": WEB_APP_URL
            }
        ]
    ]
}

def post_promo():
    print("=== Запуск публикации сочного рекламного баннера во все каналы ===")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    for t in TARGETS:
        try:
            with open(BANNER_PATH, "rb") as photo_file:
                files = {"photo": photo_file}
                data = {
                    "chat_id": t["id"],
                    "caption": CAPTION,
                    "parse_mode": "HTML",
                    "reply_markup": requests.compat.json.dumps(REPLY_MARKUP)
                }
                resp = requests.post(url, data=data, files=files, timeout=20)
                res_json = resp.json()
                if res_json.get("ok"):
                    print(f"✅ Рекламный баннер успешно отправлен в: {t['name']}")
                else:
                    print(f"❌ Ошибка отправки в {t['name']}: {res_json.get('description')}")
        except Exception as e:
            print(f"⚠️ Ошибка при отправке в {t['name']}: {e}")

if __name__ == "__main__":
    post_promo()
