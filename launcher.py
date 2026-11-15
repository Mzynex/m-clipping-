"""Starts The M clipping from the Windows exe: sets up folders next to the exe, starts the server, opens the browser."""
import os
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

HOME = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent

# Everything the app keeps lives beside the exe, so the whole folder can be moved or copied.
os.environ.setdefault("PEAKCUT_DATA", str(HOME / "data"))
os.environ.setdefault("PEAKCUT_MODELS", str(HOME / "models"))
os.environ.setdefault("PEAKCUT_FFMPEG_DIR", str(HOME / "ffmpeg" / "bin"))
os.environ.setdefault("PEAKCUT_PORT", "8765")
os.environ.setdefault("PEAKCUT_UPDATE_CHECK", "0")


def _open_when_ready(url: str):
    for _ in range(120):
        try:
            urllib.request.urlopen(url, timeout=1)
            break
        except Exception:  # noqa: BLE001
            time.sleep(0.5)
    webbrowser.open(url)


if __name__ == "__main__":
    from studio import config, server
    threading.Thread(target=_open_when_ready, args=(f"http://127.0.0.1:{config.PORT}/",), daemon=True).start()
    print("\n  The M clipping - keep this window open while you use it. Close it to stop.\n")
    server.main()
