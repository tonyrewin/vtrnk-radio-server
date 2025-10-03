# Test Plan for VTRNK Radio

## 1. Introduction
- **Project**: VTRNK Internet Radio
- **Objective**: Ensure stable streaming, functional web UI, secure configuration, and proper handling of paths/logs from .env.
- **Scope**: Testing Icecast streaming, Liquidsoap scripts, web interface (styles.css), paths/dirs from .env, Telnet communication, and Nginx proxies/logs without exposing secrets.
- **Version**: Based on `qa-setup` branch (synced with `main`). Secrets loaded from `.env` (e.g., via python-dotenv in scripts).
- **Security Note**: All sensitive data (passwords, tokens) referenced via .env variables only. Do not hardcode secrets in tests or docs.

## 2. Test Environment
- **Server**: 89.169.174.227
- **Software**: 
  - Liquidsoap (`/home/beasty197/.opam/4.14.0/bin/liquidsoap /home/beasty197/projects/vtrnk_radio/liquidsoap/radio.liq`)
  - Icecast (config loaded from .env: SOURCE_PASSWORD, ADMIN_PASSWORD, etc.)
  - Web UI (`/web/css/styles.css`)
  - Python venv (`source /home/beasty197/projects/vtrnk_radio/venv/bin/activate`)
  - .env for paths (e.g., TRACKS_DIR, AUDIO_DIR, DB_PATH) and secrets (e.g., BOT_TOKEN_DMB, NGINX_SSL_CERT)
- **Tools**: pytest for automation, manual browser testing (Chrome/Firefox), terminal for scripts. Load .env in tests via `os.getenv` or dotenv.

## 3. Test Scenarios
### 3.1 Setup Tests
- Verify venv activation (`source venv/bin/activate`).
- Check .env loading: Ensure scripts access vars like TRACKS_DIR (`/home/beasty197/projects/vtrnk_radio/audio/mp3`), DB_PATH, without errors.
- Validate paths existence: Test if dirs like AUDIO_RADIO_SHOW_DIR, LOGS_DIR, IMAGES_DIR exist and are writable.

### 3.2 Streaming Tests
- Launch Liquidsoap and connect source to Icecast using SOURCE_PASSWORD from .env.
- Verify audio stream playback in browser (e.g., via NGINX_ICECAST_PORT=8000).
- Test stream stability (e.g., 5-minute playback without drops, check logs in ICECAST_LOG_DIR).
- Test v2 stream (ICECAST_V2_PORT=8001, SOURCE_PASSWORD_V2 from .env).

### 3.3 Web UI and Nginx Tests
- Check responsiveness of `/web/css/styles.css` (e.g., green buttons on mobile/desktop).
- Validate Nginx proxies: Test access to NGINX_WEB_ROOT, images in NGINX_IMAGES_DIR, logs in NGINX_ACCESS_LOG etc.
- Test upload endpoints (e.g., UPLOAD_DIR handling) without exposing logs like NGINX_UPLOAD_TRACK_LOG.

### 3.4 Integration Tests
- Telnet communication: Connect to TELNET_HOST:TELNET_PORT, send commands (e.g., skip track), verify response.
- Database and Files: Test SQLite at DB_PATH, metadata in TRACKS_DATA_DIR, history in PLAYBACK_HISTORY_FILE.
- Bot Notifications: Mock send to CHAT_ID with BOT_TOKEN_DMB (test without real send, check env load).
- Limits: Verify MP3_LIMIT (300 tracks in AUDIO_DIR), RADIO_SHOW_LIMIT (20 in AUDIO_RADIO_SHOW_DIR).

### 3.5 Security and Edge Cases
- Test invalid password input (e.g., wrong SOURCE_PASSWORD — expect auth error, without revealing real value).
- Simulate Liquidsoap crash and verify recovery (check logs in LOGS_DIR).
- Check SSL in Nginx (NGINX_SSL_CERT, NGINX_SSL_KEY — verify HTTPS without exposing paths).
- Edge: Overlimit dirs (e.g., >MP3_LIMIT tracks — expect cleanup or error).

## 4. Test Execution
- **Manual**: Run Liquidsoap, test stream in browser, check UI and paths.
- **Automated**: Use pytest for config/path checks (in `/tests/`), load .env in tests.
- **Schedule**: Run tests after each merge from `dev` to `qa-setup`.

## 5. Defect Tracking
- Use GitHub Issues with labels: `bug`, `test-case`, `qa-review`.
- Example: Log stream disconnects as bugs with steps to reproduce (reference .env vars, not values).

## 6. Risks
- **Risk**: .env misload leading to path/password errors.
- **Mitigation**: Add env validation in setup tests.
- **Risk**: UI breaks on mobile due to CSS issues.
- **Mitigation**: Test responsiveness across devices.
- **Risk**: Secret exposure in logs (e.g., NGINX_ERROR_LOG).
- **Mitigation**: Review logs for leaks, use mocked values in tests.

## 7. Deliverables
- Test Plan (this document).
- Test scripts in `/tests/` (with .env integration).
- Bug reports in GitHub Issues.