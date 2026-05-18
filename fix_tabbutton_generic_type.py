#!/usr/bin/env python3
"""
Fix the remaining Luau generic type error in:
src/client/UI/UIManager/Components/Tabs/TabButton.lua

Error:
  Type Error: (19,23) Type parameter list is required
  line: type TabButtonProps = Types.TabButtonProps

Cause:
  Types.TabButtonProps is a generic exported type, so it must be referenced with
  a concrete type parameter. Tab ids in this UI system are strings, so the alias
  should be Types.TabButtonProps<string>.

Usage:
  python fix_tabbutton_generic_type.py --dry-run
  python fix_tabbutton_generic_type.py
"""

from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import sys

ROOT_CANDIDATES = [
    pathlib.Path("src/client/UI/UIManager/Components/Tabs/TabButton.lua"),
    pathlib.Path("src/Client/UI/UIManager/Components/Tabs/TabButton.lua"),
]

OLD = "type TabButtonProps = Types.TabButtonProps"
NEW = "type TabButtonProps = Types.TabButtonProps<string>"


def find_file(repo_root: pathlib.Path) -> pathlib.Path | None:
    for rel in ROOT_CANDIDATES:
        path = repo_root / rel
        if path.exists():
            return path
    # Fallback for slightly different capitalization/layout.
    matches = list(repo_root.glob("**/UIManager/Components/Tabs/TabButton.lua"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print("Found multiple TabButton.lua files:")
        for m in matches:
            print(f"  - {m}")
        print("Please run the script from the correct repo root or patch manually.")
    return None


def make_backup(path: pathlib.Path, repo_root: pathlib.Path) -> pathlib.Path:
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    rel = path.relative_to(repo_root)
    backup = repo_root / ".patch_backups" / f"fix_tabbutton_generic_type_{stamp}" / rel
    backup.parent.mkdir(parents=True, exist_ok=True)
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")
    parser.add_argument("--root", default=".", help="Repo root. Default: current directory.")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.root).resolve()
    path = find_file(repo_root)
    if path is None:
        print("Could not find UIManager/Components/Tabs/TabButton.lua")
        return 1

    text = path.read_text(encoding="utf-8")

    if NEW in text:
        print(f"Already fixed: {path}")
        return 0

    if OLD not in text:
        print(f"Could not find the expected line in: {path}")
        print("Expected:")
        print(f"  {OLD}")
        print("Manual fix:")
        print(f"  {NEW}")
        return 1

    updated = text.replace(OLD, NEW, 1)

    print(f"Target: {path}")
    print("Change:")
    print(f"  - {OLD}")
    print(f"  + {NEW}")

    if args.dry_run:
        print("Dry run only. No files written.")
        return 0

    backup = make_backup(path, repo_root)
    path.write_text(updated, encoding="utf-8", newline="")
    print(f"Wrote: {path}")
    print(f"Backup: {backup}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
