#!/usr/bin/env python3
# Fix SideKicks menu becoming empty after shared divider patch.
#
# Run from the Arcadia-Vide repository root:
#   python fix_empty_sidekicks_after_divider_patch.py --dry-run
#   python fix_empty_sidekicks_after_divider_patch.py
#
# Cause:
# The previous patch correctly inserted AnimatedPulseDivider, but left behind the old
# SideKickDivider table as a plain grouped table:
#   ({ Name = "SideKickDivider", ... })
#
# That plain table is not a Roblox Instance / Vide component child. It can break the
# Frame's children list and prevent the rest of the menu content from rendering.
#
# This script removes that leftover plain table only. It does NOT remove the new
# AnimatedPulseDivider call.
#
# Backup:
#   .patch_backups/fix_empty_sidekicks_after_divider_patch/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


SIDEKICKS_INIT = Path("src/client/UI/UIManager/Menus/SideKicks/init.luau")
INVENTORY_INIT = Path("src/client/UI/UIManager/Menus/Inventory/init.lua")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def make_backup(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    safe_name = "__".join(path.parts[-5:])
    backup_path = backup_root / safe_name
    shutil.copy2(path, backup_path)
    return backup_path


def unified_diff(path: Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"{path} (before)",
            tofile=f"{path} (after)",
        )
    )


def find_balanced_expression_end(text: str, start: int) -> int:
    paren = 0
    brace = 0
    bracket = 0
    opened = False
    string_quote: str | None = None
    escape = False

    i = start
    while i < len(text):
        ch = text[i]

        if string_quote is not None:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == string_quote:
                string_quote = None
            i += 1
            continue

        if ch in ('"', "'", "`"):
            string_quote = ch
            i += 1
            continue

        if ch == "(":
            paren += 1
            opened = True
        elif ch == ")":
            paren -= 1
        elif ch == "{":
            brace += 1
            opened = True
        elif ch == "}":
            brace -= 1
        elif ch == "[":
            bracket += 1
            opened = True
        elif ch == "]":
            bracket -= 1

        if opened and paren == 0 and brace == 0 and bracket == 0:
            return i + 1

        i += 1

    raise RuntimeError("Could not find end of balanced expression")


def include_trailing_comma_and_spaces(text: str, start: int, end: int) -> tuple[int, int]:
    """
    Remove a full child expression cleanly.

    For:
        ..., AnimatedPulseDivider(...), ({ Name = "SideKickDivider", ... }), SideKickInfo(...)
                                      ^start                         ^end

    we remove from start through the trailing comma/spaces, leaving the comma after
    AnimatedPulseDivider intact.
    """
    i = end
    while i < len(text) and text[i].isspace():
        i += 1

    if i < len(text) and text[i] == ",":
        i += 1
        while i < len(text) and text[i].isspace():
            i += 1

    return start, i


def remove_plain_grouped_named_table(text: str, name: str) -> tuple[str, int]:
    """
    Remove leftover plain grouped table children:
        ({ Name = "SomeName", ... }),
    but DO NOT remove proper:
        create("Frame")({ Name = "SomeName", ... })
    and DO NOT remove:
        AnimatedPulseDivider({ name = "SomeName", ... })
    """
    pattern = re.compile(
        rf"\(\s*\{{\s*Name\s*=\s*{re.escape(chr(34) + name + chr(34))}",
        re.DOTALL,
    )

    count = 0
    result = text

    while True:
        match = pattern.search(result)
        if match is None:
            break

        start = match.start()

        # If this is part of create("Something")({ ... }), do not touch it.
        before = result[max(0, start - 40):start]
        if re.search(r"create\s*\(\s*['\"][A-Za-z]+['\"]\s*\)\s*$", before):
            # Skip this match by temporarily protecting it.
            protected = result[:start] + "__PROTECTED_CREATE_GROUPED_TABLE__(" + result[start + 1:]
            result = protected
            continue

        end = find_balanced_expression_end(result, start)
        remove_start, remove_end = include_trailing_comma_and_spaces(result, start, end)

        result = result[:remove_start] + result[remove_end:]
        count += 1

    # Undo rare protection fallback if it happened.
    result = result.replace("__PROTECTED_CREATE_GROUPED_TABLE__(", "(")

    return result, count


def sanity_check_sidekicks(text: str) -> list[str]:
    warnings: list[str] = []

    if "AnimatedPulseDivider({" not in text:
        warnings.append("AnimatedPulseDivider call is missing from SideKicks/init.luau")

    if 'name = "SideKickDivider"' not in text:
        warnings.append('AnimatedPulseDivider name = "SideKickDivider" was not found')

    if '({ Name = "SideKickDivider"' in text:
        warnings.append('leftover plain ({ Name = "SideKickDivider" ... }) still exists')

    for required in ["SideKickCard({", "ScrollArea({", "SideKickInfo({", "SideKickButtons({"]:
        if required not in text:
            warnings.append(f"expected SideKicks content missing: {required}")

    return warnings


def patch_sidekicks(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    text, removed = remove_plain_grouped_named_table(text, "SideKickDivider")
    notes.append(f"removed {removed} leftover plain SideKickDivider table(s)")

    warnings = sanity_check_sidekicks(text)
    notes.extend([f"WARNING: {warning}" for warning in warnings])

    return text, notes


def patch_inventory_optional(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    # Optional cleanup if the old malformed InventoryDivider table ever survived locally.
    text, removed_divider = remove_plain_grouped_named_table(text, "InventoryDivider")
    if removed_divider > 0:
        notes.append(f"removed {removed_divider} leftover plain InventoryDivider table(s)")

    text, removed_content = remove_plain_grouped_named_table(text, "InventoryContent")
    if removed_content > 0:
        notes.append(f"removed {removed_content} leftover plain InventoryContent table(s)")

    if not notes:
        notes.append("no optional Inventory leftover grouped tables found")

    return text, notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove leftover plain SideKickDivider grouped table that makes SideKicks empty."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backups before writing.")
    parser.add_argument(
        "--inventory-too",
        action="store_true",
        help="Also remove leftover plain grouped InventoryDivider/InventoryContent tables if present.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    sidekicks_path = repo_root / SIDEKICKS_INIT

    if not sidekicks_path.exists():
        print(f"ERROR: Could not find {SIDEKICKS_INIT}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    patches: list[tuple[Path, str, str, list[str]]] = []

    sidekicks_before = read_text(sidekicks_path)
    sidekicks_after, sidekicks_notes = patch_sidekicks(sidekicks_before)
    patches.append((SIDEKICKS_INIT, sidekicks_before, sidekicks_after, sidekicks_notes))

    if args.inventory_too:
        inventory_path = repo_root / INVENTORY_INIT
        if not inventory_path.exists():
            print(f"ERROR: Could not find {INVENTORY_INIT}")
            return 1

        inventory_before = read_text(inventory_path)
        inventory_after, inventory_notes = patch_inventory_optional(inventory_before)
        patches.append((INVENTORY_INIT, inventory_before, inventory_after, inventory_notes))

    print("Patch notes:")
    has_error_warning = False

    for path, before, after, notes in patches:
        print(f"\n{path}")
        for note in notes:
            print(f"  - {note}")
            if note.startswith("WARNING:"):
                has_error_warning = True

    changed = [(path, before, after, notes) for path, before, after, notes in patches if before != after]

    if not changed:
        print("\nNo file changes needed.")
        return 0 if not has_error_warning else 1

    print("\nDiff:\n")
    for path, before, after, _notes in changed:
        print(unified_diff(path, before, after))

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0 if not has_error_warning else 1

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "fix_empty_sidekicks_after_divider_patch" / timestamp

        for path, before, after, _notes in changed:
            backup_path = make_backup(repo_root / path, backup_root)
            print(f"Backup created: {backup_path}")

    for path, before, after, _notes in changed:
        write_text(repo_root / path, after)
        print(f"Updated: {path}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Studio/Hoarcekat")
    print("  3) Open SideKicks again. Cards/info/buttons should return.")
    print("  4) If Inventory also has leftover grouped tables, rerun with --inventory-too.")
    return 0 if not has_error_warning else 1


if __name__ == "__main__":
    raise SystemExit(main())
