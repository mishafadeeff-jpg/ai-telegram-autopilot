import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

token = "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk"
web_app_url = "https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/"

targets = [
    {"id": -1003717035094, "name": "AI Pulse Daily (@aipulse_daily_global)"},
    {"id": -1004485345052, "name": "Remote Tech Jobs Daily (@remotetech_jobs_global)"},
    {"id": 860392517, "name": "Misha (@MigOdin) Личные сообщения"}
]

text = (
    "🎰 <b>ГРАНДИОЗНЫЙ РОЗЫГРЫШ: КОЛЕСО ФОРТУНЫ!</b> 🎡\n\n"
    "Испытайте свою удачу в новом неоновом Telegram-розыгрыше:\n\n"
    "👑 <b>Telegram Premium на 3 месяца</b>\n"
    "🌟 <b>Джекпот +1,000 Telegram Stars ⭐</b>\n"
    "🎟️ <b>Золотые Билеты на Супер-Розыгрыш</b>\n"
    "💎 <b>Звёзды, Секретные Боксы и Призы</b>\n\n"
    "🎁 <b>БЕСПЛАТНАЯ КРУТКА ДОСТУПНА ПРЯМО СЕЙЧАС!</b>\n"
    "Нажмите на кнопку ниже, чтобы запустить Колесо Фортуны 👇"
)

reply_markup = {
    "inline_keyboard": [
        [
            {
                "text": "🎰 Крутить Колесо Фортуны (Бесплатно) 🎡",
                "url": web_app_url
            }
        ]
    ]
}

url = f"https://api.telegram.org/bot{token}/sendMessage"

for t in targets:
    payload = {
        "chat_id": t["id"],
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": reply_markup
    }
    r = requests.post(url, json=payload, timeout=10).json()
    if r.get("ok"):
        print(f"✅ Опубликован розыгрыш в: {t['name']}")
    else:
        print(f"❌ Ошибка в {t['name']}: {r.get('description')}")
