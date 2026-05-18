#!/usr/bin/env python3
"""
Tune scrollbars and divider thickness for SideKicks + Inventory.

Run from the Arcadia-Vide repository root:

    python tune_scrollbars_and_dividers.py --dry-run
    python tune_scrollbars_and_dividers.py

What it changes:
1) Components/ScrollArea.lua
   - Adds support for ScrollingFrame.VerticalScrollBarPosition.
   - Default stays Right, so existing scroll areas do not silently change.

2) UITypes/ComponentTypes/ScrollAreaTypes.lua
   - Adds verticalScrollBarPosition: Enum.VerticalScrollBarPosition?

3) Menus/SideKicks/init.luau
   - Sets SideKickScrollArea.verticalScrollBarPosition = Enum.VerticalScrollBarPosition.Left.
   - Ensures SideKickScrollArea.ScrollBarImageColor3 is black.
   - Ensures SideKick divider thickness is slim: UDim2.fromScale(0.0015, 0.5).

4) Menus/Inventory/SkinsPage.lua
   - Sets SkinsScrollArea.verticalScrollBarPosition = Enum.VerticalScrollBarPosition.Left.
   - Sets SkinsScrollArea.ScrollBarImageColor3 to black.
   - Sets ScrollBarImageTransparency to 0 for a solid black scrollbar.

5) Menus/Inventory/init.lua
   - Sets Inventory divider thickness to match SideKicks:
     UDim2.fromScale(0.0015, 0.5).

Backups:
- Before writing, backups are created under:
  .patch_backups/scrollbars_and_dividers/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SCROLLAREA_FILE = Path("src/client/UI/UIManager/Components/ScrollArea.lua")
SCROLLAREA_TYPES_FILE = Path("src/client/UI/UIManager/UITypes/ComponentTypes/ScrollAreaTypes.lua")
SIDEKICKS_FILE = Path("src/client/UI/UIManager/Menus/SideKicks/init.luau")
INVENTORY_SKINS_FILE = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")
INVENTORY_INIT_FILE = Path("src/client/UI/UIManager/Menus/Inventory/init.lua")


@dataclass(frozen=True)
class FilePatch:
    path: Path
    before: str
    after: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def make_backup(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)

    # Preserve a little path context to avoid collisions between init.lua files.
    safe_name = "__".join(path.parts[-5:])
    backup_path = backup_root / safe_name
    shutil.copy2(path, backup_path)
    return backup_path


def replace_once(text: str, pattern: str, replacement: str, description: str, flags: int = 0) -> str:
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"Could not patch: {description}")
    return new_text


def ensure_scrollarea_type_support(text: str) -> str:
    if "verticalScrollBarPosition: Enum.VerticalScrollBarPosition?" in text:
        return text

    # Current type has verticalScrollBarInset followed by horizontalScrollBarInset.
    return replace_once(
        text,
        r"(verticalScrollBarInset:\s*Enum\.ScrollBarInset\?,\s*)",
        r"\1verticalScrollBarPosition: Enum.VerticalScrollBarPosition?, ",
        "ScrollAreaTypes.verticalScrollBarPosition",
    )


def ensure_scrollarea_runtime_support(text: str) -> str:
    if "VerticalScrollBarPosition =" in text:
        return text

    # Insert the ScrollingFrame property near VerticalScrollBarInset.
    return replace_once(
        text,
        r"(VerticalScrollBarInset\s*=\s*resolvedProps\.verticalScrollBarInset\s+or\s+Enum\.ScrollBarInset\.None,\s*)",
        r"\1VerticalScrollBarPosition = resolvedProps.verticalScrollBarPosition or Enum.VerticalScrollBarPosition.Right, ",
        "ScrollArea.VerticalScrollBarPosition",
    )


def ensure_scrollarea_prop_in_call(text: str, area_name: str) -> str:
    """
    Add verticalScrollBarPosition to a ScrollArea call after name = "<area_name>".

    This is intentionally simple and local:
    - If the file already contains verticalScrollBarPosition anywhere, we do not add another.
    - That is fine for these feature files because each target file has one relevant ScrollArea.
    """
    if "verticalScrollBarPosition" in text:
        return text

    pattern = rf'(name\s*=\s*"{re.escape(area_name)}"\s*,\s*)'
    replacement = rf'\1verticalScrollBarPosition = Enum.VerticalScrollBarPosition.Left, '
    return replace_once(
        text,
        pattern,
        replacement,
        f"{area_name}.verticalScrollBarPosition",
    )


def set_scrollbar_black(text: str, preferred_expr: str = "Color3.fromRGB(0, 0, 0)") -> str:
    pattern = r"scrollBarImageColor3\s*=\s*[^,\n]+,"
    replacement = f"scrollBarImageColor3 = {preferred_expr},"
    return replace_once(
        text,
        pattern,
        replacement,
        "scrollBarImageColor3 black",
    )


def set_scrollbar_transparency(text: str, value: str = "0") -> str:
    pattern = r"scrollBarImageTransparency\s*=\s*[^,\n]+,"
    replacement = f"scrollBarImageTransparency = {value},"
    return replace_once(
        text,
        pattern,
        replacement,
        "scrollBarImageTransparency",
    )


def set_local_udim2_constant(text: str, constant_name: str, value: str) -> str:
    pattern = (
        rf"(?P<prefix>\blocal\s+{re.escape(constant_name)}\s*=\s*)"
        rf"UDim2\.fromScale\(\s*[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*\)"
    )
    replacement = rf"\g<prefix>{value}"
    return replace_once(text, pattern, replacement, constant_name)


def set_inline_frame_size(text: str, frame_name: str, value: str) -> str:
    """
    SideKickDivider currently uses inline:
        Name = "SideKickDivider", Size = UDim2.fromScale(...)
    """
    pattern = (
        rf'(?P<prefix>Name\s*=\s*"{re.escape(frame_name)}"\s*,\s*Size\s*=\s*)'
        rf"UDim2\.fromScale\(\s*[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*\)"
    )
    replacement = rf"\g<prefix>{value}"
    return replace_once(text, pattern, replacement, f"{frame_name}.Size")


def patch_scrollarea_types(repo_root: Path) -> FilePatch:
    path = repo_root / SCROLLAREA_TYPES_FILE
    before = read_text(path)
    after = ensure_scrollarea_type_support(before)
    return FilePatch(SCROLLAREA_TYPES_FILE, before, after)


def patch_scrollarea_component(repo_root: Path) -> FilePatch:
    path = repo_root / SCROLLAREA_FILE
    before = read_text(path)
    after = ensure_scrollarea_runtime_support(before)
    return FilePatch(SCROLLAREA_FILE, before, after)


def patch_sidekicks(repo_root: Path) -> FilePatch:
    path = repo_root / SIDEKICKS_FILE
    before = read_text(path)
    after = before
    after = ensure_scrollarea_prop_in_call(after, "SideKickScrollArea")
    after = set_scrollbar_black(after, "Color3.fromRGB(0, 0, 0)")
    after = set_scrollbar_transparency(after, "0")
    after = set_inline_frame_size(after, "SideKickDivider", "UDim2.fromScale(0.0015, 0.5)")
    return FilePatch(SIDEKICKS_FILE, before, after)


def patch_inventory_skins(repo_root: Path) -> FilePatch:
    path = repo_root / INVENTORY_SKINS_FILE
    before = read_text(path)
    after = before
    after = ensure_scrollarea_prop_in_call(after, "SkinsScrollArea")
    after = set_scrollbar_black(after, "Color3.fromRGB(0, 0, 0)")
    after = set_scrollbar_transparency(after, "0")
    return FilePatch(INVENTORY_SKINS_FILE, before, after)


def patch_inventory_init(repo_root: Path) -> FilePatch:
    path = repo_root / INVENTORY_INIT_FILE
    before = read_text(path)
    after = set_local_udim2_constant(before, "DIVIDER_SIZE", "UDim2.fromScale(0.0015, 0.5)")
    return FilePatch(INVENTORY_INIT_FILE, before, after)


def print_diff(patch: FilePatch) -> None:
    diff = difflib.unified_diff(
        patch.before.splitlines(keepends=True),
        patch.after.splitlines(keepends=True),
        fromfile=f"{patch.path} (before)",
        tofile=f"{patch.path} (after)",
    )
    print("".join(diff))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Move SideKicks/Inventory scrollbars left, make them black, and slim Inventory divider."
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

    required = [
        SCROLLAREA_FILE,
        SCROLLAREA_TYPES_FILE,
        SIDEKICKS_FILE,
        INVENTORY_SKINS_FILE,
        INVENTORY_INIT_FILE,
    ]

    missing = [path for path in required if not (repo_root / path).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from the Arcadia-Vide repository root.")
        return 1

    try:
        patches = [
            patch_scrollarea_types(repo_root),
            patch_scrollarea_component(repo_root),
            patch_sidekicks(repo_root),
            patch_inventory_skins(repo_root),
            patch_inventory_init(repo_root),
        ]
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("The current files differ from the expected structure. Patch manually or update this script.")
        return 1

    changed = [patch for patch in patches if patch.before != patch.after]

    if not changed:
        print("No changes needed. Scrollbar/divider tuning already appears to be applied.")
        return 0

    print("Planned changes:")
    print("  - Add ScrollArea.verticalScrollBarPosition prop/type support")
    print("  - SideKickScrollArea: scrollbar left + black")
    print("  - SkinsScrollArea: scrollbar left + black")
    print("  - SideKickDivider and InventoryDivider thickness: 0.0015")
    print("\nDiff:\n")

    for patch in changed:
        print_diff(patch)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "scrollbars_and_dividers" / timestamp
        for patch in changed:
            backup_path = make_backup(repo_root / patch.path, backup_root)
            print(f"Backup created: {backup_path}")

    for patch in changed:
        write_text(repo_root / patch.path, patch.after)
        print(f"Updated: {patch.path}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Hoarcekat/Studio")
    print("  3) If the left scrollbar overlaps cards too much, increase left padding slightly in the relevant ScrollArea.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
