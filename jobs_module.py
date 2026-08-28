import requests
import feedparser
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_text(raw_html: str) -> str:
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def fetch_remote_jobs() -> List[Dict]:
    """Fetch latest remote tech jobs from top global job boards."""
    jobs = []

    # 1. Remotive API
    try:
        logging.info("Fetching remote jobs from Remotive API...")
        res = requests.get("https://remotive.com/api/remote-jobs?limit=15", headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            for j in data.get("jobs", [])[:10]:
                title = j.get("title", "").strip()
                company = j.get("company_name", "").strip()
                url = j.get("url", "").strip()
                category = j.get("category", "Software Development").strip()
                salary = j.get("salary", "").strip() or "Competitive / Negotiable"
                location = j.get("candidate_required_location", "").strip() or "Worldwide / Remote"
                desc = clean_text(j.get("description", ""))[:250]

                if title and url:
                    jobs.append({
                        "source": "Remotive",
                        "title": title,
                        "company": company,
                        "url": url,
                        "category": category,
                        "salary": salary,
                        "location": location,
                        "description": desc,
                        "image_url": j.get("company_logo", "")
                    })
    except Exception as e:
        logging.warning(f"Error fetching from Remotive: {e}")

    # 2. WeWorkRemotely RSS Feeds
    wwr_feeds = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss"
    ]

    for feed_url in wwr_feeds:
        try:
            logging.info(f"Scanning WWR Feed: {feed_url}...")
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                raw_title = entry.get("title", "").strip()
                url = entry.get("link", "").strip()
                desc = clean_text(entry.get("summary", "") or entry.get("description", ""))[:250]

                # Parse Company and Position from "Company: Position" title
                if ":" in raw_title:
                    company, title = raw_title.split(":", 1)
                    company = company.strip()
                    title = title.strip()
                else:
                    company = "Global Tech Company"
                    title = raw_title

                if title and url:
                    jobs.append({
                        "source": "WeWorkRemotely",
                        "title": title,
                        "company": company,
                        "url": url,
                        "category": "Tech & Engineering",
                        "salary": "Competitive (USD/EUR)",
                        "location": "100% Remote (Global)",
                        "description": desc,
                        "image_url": ""
                    })
        except Exception as e:
            logging.warning(f"Error fetching from WWR: {e}")

    logging.info(f"Total remote tech jobs collected: {len(jobs)}")
    return jobs

def format_job_post(job: Dict, channel_name: str, channel_link: str) -> str:
    """Format remote job into clean, high-conversion Telegram post."""
    title = job["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    company = job["company"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    salary = job["salary"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    location = job["location"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    url = job["url"]

    post = f"""💼 <b>NEW REMOTE OPPORTUNITY</b>

🚀 <b>Role:</b> {title}
🏢 <b>Company:</b> {company}
💰 <b>Compensation:</b> {salary}
🌍 <b>Location:</b> {location}
📌 <b>Category:</b> {job.get('category', 'Tech')}

📝 <b>Quick Overview:</b>
Looking for an ambitious specialist to join a modern distributed team. Full remote flexibility.

👉 <a href="{url}"><b>Apply for this Position (Official Link) →</b></a>

━━━━━━━━━━━━━━━
🌐 <i>Follow <b><a href="{channel_link}">{channel_name}</a></b> for daily 100% Remote Tech Jobs!</i>
#RemoteJobs #Hiring #TechCareers #WorkFromHome #SoftwareJobs"""

    return post
