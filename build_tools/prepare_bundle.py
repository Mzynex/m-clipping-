"""Puts ffmpeg and the speech model next to the exe, so the finished folder needs nothing installed and no download."""
import io
import os
import sys
import zipfile
import urllib.request
from pathlib import Path

out = Path(sys.argv[1]).resolve()
FF = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

bin_dir = out / "ffmpeg" / "bin"
bin_dir.mkdir(parents=True, exist_ok=True)
if not (bin_dir / "ffmpeg.exe").is_file():
    print("Downloading ffmpeg ...", flush=True)
    data = urllib.request.urlopen(FF).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for n in z.namelist():
            if n.endswith(("/ffmpeg.exe", "/ffprobe.exe")):
                (bin_dir / Path(n).name).write_bytes(z.read(n))

os.environ["PEAKCUT_MODELS"] = str(out / "models")
os.environ["PEAKCUT_DATA"] = str(out / "data")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from studio import fetch_model  # noqa: E402
fetch_model.ensure()
print("Bundle ready:", out)
