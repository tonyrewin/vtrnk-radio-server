from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import os
import tempfile

def parse_color(color_str):
    """Parse color string to RGB values for comparison."""
    color_str = color_str.lower()
    rgba_match = re.match(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)', color_str)
    if rgba_match:
        r, g, b = map(int, rgba_match.groups())
        return (r, g, b)
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color_str)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        return (r, g, b)
    return None

def test_play_stop_button():
    """Check that play-stop-btn in /web/css/styles.css is grey and clickable."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=390,844")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1")
    if os.environ.get('CI'):
        chrome_options.binary_location = '/snap/bin/chromium'
        # Use unique user data dir to avoid conflicts
        temp_dir = tempfile.mkdtemp(prefix='chromium_play_stop_')
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("http://vtrnk.online")
        time.sleep(2)
        buttons = driver.find_elements(By.CLASS_NAME, "play-stop-btn")
        assert len(buttons) > 0, "No play-stop-btn found on page"
        
        for button in buttons:
            color = button.value_of_css_property("background-color")
            rgb = parse_color(color)
            assert rgb == (51, 51, 51), f"Play-stop-btn color is not grey (#333): {color} -> RGB {rgb}"
            assert button.is_enabled(), f"Play-stop-btn is not clickable: {button.text}"
        
        print("All play-stop-btn buttons are grey (#333) and clickable")
    
    finally:
        driver.quit()

def test_hamburger_button():
    """Check that hamburger-icon in /web/css/styles.css is transparent and clickable."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=390,844")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1")
    if os.environ.get('CI'):
        chrome_options.binary_location = '/snap/bin/chromium'
        temp_dir = tempfile.mkdtemp(prefix='chromium_hamburger_')
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("http://vtrnk.online")
        time.sleep(2)
        buttons = driver.find_elements(By.CLASS_NAME, "hamburger-icon")
        assert len(buttons) > 0, "No hamburger-icon found on page"
        
        for button in buttons:
            color = button.value_of_css_property("background-color")
            assert "rgba(0, 0, 0, 0)" in color.lower() or "transparent" in color.lower(), f"Hamburger-icon color is not transparent: {color}"
            assert button.is_enabled(), f"Hamburger-icon is not clickable: {button.text}"
        
        print("All hamburger-icon buttons are transparent and clickable")
    
    finally:
        driver.quit()