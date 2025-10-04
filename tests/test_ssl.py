import requests
import ssl
import socket
from urllib.parse import urlparse

def test_ssl_configuration():
    """Check that https://vtrnk.online serves with valid SSL."""
    url = "https://vtrnk.online"
    try:
        response = requests.get(url, timeout=5, verify=True)
        assert response.status_code == 200, f"HTTPS returned status {response.status_code}"
        
        # Check SSL certificate
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                assert cert, "No SSL certificate found"
                print("SSL certificate is valid")
    except requests.ConnectionError:
        assert False, "Failed to connect to https://vtrnk.online"
    except ssl.SSLError:
        assert False, "Invalid SSL certificate"
