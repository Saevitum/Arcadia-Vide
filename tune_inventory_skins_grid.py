#!/usr/bin/env python3
"""
Tune Inventory SkinsPage grid/card layout to better resemble SideKicks.

Run this from the repository root:

    python tune_inventory_skins_grid.py --dry-run
    python tune_inventory_skins_grid.py

What it changes:
- src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua
- Makes the Inventory skin grid wider in both full and detail states.
- Makes selected/detail SkinCards less portrait-shaped by reducing CellSize.Y.
- Keeps 5-column-friendly CellSize.X = 0.1625.

Backups:
- Before writing, the script creates a backup under:
  .patch_backups/inventory_skins_grid_tuning/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET_FILE = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")

# Recommended tuning values.
REPLACEMENTS: dict[str, str] = {
    "PAGE_FULL_SIZE": "UDim2.fromScale(0.75, 0.53)",
    "PAGE_FULL_POSITION": "UDim2.fromScale(0.5, 0.55)",
    "PAGE_DETAIL_SIZE": "UDim2.fromScale(0.5, 0.53)",
    "PAGE_DETAIL_POSITION": "UDim2.fromScale(0.38, 0.55)",
    "GRID_FULL_CELL_SIZE": "UDim2.fromScale(0.1625, 0.305)",
    "GRID_DETAIL_CELL_SIZE": "UDim2.fromScale(0.1625, 0.265)",
    "GRID_CELL_PADDING": "UDim2.fromScale(0.03, 0.045)",
}


def repo_root() -> Path:
    return Path.cwd()


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "inventory_skins_grid_tuning" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def replace_local_constant(text: str, name: str, value: str) -> tuple[str, bool]:
    """
    Replace lines like:
        local PAGE_FULL_SIZE = UDim2.fromScale(...)
    while preserving indentation.
    """
    pattern = re.compile(
        rf"^(?P<indent>\s*)local\s+{re.escape(name)}\s*=\s*UDim2\.fromScale\([^\n]*\)",
        re.MULTILINE,
    )
    replacement = rf"\g<indent>local {name} = {value}"
    new_text, count = pattern.subn(replacement, text, count=1)
    return new_text, count == 1


def patch_text(text: str) -> tuple[str, list[str]]:
    changed: list[str] = []
    missing: list[str] = []

    new_text = text
    for name, value in REPLACEMENTS.items():
        new_text, ok = replace_local_constant(new_text, name, value)
        if ok:
            changed.append(name)
        else:
            missing.append(name)

    if missing:
        raise RuntimeError(
            "Could not find these constants in SkinsPage.lua: "
            + ", ".join(missing)
            + "\nThe file may have changed. Patch manually or update this script."
        )

    return new_text, changed


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
        description="Tune Inventory SkinCard grid proportions in SkinsPage.lua."
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
    args = parser.parse_args()

    path = repo_root() / TARGET_FILE

    if not path.exists():
        print(f"ERROR: Could not find {TARGET_FILE}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    old_text = path.read_text(encoding="utf-8")
    try:
        new_text, changed = patch_text(old_text)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        return 1

    if old_text == new_text:
        print("No changes needed. SkinsPage.lua already has the recommended values.")
        return 0

    print("Planned changes:")
    for name in changed:
        print(f"  - {name} = {REPLACEMENTS[name]}")

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
    print("  1) Check git diff")
    print("  2) Reopen/refresh Hoarcekat or Studio")
    print("  3) If cards still feel too tall, try GRID_DETAIL_CELL_SIZE Y = 0.255")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
