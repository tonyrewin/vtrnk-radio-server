from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_play_stop_button():
    """Check that play-stop-btn in /web/css/styles.css is grey and clickable."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Simulate mobile view (iPhone 12 Pro)
    chrome_options.add_argument("--window-size=390,844")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("http://vtrnk.online")
        time.sleep(2)  # Wait for CSS to load
        buttons = driver.find_elements(By.CLASS_NAME, "play-stop-btn")
        assert len(buttons) > 0, "No play-stop-btn found on page"
        
        for button in buttons:
            color = button.value_of_css_property("background-color")
            assert any(s in color.lower() for s in ["grey", "#333", "rgb(51, 51, 51)", "rgba(51, 51, 51, 1)"]), f"Play-stop-btn color is not grey: {color}"
            assert button.is_enabled(), f"Play-stop-btn is not clickable: {button.text}"
        
        print("All play-stop-btn buttons are grey (#333 or rgba(51, 51, 51, 1)) and clickable")
    
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