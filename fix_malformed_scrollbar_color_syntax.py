#!/usr/bin/env python3
"""
Fix syntax errors caused by malformed scrollBarImageColor3 replacement.

Run from the Arcadia-Vide repository root:

    python fix_malformed_scrollbar_color_syntax.py --dry-run
    python fix_malformed_scrollbar_color_syntax.py

What this fixes:
A previous patch could turn this valid Luau:

    scrollBarImageColor3 = Color3.fromRGB(0, 229, 255),

into this invalid Luau:

    scrollBarImageColor3 = Color3.fromRGB(0, 0, 0), 229, 255),

because the earlier regex stopped at the first comma inside Color3.fromRGB(...).

This script normalizes every scrollBarImageColor3 assignment in the targeted menu files to:

    scrollBarImageColor3 = Color3.fromRGB(0, 0, 0),

Targets:
- src/client/UI/UIManager/Menus/SideKicks/init.luau
  fallback: src/client/UI/UIManager/Menus/SideKicks/init.lua
- src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua

Backups:
- Before writing, backups are created under:
  .patch_backups/fix_malformed_scrollbar_color_syntax/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SIDEKICKS_LUAU = Path("src/client/UI/UIManager/Menus/SideKicks/init.luau")
SIDEKICKS_LUA = Path("src/client/UI/UIManager/Menus/SideKicks/init.lua")
INVENTORY_SKINS = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")


@dataclass(frozen=True)
class PatchResult:
    path: Path
    before: str
    after: str
    replacements: int


def make_backup(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    safe_name = "__".join(path.parts[-5:])
    backup_path = backup_root / safe_name
    shutil.copy2(path, backup_path)
    return backup_path


def normalize_scrollbar_color(text: str) -> tuple[str, int]:
    """
    Normalize scrollBarImageColor3 assignments to black.

    Handles both valid and malformed versions, including:
      scrollBarImageColor3 = Color3.fromRGB(0, 229, 255),
      scrollBarImageColor3 = Color3.fromRGB(0, 0, 0), 229, 255),
      scrollBarImageColor3 = Color3.fromRGB(0, 0, 0), 255, 255),

    It intentionally only targets the exact property name scrollBarImageColor3.
    """
    total = 0

    # First fix the malformed "extra two numeric args after the call" version.
    malformed_pattern = re.compile(
        r"(?P<prefix>\bscrollBarImageColor3\s*=\s*)"
        r"Color3\.fromRGB\(\s*[-+]?\d+\.?\d*\s*,\s*[-+]?\d+\.?\d*\s*,\s*[-+]?\d+\.?\d*\s*\)"
        r"\s*,\s*[-+]?\d+\.?\d*\s*,\s*[-+]?\d+\.?\d*\s*\)\s*,"
    )

    text, count = malformed_pattern.subn(
        r"\g<prefix>Color3.fromRGB(0, 0, 0),",
        text,
    )
    total += count

    # Then normalize any normal Color3.fromRGB assignment.
    normal_pattern = re.compile(
        r"(?P<prefix>\bscrollBarImageColor3\s*=\s*)"
        r"Color3\.fromRGB\(\s*[-+]?\d+\.?\d*\s*,\s*[-+]?\d+\.?\d*\s*,\s*[-+]?\d+\.?\d*\s*\)\s*,"
    )

    text, count = normal_pattern.subn(
        r"\g<prefix>Color3.fromRGB(0, 0, 0),",
        text,
    )
    total += count

    return text, total


def has_malformed_scrollbar_color(text: str) -> bool:
    return re.search(
        r"\bscrollBarImageColor3\s*=\s*Color3\.fromRGB\([^)]*\)\s*,\s*[-+]?\d+\.?\d*\s*,\s*[-+]?\d+\.?\d*\s*\)",
        text,
    ) is not None


def patch_file(path: Path) -> PatchResult:
    before = path.read_text(encoding="utf-8")
    after, replacements = normalize_scrollbar_color(before)

    if has_malformed_scrollbar_color(after):
        raise RuntimeError(
            f"{path}: malformed scrollBarImageColor3 pattern still exists after patch"
        )

    return PatchResult(path=path, before=before, after=after, replacements=replacements)


def print_diff(result: PatchResult) -> None:
    diff = difflib.unified_diff(
        result.before.splitlines(keepends=True),
        result.after.splitlines(keepends=True),
        fromfile=f"{result.path} (before)",
        tofile=f"{result.path} (after)",
    )
    print("".join(diff))


def find_targets(repo_root: Path) -> list[Path]:
    targets: list[Path] = []

    if (repo_root / SIDEKICKS_LUAU).exists():
        targets.append(SIDEKICKS_LUAU)
    elif (repo_root / SIDEKICKS_LUA).exists():
        targets.append(SIDEKICKS_LUA)
    else:
        raise FileNotFoundError(
            f"Could not find {SIDEKICKS_LUAU} or {SIDEKICKS_LUA}"
        )

    if (repo_root / INVENTORY_SKINS).exists():
        targets.append(INVENTORY_SKINS)
    else:
        raise FileNotFoundError(f"Could not find {INVENTORY_SKINS}")

    return targets


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix malformed scrollBarImageColor3 syntax in SideKicks/Inventory menu files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the diff without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backups before writing.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()

    try:
        targets = find_targets(repo_root)
        results = [patch_file(repo_root / target) for target in targets]
    except (FileNotFoundError, RuntimeError) as err:
        print(f"ERROR: {err}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    changed = [result for result in results if result.before != result.after]

    if not changed:
        print("No changes needed. No malformed scrollBarImageColor3 assignment was found.")
        return 0

    print("Planned fixes:")
    for result in changed:
        print(f"  - {result.path}: normalized {result.replacements} scrollBarImageColor3 assignment(s)")

    print("\nDiff:\n")
    for result in changed:
        print_diff(result)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "fix_malformed_scrollbar_color_syntax" / timestamp
        for result in changed:
            backup_path = make_backup(result.path, backup_root)
            print(f"Backup created: {backup_path}")

    for result in changed:
        result.path.write_text(result.after, encoding="utf-8")
        print(f"Updated: {result.path}")

    print("\nNext steps:")
    print("  1) Refresh Studio type/syntax checker")
    print("  2) Check: git diff")
    print("  3) If any syntax error remains, upload the affected SideKicks/init.luau file and I will patch it directly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
