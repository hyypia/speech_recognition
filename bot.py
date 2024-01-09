import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")


if __name__ == "__main__":
    load_dotenv()

    telegram_token = os.environ.get("TELEGRAM_API_TOKEN")
    if telegram_token:
        app = ApplicationBuilder().token(telegram_token).build()

        start_handler = CommandHandler("start", start)
        app.add_handler(start_handler)

        app.run_polling()
