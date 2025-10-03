import os
from dotenv import load_dotenv

load_dotenv()

def test_env_loading():
    assert os.getenv('SOURCE_PASSWORD') is not None, "SOURCE_PASSWORD missing in .env"
    assert os.getenv('ADMIN_PASSWORD') is not None, "ADMIN_PASSWORD missing in .env"
    assert os.path.exists(os.getenv('TRACKS_DIR')), "TRACKS_DIR does not exist"
