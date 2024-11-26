import requests
import asyncio
import sqlite3
import json
from telegram import Bot

HN_API_URL = "https://hacker-news.firebaseio.com/v0"
DB_FILE = "matches.db"

SEARCH_STRING = "product hunt"

with open("config.json", "r") as config_file:
    config = json.load(config_file)

TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
TELEGRAM_CHAT_ID = config["telegram_chat_id"]
SEARCH_STRING = config["search_string"]

SLEEP_TIME = config.get("sleep_time", 600)

def setup_database():
    """Create the SQLite database and table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            item_id INTEGER UNIQUE,
            title TEXT,
            link TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_match(item_id, title, link):
    """Save a match to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO matches (item_id, title, link) VALUES (?, ?, ?)", (item_id, title, link))
        conn.commit()
        return True  # Successfully saved
    except sqlite3.IntegrityError:
        return False  # Duplicate entry
    finally:
        conn.close()

def fetch_top_stories():
    """Fetch top stories from Hacker News."""
    top_stories = requests.get(f"{HN_API_URL}/topstories.json").json()
    return top_stories[:30] 

def fetch_item(item_id):
    """Fetch a single item (story or comment) from Hacker News."""
    return requests.get(f"{HN_API_URL}/item/{item_id}.json").json()

def search_hacker_news():
    """Search Hacker News titles and comments for the string."""
    top_stories = fetch_top_stories()
    matched_items = []

    for story_id in top_stories:
        story = fetch_item(story_id)
        if SEARCH_STRING.lower() in (story.get("title") or "").lower():
            matched_items.append(story)

        if "kids" in story:
            for comment_id in story["kids"]:
                comment = fetch_item(comment_id)
                if SEARCH_STRING.lower() in (comment.get("text") or "").lower():
                    matched_items.append(comment)
    return matched_items

async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    setup_database()

    while True:
        matches = search_hacker_news()
        for match in matches:
            item_id = match["id"]
            title = match.get("title", match.get("text", "No title or text"))
            link = f"https://news.ycombinator.com/item?id={item_id}"

            if save_match(item_id, title, link):
                message = f"Matched: {title}\nLink: {link}"
                await send_telegram_message(bot, message)

        await asyncio.sleep(SLEEP_TIME)  # Wait 10 minutes before checking again

if __name__ == "__main__":
    asyncio.run(main())
