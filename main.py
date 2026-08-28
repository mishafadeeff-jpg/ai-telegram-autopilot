import sys
import time
import argparse
import logging

# Ensure UTF-8 output encoding in Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from config import POSTING_INTERVAL_HOURS, MAX_POSTS_PER_RUN
from aggregator import fetch_trending_items
from generator import generate_post
from publisher import send_telegram_post
from database import is_already_posted, mark_as_posted

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def run_cycle(dry_run: bool = False) -> int:
    """Execute one aggregation and posting cycle."""
    logging.info("=== Starting Autopilot Cycle ===")
    items = fetch_trending_items()
    posted_count = 0

    for item in items:
        if posted_count >= MAX_POSTS_PER_RUN:
            break

        url = item["url"]
        title = item["title"]

        if is_already_posted(url):
            logging.info(f"Skipping already posted item: {title}")
            continue

        logging.info(f"Generating post for: {title}")
        formatted_post = generate_post(item)

        if dry_run:
            print("\n" + "=" * 50)
            print("🚀 [DRY RUN PREVIEW] POST TO BE PUBLISHED:")
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
                logging.info(f"Successfully posted item {posted_count}/{MAX_POSTS_PER_RUN}")
                # Brief sleep between multiple posts in one batch
                time.sleep(5)
            else:
                logging.warning(f"Failed to post: {title}")

    logging.info(f"=== Cycle Completed. Posted {posted_count} item(s) ===\n")
    return posted_count

def main():
    parser = argparse.ArgumentParser(description="AI Telegram Channel Autopilot")
    parser.add_argument("--dry-run", action="store_true", help="Preview generated posts without sending to Telegram")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    print("""
    =====================================================
    🤖 GLOBAL AI TELEGRAM AUTOPILOT
    Automated Content Curation, AI Formatting & Posting
    =====================================================
    """)

    if args.once or args.dry_run:
        run_cycle(dry_run=args.dry_run)
    else:
        logging.info(f"Autopilot started in continuous mode. Posting every {POSTING_INTERVAL_HOURS} hours.")
        while True:
            try:
                run_cycle(dry_run=False)
            except Exception as e:
                logging.error(f"Unexpected error in cycle: {e}")

            sleep_seconds = POSTING_INTERVAL_HOURS * 3600
            logging.info(f"Sleeping for {POSTING_INTERVAL_HOURS} hours ({sleep_seconds}s)...")
            time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
