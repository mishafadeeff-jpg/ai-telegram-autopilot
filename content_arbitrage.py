import random
from typing import Dict

VIRAL_GLOBAL_TOPICS = [
    {
        "source": "TechCrunch & Silicon Valley Insights",
        "topic": "Как новые AI-агенты заменяют целые отделы маркетинга в США",
        "key_takeaway": "Компании увольняют подрядчиков и подключают одного автономного агента, который генерирует 50 постов в день, тестирует гипотезы и общается с лидами.",
        "actionable_tip": "Внедряйте AI-автоматизацию в Telegram прямо сейчас, пока рынок в СНГ только зарождается."
    },
    {
        "source": "Huberman Biohacking Lab",
        "topic": "Простой утренний протокол для повышения энергии и концентрации на 200%",
        "key_takeaway": "10 минут естественного солнечного света в первый час после пробуждения + 500 мл воды с щепоткой гималайской соли нормализуют кортизол и дофамин.",
        "actionable_tip": "Попробуйте данный протокол в течение 5 дней для полной перезагрузки продуктивности."
    },
    {
        "source": "Wall Street & Crypto Alpha",
        "topic": "Скрытые тренды микроплатежей в Telegram Stars и TON",
        "key_takeaway": "За последние 6 месяцев объём платежей внутри Telegram Mini Apps вырос на 450%. Игры и сервисы с микро-оплатами обгоняют классические сайты.",
        "actionable_tip": "Запускайте свои Mini Apps со встроенным приемом Stars уже сегодня."
    }
]

def generate_adapted_viral_post() -> str:
    item = random.choice(VIRAL_GLOBAL_TOPICS)
    
    post = (
        f"🔥 <b>МИРОВОЙ ТРЕНД: {item['topic'].upper()}</b>\n\n"
        f"🌐 <i>Источник: {item['source']}</i>\n\n"
        f"📌 <b>Главная суть:</b>\n"
        f"{item['key_takeaway']}\n\n"
        f"💡 <b>Практический совет:</b>\n"
        f"{item['actionable_tip']}\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Ежедневная выжимка мировых трендов в канале: <a href=\"https://t.me/aipulse_daily_global\">AI Pulse Daily</a></i>\n"
        f"#Trends #AI #Productivity #GlobalInsights #Future"
    )
    return post

if __name__ == "__main__":
    print("=== ТЕСТ КОНТЕНТ-АРБИТРАЖА ===")
    print(generate_adapted_viral_post())
