import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Define your channel buttons
CHANNELS = [
    {
        "name": "Official News",
        "url": "https://t.me/officialnews",
        "image": "https://example.com/news.jpg"
    },
    {
        "name": "Patriot Voice",
        "url": "https://t.me/patriotvoice",
        "image": "https://example.com/voice.jpg"
    },
    {
        "name": "Truth Central",
        "url": "https://t.me/truthcentral",
        "image": "https://example.com/truth.jpg"
    }
]

WELCOME_TEXT = """
👋 Welcome Patriot!

Before you get access, please make sure to join the following channels 👇
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(channel["name"], url=channel["url"])]
        for channel in CHANNELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
