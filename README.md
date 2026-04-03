# 📰 Aio Crafters Telegram Channel Bot (AI Powered)

A powerful and automated **Google News → Telegram Bot** that fetches topic-based news (e.g., *AI News*), generates **AI summaries**, and posts updates to your Telegram channel — fully serverless using GitHub Actions.

---

## 🔗 Repository

👉 https://github.com/aiocrafters/telegram-channel

---

## 🚀 Features

* 🔍 Topic-based Google News scraping (RSS)
* 🤖 AI-generated summaries (OpenRouter / LLM)
* 📤 Sends formatted news directly to Telegram
* 🧠 Summary caching (reduces API cost)
* ⏱ Runs automatically every hour using GitHub Actions
* 🔁 Avoids duplicate posts using `seen_news.json`
* ⚡ Lightweight, serverless, and free to run

---

## 🛠 Tech Stack

* Python
* feedparser (RSS parsing)
* requests (Telegram API + OpenRouter)
* GitHub Actions (automation)
* OpenRouter (AI summaries)

---

## 📁 Project Structure

```bash
.
├── main.py
├── requirements.txt
├── seen_news.json
├── summary_cache.json
└── .github/
    └── workflows/
        └── news.yml
```

---

## ⚙️ Setup Guide

### 1. Clone Repository

```bash
git clone https://github.com/aiocrafters/telegram-channel.git
cd telegram-channel
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create Telegram Bot

* Open Telegram → search **BotFather**
* Run `/start`
* Run `/newbot`
* Follow instructions to get your **BOT TOKEN**

---

### 4. Get Channel Chat ID

* Create or open your Telegram channel
* Add your bot as **admin**
* Use your channel username:

```bash
@your_channel_username
```

---

### 5. Get OpenRouter API Key (For AI Summaries)

1. Go to: https://openrouter.ai/
2. Sign in
3. Generate an API key

---

### 6. Setup Environment Variables

Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=@your_channel
OPENROUTER_API_KEY=your_openrouter_key
```

---

## ▶️ Run Locally

```bash
python main.py
```

---

## 🤖 GitHub Actions Setup (Recommended)

### 1. Add Repository Secrets

Go to:

**Settings → Secrets and variables → Actions**

Add:

#### 🔑 TELEGRAM_BOT_TOKEN

Your bot token

#### 🔑 TELEGRAM_CHAT_ID

Your channel username (e.g., `@your_channel`)

#### 🔑 OPENROUTER_API_KEY

Your OpenRouter API key

---

### 2. Workflow File

Already included:

```bash
.github/workflows/news.yml
```

⏱ Runs automatically **every 1 hour**

You can also trigger it manually from the **Actions tab**

---

## 🔄 How It Works

1. Fetches news from Google News RSS:

```bash
https://news.google.com/rss/search?q=AI News
```

2. Filters already sent news using:

```bash
seen_news.json
```

3. Generates AI summary using OpenRouter

4. Sends formatted message to Telegram

5. Stores summary in:

```bash
summary_cache.json
```

6. Updates seen news to prevent duplicates

---

## 🧠 AI Summary Details

* Uses OpenRouter API
* Default model: `mistralai/mistral-7b-instruct`
* Generates:

  * 2-line concise summaries
  * Simple, factual English
  * No opinions

---

## 🧠 Customization

### 🔹 Change Topic

Edit in `config.py`:

```python
TOPIC = "AI News"
```

Examples:

* `"India Jobs"`
* `"AI News"`
* `"Cricket"`

---

### 🔹 Change AI Model

Inside `config.py`:

```python
MODEL = "mistralai/mistral-7b-instruct"
```

Other options:

* `openai/gpt-4o-mini` (better quality)
* `google/gemini-pro` (if available)

---

### 🔹 Change Schedule

Edit:

```bash
.github/workflows/news.yml
```

Example (every 30 minutes):

```bash
*/30 * * * *
```

---

## ⚠️ Notes

* Google RSS does not provide full article content (summary is based on title)
* GitHub Actions may delay runs slightly
* Telegram bot must be **admin**
* Avoid sending too many messages rapidly (rate limits)

---

## 🚀 Future Improvements

* 🌐 Full article scraping (better summaries)
* 🗄 Store news in Supabase
* 📡 Public API for your website
* 🏷 Auto hashtags
* 🌍 Multi-language summaries (Hindi / Urdu)
* 📊 Admin dashboard

---

## 📜 License

MIT License — free to use and modify

---

## 🙌 Credits

Built with ❤️ by **aiocrafters**
