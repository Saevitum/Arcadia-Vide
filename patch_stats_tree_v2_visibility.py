#!/usr/bin/env python3
# StatsTree V2 behavior patch: hide/reveal nodes correctly.
#
# Run from the Arcadia-Vide repository root:
#   python patch_stats_tree_v2_visibility.py --dry-run
#   python patch_stats_tree_v2_visibility.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsTree/init.lua
#
# What it fixes:
# - V1 already hides/reveals connection lines with isVisible(...)
# - but nodeView itself does not set Visible, so all stat/mystery nodes can still render
#   even before their group or requirement is opened/met.
#
# This patch:
# - passes opened into nodeView(...)
# - sets ImageButton.Visible = function() return isVisible(node, opened(), levels()) end
# - updates all nodeView(...) calls
#
# Result:
# - only Economy / Skills / Stamina group hubs are visible at first
# - clicking a group hub reveals its first-tier named stat nodes
# - mystery ? nodes appear only after their point requirement is met
#
# Backup:
#   .patch_backups/patch_stats_tree_v2_visibility/<timestamp>/

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
    backup_dir = Path(".patch_backups") / "patch_stats_tree_v2_visibility" / timestamp
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


def patch_node_view_signature(text: str) -> tuple[str, str]:
    if "node: NodeDefinition, levels: Source<{ [string]: number }>, opened: Source<{ [string]: boolean }>," in text:
        return text, "nodeView signature already receives opened"

    pattern = re.compile(
        r"(local\s+function\s+nodeView\s*\(\s*"
        r"node\s*:\s*NodeDefinition\s*,\s*"
        r"levels\s*:\s*Source<\{\s*\[string\]\s*:\s*number\s*\}>\s*,\s*)"
    )

    replacement = r"\1opened: Source<{ [string]: boolean }>, "

    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not patch nodeView signature")

    return text, "Passed opened source into nodeView signature"


def patch_node_visible_property(text: str) -> tuple[str, str]:
    visible_snippet = "Visible = function() return isVisible(node, opened(), levels()) end,"

    if visible_snippet in text:
        return text, "nodeView ImageButton already has Visible binding"

    # In current compact file, this part exists inside nodeView's ImageButton props.
    old = "AutoButtonColor = false, ZIndex = z, Activated = function() onClick(node) end,"
    new = (
        "AutoButtonColor = false, ZIndex = z, "
        + visible_snippet
        + " Activated = function() onClick(node) end,"
    )

    if old in text:
        return text.replace(old, new, 1), "Added Visible binding to nodeView ImageButton"

    # Fallback for slightly different formatting.
    pattern = re.compile(
        r"(AutoButtonColor\s*=\s*false\s*,\s*ZIndex\s*=\s*z\s*,\s*)"
        r"(Activated\s*=\s*function\s*\(\s*\)\s*onClick\(node\)\s*end\s*,)"
    )
    text, count = pattern.subn(r"\1" + visible_snippet + r" \2", text, count=1)
    if count != 1:
        raise RuntimeError("Could not insert Visible binding in nodeView ImageButton")

    return text, "Added Visible binding to nodeView ImageButton via fallback"


def patch_node_view_calls(text: str) -> tuple[str, str]:
    old = "nodeView(n, levels, selectedId, points, clickNode, 110)"
    new = "nodeView(n, levels, opened, selectedId, points, clickNode, 110)"

    if new in text:
        return text, "nodeView calls already pass opened"

    if old in text:
        return text.replace(old, new, 1), "Updated nodeView calls to pass opened"

    # Fallback for typed sources after previous type fixes.
    pattern = re.compile(
        r"nodeView\s*\(\s*n\s*,\s*levels\s*,\s*selectedId\s*,\s*points\s*,\s*clickNode\s*,\s*110\s*\)"
    )
    text, count = pattern.subn(new, text, count=1)
    if count != 1:
        raise RuntimeError("Could not update nodeView call to pass opened")

    return text, "Updated nodeView calls to pass opened via fallback"


def patch_text(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    text, note = patch_node_view_signature(text)
    notes.append(note)

    text, note = patch_node_visible_property(text)
    notes.append(note)

    text, note = patch_node_view_calls(text)
    notes.append(note)

    return text, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch StatsTree V2 node visibility/reveal behavior.")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backup before writing.")
    args = parser.parse_args()

    path = Path.cwd() / TARGET

    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    before = path.read_text(encoding="utf-8")

    try:
        after, notes = patch_text(before)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("No files were changed.")
        return 1

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
    print("  2) Refresh Studio/Hoarcekat")
    print("  3) Open StatsTree.")
    print("  4) Expected behavior:")
    print("     - only Economy / Skills / Stamina hubs visible at first")
    print("     - click Economy to show Money/EXP/Gems/Points/Lucky")
    print("     - spend 1 point into Money or Lucky to reveal its ? node")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
