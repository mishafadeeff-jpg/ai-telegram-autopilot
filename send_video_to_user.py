import os
import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

token = "8540258549:AAEI1mQFP8Vs_rNsavUq0ojZDPzalrwKNsk"
chat_id = 860392517  # Misha (@MigOdin)
video_path = os.path.join(os.path.expanduser("~"), "Desktop", "lucky_wheel_promo.mp4")

url = f"https://api.telegram.org/bot{token}/sendVideo"

caption = (
    "🎬 <b>Ваш готовый видео-ролик для TikTok!</b>\n\n"
    "📲 <b>Как выложить в TikTok с телефона за 1 минуту:</b>\n"
    "1. Нажмите на видео в Telegram и сохраните его в галерею телефона (или нажмите «Поделиться в TikTok»).\n"
    "2. Включите VPN на телефоне.\n"
    "3. В приложении TikTok нажмите <b>[ + ]</b> ➔ выберите это видео из галереи ➔ Опубликовать!\n\n"
    "📝 <b>Текст для видео:</b>\n"
    "Бесплатный розыгрыш Telegram Premium и Stars! 🎁 Ссылка на бота в шапке профиля! 👆\n"
    "#telegram #розыгрыш #халява #telegrampremium #stars #игры #колесофортуны"
)

try:
    with open(video_path, "rb") as vf:
        files = {"video": vf}
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"}
        resp = requests.post(url, data=data, files=files, timeout=60).json()
        if resp.get("ok"):
            print("✅ Видео успешно доставлено прямо в ваш Telegram на телефон!")
        else:
            print("❌ Ошибка Telegram:", resp)
except Exception as e:
    print("Ошибка отправки:", e)
