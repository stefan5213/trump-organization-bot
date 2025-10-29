import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Trump bot e aktiviran! Dobrodojde!")

# Set message command
async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = ' '.join(context.args)
    if message:
        await update.message.reply_text(f"✅ Porakata e setirana: {message}")
    else:
        await update.message.reply_text("⚠️ Ve molime vnesete poraka: /set_message VashataPoraka")

# Main app
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_message", set_message))

    print("🚀 Botot e startuvan...")
    app.run_polling()
