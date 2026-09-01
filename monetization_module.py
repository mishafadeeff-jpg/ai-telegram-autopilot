import os
import sys
import random
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# CPA & Affiliate Footers for News Channel
SPONSOR_FOOTERS = [
    (
        "\n\n💳 <b>Полезно:</b> Оформите зарубежную виртуальную карту для оплаты зарубежных сервисов и подписок (ChatGPT, Midjourney) ➔ <a href=\"https://t.me/aipulsedaily_news_bot\">Оформить через бота</a>"
    ),
    (
        "\n\n🤖 <b>Для владельцев каналов:</b> Хотите такой же умный AI-Автопилот 24/7 для своего бизнеса или блога? ➔ Напишите: @MigOdin"
    ),
    (
        "\n\n💼 <b>Карьера в IT & AI:</b> Вакансии с зарплатой от $3,000/мес на удаленке в нашем канале ➔ @remotetech_jobs_global"
    ),
    (
        "\n\n🎰 <b>Розыгрыш:</b> Крутите Колесо Фортуны и забирайте Telegram Premium и Stars бесплатно! ➔ <a href=\"https://mishafadeeff-jpg.github.io/ai-telegram-autopilot/\">Крутить колесо</a>"
    )
]

def get_monetized_footer():
    return random.choice(SPONSOR_FOOTERS)
