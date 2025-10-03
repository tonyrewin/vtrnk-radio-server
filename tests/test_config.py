import os
from dotenv import load_dotenv

load_dotenv()

def test_env_loading():
    """Check that essential .env variables are defined."""
    # Check critical variables (fail if missing)
    assert os.getenv('SOURCE_PASSWORD') is not None, "SOURCE_PASSWORD missing in .env"
    assert os.getenv('ADMIN_PASSWORD') is not None, "ADMIN_PASSWORD missing in .env"
    
    # Check optional path variable
    tracks_dir = os.getenv('TRACKS_DIR', '/tmp/dummy')
    if not os.path.exists(tracks_dir):
        print(f"Optional TRACKS_DIR={tracks_dir} does not exist, skipping")
        return
    assert os.path.exists(tracks_dir), "TRACKS_DIR does not exist"