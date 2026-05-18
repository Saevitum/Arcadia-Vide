#!/usr/bin/env python3
"""
Tune Inventory selected info panel + divider spacing to visually match SideKicks.

Run from the Arcadia-Vide repository root:

    python tune_inventory_info_divider_spacing.py --dry-run
    python tune_inventory_info_divider_spacing.py

What it changes:
- src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua
    INFO_SIZE -> UDim2.fromScale(0.159, 0.52)
    INFO_OPEN_POSITION -> UDim2.fromScale(0.7475, 0.55)

- src/client/UI/UIManager/Menus/Inventory/init.lua
    DIVIDER_POSITION -> UDim2.fromScale(0.636, 0.55)

Why:
- Inventory info panel was wider than SideKickInfo.
- Inventory divider was visually too far left compared to the SideKicks layout.
- These values make the info panel width match SideKicks more closely and place the divider
  near the right edge of the tuned SkinsPage detail grid.

Backups:
- Before writing, backups are created under:
  .patch_backups/inventory_info_divider_spacing/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


PATCHES = {
    Path("src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua"): {
        "INFO_SIZE": "UDim2.fromScale(0.159, 0.52)",
        "INFO_OPEN_POSITION": "UDim2.fromScale(0.7475, 0.55)",
    },
    Path("src/client/UI/UIManager/Menus/Inventory/init.lua"): {
        "DIVIDER_POSITION": "UDim2.fromScale(0.636, 0.55)",
    },
}


def make_backup(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    backup_path = backup_root / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def replace_local_udim2_constant(text: str, name: str, value: str) -> tuple[str, bool]:
    """
    Replace lines/fragments like:
        local INFO_SIZE = UDim2.fromScale(...)
    Works even if the file has been accidentally minified into one long line.
    """
    pattern = re.compile(
        rf"(?P<prefix>\blocal\s+{re.escape(name)}\s*=\s*)UDim2\.fromScale\(\s*[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*\)"
    )
    replacement = rf"\g<prefix>{value}"
    new_text, count = pattern.subn(replacement, text, count=1)
    return new_text, count == 1


def patch_file(path: Path, constants: dict[str, str]) -> tuple[str, str, list[str]]:
    old_text = path.read_text(encoding="utf-8")
    new_text = old_text
    changed: list[str] = []
    missing: list[str] = []

    for name, value in constants.items():
        new_text, ok = replace_local_udim2_constant(new_text, name, value)
        if ok:
            changed.append(name)
        else:
            missing.append(name)

    if missing:
        raise RuntimeError(
            f"{path}: could not find constants: {', '.join(missing)}"
        )

    return old_text, new_text, changed


def print_diff(path: Path, old: str, new: str) -> None:
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
    )
    diff_text = "".join(diff)
    if diff_text:
        print(diff_text)
    else:
        print(f"No textual diff for {path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tune Inventory info panel width and divider spacing."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backup files before writing.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = Path(".patch_backups") / "inventory_info_divider_spacing" / timestamp

    planned: list[tuple[Path, str, str, list[str]]] = []

    for rel_path, constants in PATCHES.items():
        path = repo_root / rel_path
        if not path.exists():
            print(f"ERROR: Could not find {rel_path}")
            print("Run this script from the Arcadia-Vide repository root.")
            return 1

        try:
            old_text, new_text, changed = patch_file(path, constants)
        except RuntimeError as err:
            print(f"ERROR: {err}")
            print("The file may have changed. Patch manually or update this script.")
            return 1

        planned.append((rel_path, old_text, new_text, changed))

    any_changes = any(old != new for _, old, new, _ in planned)
    if not any_changes:
        print("No changes needed. The recommended values are already applied.")
        return 0

    print("Planned changes:")
    for rel_path, old_text, new_text, changed in planned:
        if old_text == new_text:
            continue
        print(f"\n{rel_path}")
        for name in changed:
            print(f"  - {name} = {PATCHES[rel_path][name]}")

    print("\nDiff:")
    for rel_path, old_text, new_text, _ in planned:
        if old_text != new_text:
            print_diff(rel_path, old_text, new_text)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        for rel_path, old_text, new_text, _ in planned:
            if old_text != new_text:
                backup_path = make_backup(repo_root / rel_path, backup_root)
                print(f"Backup created: {backup_path}")

    for rel_path, old_text, new_text, _ in planned:
        if old_text != new_text:
            (repo_root / rel_path).write_text(new_text, encoding="utf-8")
            print(f"Updated: {rel_path}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Hoarcekat/Studio")
    print("  3) If the gap still feels too small, try DIVIDER_POSITION X = 0.632 or INFO_OPEN_POSITION X = 0.75")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
