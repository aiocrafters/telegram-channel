import requests
import feedparser
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from newspaper import Article
from config import TOPIC, MODEL, RSS_URL, MAX_ARTICLES, SEEN_FILE, SUMMARY_CACHE_FILE
from prompt_template import SUMMARY_PROMPT_TEMPLATE

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



# ---------------------------
# JSON helpers
# ---------------------------
def load_json_file(file):
    if not os.path.exists(file):
        return {}

    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}


def save_json_file(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------------
# Fetch news
# ---------------------------
def fetch_news():
    feed = feedparser.parse(RSS_URL)
    news_list = []

    for entry in feed.entries[:MAX_ARTICLES]:
        news = {
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source": entry.get("source", {}).get("title", "Google News")
        }
        news_list.append(news)

    return news_list

# ---------------------------
# Resolve real URL
# ---------------------------
def resolve_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except:
        return url

# ---------------------------
# Extract article text
# ---------------------------
def extract_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text.strip()

        if len(text) < 200:
            return None

        return text[:2000]  # 🔥 trimmed for better AI

    except Exception as e:
        print("❌ Article extraction failed:", e)
        return None

# ---------------------------
# Generate AI summary
# ---------------------------
def generate_summary(news, cache):
    news_id = news["link"]

    if news_id in cache:
        return cache[news_id]

    try:
        real_url = news.get("real_link", news["link"])
        article_text = extract_article_text(real_url)

        content = article_text if article_text else news["title"]

        if not content:
            return news["title"]

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = SUMMARY_PROMPT_TEMPLATE.format(content=content)

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        # Retry logic
        response = None
        for attempt in range(2):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                break
            except Exception as e:
                print(f"⚠️ Retry {attempt+1} failed:", e)
                time.sleep(2)

        if response is None:
            return news["title"]

        try:
            data = response.json()
        except:
            return news["title"]

        print("🔍 API Response:", data)

        if "choices" in data:
            summary = data["choices"][0]["message"]["content"].strip()
        else:
            print("❌ API Error:", data)
            return news["title"]

        if not summary or len(summary) < 20:
            summary = news["title"]

        cache[news_id] = summary
        return summary

    except Exception as e:
        print("❌ Summary Error:", e)
        return news["title"]

# ---------------------------
# Format message
# ---------------------------
def format_news(news, summary):
    url = news.get('real_link', news['link'])
    return f"""
🚨 <b>{news['title']}</b>

{summary}

📍 <i>{TOPIC}</i>
📰 {news['source']}
🕒 {news['published']}

🔗 <a href="{url}">Read more</a>
""".strip()

# ---------------------------
# Send to Telegram
# ---------------------------
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        print("❌ Telegram Error:", e)

# ---------------------------
# Main
# ---------------------------
def run():
    print(f"\n[{datetime.now()}] 🔍 Fetching '{TOPIC}' news...")

    seen = set(load_json_file(SEEN_FILE))
    summary_cache = load_json_file(SUMMARY_CACHE_FILE)

    news_list = fetch_news()
    new_count = 0

    for news in news_list:
        if not news["link"] or news["link"] in seen:
            continue
            
        news["real_link"] = resolve_url(news["link"])

        summary = generate_summary(news, summary_cache)
        message = format_news(news, summary)

        send_telegram(message)

        seen.add(news["link"])
        new_count += 1

        time.sleep(1)

    save_json_file(SEEN_FILE, list(seen))
    save_json_file(SUMMARY_CACHE_FILE, summary_cache)

    print(f"✅ Sent {new_count} news")

if __name__ == "__main__":
    run()