# ---------------------------
# config.py — Edit settings here
# ---------------------------

# 🔍 Topic to search for news
TOPIC = "AI News"

# 🤖 OpenRouter model to use
# Examples:
#   "openai/gpt-4o-mini"   (fast, cheap)
#   "openai/gpt-4o"        (smarter, slower)
#   "anthropic/claude-3-haiku"
#   "google/gemini-flash-1.5"
MODEL = "openai/gpt-4o-mini"

# 📰 Number of news articles to fetch per run
MAX_ARTICLES = 10

# 🔗 RSS feed URL (auto-built from TOPIC)
RSS_URL = f"https://news.google.com/rss/search?q={TOPIC.replace(' ', '%20')}"

# 💾 Storage files
SEEN_FILE = "seen_news.json"
SUMMARY_CACHE_FILE = "summary_cache.json"
