import os
import telnetlib
import time
from dotenv import load_dotenv

load_dotenv()

def test_telnet_config():
    """Check that Telnet configuration is defined in .env."""
    assert os.getenv('TELNET_HOST') is not None, "TELNET_HOST is not defined in .env"
    assert os.getenv('TELNET_PORT') is not None, "TELNET_PORT is not defined in .env"
    assert os.getenv('TELNET_HOST') == '127.0.0.1', "TELNET_HOST is not 127.0.0.1"
    assert os.getenv('TELNET_PORT') == '1234', "TELNET_PORT is not 1234"

def test_telnet_connectivity():
    """Check that Telnet server is running and accepts connections."""
    host = os.getenv('TELNET_HOST', '127.0.0.1')
    port = os.getenv('TELNET_PORT', '1234')
    
    try:
        # Connect to Telnet server
        tn = telnetlib.Telnet(host, port, timeout=5)
        # Send a simple command
        tn.write(b'help\n')
        # Wait briefly for response
        time.sleep(1)
        response = tn.read_very_eager().decode('ascii', errors='ignore')
        tn.close()
        # Check if response contains expected content (e.g., list of commands)
        assert len(response) > 0, "No response from Telnet server"
        assert 'HELP' in response.upper() or 'COMMANDS' in response.upper(), "Invalid Telnet response"
    except ConnectionRefusedError:
        assert False, f"Failed to connect to Telnet server at {host}:{port}"
    except Exception as e:
        assert False, f"Telnet test failed: {str(e)}"
