#!/usr/bin/env python3
# Make Inventory SkinsPage select/deselect layout tween match SideKicks exactly.
#
# Run from the Arcadia-Vide repository root:
#   python match_inventory_skinpage_bounce_to_sidekicks.py --dry-run
#   python match_inventory_skinpage_bounce_to_sidekicks.py
#
# Target:
#   src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua
#
# What it changes:
#   The ScrollArea({ name = "SkinsScrollArea", ... }) layoutTween block.
#
# It replaces Inventory's current different open/close setup:
#   duration = 0.34
#   openEasingStyle = Back
#   closeEasingStyle = Quad
#   overshoot = 0.035
#   close = false
#
# with the exact SideKicks ScrollArea bounce config:
#   duration = 0.38
#   easingStyle = Quint
#   easingDirection = Out
#   bounce.overshoot = 0.09
#   bounce.firstDuration = 0.22
#   bounce.settleDuration = 0.16
#   bounce.firstEasingStyle = Quint
#   bounce.firstEasingDirection = Out
#   bounce.settleEasingStyle = Quint
#   bounce.settleEasingDirection = Out
#
# Note:
#   This intentionally leaves your tuned Inventory sizes/positions untouched.
#   It only changes the animation behavior when selectedSkin opens/closes.
#
# Backup:
#   .patch_backups/match_inventory_skinpage_bounce_to_sidekicks/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")


LAYOUT_TWEEN_BLOCK = '''layoutTween = {
\t\t\t\tisOpen = function()
\t\t\t\t\treturn hasSelectedSkin(props)
\t\t\t\tend,
\t\t\t\ttargetSize = function()
\t\t\t\t\tif hasSelectedSkin(props) then
\t\t\t\t\t\treturn PAGE_DETAIL_SIZE
\t\t\t\t\tend

\t\t\t\t\treturn PAGE_FULL_SIZE
\t\t\t\tend,
\t\t\t\ttargetPosition = function()
\t\t\t\t\tif hasSelectedSkin(props) then
\t\t\t\t\t\treturn PAGE_DETAIL_POSITION
\t\t\t\t\tend

\t\t\t\t\treturn PAGE_FULL_POSITION
\t\t\t\tend,
\t\t\t\tduration = 0.38,
\t\t\t\teasingStyle = Enum.EasingStyle.Quint,
\t\t\t\teasingDirection = Enum.EasingDirection.Out,
\t\t\t\tbounce = {
\t\t\t\t\tovershoot = 0.09,
\t\t\t\t\tfirstDuration = 0.22,
\t\t\t\t\tsettleDuration = 0.16,
\t\t\t\t\tfirstEasingStyle = Enum.EasingStyle.Quint,
\t\t\t\t\tfirstEasingDirection = Enum.EasingDirection.Out,
\t\t\t\t\tsettleEasingStyle = Enum.EasingStyle.Quint,
\t\t\t\t\tsettleEasingDirection = Enum.EasingDirection.Out,
\t\t\t\t},
\t\t\t},'''


LAYOUT_TWEEN_BLOCK_COMPACT = 'layoutTween = { isOpen = function() return hasSelectedSkin(props) end, targetSize = function() if hasSelectedSkin(props) then return PAGE_DETAIL_SIZE end return PAGE_FULL_SIZE end, targetPosition = function() if hasSelectedSkin(props) then return PAGE_DETAIL_POSITION end return PAGE_FULL_POSITION end, duration = 0.38, easingStyle = Enum.EasingStyle.Quint, easingDirection = Enum.EasingDirection.Out, bounce = { overshoot = 0.09, firstDuration = 0.22, settleDuration = 0.16, firstEasingStyle = Enum.EasingStyle.Quint, firstEasingDirection = Enum.EasingDirection.Out, settleEasingStyle = Enum.EasingStyle.Quint, settleEasingDirection = Enum.EasingDirection.Out, }, },'


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "match_inventory_skinpage_bounce_to_sidekicks" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def find_balanced_expression_end(text: str, start: int) -> int:
    brace = 0
    paren = 0
    bracket = 0
    opened = False
    in_string: str | None = None
    escape = False

    i = start
    while i < len(text):
        ch = text[i]

        if in_string is not None:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch in ('"', "'", "`"):
            in_string = ch
            i += 1
            continue

        if ch == "{":
            brace += 1
            opened = True
        elif ch == "}":
            brace -= 1
        elif ch == "(":
            paren += 1
            opened = True
        elif ch == ")":
            paren -= 1
        elif ch == "[":
            bracket += 1
            opened = True
        elif ch == "]":
            bracket -= 1

        if opened and brace == 0 and paren == 0 and bracket == 0:
            return i + 1

        i += 1

    raise RuntimeError("Could not find end of balanced expression")


def include_trailing_comma(text: str, end: int) -> int:
    i = end
    while i < len(text) and text[i].isspace():
        i += 1

    if i < len(text) and text[i] == ",":
        return i + 1

    return end


def patch_layout_tween(text: str, pretty: bool) -> tuple[str, str]:
    skins_scroll_match = re.search(r'name\s*=\s*"SkinsScrollArea"', text)
    if skins_scroll_match is None:
        raise RuntimeError('Could not find ScrollArea with name = "SkinsScrollArea"')

    layout_match = re.search(r"layoutTween\s*=\s*\{", text[skins_scroll_match.start():])
    if layout_match is None:
        raise RuntimeError("Could not find layoutTween block inside SkinsScrollArea")

    layout_start = skins_scroll_match.start() + layout_match.start()
    table_start = text.find("{", layout_start)
    if table_start == -1:
        raise RuntimeError("Could not find opening { for layoutTween")

    table_end = include_trailing_comma(text, find_balanced_expression_end(text, table_start))

    replacement = LAYOUT_TWEEN_BLOCK if pretty else LAYOUT_TWEEN_BLOCK_COMPACT
    old_block = text[layout_start:table_end]
    new_text = text[:layout_start] + replacement + text[table_end:]

    return new_text, old_block


def already_matches_sidekicks(text: str) -> bool:
    required = [
        "duration = 0.38",
        "easingStyle = Enum.EasingStyle.Quint",
        "easingDirection = Enum.EasingDirection.Out",
        "overshoot = 0.09",
        "firstDuration = 0.22",
        "settleDuration = 0.16",
        "firstEasingStyle = Enum.EasingStyle.Quint",
        "settleEasingStyle = Enum.EasingStyle.Quint",
    ]

    skins_scroll_match = re.search(r'name\s*=\s*"SkinsScrollArea"', text)
    if skins_scroll_match is None:
        return False

    context = text[skins_scroll_match.start():skins_scroll_match.start() + 2500]
    return all(item in context for item in required)


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
        description="Make Inventory SkinsPage select/deselect bounce match SideKicks."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a backup before writing.")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Write a multi-line layoutTween block instead of a compact one-line block.",
    )
    args = parser.parse_args()

    path = Path.cwd() / TARGET

    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    before = path.read_text(encoding="utf-8")

    if already_matches_sidekicks(before):
        print("No changes needed. SkinsScrollArea layoutTween already appears to match SideKicks.")
        return 0

    try:
        after, old_block = patch_layout_tween(before, pretty=args.pretty)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("No files were changed.")
        return 1

    if before == after:
        print("No changes needed.")
        return 0

    print("Planned change:")
    print("  - Replace SkinsScrollArea.layoutTween with the exact SideKicks ScrollArea bounce config.")
    print("  - Sizes/positions are left untouched.")
    print("\nNew config summary:")
    print("  duration = 0.38")
    print("  easingStyle = Enum.EasingStyle.Quint")
    print("  easingDirection = Enum.EasingDirection.Out")
    print("  bounce.overshoot = 0.09")
    print("  bounce.firstDuration = 0.22")
    print("  bounce.settleDuration = 0.16")
    print("  bounce first/settle easing = Quint.Out")

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
    print("  3) Select and deselect a SkinCard; the grid shrink/expand should now bounce like SideKicks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
