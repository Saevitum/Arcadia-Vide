#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inventory grid + selection toggle patch.

Run from the Arcadia-Vide repo root:

    python apply_inventory_grid_toggle_v5.py

What it does:
1) Updates Inventory/SkinsPage.lua so the selected-detail grid uses the same
   5-card-row style as SideKicks:
       GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.1625, 0.28)

2) Updates Inventory/init.lua so clicking the already-selected SkinCard again
   deselects it, closes SelectedSkinInfo, and expands the ScrollingFrame.

The script is safe to run more than once.
Backups are created in:
    _local_backups/inventory_grid_toggle_v5/
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


REPO_ROOT = Path.cwd()
UI_MANAGER = REPO_ROOT / "src" / "client" / "UI" / "UIManager"
INVENTORY_DIR = UI_MANAGER / "Menus" / "Inventory"

INVENTORY_INIT = INVENTORY_DIR / "init.lua"
SKINS_PAGE = INVENTORY_DIR / "SkinsPage.lua"

BACKUP_ROOT = REPO_ROOT / "_local_backups" / "inventory_grid_toggle_v5"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup_file(path: Path) -> None:
    rel = path.relative_to(REPO_ROOT)
    dst = BACKUP_ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)


def patch_skins_page() -> bool:
    if not SKINS_PAGE.exists():
        raise FileNotFoundError(f"Missing file: {SKINS_PAGE}")

    text = read_text(SKINS_PAGE)
    original = text

    # Match any current detail cell-size value.
    pattern = re.compile(
        r"local\s+GRID_DETAIL_CELL_SIZE\s*=\s*UDim2\.fromScale\(\s*[-0-9.]+\s*,\s*[-0-9.]+\s*\)"
    )

    replacement = "local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.1625, 0.28)"

    if pattern.search(text):
        text = pattern.sub(replacement, text, count=1)
    else:
        raise RuntimeError(
            "Could not find GRID_DETAIL_CELL_SIZE in Inventory/SkinsPage.lua. "
            "Please check the file manually."
        )

    if text != original:
        backup_file(SKINS_PAGE)
        write_text(SKINS_PAGE, text)
        print(f"[UPDATED] {SKINS_PAGE.relative_to(REPO_ROOT)}")
        return True

    print(f"[UNCHANGED] {SKINS_PAGE.relative_to(REPO_ROOT)} already patched")
    return False


def patch_inventory_init() -> bool:
    if not INVENTORY_INIT.exists():
        raise FileNotFoundError(f"Missing file: {INVENTORY_INIT}")

    text = read_text(INVENTORY_INIT)
    original = text

    if "if selectedSkinId() == skin.SkinId then" in text:
        print(f"[UNCHANGED] {INVENTORY_INIT.relative_to(REPO_ROOT)} already has selection toggle")
        return False

    new_select_skin = """local function selectSkin(skin: SkinItem)
\t\tif selectedSkinId() == skin.SkinId then
\t\t\tselectedSkin(nil)
\t\t\tselectedSkinId(nil)
\t\t\treturn
\t\tend

\t\tselectedSkin(skin)
\t\tselectedSkinId(skin.SkinId)
\tend"""

    # Robust version: replace the whole selectSkin function by capturing until
    # the next local function equipSkin. Works with normal formatting and one-line
    # compressed files.
    pattern = re.compile(
        r"local\s+function\s+selectSkin\s*\(\s*skin\s*:\s*SkinItem\s*\).*?end(?=\s*local\s+function\s+equipSkin\s*\()",
        re.DOTALL,
    )

    text, count = pattern.subn(new_select_skin, text, count=1)

    if count == 0:
        # Fallback: exact old function body, with flexible whitespace.
        fallback_pattern = re.compile(
            r"local\s+function\s+selectSkin\s*\(\s*skin\s*:\s*SkinItem\s*\)\s*"
            r"selectedSkin\s*\(\s*skin\s*\)\s*"
            r"selectedSkinId\s*\(\s*skin\.SkinId\s*\)\s*"
            r"end",
            re.DOTALL,
        )

        text, count = fallback_pattern.subn(new_select_skin, text, count=1)

    if count == 0:
        raise RuntimeError(
            "Could not find the selectSkin function in Inventory/init.lua. "
            "Expected a function named: local function selectSkin(skin: SkinItem)"
        )

    if text != original:
        backup_file(INVENTORY_INIT)
        write_text(INVENTORY_INIT, text)
        print(f"[UPDATED] {INVENTORY_INIT.relative_to(REPO_ROOT)}")
        return True

    print(f"[UNCHANGED] {INVENTORY_INIT.relative_to(REPO_ROOT)}")
    return False


def main() -> None:
    if not INVENTORY_DIR.exists():
        raise SystemExit(f"Inventory folder not found: {INVENTORY_DIR}")

    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    changed = 0

    if patch_skins_page():
        changed += 1

    if patch_inventory_init():
        changed += 1

    print()
    print(f"Done. Modified files: {changed}")
    print(f"Backups: {BACKUP_ROOT}")


if __name__ == "__main__":
    main()
