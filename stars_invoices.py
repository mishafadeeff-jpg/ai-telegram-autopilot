import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk")

# Packages in Telegram Stars (Currency code: XTR)
PACKAGES = {
    "spin_1": {
        "title": "1 Крутка в Колесе Фортуны",
        "description": "Попытка выиграть Telegram Premium и 1,000 Stars",
        "stars": 50,
        "spins": 1
    },
    "spin_5": {
        "title": "5 Круток в Колесе Фортуны (-20%)",
        "description": "Выгодный пакет: 5 попыток со скидкой 20%",
        "stars": 200,
        "spins": 5
    },
    "spin_15": {
        "title": "15 Круток VIP в Колесе Фортуны",
        "description": "VIP пакет: 15 попыток с максимальным шансом на джекпот",
        "stars": 500,
        "spins": 15
    }
}

def create_stars_invoice(package_key):
    pkg = PACKAGES.get(package_key)
    if not pkg:
        return None

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/createInvoiceLink"
    payload = {
        "title": pkg["title"],
        "description": pkg["description"],
        "payload": f"order_{package_key}",
        "currency": "XTR",  # OFFICIAL TELEGRAM STARS CURRENCY CODE
        "prices": [
            {"label": pkg["title"], "amount": pkg["stars"]} # Amount in Stars
        ]
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        res_json = resp.json()
        if res_json.get("ok"):
            invoice_link = res_json.get("result")
            print(f"✅ Создан официальный инвойс Telegram Stars для [{pkg['title']}]: {invoice_link}")
            return invoice_link
        else:
            print(f"❌ Ошибка создания инвойса для {package_key}:", res_json)
            return None
    except Exception as e:
        print("Network error:", e)
        return None

def generate_all_invoices():
    print("=== Генерация официальных платёжных ссылок Telegram Stars (XTR) ===")
    links = {}
    for key in PACKAGES:
        link = create_stars_invoice(key)
        if link:
            links[key] = link
    return links

if __name__ == "__main__":
    links = generate_all_invoices()
    print("\nГотовые ссылки Telegram Stars:")
    for k, v in links.items():
        print(f"{k}: {v}")
