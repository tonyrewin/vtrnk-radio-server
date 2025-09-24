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
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Фильтр для исключения DEBUG-логов
class NoDebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno > logging.DEBUG
handler.addFilter(NoDebugFilter())
logger.addHandler(handler)

# Загрузка .env
load_dotenv('/home/beasty197/projects/vtrnk_radio/.env')
BOT_TOKEN = os.getenv('BOT_TOKEN_DMB')
CHAT_ID = os.getenv('CHAT_ID')
RADIO_SHOW_DIR = '/home/beasty197/projects/vtrnk_radio/audio/radio_show'

async def radio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            # Получаем текущий трек
            async with session.get("https://vtrnk.online/track") as track_response:
                track_data = await track_response.json()
                artist = track_data[1][1] if track_data and len(track_data) > 1 else "VTRNK"
                title = track_data[2][1] if track_data and len(track_data) > 2 else "Unknown Track"

            # Получаем обложку
            async with session.get("https://vtrnk.online/get_cover_path") as cover_response:
                cover_data = await cover_response.json()
                cover_url = cover_data.get("cover_path", "https://vtrnk.online/images/placeholder2.png")

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
            async with aiohttp.ClientSession() as session:
                # Получаем текущий трек
                async with session.get("https://vtrnk.online/track") as track_response:
                    track_data = await track_response.json()
                    filename = track_data[0][1] if track_data and len(track_data) > 0 else ""
                    artist = track_data[1][1] if track_data and len(track_data) > 1 else "VTRNK"
                    title = track_data[2][1] if track_data and len(track_data) > 2 else "Radio Show"

                # Проверяем, является ли трек подкастом
                is_podcast = filename.startswith(RADIO_SHOW_DIR)
                if is_podcast and filename != last_track:
                    logger.info(f"Detected potential podcast: {filename}")
                    # Ждём минуту для повторной проверки
                    await asyncio.sleep(60)
                    # Проверяем снова
                    async with session.get("https://vtrnk.online/track") as track_response:
                        track_data = await track_response.json()
                        new_filename = track_data[0][1] if track_data and len(track_data) > 0 else ""
                        new_artist = track_data[1][1] if track_data and len(track_data) > 1 else "VTRNK"
                        new_title = track_data[2][1] if track_data and len(track_data) > 2 else "Radio Show"

                    # Если трек тот же и это подкаст, делаем пост
                    if new_filename == filename and new_filename != announced_track:
                        async with session.get("https://vtrnk.online/get_cover_path") as cover_response:
                            cover_data = await cover_response.json()
                            cover_url = cover_data.get("cover_path", "https://vtrnk.online/images/placeholder2.png")

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
                        announced_track = new_filename  # Запоминаем, чтобы не дублировать
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
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("radio", radio))
    application.job_queue.run_repeating(monitor_podcast, interval=60, first=0)
    application.run_polling()

if __name__ == "__main__":
    main()