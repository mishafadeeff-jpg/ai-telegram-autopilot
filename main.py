import sys
import time
import argparse
import logging

# Ensure UTF-8 output encoding in Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from config import (
    POSTING_INTERVAL_HOURS, MAX_POSTS_PER_RUN,
    TELEGRAM_CHANNEL_ID, JOBS_CHANNEL_ID,
    JOBS_CHANNEL_NAME, JOBS_CHANNEL_LINK
)
from aggregator import fetch_trending_items
from generator import generate_post
from publisher import send_telegram_post
from database import is_already_posted, mark_as_posted
from jobs_module import fetch_remote_jobs, format_job_post

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def run_ai_channel_cycle(dry_run: bool = False) -> int:
    """Cycle for Channel 1: AI News."""
    logging.info("=== [Channel 1] AI News Autopilot Cycle ===")
    items = fetch_trending_items()
    posted_count = 0

    for item in items:
        if posted_count >= MAX_POSTS_PER_RUN:
            break

        url = item["url"]
        title = item["title"]

        if is_already_posted(url):
            logging.info(f"Skipping already posted AI item: {title}")
            continue

        logging.info(f"Generating AI post for: {title}")
        formatted_post = generate_post(item)

        if dry_run:
            print("\n" + "=" * 50)
            print("🚀 [DRY RUN PREVIEW - AI NEWS] POST:")
            print("=" * 50)
            print(formatted_post)
            print("=" * 50 + "\n")
            posted_count += 1
            mark_as_posted(item["source"], title, url)
        else:
            success = send_telegram_post(formatted_post, item.get("image_url"))
            if success:
                mark_as_posted(item["source"], title, url)
                posted_count += 1
                logging.info(f"Successfully posted AI item {posted_count}/{MAX_POSTS_PER_RUN}")
                time.sleep(5)
            else:
                logging.warning(f"Failed to post AI item: {title}")

    return posted_count

def run_jobs_channel_cycle(dry_run: bool = False) -> int:
    """Cycle for Channel 2: Remote Tech Jobs."""
    if not JOBS_CHANNEL_ID and not dry_run:
        logging.info("Jobs Channel ID not configured, skipping.")
        return 0

    logging.info("=== [Channel 2] Remote Jobs Autopilot Cycle ===")
    jobs = fetch_remote_jobs()
    posted_count = 0

    for job in jobs:
        if posted_count >= MAX_POSTS_PER_RUN:
            break

        url = job["url"]
        title = f"{job['company']}: {job['title']}"

        if is_already_posted(url):
            logging.info(f"Skipping already posted Job: {title}")
            continue

        logging.info(f"Formatting Job post: {title}")
        formatted_post = format_job_post(
            job,
            channel_name=JOBS_CHANNEL_NAME,
            channel_link=JOBS_CHANNEL_LINK or f"https://t.me/{JOBS_CHANNEL_ID.lstrip('@')}"
        )

        if dry_run:
            print("\n" + "=" * 50)
            print("💼 [DRY RUN PREVIEW - REMOTE JOBS] POST:")
            print("=" * 50)
            print(formatted_post)
            print("=" * 50 + "\n")
            posted_count += 1
            mark_as_posted("JobBoard", title, url)
        else:
            import requests
            from config import TELEGRAM_BOT_TOKEN
            # Post directly to jobs channel
            endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": JOBS_CHANNEL_ID,
                "text": formatted_post,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            try:
                res = requests.post(endpoint, json=payload, timeout=25).json()
                if res.get("ok"):
                    mark_as_posted("JobBoard", title, url)
                    posted_count += 1
                    logging.info(f"Successfully posted Job {posted_count}/{MAX_POSTS_PER_RUN}")
                    time.sleep(5)
                else:
                    logging.error(f"Jobs Channel Post Error: {res.get('description')}")
            except Exception as e:
                logging.error(f"Jobs channel network error: {e}")

    return posted_count

def main():
    parser = argparse.ArgumentParser(description="Multi-Channel Telegram Autopilot")
    parser.add_argument("--dry-run", action="store_true", help="Preview generated posts without sending to Telegram")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    print("""
    =====================================================
    🤖 MULTI-CHANNEL TELEGRAM MEDIA NETWORK AUTOPILOT
    Channel 1: AI & Tech News (@aipulse_daily_global)
    Channel 2: Remote Tech Jobs (Global Careers)
    =====================================================
    """)

    if args.once or args.dry_run:
        run_ai_channel_cycle(dry_run=args.dry_run)
        run_jobs_channel_cycle(dry_run=args.dry_run)
    else:
        logging.info(f"Autopilot started in continuous mode. Posting every {POSTING_INTERVAL_HOURS} hours.")
        while True:
            try:
                run_ai_channel_cycle(dry_run=False)
                run_jobs_channel_cycle(dry_run=False)
            except Exception as e:
                logging.error(f"Unexpected error in cycle: {e}")

            sleep_seconds = POSTING_INTERVAL_HOURS * 3600
            logging.info(f"Sleeping for {POSTING_INTERVAL_HOURS} hours ({sleep_seconds}s)...")
            time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
