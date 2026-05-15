#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventory menu patch v4

Run this from the Arcadia-Vide repo root:
    python apply_inventory_grid_toggle_v4.py

What it changes:
1) Inventory/SkinsPage.lua
   - When SelectedSkinInfo is open, the skin grid uses SideKicks-like 5-card rows.
   - Updates GRID_DETAIL_CELL_SIZE from the larger 3-column size to the SideKicks detail size.

2) Inventory/init.lua
   - Selecting the already-selected SkinCard toggles it off.
   - This closes SelectedSkinInfo and returns the ScrollingFrame to the full layout,
     matching the SideKicks menu behavior.

Backups are created under:
    _local_backups/inventory_grid_toggle_v4/
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path.cwd()
BACKUP_ROOT = ROOT / "_local_backups" / "inventory_grid_toggle_v4"

SKINS_PAGE = ROOT / "src" / "client" / "UI" / "UIManager" / "Menus" / "Inventory" / "SkinsPage.lua"
INVENTORY_INIT = ROOT / "src" / "client" / "UI" / "UIManager" / "Menus" / "Inventory" / "init.lua"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup(path: Path) -> None:
    rel = path.relative_to(ROOT)
    dst = BACKUP_ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)


def replace_required(text: str, old: str, new: str, file_label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Could not find expected text in {file_label}:\n{old}")
    return text.replace(old, new, 1)


def patch_skins_page() -> bool:
    if not SKINS_PAGE.exists():
        raise FileNotFoundError(f"Missing file: {SKINS_PAGE}")

    original = read(SKINS_PAGE)
    text = original

    # Detail layout: 5 cards per row in the shrunken grid, matching SideKicks detail layout.
    # Existing value produced only ~3 cards per row.
    replacements = [
        (
            "local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.29, 0.305)",
            "local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.1625, 0.28)",
        ),
        # Fallback in case a previous local edit changed only height/width spacing.
        (
            "local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.29,0.305)",
            "local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.1625, 0.28)",
        ),
    ]

    did_replace = False
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new, 1)
            did_replace = True
            break

    if not did_replace:
        raise RuntimeError(
            "Could not find GRID_DETAIL_CELL_SIZE in SkinsPage.lua. "
            "Expected something like: local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.29, 0.305)"
        )

    # Optional safety: keep no hard max; with this cell size + padding, five cells fit.
    # Do not force FillDirectionMaxCells = 5 because the full/open layout should remain flexible.

    if text != original:
        backup(SKINS_PAGE)
        write(SKINS_PAGE, text)
        return True

    return False


def patch_inventory_init() -> bool:
    if not INVENTORY_INIT.exists():
        raise FileNotFoundError(f"Missing file: {INVENTORY_INIT}")

    original = read(INVENTORY_INIT)
    text = original

    old_one_line = "local function selectSkin(skin: SkinItem) selectedSkin(skin) selectedSkinId(skin.SkinId) end"
    new_one_line = (
        "local function selectSkin(skin: SkinItem) "
        "if selectedSkinId() == skin.SkinId then "
        "selectedSkin(nil) "
        "selectedSkinId(nil) "
        "return "
        "end "
        "selectedSkin(skin) "
        "selectedSkinId(skin.SkinId) "
        "end"
    )

    old_multi = """local function selectSkin(skin: SkinItem)
	selectedSkin(skin)
	selectedSkinId(skin.SkinId)
end"""
    new_multi = """local function selectSkin(skin: SkinItem)
	if selectedSkinId() == skin.SkinId then
		selectedSkin(nil)
		selectedSkinId(nil)
		return
	end

	selectedSkin(skin)
	selectedSkinId(skin.SkinId)
end"""

    if old_multi in text:
        text = text.replace(old_multi, new_multi, 1)
    elif old_one_line in text:
        text = text.replace(old_one_line, new_one_line, 1)
    elif "local function selectSkin(skin: SkinItem)" in text and "selectedSkinId() == skin.SkinId" in text:
        print("[SKIP] Inventory/init.lua already appears to have toggle-select behavior.")
    else:
        raise RuntimeError(
            "Could not find the expected selectSkin function in Inventory/init.lua. "
            "Expected either the old one-line or multi-line version."
        )

    if text != original:
        backup(INVENTORY_INIT)
        write(INVENTORY_INIT, text)
        return True

    return False


def main() -> None:
    if not (ROOT / "src" / "client" / "UI" / "UIManager").exists():
        raise SystemExit(
            "Could not find src/client/UI/UIManager. "
            "Run this script from the Arcadia-Vide repo root."
        )

    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    changed = []

    if patch_skins_page():
        changed.append(SKINS_PAGE)
        print(f"[UPDATED] {SKINS_PAGE.relative_to(ROOT)}")
    else:
        print(f"[UNCHANGED] {SKINS_PAGE.relative_to(ROOT)}")

    if patch_inventory_init():
        changed.append(INVENTORY_INIT)
        print(f"[UPDATED] {INVENTORY_INIT.relative_to(ROOT)}")
    else:
        print(f"[UNCHANGED] {INVENTORY_INIT.relative_to(ROOT)}")

    print()
    print("Done.")
    print(f"Changed files: {len(changed)}")
    print(f"Backups: {BACKUP_ROOT}")
    print()
    print("Next steps:")
    print("  git diff")
    print("  Test Inventory in Hoarcekat/Studio")
    print("  git add src/client/UI/UIManager/Menus/Inventory")
    print('  git commit -m "Inventory grid and toggle select"')


if __name__ == "__main__":
    main()
