import requests
import logging
from typing import Optional
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

try:
    from monetization_module import get_monetized_footer
except ImportError:
    def get_monetized_footer():
        return ""

def send_telegram_post(text: str, image_url: Optional[str] = None) -> bool:
    """Send post to Telegram channel with optional photo and monetization footer."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        logging.error("Telegram credentials not configured! Please check your .env file.")
        return False

    # Append CPA / monetization footer
    footer = get_monetized_footer()
    full_text = text + footer

    # If caption exceeds Telegram 1024 limit for photo, trim or send as text
    if len(full_text) > 1020:
        full_text = text[:950] + "..." + footer

    # Attempt to send with photo if image_url is present and valid
    if image_url and image_url.startswith("http"):
        photo_endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "photo": image_url,
            "caption": full_text,
            "parse_mode": "HTML"
        }
        try:
            res = requests.post(photo_endpoint, json=payload, timeout=25)
            data = res.json()
            if data.get("ok"):
                logging.info("Successfully published post WITH image and monetization footer!")
                return True
            else:
                logging.warning(f"Failed to send with image ({data.get('description')}), falling back to text.")
        except Exception as e:
            logging.warning(f"Exception sending photo ({e}), falling back to text.")

    # Fallback to standard text message
    text_endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": full_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        res = requests.post(text_endpoint, json=payload, timeout=25)
        data = res.json()
        if data.get("ok"):
            logging.info("Successfully published text post with monetization footer!")
            return True
        else:
            logging.error(f"Telegram API Error: {data.get('description')}")
            return False
    except Exception as e:
        logging.error(f"Network error publishing to Telegram: {e}")
        return False
