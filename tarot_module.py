import random
import datetime

TAROT_DECK = [
    {"name": "Шут (The Fool)", "theme": "Новые начинания, смелость, чистый лист", "element": "Воздух"},
    {"name": "Маг (The Magician)", "theme": "Сила воли, ресурсы, реализация желаний", "element": "Огонь"},
    {"name": "Верховная Жрица (High Priestess)", "theme": "Интуиция, скрытые тайны, мудрость", "element": "Вода"},
    {"name": "Императрица (The Empress)", "theme": "Изобилие, рост, плодородие, любовь", "element": "Земля"},
    {"name": "Колесо Фортуны (Wheel of Fortune)", "theme": "Неожиданная удача, поворот судьбы, прорыв", "element": "Огонь"},
    {"name": "Солнце (The Sun)", "theme": "Триумф, радость, материальное процветание", "element": "Огонь"},
    {"name": "Туз Пентаклей (Ace of Pentacles)", "theme": "Большие деньги, подарок судьбы, выгодный контракт", "element": "Земля"},
    {"name": "Влюбленные (The Lovers)", "theme": "Судьбоносный выбор, гармония, глубокие чувства", "element": "Воздух"}
]

ADVICES = [
    "Вселенная открывает перед вами денежный коридор: действуйте решительно в ближайшие 48 часов!",
    "Интуиция подсказывает верный путь. Не сомневайтесь в своих силах — вас ждет финансовый рост.",
    "Отпустите старые сомнения. Человек из вашего окружения принесет выгодное предложение.",
    "Период затишья подошел к концу: сейчас идеальный момент для запуска новых проектов."
]

def generate_tarot_reading(category: str = "Деньги и Успех", user_name: str = "Искатель") -> dict:
    card = random.choice(TAROT_DECK)
    advice = random.choice(ADVICES)
    date_str = datetime.datetime.now().strftime("%d.%m.%Y")
    
    reading_text = (
        f"🔮 <b>ПЕРСОНАЛЬНЫЙ РАСКЛАД ТАРО ДЛЯ: {user_name.upper()}</b>\n"
        f"📅 Дата: {date_str} | Сфера: <b>{category}</b>\n\n"
        f"🃏 <b>Выпавшая карта:</b> <b>{card['name']}</b> (Стихия: {card['element']})\n"
        f"✨ <b>Значение:</b> {card['theme']}\n\n"
        f"📜 <b>Послание Высших Сил:</b>\n"
        f"{advice}\n\n"
        f"💎 <i>Для закрепления энергии изобилия подтвердите намерение в течение суток.</i>"
    )
    
    return {
        "card": card["name"],
        "element": card["element"],
        "text": reading_text
    }

if __name__ == "__main__":
    test = generate_tarot_reading("Финансы", "Михаил")
    print("=== ТЕСТ AI-ТАРО МОДУЛЯ ===")
    print(test["text"])
