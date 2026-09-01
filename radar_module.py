import random
import datetime

SAMPLE_DEALS = [
    {
        "category": "Apple & Гаджеты 📱",
        "title": "iPhone 15 Pro Max 256GB (Идеальное состояние)",
        "market_price": 115000,
        "deal_price": 72000,
        "discount_percent": 37,
        "location": "Москва / Доставка",
        "profit": 43000
    },
    {
        "category": "Авто / Перепродажа 🚗",
        "title": "Toyota Camry 2.5 AT (2020, 1 владелец, срочная продажа)",
        "market_price": 2700000,
        "deal_price": 2050000,
        "discount_percent": 24,
        "location": "Санкт-Петербург",
        "profit": 650000
    },
    {
        "category": "Ноутбуки & Рабочие станции 💻",
        "title": "MacBook Pro 16 M3 Max 36GB / 1TB SSD",
        "market_price": 310000,
        "deal_price": 210000,
        "discount_percent": 32,
        "location": "Казань / СДЭК",
        "profit": 100000
    }
]

def scan_hot_deals() -> list:
    deals = []
    for d in SAMPLE_DEALS:
        deal_copy = d.copy()
        deal_copy["found_at"] = (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 15))).strftime("%H:%M")
        deals.append(deal_copy)
    return deals

def format_deal_alert(deal: dict) -> str:
    return (
        f"🚨 <b>ГОРЯЧИЙ ЛОТ С ДИСКОНТОМ -{deal['discount_percent']}%!</b>\n\n"
        f"📦 <b>Товар:</b> {deal['title']}\n"
        f"🏷️ <b>Категория:</b> {deal['category']}\n"
        f"💰 <b>Цена продавца:</b> <b>{deal['deal_price']:,} ₽</b> (Рыночная: {deal['market_price']:,} ₽)\n"
        f"💵 <b>Потенциальная выгода:</b> <b>+{deal['profit']:,} ₽</b>\n"
        f"📍 <b>Локация:</b> {deal['location']} (Найдено: {deal['found_at']})\n\n"
        f"👉 <a href=\"https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/\"><b>Открыть контакт продавца в Радаре →</b></a>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Подпишитесь на VIP-Радар для моментальных уведомлений в секунду публикации!</i>"
    )

if __name__ == "__main__":
    deals = scan_hot_deals()
    print("=== ТЕСТ AI-РАДАРА ВЫГОДНЫХ СДЕЛОК ===")
    print(format_deal_alert(deals[0]))
