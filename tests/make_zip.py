"""Package the ARM bundle: python tests/make_zip.py [out.zip]  (skips __pycache__, .git, work dirs, LaTeX temp dirs and the arXiv test PDFs)"""
import hashlib
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), "intro-gap-ledger_arm_v0.1.0.zip")
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for r, ds, fs in os.walk(ROOT):
        ds[:] = [d for d in ds if d not in ("__pycache__", ".git", "_latex") and not (d == "work" and "tests" in r)]
        for f in fs:
            p = os.path.join(r, f)
            rp = os.path.relpath(p, ROOT).replace(os.sep, "/")
            if f.endswith(".pdf") and (rp.startswith("tests/cases/") or "/input/" in rp):
                continue  # third-party PDFs: see tests/SOURCES.md
            if "/work/sources/" in rp or rp.endswith("/work/evidence.json"):
                continue  # extracted full texts of third-party papers
            z.write(p, rp)
            n += 1
with open(out, "rb") as fh:
    print(n, "files", round(os.path.getsize(out) / 1e6, 2), "MB", hashlib.sha256(fh.read()).hexdigest(), out)
