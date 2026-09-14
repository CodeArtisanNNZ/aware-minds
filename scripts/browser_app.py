"""Start Aware Minds silently and open its workspace in the default browser."""
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
URL = "http://127.0.0.1:8000/hub"

logging.basicConfig(
    filename=DATA_DIR / "aware-minds.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def aware_minds_running() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=1) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def port_available() -> bool:
    with socket.socket() as probe:
        try:
            probe.bind(("127.0.0.1", 8000))
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
    if aware_minds_running():
        webbrowser.open(URL, new=2)
        return
    if not port_available():
        raise RuntimeError("Port 8000 is used by another application.")

    from scripts.prepare_local import prepare
    prepare(ROOT, DATA_DIR)

    import uvicorn
    config = uvicorn.Config(
        "services.api.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning",
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    threading.Thread(target=open_browser_when_ready, args=(server,), daemon=True).start()
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
