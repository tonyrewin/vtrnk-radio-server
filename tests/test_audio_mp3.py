import os
from dotenv import load_dotenv

load_dotenv()

def test_audio_mp3_directory():
    audio_dir = os.getenv('AUDIO_DIR')
    assert audio_dir is not None, "AUDIO_DIR not defined in .env"
    assert os.path.exists(audio_dir), f"Directory {audio_dir} does not exist"
    assert os.path.isdir(audio_dir), f"{audio_dir} is not a directory"  
    try:
        files = os.listdir(audio_dir)  
    except OSError as e:
        raise AssertionError(f"Cannot list files in {audio_dir}: {e}")
    assert len(files) > 0, f"No files in directory {audio_dir}"
    mp3_files = [f for f in files if f.lower().endswith('.mp3')]
    assert len(mp3_files) == len(files), f"Not all files are MP3 in {audio_dir}: {len(files) - len(mp3_files)} non-MP3 files"  # Добавил пробел после :
    print(f"Directory {audio_dir} has {len(files)} MP3 files")  