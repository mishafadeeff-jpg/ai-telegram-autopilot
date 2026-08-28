import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")  # e.g., @AIToolStash or -1001234567890

# AI Provider Settings (Optional Gemini API key for deep rewrites, fallback to smart template engine)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Channel Branding
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "⚡ AI Pulse Daily")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/AIPulseDaily")

# Posting Settings
POSTING_INTERVAL_HOURS = int(os.getenv("POSTING_INTERVAL_HOURS", "4"))
MAX_POSTS_PER_RUN = int(os.getenv("MAX_POSTS_PER_RUN", "1"))

# Database path
DB_PATH = BASE_DIR / "autopilot.db"
