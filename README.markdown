# VTRNK Radio Server

A server-side implementation of an internet radio streaming service built with Liquidsoap for audio streaming and playlist management. This repository contains configuration templates, Python scripts for managing tracks and uploads, and web interface styles, showcasing skills in server-side scripting, configuration management, and deployment on Ubuntu.

## Project Structure

- **liquidsoap/**: Liquidsoap configuration templates (no sensitive data).
  - `radio-template.liq`: Sample configuration file (replace with your own parameters).
- **web/css/**: Styles for the web interface.
  - `styles.css`: CSS for buttons and UI components.
- **scripts/**: Python scripts for managing the radio server.
  - `radio_player.py`: Flask-based server for controlling Liquidsoap and handling track playback.
  - `track_watcher.py`: Monitors audio directories and syncs track metadata with the database.
  - `upload_manager.py`: Processes uploaded audio files and converts them to MP3.

## Scripts Overview

### radio_player.py
- **Purpose**: Manages the radio playback system, serving as the core backend for track playback, scheduling, and API endpoints.
- **Functions**:
  - Communicates with Liquidsoap via Telnet (`127.0.0.1:1234`) to control track playback (`play_radio_show`, `play_jingle`, `skip_track`).
  - Provides API endpoints (`/track`, `/upload_radio_show`, `/play_radio_show`, `/get_cover_path`, etc.) for track metadata, uploads, and scheduling.
  - Maintains playback history (`/data/playback_history.txt`, up to 30 tracks) and current track info (`/data/radio_current_track.txt`).
  - Uses WebSocket (SocketIO) to push real-time updates (`track_update`, `track_added_special`) to clients.
  - Schedules radio shows via a database (`radio.db`, table `schedule`) with a 5-minute window for playback.
- **Why Needed**: Centralizes control of the radio stream, integrates with Liquidsoap, and exposes APIs for the web interface and bot (`@drum_n_bot`).

### track_watcher.py
- **Purpose**: Monitors audio directories and maintains the track database (`radio.db`) for consistency.
- **Functions**:
  - Scans directories (`/audio/mp3`, `/audio/radio_show`, `/audio/jingles`) every 10 seconds for new MP3 files.
  - Extracts metadata (`artist`, `title`, `style`, `duration`) using `mutagen` and adds tracks to the `tracks` table in `radio.db`.
  - Saves cover art to `/images/track_covers`, `/images/show_covers`, or `/images/jingle_covers` from MP3 tags (`APIC`).
  - Synchronizes the database with the filesystem, marking deleted files as `status='deleted'` and cleaning up (`delete_marked_files`).
  - Limits radio shows to 20 files in `/audio/radio_show`, removing older files and updating the database.
- **Why Needed**: Ensures the database reflects the current state of audio files, providing accurate metadata for playback and the bot.

### upload_manager.py
- **Purpose**: Handles file uploads, converting non-MP3 formats to MP3 and managing file limits.
- **Functions**:
  - Monitors `/audio/upload_dir` every 10 seconds for new files (MP3, FLAC, WAV).
  - Converts FLAC/WAV to MP3 using `ffmpeg`, preserving metadata (`artist`, `title`, `cover`).
  - Saves tracks to `/audio/mp3` and cover art to `/images/track_covers`.
  - Creates JSON metadata files in `/data/tracks` for each track.
  - Limits MP3 files in `/audio/mp3` to 200 and radio shows in `/audio/radio_show` to 20, deleting older files.
- **Why Needed**: Automates the processing of uploaded audio, ensuring compatibility (MP3) and maintaining storage limits.

## Requirements

- Liquidsoap (installed at `~/.opam/4.14.0/bin/liquidsoap`).
- Python virtual environment (`venv/` for dependencies).
- Ubuntu 24.04+ (or compatible OS).
- FFmpeg (for `upload_manager.py` conversions).

## Setup Instructions

1. Activate the virtual environment:
   ```bash
   source /home/beasty197/projects/vtrnk_radio/venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run Liquidsoap with your local configuration (not included in this repo):
   ```bash
   /home/beasty197/.opam/4.14.0/bin/liquidsoap liquidsoap/radio.liq
   ```

4. Configure `.env` with your credentials and paths (excluded from git):
   ```bash
   nano .env
   ```
   Example:
   ```
   BOT_TOKEN_DMB=your_token
   CHAT_ID=your_chat_id
   DB_PATH=/home/beasty197/projects/vtrnk_radio/data/radio.db
   AUDIO_DIR=/home/beasty197/projects/vtrnk_radio/audio/mp3
   AUDIO_RADIO_SHOW_DIR=/home/beasty197/projects/vtrnk_radio/audio/radio_show
   AUDIO_JINGLES_DIR=/home/beasty197/projects/vtrnk_radio/audio/jingles
   COVER_DIR=/home/beasty197/projects/vtrnk_radio/images/track_covers
   SHOW_COVER_DIR=/home/beasty197/projects/vtrnk_radio/images/show_covers
   JINGLE_COVER_DIR=/home/beasty197/projects/vtrnk_radio/images/jingle_covers
   TRACKS_DATA_DIR=/home/beasty197/projects/vtrnk_radio/data/tracks
   LOGS_DIR=/home/beasty197/projects/vtrnk_radio/logs
   ```

5. Start systemd services for scripts:
   ```bash
   sudo systemctl start drum_n_bot track_watcher upload_manager
   ```

## Notes

- All sensitive data (passwords, tokens, paths) is stored in `.env` and excluded via `.gitignore` for security.
- Use `radio-template.liq` as a base and add your own parameters.
- Logs are stored in `/home/beasty197/projects/vtrnk_radio/logs/` (e.g., `drum_n_bot.log`, `track_watcher.log`, `upload_manager.log`).
- This project demonstrates proficiency in Linux server management, Liquidsoap scripting, Python automation, and secure configuration practices.

## QA Process

- **Test Plan**: [qa/test-plan.markdown](qa/test-plan.markdown)
- **Automated Tests**:
  - `tests/test_config.py`: Validates `.env` configuration (e.g., `SOURCE_PASSWORD`, `TRACKS_DIR`).
  - `tests/test_database.py`: Checks `radio.db` and `channels.db` connectivity and schema.
  - `tests/test_env_paths.py`: Verifies paths and files from `.env`.
  - `tests/test_stream.py`: Ensures Liquidsoap starts correctly.
  - `tests/test_telnet.py`: Tests Telnet server connectivity (127.0.0.1:1234).
  - `tests/test_css.py`: Temporarily disabled due to ChromeDriver compatibility issues (Issue #7).
  - `tests/test_nginx.py`: Confirms Nginx availability (HTTP 200).
  - `tests/test_performance.py`: Verifies page load time (<5s).
  - `tests/test_api.py`: Tests /track API endpoint (HTTP 200, valid JSON).
  - `tests/test_ssl.py`: Verifies HTTPS and SSL certificate validity (Issue #11).
- **Test Plan Coverage**: All components (.env, Liquidsoap, databases, Telnet, Nginx, performance, API, SSL) tested, except Web UI buttons (pending ChromeDriver fix, Issue #7).
- **CI/CD**: GitHub Actions runs `pytest` (excluding test_css.py) on push to `qa-setup` branch (https://github.com/Beasty177/vtrnk-radio-server/actions).
- **Issues**: Bug tracking and test cases (#2-#11) at https://github.com/Beasty177/vtrnk-radio-server/issues.

## License
MIT