import os
import subprocess
from mutagen.id3 import ID3, TIT2, TPE1, APIC
from mutagen.flac import FLAC
from mutagen.wave import WAVE
import logging
from datetime import datetime
import time
import shutil
import json
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

# Настройка логирования с fallback
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.getenv('LOGS_DIR'), 'upload_manager.log'), mode='a'),
            logging.StreamHandler()
        ]
    )
except Exception as e:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    print(f"Ошибка настройки файл-лога: {str(e)}. Используем только консоль.")

logger = logging.getLogger(__name__)

# Константы из .env
UPLOAD_DIR = os.getenv('UPLOAD_DIR')
AUDIO_DIR = os.getenv('AUDIO_DIR')
AUDIO_RADIO_SHOW_DIR = os.getenv('AUDIO_RADIO_SHOW_DIR')
COVER_DIR = os.getenv('COVER_DIR')
TEMP_DIR = os.getenv('TEMP_DIR')
PLACEHOLDER_POSTER = os.getenv('PLACEHOLDER_POSTER')
PLACEHOLDER_RELATIVE = os.getenv('PLACEHOLDER_RELATIVE')
MP3_LIMIT = int(os.getenv('MP3_LIMIT', 200))
RADIO_SHOW_LIMIT = int(os.getenv('RADIO_SHOW_LIMIT', 20))

# Создание директорий
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(AUDIO_RADIO_SHOW_DIR, exist_ok=True)
os.makedirs(COVER_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def get_cover_art(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        data = None
        mime = 'image/jpeg'  # Default
        if ext == '.mp3':
            audio = ID3(file_path)
            for tag in audio.values():
                if tag.FrameID == 'APIC':
                    data = tag.data
                    mime = tag.mime
                    break
        elif ext == '.flac':
            audio = FLAC(file_path)
            if audio.pictures:
                data = audio.pictures[0].data
                mime = audio.pictures[0].mime
        elif ext == '.wav':
            audio = WAVE(file_path)
            for tag in audio.values():
                if tag.FrameID == 'APIC':
                    data = tag.data
                    mime = tag.mime
                    break
        if data:
            if 'png' in mime.lower():
                return data, '.png'
            else:
                return data, '.jpg'
        return None, None
    except Exception as e:
        logger.error(f"Ошибка извлечения обложки из {file_path}: {str(e)}")
        return None, None

def get_track_info(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.mp3':
            audio = ID3(file_path)
            artist = audio.get('TPE1', ["VTRNK"]).text[0]
            title = audio.get('TIT2', [os.path.basename(file_path).split('.')[0]]).text[0]
        elif ext == '.flac':
            audio = FLAC(file_path)
            artist = audio.get('artist', ["VTRNK"])[0]
            title = audio.get('title', [os.path.basename(file_path).split('.')[0]])[0]
        elif ext == '.wav':
            audio = WAVE(file_path)
            artist = audio.get('TPE1', ["VTRNK"]).text[0]
            title = audio.get('TIT2', [os.path.basename(file_path).split('.')[0]]).text[0]
        return artist, title
    except Exception as e:
        logger.error(f"Ошибка извлечения метаданных из {file_path}: {str(e)}")
        return "VTRNK", os.path.basename(file_path).split('.')[0]

def update_metadata(file_path, title, author, cover_data=None, cover_mime='image/jpeg'):
    try:
        audio = ID3(file_path)
        audio['TIT2'] = TIT2(encoding=3, text=title)
        audio['TPE1'] = TPE1(encoding=3, text=author)
        if cover_data:
            audio['APIC'] = APIC(
                encoding=3,
                mime=cover_mime,
                type=3,
                desc='Cover',
                data=cover_data
            )
        audio.save()
        logger.info(f"Обновлены метаданные для {file_path}: title={title}, author={author}, cover={'added' if cover_data else 'not added'}")
    except Exception as e:
        logger.error(f"Ошибка обновления метаданных для {file_path}: {str(e)}")
        raise

def convert_to_mp3(input_path, output_path):
    try:
        subprocess.run([
            'ffmpeg', '-i', input_path, '-c:a', 'libmp3lame', '-q:a', '2',
            '-map_metadata', '0', '-metadata', 'playcount=0', output_path, '-y', '-loglevel', 'error'
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Конвертирован в MP3: {os.path.basename(output_path)}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка конвертации в MP3: {e.stderr.decode()}")
        raise
    except Exception as e:
        logger.error(f"Неизвестная ошибка при конвертации: {str(e)}")
        raise

def process_file(file_path):
    file_name = os.path.basename(file_path)
    logger.info(f"Обнаружен файл: {file_name}, жду завершения загрузки...")
    time.sleep(5)

    if file_name.endswith('.filepart'):
        logger.warning(f"Файл {file_name} ещё загружается, пропускаю.")
        return

    temp_path = os.path.join(TEMP_DIR, file_name)
    shutil.copy2(file_path, temp_path)

    author, title = get_track_info(temp_path)
    cover_data, cover_ext = get_cover_art(temp_path)
    cover_mime = 'image/png' if cover_ext == '.png' else 'image/jpeg'

    if file_name.lower().endswith(('.flac', '.wav')):
        mp3_name = file_name.rsplit('.', 1)[0] + '.mp3'
        mp3_path = os.path.join(AUDIO_DIR, mp3_name)
        convert_to_mp3(temp_path, mp3_path)
        os.remove(temp_path)
        update_metadata(mp3_path, title, author, cover_data, cover_mime)
    elif file_name.lower().endswith('.mp3'):
        mp3_path = os.path.join(AUDIO_DIR, file_name)
        shutil.move(temp_path, mp3_path)
    else:
        logger.error(f"Не поддерживаемый формат: {file_name}")
        os.remove(temp_path)
        os.remove(file_path)
        return

    if not os.path.exists(mp3_path):
        logger.error(f"MP3 не создан: {mp3_path}")
        os.remove(file_path)
        return

    mp3_name = os.path.basename(mp3_path)
    cover_saved = False
    if cover_data:
        cover_path = os.path.join(COVER_DIR, mp3_name.replace('.mp3', cover_ext or '.jpg'))
        try:
            with open(cover_path, 'wb') as f:
                f.write(cover_data)
            logger.info(f"Сохранена обложка: {cover_path}")
            cover_saved = True
        except Exception as e:
            logger.error(f"Ошибка сохранения обложки: {str(e)}")
    if not cover_saved:
        cover_path = os.path.join(COVER_DIR, mp3_name.replace('.mp3', '.jpg'))
        shutil.copy2(PLACEHOLDER_POSTER, cover_path)
        logger.info(f"Плейсхолдер для обложки: {cover_path}")
        cover_ext = '.jpg'

    track_data_path = os.path.join(os.path.dirname(AUDIO_DIR), 'data/tracks', mp3_name.replace('.mp3', '.json'))
    track_data = {
        "name": mp3_name,
        "cover": f"/images/track_covers/{mp3_name.replace('.mp3', cover_ext)}" if cover_saved else PLACEHOLDER_RELATIVE,
        "title": f"{author} - {title}",
        "style": "",
        "history": "",
        "uploaded_by": "manual_upload",
        "upload_date": datetime.now().strftime("%Y-%m-%d")
    }
    with open(track_data_path, 'w') as f:
        json.dump(track_data, f)
    logger.info(f"Сохранены данные трека: {track_data_path}")

    os.chmod(mp3_path, 0o644)
    logger.info(f"Права 644 на {mp3_path}")

    os.remove(file_path)
    logger.info(f"Удалён исходный: {file_path}")

def manage_files():
    # Управление mp3
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')]
    if len(files) > MP3_LIMIT:
        logger.info(f"Найдено {len(files)} mp3-файлов, превышает MP3_LIMIT ({MP3_LIMIT}), удаляю старые.")
        files.sort(key=lambda x: os.path.getctime(os.path.join(AUDIO_DIR, x)))
        for old_file in files[:-MP3_LIMIT]:
            file_path = os.path.join(AUDIO_DIR, old_file)
            os.remove(file_path)
            logger.info(f"Удалён старый mp3-файл: {file_path}")
            cover_path = os.path.join(COVER_DIR, old_file.replace('.mp3', '.jpg'))
            if os.path.exists(cover_path):
                os.remove(cover_path)
                logger.info(f"Удалена обложка: {cover_path}")
            png_path = os.path.join(COVER_DIR, old_file.replace('.mp3', '.png'))
            if os.path.exists(png_path):
                os.remove(png_path)
                logger.info(f"Удалена обложка: {png_path}")

    # Управление радио-шоу
    radio_files = [f for f in os.listdir(AUDIO_RADIO_SHOW_DIR) if f.endswith('.mp3')]
    if len(radio_files) > RADIO_SHOW_LIMIT:
        logger.info(f"Найдено {len(radio_files)} радио-шоу, превышает RADIO_SHOW_LIMIT ({RADIO_SHOW_LIMIT}), удаляю старые.")
        radio_files.sort(key=lambda x: os.path.getctime(os.path.join(AUDIO_RADIO_SHOW_DIR, x)))
        for old_file in radio_files[:-RADIO_SHOW_LIMIT]:
            file_path = os.path.join(AUDIO_RADIO_SHOW_DIR, old_file)
            os.remove(file_path)
            logger.info(f"Удалён старый файл радио-шоу: {file_path}")

def main():
    logger.info("Запуск скрипта для управления загрузками...")
    while True:
        for file_name in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if os.path.isfile(file_path):
                logger.info(f"Обнаружен файл для обработки: {file_name}")
                try:
                    process_file(file_path)
                    manage_files()
                except Exception as e:
                    logger.error(f"Ошибка обработки файла {file_name}: {str(e)}")
                    if os.path.exists(file_path):
                        os.remove(file_path)
        time.sleep(10)

if __name__ == "__main__":
    main()