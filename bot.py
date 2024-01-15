import logging
import os

import assemblyai as aai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="enotebot.log",
    filemode="w",
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n\n"
        "Я бот для распознавания голосовых сообщений в текст."
        "Присылай мне свои голосовые.\n\nЯ ничего не записываю и не храню.)"
    )


async def handle_voice(update: Update, context: CallbackContext) -> None:
    try:
        if update.message.voice:
            file_id = update.message.voice.file_id
        elif update.message.audio:
            file_id = update.message.audio.file_id
        new_file = await context.bot.get_file(file_id)

        config = aai.TranscriptionConfig(language_code="ru")
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(new_file.file_path)
        await update.message.reply_text(transcript.text)

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        await update.message.reply_text("Не удалось распознать, попробуй еще раз.")


def main() -> None:
    app = Application.builder().token(telegram_token).build()

    start_handler = CommandHandler("start", start)
    voice_handler = MessageHandler(
        filters.ChatType.PRIVATE & (filters.VOICE | filters.AUDIO), handle_voice
    )

    app.add_handler(start_handler)
    app.add_handler(voice_handler)

    app.run_polling()


if __name__ == "__main__":
    load_dotenv()
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    telegram_token = os.environ.get("TELEGRAM_API_TOKEN")

    main()
