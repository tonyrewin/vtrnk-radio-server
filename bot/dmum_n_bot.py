import os
import logging
import logging.handlers
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import aiohttp
import asyncio

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_path = '/home/beasty197/projects/vtrnk_radio/logs/dmum_n_bot.log'
handler = logging.handlers.RotatingFileHandler(
    filename=log_path,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5
)
console_handler = logging.StreamHandler()  # Консольный вывод для отладки
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
class NoDebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno > logging.DEBUG
handler.addFilter(NoDebugFilter())
console_handler.addFilter(NoDebugFilter())
logger.addHandler(handler)
logger.addHandler(console_handler)

# Загрузка .env
load_dotenv('/home/beasty197/projects/vtrnk_radio/.env')
BOT_TOKEN = os.getenv('BOT_TOKEN_DMB')
CHAT_ID = os.getenv('CHAT_ID')
RADIO_SHOW_DIR = '/home/beasty197/projects/vtrnk_radio/audio/radio_show'
BASE_DIR = '/home/beasty197/projects/vtrnk_radio'

async def radio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            logger.info("Fetching track data for /radio")
            async with session.get("https://vtrnk.online/track") as track_response:
                track_data = await track_response.json()
                logger.info(f"Track response: {track_data}")
                artist = track_data[1][1] if track_data and len(track_data) > 1 else "VTRNK"
                title = track_data[2][1] if track_data and len(track_data) > 2 else "Unknown Track"

            logger.info("Fetching cover path for /radio")
            async with session.get("https://vtrnk.online/get_cover_path") as cover_response:
                cover_data = await cover_response.json()
                cover_path = cover_data.get("cover_path", "/images/placeholder2.png")
                file_path = f"{BASE_DIR}{cover_path}" if cover_path.startswith("/") else cover_path
                logger.info(f"Local file path for /radio: {file_path}")

        # Проверяем существование файла
        if os.path.exists(file_path) and os.path.isfile(file_path):
            logger.info(f"Sending cover as file: {file_path}")
            with open(file_path, 'rb') as photo:
                keyboard = [[InlineKeyboardButton("Слушать радио", web_app={"url": "https://vtrnk.online/telegram-mini-app.html"})]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                caption = f"Сейчас в эфире: {title} от {artist}\nСлушай на VTRNK Radio: https://vtrnk.online"
                logger.info(f"Sending /radio response: {caption}")
                await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    reply_markup=reply_markup
                )
        else:
            logger.error(f"Cover file not found: {file_path}")
            cover_url = "https://vtrnk.online/images/placeholder2.png"
            logger.info(f"Falling back to default cover URL: {cover_url}")
            keyboard = [[InlineKeyboardButton("Слушать радио", web_app={"url": "https://vtrnk.online/telegram-mini-app.html"})]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            caption = f"Сейчас в эфире: {title} от {artist}\nСлушай на VTRNK Radio: https://vtrnk.online"
            await update.message.reply_photo(
                photo=cover_url,
                caption=caption,
                reply_markup=reply_markup
            )
        logger.info(f"Sent /radio response: {title} by {artist}")
    except Exception as e:
        logger.error(f"Error in /radio: {str(e)}")
        await update.message.reply_text("Не удалось получить информацию о текущем треке. Попробуйте позже!")

async def monitor_podcast(context: ContextTypes.DEFAULT_TYPE):
    last_track = None  # Последний трек, проверенный на подкаст
    announced_track = None  # Последний трек, о котором был пост
    while True:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                logger.info("Fetching track data for podcast monitoring")
                async with session.get("https://vtrnk.online/track") as track_response:
                    track_data = await track_response.json()
                    logger.info(f"Track response: {track_data}")
                    filename = track_data[0][1] if track_data and len(track_data) > 0 else ""
                    artist = track_data[1][1] if track_data and len(track_data) > 1 else "VTRNK"
                    title = track_data[2][1] if track_data and len(track_data) > 2 else "Radio Show"

                is_podcast = filename.startswith(RADIO_SHOW_DIR)
                if is_podcast and filename != last_track:
                    logger.info(f"Detected potential podcast: {filename}")
                    await asyncio.sleep(60)
                    logger.info("Re-checking track for podcast confirmation")
                    async with session.get("https://vtrnk.online/track") as track_response:
                        track_data = await track_response.json()
                        logger.info(f"Track re-check response: {track_data}")
                        new_filename = track_data[0][1] if track_data and len(track_data) > 0 else ""
                        new_artist = track_data[1][1] if track_data and len(track_data) > 1 else "VTRNK"
                        new_title = track_data[2][1] if track_data and len(track_data) > 2 else "Radio Show"

                    if new_filename == filename and new_filename != announced_track:
                        logger.info("Fetching cover path for podcast")
                        async with session.get("https://vtrnk.online/get_cover_path") as cover_response:
                            cover_data = await cover_response.json()
                            cover_path = cover_data.get("cover_path", "/images/placeholder2.png")
                            file_path = f"{BASE_DIR}{cover_path}" if cover_path.startswith("/") else cover_path
                            logger.info(f"Local file path for podcast: {file_path}")

                        # Проверяем существование файла
                        if os.path.exists(file_path) and os.path.isfile(file_path):
                            logger.info(f"Sending cover as file: {file_path}")
                            with open(file_path, 'rb') as photo:
                                caption = f"Сейчас у нас в эфире радио подкаст {new_title} от {new_artist}. Подключайтесь!"
                                keyboard = [[InlineKeyboardButton("Слушать радио", web_app={"url": "https://vtrnk.online/telegram-mini-app.html"})]]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                logger.info(f"Sending podcast notification: {caption}")
                                await context.bot.send_photo(
                                    chat_id=CHAT_ID,
                                    photo=photo,
                                    caption=caption,
                                    reply_markup=reply_markup
                                )
                        else:
                            logger.error(f"Cover file not found: {file_path}")
                            cover_url = "https://vtrnk.online/images/placeholder2.png"
                            logger.info(f"Falling back to default cover URL: {cover_url}")
                            caption = f"Сейчас у нас в эфире радио подкаст {new_title} от {new_artist}. Подключайтесь!"
                            keyboard = [[InlineKeyboardButton("Слушать радио", web_app={"url": "https://vtrnk.online/telegram-mini-app.html"})]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            await context.bot.send_photo(
                                chat_id=CHAT_ID,
                                photo=cover_url,
                                caption=caption,
                                reply_markup=reply_markup
                            )
                        logger.info(f"Sent podcast notification: {new_title} by {new_artist}")
                        announced_track = new_filename
                    else:
                        logger.info(f"Podcast not confirmed or already announced: {new_filename}")
                    last_track = new_filename
                else:
                    logger.info("No podcast detected or same track")
                    last_track = filename

        except Exception as e:
            logger.error(f"Error in monitor: {str(e)}")

        await asyncio.sleep(60)  # Проверка каждую минуту

def main():
    logger.info("Starting dmum_n_bot")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("radio", radio))
    application.job_queue.run_repeating(monitor_podcast, interval=60, first=0)
    application.run_polling()

if __name__ == "__main__":
    main()