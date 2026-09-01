import sys
import json
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

token = "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk"

print("=" * 50)
print("🔍 ПОЛНЫЙ АУДИТ СИСТЕМЫ И ПРОВЕРКА БАЛАНСА")
print("=" * 50)

# 1. Bot Health
try:
    me = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10).json()
    if me.get("ok"):
        bot_res = me["result"]
        print(f"🤖 БОТ: @{bot_res.get('username')} [{bot_res.get('first_name')}] — АКТИВЕН И ОНЛАЙН ✅")
    else:
        print(f"❌ Ошибка бота: {me}")
except Exception as e:
    print(f"❌ Исключение при проверке бота: {e}")

# 2. Telegram Stars Transactions
try:
    stars = requests.get(f"https://api.telegram.org/bot{token}/getMyStarTransactions", timeout=10).json()
    print("\n💰 ТРАНЗАКЦИИ TELEGRAM STARS:")
    if stars.get("ok"):
        transactions = stars.get("result", {}).get("transactions", [])
        print(f"📊 Всего транзакций: {len(transactions)}")
        total_stars = 0
        for tx in transactions:
            amount = tx.get("amount", 0)
            total_stars += amount
            print(f"  ⭐ Транзакция: {amount} Stars | ID: {tx.get('id')}")
        print(f"💵 ИТОГОВЫЙ БАЛАНС STARS: {total_stars} ⭐ (≈ {total_stars * 1.5:.2f} ₽)")
    else:
        print(f"Ответ Stars API: {stars.get('description')}")
except Exception as e:
    print(f"❌ Исключение при проверке Stars: {e}")

# 3. Channels Audit
channels = [
    {"id": "@aipulse_daily_global", "name": "AI Pulse Daily"},
    {"id": "@remotetech_jobs_global", "name": "Remote Tech Jobs Daily"}
]

print("\n📢 СОСТОЯНИЕ КАНАЛОВ:")
for ch in channels:
    try:
        cnt_res = requests.get(f"https://api.telegram.org/bot{token}/getChatMemberCount?chat_id={ch['id']}", timeout=10).json()
        chat_res = requests.get(f"https://api.telegram.org/bot{token}/getChat?chat_id={ch['id']}", timeout=10).json()
        if chat_res.get("ok"):
            title = chat_res["result"].get("title")
            members = cnt_res.get("result", 0)
            print(f"  ✅ Канал: {title} ({ch['id']}) | Подписчиков: {members}")
        else:
            print(f"  ⚠️ Канал {ch['name']}: {chat_res.get('description')}")
    except Exception as e:
        print(f"  ❌ Ошибка проверки {ch['name']}: {e}")

# 4. GitHub Pages Mini App Health
print("\n🌐 СОСТОЯНИЕ ИГРЫ И ХОСТИНГА (GITHUB PAGES):")
try:
    r = requests.get("https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/", timeout=10)
    if r.status_code == 200:
        print("  ✅ Игра Lucky Wheel Stars доступна по всему миру (200 OK)")
        print(f"  📦 Размер страницы: {len(r.text)} байт")
    else:
        print(f"  ⚠️ Статус хостинга: {r.status_code}")
except Exception as e:
    print(f"  ❌ Ошибка подключения к GitHub Pages: {e}")

print("=" * 50)
