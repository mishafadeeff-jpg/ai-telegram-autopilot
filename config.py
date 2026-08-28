import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Telegram Bot Token (can be the same bot as admin in all your channels!)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Channel 1: AI News
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "@aipulse_daily_global")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "⚡ AI Pulse Daily")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/aipulse_daily_global")

# Channel 2: Remote Tech Jobs
JOBS_CHANNEL_ID = os.getenv("JOBS_CHANNEL_ID", "")
JOBS_CHANNEL_NAME = os.getenv("JOBS_CHANNEL_NAME", "💼 Remote Tech Jobs Daily")
JOBS_CHANNEL_LINK = os.getenv("JOBS_CHANNEL_LINK", "")

# AI Provider Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Posting Settings
POSTING_INTERVAL_HOURS = int(os.getenv("POSTING_INTERVAL_HOURS", "4"))
MAX_POSTS_PER_RUN = int(os.getenv("MAX_POSTS_PER_RUN", "1"))

# Database path
DB_PATH = BASE_DIR / "autopilot.db"
