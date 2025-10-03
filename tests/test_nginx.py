import requests

def test_nginx_availability():
    """Check that Nginx serves http://vtrnk.online."""
    try:
        response = requests.get("http://vtrnk.online", timeout=5)
        assert response.status_code == 200, f"Nginx returned status {response.status_code}"
    except requests.ConnectionError:
        assert False, "Failed to connect to http://vtrnk.online"
