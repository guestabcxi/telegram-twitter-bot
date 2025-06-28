from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from collections import deque
import tweepy
import os

# === ENV TOKENS ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

# === Twitter v2 Setup ===
client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)

buffer = deque(maxlen=4)

def post_tweet(messages):
    tweet_text = "\n\n".join(messages)
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    try:
        client.create_tweet(text=tweet_text)
        print("✅ Tweet posted:\n", tweet_text)
    except Exception as e:
        print("❌ Tweet failed:", e)

def handle_channel_message(update: Update, context):
    if update.channel_post:
        text = update.channel_post.text
        if text:
            print("📩 Received:", text)
            buffer.append(text)
            if len(buffer) == 4:
                post_tweet(list(buffer))
                buffer.clear()

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.update.channel_posts, handle_channel_message))
    updater.start_polling()
    print("🤖 Bot is live on Render")
    updater.idle()

if __name__ == "__main__":
    main()
