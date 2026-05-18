#!/usr/bin/env python3
"""
Fix Luau type error in Effects/TweenGradientAccentColor.lua.

Run from the Arcadia-Vide repository root:

    python fix_tween_gradient_accent_type.py --dry-run
    python fix_tween_gradient_accent_type.py

Fixes:
    Type Error: Expected '"EdgeAccent" | "StartAccent"' but got 'string | string | string'

Cause:
    Luau widens:
        local mode = options.mode or "StartAccent"
    to a generic string-ish type, even though the option type is a string literal union.

Patch:
    local mode: "StartAccent" | "EdgeAccent" = options.mode or "StartAccent"

Backups:
- Before writing, creates a backup under:
  .patch_backups/fix_tween_gradient_accent_type/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Effects/TweenGradientAccentColor.lua")


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "fix_tween_gradient_accent_type" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def patch_text(text: str) -> tuple[str, int]:
    # Most likely current line from the generated file.
    pattern = re.compile(
        r'local\s+mode\s*=\s*options\.mode\s+or\s+"StartAccent"'
    )

    replacement = 'local mode: "StartAccent" | "EdgeAccent" = options.mode or "StartAccent"'
    new_text, count = pattern.subn(replacement, text, count=1)

    return new_text, count


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
        description="Fix mode literal-union widening in TweenGradientAccentColor.lua."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show diff without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a backup before writing.",
    )
    args = parser.parse_args()

    path = Path.cwd() / TARGET

    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    old_text = path.read_text(encoding="utf-8")
    new_text, count = patch_text(old_text)

    if count == 0:
        if 'local mode: "StartAccent" | "EdgeAccent"' in old_text:
            print("No changes needed. The mode variable is already explicitly typed.")
            return 0

        print('ERROR: Could not find `local mode = options.mode or "StartAccent"`.')
        print("The file may have changed. Patch manually with:")
        print('  local mode: "StartAccent" | "EdgeAccent" = options.mode or "StartAccent"')
        return 1

    print("Planned change:")
    print('  - local mode = options.mode or "StartAccent"')
    print('  + local mode: "StartAccent" | "EdgeAccent" = options.mode or "StartAccent"')
    print()
    print_diff(TARGET, old_text, new_text)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        backup_path = make_backup(path)
        print(f"\nBackup created: {backup_path}")

    path.write_text(new_text, encoding="utf-8")
    print(f"Updated: {TARGET}")

    print("\nNext steps:")
    print("  1) Refresh Studio type checker")
    print("  2) Check: git diff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
