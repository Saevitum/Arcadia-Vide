#!/usr/bin/env python3
# Fix StatsTree V1 strict type errors caused by optional props and generic Source alias.
#
# Run from the Arcadia-Vide repository root:
#   python fix_stats_tree_v1_type_errors.py --dry-run
#   python fix_stats_tree_v1_type_errors.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsTree/init.lua
#
# Fixes:
# - `props: StatsTreeMenuProps?` was assigned `props = props or {}`, but Luau strict
#   still treats later `props.visible` / `props.store` reads as possibly nil.
# - Replaces that with:
#     local function StatsTreeMenu(rawProps: StatsTreeMenuProps?)
#         local props: StatsTreeMenuProps = rawProps or {}
# - Rewrites the two props.store/currentMenu access blocks to use local narrowed variables.
# - Fixes the generic Source alias and several missing Source<T> annotations.
#
# Backup:
#   .patch_backups/fix_stats_tree_v1_type_errors/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/StatsTree/init.lua")


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "fix_stats_tree_v1_type_errors" / timestamp
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


def patch_source_aliases(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    after = text

    replacements = [
        (
            r"type\s+Source\s*=\s*\(\(\)\s*->\s*T\)\s*&\s*\(\(T\)\s*->\s*\(\)\)",
            "type Source<T> = (() -> T) & ((T) -> ())",
            "Fixed generic Source<T> alias",
        ),
        (
            r"selectedId\s*:\s*Source\s*=\s*source\(nil\s*::\s*string\?\)",
            "selectedId: Source<string?> = source(nil :: string?)",
            "Typed selectedId as Source<string?>",
        ),
        (
            r"points\s*:\s*Source\s*=\s*source\(INITIAL_POINTS\)",
            "points: Source<number> = source(INITIAL_POINTS)",
            "Typed points as Source<number>",
        ),
        (
            r"pan\s*:\s*Source\s*=\s*source\(Vector2\.new\(0,\s*0\)\)",
            "pan: Source<Vector2> = source(Vector2.new(0, 0))",
            "Typed pan as Source<Vector2>",
        ),
        (
            r"zoom\s*:\s*Source\s*=\s*source\(1\)",
            "zoom: Source<number> = source(1)",
            "Typed zoom as Source<number>",
        ),
        (
            r"selectedId\s*:\s*Source,\s*points\s*:\s*Source,",
            "selectedId: Source<string?>, points: Source<number>,",
            "Typed nodeView selectedId/points parameters",
        ),
        (
            r"detailsView\(selectedId\s*:\s*Source,\s*levels\s*:\s*Source<\{\s*\[string\]\s*:\s*number\s*\}>,\s*points\s*:\s*Source,",
            "detailsView(selectedId: Source<string?>, levels: Source<{ [string]: number }>, points: Source<number>,",
            "Typed detailsView selectedId/points parameters",
        ),
    ]

    for pattern, replacement, note in replacements:
        after, count = re.subn(pattern, replacement, after, count=1)
        if count > 0:
            notes.append(note)

    return after, notes


def patch_optional_props(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    after = text

    # Current V1 compact form:
    # local function StatsTreeMenu(props: StatsTreeMenuProps?) props = props or {}
    after, count = re.subn(
        r"local\s+function\s+StatsTreeMenu\s*\(\s*props\s*:\s*StatsTreeMenuProps\?\s*\)\s*props\s*=\s*props\s*or\s*\{\}",
        "local function StatsTreeMenu(rawProps: StatsTreeMenuProps?) local props: StatsTreeMenuProps = rawProps or {}",
        after,
        count=1,
    )
    if count > 0:
        notes.append("Changed optional props parameter to non-nil local props")
    elif "local function StatsTreeMenu(rawProps: StatsTreeMenuProps?) local props: StatsTreeMenuProps = rawProps or {}" in after:
        notes.append("Props nil-narrowing patch already present")
    else:
        raise RuntimeError("Could not find StatsTreeMenu optional props initializer")

    old_menu_visible = (
        'local function menuVisible(): boolean '
        'if props.visible ~= nil then return props.visible() end '
        'if props.store ~= nil and props.store.currentMenu ~= nil then return props.store.currentMenu() == "StatsTree" end '
        'return true end'
    )

    new_menu_visible = (
        'local function menuVisible(): boolean '
        'local visible = props.visible '
        'if visible ~= nil then return visible() end '
        'local store = props.store '
        'if store ~= nil then '
        'local currentMenu = store.currentMenu '
        'if currentMenu ~= nil then return currentMenu() == "StatsTree" end '
        'end '
        'return true end'
    )

    if old_menu_visible in after:
        after = after.replace(old_menu_visible, new_menu_visible, 1)
        notes.append("Rewrote menuVisible with local narrowed visible/store/currentMenu")
    elif new_menu_visible in after:
        notes.append("menuVisible narrowing already present")
    else:
        # More flexible fallback for formatted / changed versions.
        pattern = re.compile(
            r"local\s+function\s+menuVisible\s*\(\s*\)\s*:\s*boolean\s*"
            r"if\s+props\.visible\s*~=\s*nil\s+then\s+return\s+props\.visible\(\)\s+end\s*"
            r"if\s+props\.store\s*~=\s*nil\s+and\s+props\.store\.currentMenu\s*~=\s*nil\s+then\s+return\s+props\.store\.currentMenu\(\)\s*==\s*\"StatsTree\"\s+end\s*"
            r"return\s+true\s+end",
            re.DOTALL,
        )
        after, fallback_count = pattern.subn(new_menu_visible, after, count=1)
        if fallback_count > 0:
            notes.append("Rewrote menuVisible with local narrowed visible/store/currentMenu via fallback")
        else:
            raise RuntimeError("Could not find menuVisible props access block")

    old_close = (
        'Activated = function() '
        'if props.store ~= nil and props.store.currentMenu ~= nil then props.store.currentMenu(nil) end '
        'end,'
    )

    new_close = (
        'Activated = function() '
        'local store = props.store '
        'if store == nil then return end '
        'local currentMenu = store.currentMenu '
        'if currentMenu ~= nil then currentMenu(nil) end '
        'end,'
    )

    if old_close in after:
        after = after.replace(old_close, new_close, 1)
        notes.append("Rewrote CloseButton Activated with local narrowed store/currentMenu")
    elif new_close in after:
        notes.append("CloseButton narrowing already present")
    else:
        pattern = re.compile(
            r"Activated\s*=\s*function\(\)\s*"
            r"if\s+props\.store\s*~=\s*nil\s+and\s+props\.store\.currentMenu\s*~=\s*nil\s+then\s+props\.store\.currentMenu\(nil\)\s+end\s*"
            r"end\s*,",
            re.DOTALL,
        )
        after, fallback_count = pattern.subn(new_close, after, count=1)
        if fallback_count > 0:
            notes.append("Rewrote CloseButton Activated with local narrowed store/currentMenu via fallback")
        else:
            raise RuntimeError("Could not find CloseButton props.store access block")

    return after, notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix StatsTree V1 Luau strict type errors around optional props."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a backup before writing.")
    args = parser.parse_args()

    path = Path.cwd() / TARGET

    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    before = path.read_text(encoding="utf-8")

    try:
        after, source_notes = patch_source_aliases(before)
        after, props_notes = patch_optional_props(after)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("No files were changed.")
        return 1

    notes = source_notes + props_notes

    print("Patch notes:")
    for note in notes:
        print(f"  - {note}")

    if before == after:
        print("\nNo changes needed.")
        return 0

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
    print("  2) Refresh Studio type checker")
    print("  3) If more StatsTree errors appear, send the new list and we will patch the next layer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
