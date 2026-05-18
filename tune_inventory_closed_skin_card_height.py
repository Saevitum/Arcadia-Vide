#!/usr/bin/env python3
"""
Tune Inventory SkinCard FULL/CLOSED grid card height.

Run from the Arcadia-Vide repository root:

    python tune_inventory_closed_skin_card_height.py --dry-run
    python tune_inventory_closed_skin_card_height.py

What it changes:
- src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua

Recommended change:
- GRID_FULL_CELL_SIZE = UDim2.fromScale(0.1625, 0.385)

Why:
- Inventory full/closed state has less vertical area because of the tab strip.
- The previous full card height was too short, making SkinCards look like wide rectangles.
- 0.385 compensates for the shorter Inventory page height and makes the cards visually closer
  to the SideKicks closed-state card proportions.
- GRID_DETAIL_CELL_SIZE is intentionally left unchanged, because the selected/open state was
  already improved by the previous tuning pass.

Backups:
- Before writing, backups are created under:
  .patch_backups/inventory_closed_skin_card_height/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET_FILE = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")

DEFAULT_FULL_CELL_SIZE = "UDim2.fromScale(0.1625, 0.385)"


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "inventory_closed_skin_card_height" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def patch_grid_full_cell_size(text: str, replacement_value: str) -> tuple[str, bool]:
    """
    Replace:
        local GRID_FULL_CELL_SIZE = UDim2.fromScale(...)
    Works even if the file has been minified into one long line.
    """
    pattern = re.compile(
        r"(?P<prefix>\blocal\s+GRID_FULL_CELL_SIZE\s*=\s*)"
        r"UDim2\.fromScale\(\s*[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*\)"
    )

    new_text, count = pattern.subn(rf"\g<prefix>{replacement_value}", text, count=1)
    return new_text, count == 1


def print_diff(path: Path, old: str, new: str) -> None:
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
    )
    print("".join(diff))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Make Inventory SkinCards taller in the closed/full grid state."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the diff without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a backup before writing.",
    )
    parser.add_argument(
        "--cell-y",
        type=float,
        default=0.385,
        help="Override GRID_FULL_CELL_SIZE Y scale. Default: 0.385",
    )
    args = parser.parse_args()

    path = Path.cwd() / TARGET_FILE

    if not path.exists():
        print(f"ERROR: Could not find {TARGET_FILE}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    replacement_value = f"UDim2.fromScale(0.1625, {args.cell_y:g})"

    old_text = path.read_text(encoding="utf-8")
    new_text, ok = patch_grid_full_cell_size(old_text, replacement_value)

    if not ok:
        print("ERROR: Could not find `local GRID_FULL_CELL_SIZE = UDim2.fromScale(...)`")
        print("The file may have changed. Patch manually or update this script.")
        return 1

    if old_text == new_text:
        print(f"No changes needed. GRID_FULL_CELL_SIZE is already {replacement_value}.")
        return 0

    print("Planned change:")
    print(f"  - GRID_FULL_CELL_SIZE = {replacement_value}")
    print()
    print_diff(TARGET_FILE, old_text, new_text)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        backup_path = make_backup(path)
        print(f"\nBackup created: {backup_path}")

    path.write_text(new_text, encoding="utf-8")
    print(f"Updated: {TARGET_FILE}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Hoarcekat/Studio")
    print("  3) If cards are too tall, rerun with: python tune_inventory_closed_skin_card_height.py --cell-y 0.37")
    print("  4) If cards are still too wide/short, rerun with: python tune_inventory_closed_skin_card_height.py --cell-y 0.395")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
