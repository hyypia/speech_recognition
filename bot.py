import logging
import os
import soundfile as sf
import speech_recognition as sr
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
    file_id = update.message.voice.file_id
    new_file = await context.bot.get_file(file_id)
    path = await new_file.download_to_drive()
    data, samplerate = sf.read(path.name)
    sf.write("output.wav", data, samplerate)
    r = sr.Recognizer()
    voice_audio = sr.AudioFile("output.wav")
    with voice_audio as source:
        audio = r.record(source)
    transcript = r.recognize_google(audio, language="ru-RU")
    await update.message.reply_text(transcript)


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
    telegram_token = os.environ.get("TELEGRAM_API_TOKEN")

    main()
