import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

def test_radio_db_connectivity():
    """Check that radio.db exists and is accessible."""
    db_path = os.getenv('DB_PATH', '/tmp/radio.db')
    if not os.path.isfile(db_path):
        print(f"Optional radio.db={db_path} does not exist, skipping")
        return
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
    except sqlite3.Error as e:
        assert False, f"Failed to connect to radio.db {db_path}: {str(e)}"

def test_radio_db_schema():
    """Check that expected tables exist in radio.db."""
    db_path = os.getenv('DB_PATH', '/tmp/radio.db')
    if not os.path.isfile(db_path):
        print(f"Optional radio.db={db_path} does not exist, skipping")
        return
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        expected_tables = ['tracks', 'history', 'schedule', 'listeners_stats']
        for table in expected_tables:
            assert table in tables, f"Table {table} not found in radio.db"
    except sqlite3.Error as e:
        assert False, f"Failed to check schema in radio.db {db_path}: {str(e)}"

def test_channels_db_connectivity():
    """Check that channels.db exists and is accessible."""
    db_path = "/home/beasty197/projects/vtrnk_radio/data/channels.db"
    if not os.path.isfile(db_path):
        print(f"Optional channels.db={db_path} does not exist, skipping")
        return
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
    except sqlite3.Error as e:
        assert False, f"Failed to connect to channels.db {db_path}: {str(e)}"

def test_channels_db_schema():
    """Check that expected tables exist in channels.db."""
    db_path = "/home/beasty197/projects/vtrnk_radio/data/channels.db"
    if not os.path.isfile(db_path):
        print(f"Optional channels.db={db_path} does not exist, skipping")
        return
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        expected_tables = ['users_channels']
        for table in expected_tables:
            assert table in tables, f"Table {table} not found in channels.db"
    except sqlite3.Error as e:
        assert False, f"Failed to check schema in channels.db {db_path}: {str(e)}"