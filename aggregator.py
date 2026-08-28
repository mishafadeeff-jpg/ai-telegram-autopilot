import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SOURCES = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "type": "rss"
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "type": "rss"
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "type": "rss"
    },
    {
        "name": "MIT Tech Review AI",
        "url": "https://www.technologyreview.com/feed/",
        "type": "rss"
    },
    {
        "name": "HackerNews AI",
        "url": "https://hnrss.org/frontpage?q=AI+OR+LLM+OR+GPT+OR+Claude",
        "type": "rss"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def extract_image(entry) -> str:
    """Extract banner or thumbnail image if available in feed entry."""
    # 1. Check media_content
    if "media_content" in entry and entry.media_content:
        for media in entry.media_content:
            if "url" in media and media.get("type", "").startswith("image"):
                return media["url"]
            elif "url" in media:
                return media["url"]

    # 2. Check enclosures
    if "enclosures" in entry and entry.enclosures:
        for enc in entry.enclosures:
            if "href" in enc and enc.get("type", "").startswith("image"):
                return enc["href"]
            elif "href" in enc:
                return enc["href"]

    # 3. Check raw description for <img> tag
    raw_desc = entry.get("summary", "") or entry.get("description", "")
    if "<img" in raw_desc:
        soup = BeautifulSoup(raw_desc, "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]

    return ""

def fetch_trending_items() -> List[Dict]:
    """Fetch raw items from all configured sources."""
    items = []

    for src in SOURCES:
        try:
            logging.info(f"Scanning source: {src['name']}...")
            feed = feedparser.parse(src["url"])

            for entry in feed.entries[:5]:  # Top 5 items from each source
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = clean_html(entry.get("summary", "") or entry.get("description", ""))
                image_url = extract_image(entry)

                if title and link:
                    items.append({
                        "source": src["name"],
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "image_url": image_url
                    })
        except Exception as e:
            logging.error(f"Error fetching from {src['name']}: {e}")

    logging.info(f"Total aggregated items: {len(items)}")
    return items
