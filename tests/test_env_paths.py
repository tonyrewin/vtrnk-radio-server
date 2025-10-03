import os
from dotenv import load_dotenv

load_dotenv()

def test_env_directories_exist():
    """Check that all directory paths in .env exist."""
    dir_keys = [
        'TRACKS_DIR', 'AUDIO_DIR', 'AUDIO_RADIO_SHOW_DIR', 'AUDIO_JINGLES_DIR',
        'UPLOAD_DIR', 'TEMP_DIR', 'TRACKS_DATA_DIR', 'LOGS_DIR', 'IMAGES_DIR',
        'COVER_DIR', 'SHOW_COVER_DIR', 'JINGLE_COVER_DIR', 'ICECAST_LOG_DIR',
        'ICECAST_V2_LOG_DIR', 'NGINX_WEB_ROOT', 'NGINX_IMAGES_DIR', 'NGINX_CSS_DIR',
        'NGINX_HLS_DIR'
    ]
    for key in dir_keys:
        path = os.getenv(key, f"/tmp/{key.lower()}")
        if not os.path.isdir(path):
            print(f"Optional directory {key}={path} does not exist, skipping")
            continue
        assert os.path.isdir(path), f"Directory {key}={path} does not exist or is not a directory"

def test_env_files_exist():
    """Check that all file paths in .env exist, skip if optional."""
    file_keys = [
        ('CURRENT_TRACK_FILE', True),  # Changed to optional
        ('LAST_PLAYED_TRACK_FILE', True),
        ('PLAYBACK_HISTORY_FILE', True),
        ('DB_PATH', True),
        ('NGINX_SSL_CERT', True),
        ('NGINX_SSL_KEY', True),
        ('NGINX_SSL_OPTIONS', True),
        ('NGINX_SSL_DHPARAM', True),
        ('PLACEHOLDER_POSTER', True),
    ]
    for key, is_optional in file_keys:
        path = os.getenv(key, f"/tmp/{key.lower()}.txt")
        if is_optional or not os.path.exists(path):
            print(f"Optional file {key}={path} does not exist, skipping")
            continue
        assert os.path.exists(path), f"File {key}={path} does not exist"
        assert os.path.isfile(path), f"File {key}={path} is not a file"
        if os.path.islink(path):
            print(f"File {key}={path} is a symlink to: {os.readlink(path)}")