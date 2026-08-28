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
    "☦️ <b>У каждого свой крест...</b>\n\n"
    "<i>«Но с любовью, верой и поддержкой мы сможем донести его до самой вершины.»</i>\n\n"
    "🕊️ <b>Интерактивный путь веры:</b>\n"
    "Каждое доброе пожертвование в Telegram Stars оживляет историю, облегчает ношу путника и открывает слова личного благословения батюшки.\n\n"
    "⭐ <b>Поддержите сбор и откройте живую игру прямо в Telegram:</b>"
)

reply_markup = {
    "inline_keyboard": [
        [
            {
                "text": "☦️ Открыть путь веры и поддержать ⭐",
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
        print(f"✅ Успешно отправлено в: {t['name']}")
    else:
        print(f"❌ Ошибка в {t['name']}: {r.get('description')}")
