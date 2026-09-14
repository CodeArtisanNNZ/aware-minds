"""Start the current Aware Minds release and open it in the default browser."""
from __future__ import annotations

import logging
import os
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA_DIR = Path(os.environ.get("LOCALAPPDATA", ROOT / "data")) / "AwareMinds"
DATA_DIR.mkdir(parents=True, exist_ok=True)
os.environ["AWARE_MINDS_DATA_DIR"] = str(DATA_DIR)
os.environ["SERVE_WEB"] = "1"
os.environ["AI_PROVIDER"] = "disabled"
os.environ["AWARE_MINDS_ENABLE_ACCOUNTS"] = "0"

# Use a release-specific port so an obsolete Aware Minds process on the old
# development port cannot impersonate this build and serve stale frontend files.
HOST = "127.0.0.1"
PORT = 8765
BASE_URL = f"http://{HOST}:{PORT}"
URL = BASE_URL + "/hub"

logging.basicConfig(
    filename=DATA_DIR / "aware-minds.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def current_release_running() -> bool:
    try:
        with urllib.request.urlopen(BASE_URL + "/health", timeout=1) as response:
            if response.status != 200:
                return False
        with urllib.request.urlopen(BASE_URL + "/assets/app.js", timeout=1) as response:
            marker = response.read(4096)
        return b"START WHERE YOU ARE" in marker or b"Beginner" in marker
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def port_available() -> bool:
    with socket.socket() as probe:
        try:
            probe.bind((HOST, PORT))
            return True
        except OSError:
            return False


def open_browser_when_ready(server) -> None:
    for _ in range(100):
        if server.started:
            webbrowser.open(URL, new=2)
            return
        time.sleep(0.1)


def main() -> None:
    os.chdir(ROOT)
    if current_release_running():
        webbrowser.open(URL, new=2)
        return
    if not port_available():
        raise RuntimeError(
            f"Port {PORT} is occupied by another application. "
            "Close the older Aware Minds process in Task Manager and try again."
        )

    from scripts.prepare_local import prepare
    prepare(ROOT, DATA_DIR)

    import uvicorn
    config = uvicorn.Config(
        "services.api.main:app",
        host=HOST,
        port=PORT,
        log_level="warning",
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    threading.Thread(
        target=open_browser_when_ready,
        args=(server,),
        daemon=True,
    ).start()
    server.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logging.exception("Aware Minds failed to start")
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                f"Aware Minds could not start.\n\n{type(exc).__name__}: {exc}\n\nLog: {DATA_DIR / 'aware-minds.log'}",
                "Aware Minds",
                0x10,
            )
        except Exception:
            pass
