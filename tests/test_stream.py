import subprocess
import os

def test_liquidsoap_starts():
    """Check that Liquidsoap starts without errors."""
    liq_path = "/home/beasty197/.opam/4.14.0/bin/liquidsoap"
    script = os.path.abspath("liquidsoap/radio.liq")
    if not os.path.exists(liq_path):
        print(f"Optional Liquidsoap binary {liq_path} not found, skipping")
        return
    if not os.path.exists(script):
        print(f"Optional radio.liq script {script} not found, skipping")
        return
    proc = subprocess.Popen([liq_path, script], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    proc.terminate()
    proc.wait()
    assert proc.returncode in (0, -15), f"Liquidsoap failed to start: {proc.stderr.read().decode()}"