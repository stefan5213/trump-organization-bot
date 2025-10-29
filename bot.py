import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ChatJoinRequestHandler, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
MESSAGE_FILE = "message.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_message():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"text": "Добредојде!", "image": None, "buttons": []}

def save_message(data):
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Внеси нова порака во формат:\n\n"
        "TEXT: Добредојде во групата!\n"
        "IMAGE: https://link-do-slika.com/photo.jpg\n"
        "BUTTONS:\n"
        "1. Вебсајт - https://example.com\n"
        "2. Правила - https://example.com/rules\n"
        "3. Потврди - https://example.com/ok"
    )
    context.user_data['awaiting_message'] = True

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_message'):
        return

    lines = update.message.text.strip().split("\n")
    data = {"text": "", "image": None, "buttons": []}

    for line in lines:
        if line.startswith("TEXT:"):
            data["text"] = line[5:].strip()
        elif line.startswith("IMAGE:"):
            data["image"] = line[6:].strip()
        elif any(line.startswith(f"{i}.") for i in range(1, 10)):
            try:
                label, url = line.split("-", 1)
                data["buttons"].append({"text": label.strip()[2:].strip(), "url": url.strip()})
            except:
                pass

    save_message(data)
    context.user_data['awaiting_message'] = False
    await update.message.reply_text("✅ Новата порака е зачувана!")

async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    message_data = load_message()

    keyboard = [[InlineKeyboardButton(btn['text'], url=btn['url'])] for btn in message_data.get("buttons", [])]
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    try:
        if message_data.get("image"):
            await context.bot.send_photo(
                chat_id=user.id,
                photo=message_data["image"],
                caption=message_data["text"],
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=user.id,
                text=message_data["text"],
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Не можам да испратам порака на {user.id}: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Ботот е активен.")))
app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("Користи /set_message за да поставиш нова порака.")))
app.add_handler(CommandHandler("ping", lambda u, c: u.message.reply_text("pong")))
app.add_handler(CommandHandler("id", lambda u, c: u.message.reply_text(f"Твојот Telegram ID: {u.effective_user.id}")))
app.add_handler(CommandHandler("chatid", lambda u, c: u.message.reply_text(f"Chat ID: {u.effective_chat.id}")))
app.add_handler(CommandHandler("set_message", set_message))
app.add_handler(CommandHandler("reset", lambda u, c: (save_message({"text": "Добредојде!", "image": None, "buttons": []}), u.message.reply_text("Пораката е ресетирана."))))
app.add_handler(CommandHandler("show", lambda u, c: u.message.reply_text(json.dumps(load_message(), indent=2, ensure_ascii=False))))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(ChatJoinRequestHandler(on_join_request))

if __name__ == "__main__":
    app.run_polling()
