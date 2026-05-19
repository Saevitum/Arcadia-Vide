#!/usr/bin/env python3
# Hook the existing Stats button/menu route to the new fullscreen StatsTree.
#
# Run from the Arcadia-Vide repository root:
#   python hook_stats_button_to_stats_tree.py --dry-run
#   python hook_stats_button_to_stats_tree.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsMenu.lua
#
# Why:
# - Your ButtonBar / menu router already opens currentMenu = "Stats" when pressing Stats.
# - The old StatsMenu.lua is only a placeholder Panel with menuId = "Stats".
# - StatsTree currently defaults to currentMenu == "StatsTree" unless a custom visible
#   function is passed.
#
# This patch replaces the placeholder StatsMenu with a wrapper around StatsTree:
#   Stats button opens currentMenu = "Stats"
#   StatsMenu renders StatsTree
#   StatsTree is visible when currentMenu == "Stats"
#   StatsTree CloseButton still sets currentMenu(nil)
#
# Backup:
#   .patch_backups/hook_stats_button_to_stats_tree/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/StatsMenu.lua")


STATS_MENU_WRAPPER = '''--!strict

local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local StatsTree = require(script.Parent.StatsTree)

local function StatsMenu(props: Types.StatsMenuProps)
\tlocal store = props.store

\treturn StatsTree({
\t\tstore = store,
\t\tvisible = function()
\t\t\tif store == nil then
\t\t\t\treturn true
\t\t\tend

\t\t\tlocal currentMenu = store.currentMenu

\t\t\tif currentMenu == nil then
\t\t\t\treturn true
\t\t\tend

\t\t\treturn currentMenu() == "Stats"
\t\tend,
\t})
end

return StatsMenu
'''


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "hook_stats_button_to_stats_tree" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def print_diff(path: Path, before: str, after: str) -> None:
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
    )
    print("".join(diff))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replace placeholder StatsMenu with StatsTree wrapper so the Stats button opens the tree."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backup before writing.")
    args = parser.parse_args()

    path = Path.cwd() / TARGET

    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    stats_tree_path = path.parent / "StatsTree" / "init.lua"
    if not stats_tree_path.exists():
        print("ERROR: Could not find src/client/UI/UIManager/Menus/StatsTree/init.lua")
        print("Create the StatsTree prototype first, then run this script.")
        return 1

    before = path.read_text(encoding="utf-8")
    after = STATS_MENU_WRAPPER

    if before == after:
        print("No changes needed. StatsMenu already wraps StatsTree.")
        return 0

    print("Planned change:")
    print("  - Replace old placeholder StatsMenu Panel with StatsTree wrapper.")
    print("  - Existing Stats button/currentMenu='Stats' route will open the fullscreen tree.")
    print("  - No ButtonBar/router changes are needed.")

    print("\nDiff:\n")
    print_diff(TARGET, before, after)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        backup_path = make_backup(path)
        print(f"Backup created: {backup_path}")

    path.write_text(after, encoding="utf-8")
    print(f"Updated: {TARGET}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Studio/Hoarcekat")
    print("  3) Press the existing Stats button.")
    print("  4) Expected: fullscreen StatsTree opens instead of the old placeholder Stats panel.")
    print("  5) Press CLOSE in StatsTree; it should close by setting currentMenu(nil).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
