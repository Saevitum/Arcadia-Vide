# scripts/patch_packages_luau.py
from pathlib import Path

ROOT = Path("Packages")
HEADER_LINES = ["--!nocheck", "--!nolint"]

if not ROOT.exists():
    raise SystemExit("Packages folder not found. Run this from your project root after `wally install`.")

for file in ROOT.rglob("*.lua"):
    text = file.read_text(encoding="utf-8")

    existing_lines = text.splitlines()[:5]
    missing = [line for line in HEADER_LINES if line not in existing_lines]

    if not missing:
        continue

    file.write_text("\n".join(missing) + "\n" + text, encoding="utf-8")
    print(f"Patched {file}")

print("Done patching Packages.")