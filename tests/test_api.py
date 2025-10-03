import requests
import json

def test_track_api():
    """Check that /track endpoint returns valid data."""
    try:
        response = requests.get("http://vtrnk.online/track", timeout=5)
        assert response.status_code == 200, f"/track returned status {response.status_code}"
        data = response.json()
        assert isinstance(data, list) or isinstance(data, dict), "Response is not valid JSON"
        if isinstance(data, list):
            assert len(data) > 0, "Response is empty"
            assert any("artist" in item or item[0] == "artist" for item in data), "No artist field in response"
            assert any("title" in item or item[0] == "title" for item in data), "No title field in response"
        else:
            assert "artist" in data, "No artist field in response"
            assert "title" in data, "No title field in response"
        print("Track API returned valid data")
    except requests.ConnectionError:
        assert False, "Failed to connect to /track"
