import requests
import time

def test_page_load_time():
    """Check that http://vtrnk.online loads within 5 seconds."""
    start_time = time.time()
    try:
        response = requests.get("http://vtrnk.online", timeout=5)
        load_time = time.time() - start_time
        assert response.status_code == 200, f"Nginx returned status {response.status_code}"
        assert load_time < 5, f"Page load time {load_time:.2f}s exceeds 5s limit"
        print(f"Page load time: {load_time:.2f}s")
    except requests.ConnectionError:
        assert False, "Failed to connect to http://vtrnk.online"
