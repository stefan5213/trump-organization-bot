from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ChatJoinRequestHandler, ContextTypes
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MESSAGE_FILE = "message.json"

def load_message():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"text": "Добредојде!", "image": None, "buttons": []}

def save_message(data):
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def start(update, context):
    await update.message.reply_text("✅ Ботот е активен и работи!")

async def set_message(update, context):
    await update.message.reply_text(
        "Внеси нова порака во следниов формат:\n\n"
        "TEXT: Добредојде во групата!\n"
        "IMAGE: https://link.com\n"
        "BUTTONS:\n"
        "1. Линк - https://example.com"
    )
    context.user_data['awaiting_message'] = True

async def handle_text(update, context):
    if not context.user_data.get('awaiting_message'):
        return

    lines = update.message.text.strip().split("\n")
    data = {"text": "", "image": None, "buttons": []}

    for line in lines:
        if line.startswith("TEXT:"):
            data["text"] = line[5:].strip()
        elif line.startswith("IMAGE:"):
            data["image"] = line[6:].strip()
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            try:
                label, url = line.split("-", 1)
                data["buttons"].append({"text": label.strip()[2:].strip(), "url": url.strip()})
            except:
                pass

    save_message(data)
    context.user_data['awaiting_message'] = False
    await update.message.reply_text("✅ Новата порака е зачувана!")

async def on_join_request(update, context):
    user = update.chat_join_request.from_user
    message_data = load_message()

    keyboard = [[InlineKeyboardButton(btn['text'], url=btn['url'])] for btn in message_data.get("buttons", [])]
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    try:
        if message_data.get("image"):
            await context.bot.send_photo(chat_id=user.id, photo=message_data["image"], caption=message_data["text"], reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=user.id, text=message_data["text"], reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Не можам да испратам порака на {user.id}: {e}")

# ✅ Ова е новата правилна структура за верзија 20+
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_message", set_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.run_polling()

if __name__ == "__main__":
    main()


