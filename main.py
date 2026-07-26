"""
Local/Replit convenience launcher that runs the FastAPI backend and the
Streamlit frontend as two subprocesses in one process.
"""
import subprocess
import sys
import time

import requests

BACKEND_HEALTH_URL = "http://localhost:8000/health"


def run_backend():
    return subprocess.Popen([sys.executable, "backend/main.py"])


def run_frontend():
    return subprocess.Popen(["streamlit", "run", "frontend/main.py"])


def wait_for_backend(timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(BACKEND_HEALTH_URL, timeout=1).ok:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False


if __name__ == "__main__":
    backend_process = run_backend()

    if not wait_for_backend():
        print("Backend didn't come up in time - starting frontend anyway, check backend logs.")

    frontend_process = run_frontend()

    try:
        backend_process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        backend_process.terminate()
        frontend_process.terminate()