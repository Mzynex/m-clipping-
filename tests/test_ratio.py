"""Video shapes (9:16, 4:5, 1:1, 16:9) and the "No captions" style. Runs against the code directly."""
import os, re, sys, tempfile
os.environ["PEAKCUT_DATA"] = tempfile.mkdtemp(prefix="pc-ratio-"); os.environ["DATABASE_URL"] = ""
sys.path.insert(0, ".")
from studio import jobs, render
fails = []
def check(n, got, want=True):
    ok = want(got) if callable(want) else got == want
    print(("PASS " if ok else "FAIL ") + n + ("" if ok else f"   got {got!r}")); ok or fails.append(n)
words = [{"w": w, "s": i * 0.5, "e": i * 0.5 + 0.4} for i, w in enumerate("one two three four five six".split())]
caps = lambda ass: len(re.findall(r"^Dialogue: \d,[^,]+,[^,]+,Cap,", ass, re.M))

check("the standard shape is still 1080x1920", render.ratio_size("9:16"), (1080, 1920))
check("every shape has a size", {k: render.ratio_size(k) for k in render.RATIOS}, {"9:16": (1080, 1920), "4:5": (1080, 1350), "1:1": (1080, 1080), "16:9": (1920, 1080)})
check("an unknown shape falls back to 9:16", render.ratio_size("5:3"), (1080, 1920))
check("9:16 placement is unchanged", render.geometry(1920, 1080, "blur"), ("blur", 608, max(230, (1920 - 608) // 2 - 190), min(1640, (1920 - 608) // 2 + 608 + 180)))
check("a 16:9 video fills a 16:9 frame", render.geometry(1920, 1080, "blur", 1920, 1080)[:2], ("blur", 1080))
check("a vertical video in a 16:9 frame is filled by cropping", render.geometry(1080, 1920, "blur", 1920, 1080)[0], "crop")
check("1:1 frame: text goes on the picture", render.geometry(1920, 1080, "blur", 1080, 1080)[2:], (172, 777))

with_caps = render.build_ass(words, 0, 4, "HOOK", "bounce", [], 300, 1380)
no_caps = render.build_ass(words, 0, 4, "HOOK", "none", [], 300, 1380)
check("normal style draws captions", caps(with_caps) > 0)
check("'No captions' draws none", caps(no_caps), 0)
check("'No captions' keeps the big text", "Hook," in no_caps and "HOOK" in no_caps)
check("the new style is in the list", "none" in render.STYLES and render.STYLES["none"]["label"] == "No captions")
wide = render.build_ass(words, 0, 4, "HOOK", "bounce", [], 170, 780, 1920, 1080)
check("a 16:9 caption sheet has the 16:9 size", "PlayResX: 1920" in wide and "PlayResY: 1080" in wide)

check("options accept a shape", jobs.clean_options({"ratio": "1:1"}), {"ratio": "1:1"})
check("options reject a made-up shape", jobs.clean_options({"ratio": "7:3"}), {"ratio": "9:16"})
check("default shape is 9:16", jobs.DEFAULTS["ratio"], "9:16")
print("ALL PASSED" if not fails else f"{len(fails)} failed")
import shutil; shutil.rmtree(os.environ["PEAKCUT_DATA"], ignore_errors=True)
sys.exit(1 if fails else 0)
