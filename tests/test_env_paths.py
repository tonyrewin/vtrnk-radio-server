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
        path = os.getenv(key)
        assert path is not None, f"{key} is not defined in .env"
        assert os.path.isdir(path), f"Directory {key}={path} does not exist or is not a directory"

def test_env_files_exist():
    """Check that all file paths in .env exist, skip if optional."""
    # (ключ, optional=True/False)
    file_keys = [
        ('CURRENT_TRACK_FILE', False),
        ('LAST_PLAYED_TRACK_FILE', False),
        ('PLAYBACK_HISTORY_FILE', False),
        ('DB_PATH', False),
        ('NGINX_SSL_CERT', True),  # Optional SSL, may be symlink
        ('NGINX_SSL_KEY', True),   # Optional SSL
        ('NGINX_SSL_OPTIONS', True),  # Optional SSL
        ('NGINX_SSL_DHPARAM', True),  # Optional SSL
        ('PLACEHOLDER_POSTER', False),
    ]
    for key, is_optional in file_keys:
        path = os.getenv(key)
        assert path is not None, f"{key} is not defined in .env"
        
        if is_optional and not os.path.exists(path):
            print(f"Optional file {key}={path} does not exist, skipping")
            continue
            
        # Проверяем существование
        assert os.path.exists(path), f"File {key}={path} does not exist"
        
        # Проверяем, что это файл (для симлинков работает)
        assert os.path.isfile(path), f"File {key}={path} is not a file (symlink check passed)"
        
        # Логируем для симлинков
        if os.path.islink(path):
            print(f"File {key}={path} is a symlink to: {os.readlink(path)}")