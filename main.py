import os
from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_keyboard = [
        [KeyboardButton("English"), KeyboardButton("العربية")]
    ]
    await update.message.reply_text(
        "Please choose your language / الرجاء اختيار اللغة:",
        reply_markup=ReplyKeyboardMarkup(lang_keyboard, resize_keyboard=True)
    )

bot_app.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot_app.run_polling, daemon=True).start()
    app.run(port=10000)
