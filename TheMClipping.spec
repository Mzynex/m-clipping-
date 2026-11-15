# PyInstaller recipe for The M clipping (Windows). Build with build_windows.bat.
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas = [("web", "web"), ("studio/fonts", "studio/fonts"), (".env.example", ".")]
binaries, hiddenimports = [], []
for pkg in ("sherpa_onnx", "yt_dlp", "soundfile", "certifi"):
    d, b, h = collect_all(pkg)
    datas += d; binaries += b; hiddenimports += h
hiddenimports += collect_submodules("studio") + collect_submodules("uvicorn") + collect_submodules("sqlalchemy.dialects.sqlite")
hiddenimports += ["multipart", "python_multipart", "psycopg", "psycopg_binary"]

a = Analysis(["launcher.py"], pathex=["."], binaries=binaries, datas=datas, hiddenimports=hiddenimports, excludes=["tkinter"])
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="TheMClipping", console=True, icon="build_tools/app.ico")
coll = COLLECT(exe, a.binaries, a.datas, name="TheMClipping")
