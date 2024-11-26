# Hacker News Scraper with Telegram Alerts

A Python-based tool that monitors the Hacker News homepage for a specific search string (in titles and comments) and sends alerts to a Telegram chat when matches are found. The tool uses SQLite to store previous matches, so no duplicate alerts are sent. It runs periodically and can be deployed in a Docker container.

## Requirements
- Python 3.7+
- Telegram Bot Token (see [BotFather](https://core.telegram.org/bots#botfather))
- `requests` and `python-telegram-bot` Python packages

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/hackernews-scraper.git
   cd hackernews-scraper
   ```

2. **Set Up a Virtual Environment**

  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
  3. **Pip Install**

```bash
     pip install python-telegram-bot requests
  ```
  4. **Create `config.json`**

```json

{
    "telegram_bot_token": "your_telegram_bot_token_here",
    "telegram_chat_id": "your_telegram_chat_id_here",
    "search_string": "your_search_string_here",
    "sleep_time": 600 //optional: defaults to 600
}
```

5. Run
   ```bash
   python3 main.py
   ```

## Optionally run with docker

  ```bash
  docker build -t hackernews-scraper .
  docker run -d -v $(pwd)/config.json:/app/config.json hackernews-scraper
    ```
