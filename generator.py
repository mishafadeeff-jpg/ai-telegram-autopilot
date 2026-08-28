import requests
import json
import re
from typing import Dict
from config import GEMINI_API_KEY, CHANNEL_NAME, CHANNEL_LINK

def clean_for_telegram_html(text: str) -> str:
    """Sanitize HTML special characters to avoid Telegram parse errors."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text

def format_with_gemini(item: Dict) -> str:
    """Generate high quality AI post using Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""You are a top-tier tech journalist and Telegram channel manager for a global audience interested in Artificial Intelligence and Tech breakthroughs.

Task: Write a viral, highly engaging, clean Telegram post in ENGLISH based on this news/tool:
Title: {item['title']}
Source: {item['source']}
Summary: {item['summary']}
Link: {item['url']}

Format guidelines:
1. Start with an eye-catching headline with emojis (e.g., 🚀 <b>HEADLINE</b>).
2. Write 2 concise bullet points or 2 short punchy paragraphs explaining WHAT it is and WHY it matters.
3. Include 2-3 key highlights or practical takeaways (⚡ <b>Key Highlights:</b>).
4. Add a clean Call to Action with the link: 🔗 <a href="{item['url']}">Read Full Story / Try Tool</a>.
5. End with 3-4 relevant hashtags (#AI #Tech #Innovation #MachineLearning).
6. Footer: <i>Follow {CHANNEL_NAME} for daily AI alpha!</i>

Return ONLY the valid HTML formatted text for Telegram. Do NOT wrap in markdown code blocks.
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)
    if response.status_code == 200:
        data = response.json()
        generated_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Remove any markdown code fences if model returned them
        generated_text = re.sub(r"^```html\s*", "", generated_text, flags=re.IGNORECASE)
        generated_text = re.sub(r"^```\s*", "", generated_text)
        generated_text = re.sub(r"\s*```$", "", generated_text)
        return generated_text
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

def format_with_template(item: Dict) -> str:
    """Smart fallback generator: builds engaging Telegram post without needing API keys."""
    raw_title = item['title']
    raw_summary = item['summary']
    link = item['url']
    source = item['source']

    # Trim summary to ~250 chars cleanly
    sentences = re.split(r'(?<=[.!?]) +', raw_summary)
    short_summary = " ".join(sentences[:2]) if sentences else raw_summary[:200]
    if len(short_summary) > 280:
        short_summary = short_summary[:277] + "..."

    safe_title = clean_for_telegram_html(raw_title)
    safe_summary = clean_for_telegram_html(short_summary)
    safe_source = clean_for_telegram_html(source)

    post = f"""⚡ <b>{safe_title}</b>

🧠 <b>Overview:</b>
{safe_summary}

💡 <b>Why it matters:</b>
• Major update in the AI landscape from <b>{safe_source}</b>
• Shaping the future of tools, automation & tech workflows

🔗 <a href="{link}"><b>Explore Full Story &amp; Details →</b></a>

━━━━━━━━━━━━━━━
🚀 <i>Follow <b><a href="{CHANNEL_LINK}">{CHANNEL_NAME}</a></b> for daily AI alpha &amp; tech drops!</i>
#AI #TechNews #ArtificialIntelligence #Innovation"""

    return post

def generate_post(item: Dict) -> str:
    """Generate final post content using AI or smart template fallback."""
    if GEMINI_API_KEY:
        try:
            return format_with_gemini(item)
        except Exception as e:
            print(f"[Warning] Gemini API failed ({e}), falling back to smart template.")
            return format_with_template(item)
    else:
        return format_with_template(item)
