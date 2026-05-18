#!/usr/bin/env python3
# Update Inventory mock SKINS to NPC skin data.
#
# Run from the Arcadia-Vide repository root:
#   python update_mock_skins_npc_v2.py --dry-run
#   python update_mock_skins_npc_v2.py
#
# Target:
#   src/client/UI/UIManager/Menus/Inventory/MockInventory.lua
#
# This V2 script handles the current repo where the table is named:
#   local SKINS: { SkinItem } = { ... }
#
# not:
#   local MOCK_SKINS = { ... }
#
# It keeps the current UI-compatible fields:
#   ImageId, Owned, Equipped, Locked
#
# and adds the production-style fields:
#   IconImageId, PreviewImageId, Collection, ModelPath, Price, Enabled, ShopVisible, OwnedByDefault
#
# Backup:
#   .patch_backups/update_mock_skins_npc_v2/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/Inventory/MockInventory.lua")


SKINS_BLOCK = '''local SKINS: { SkinItem } = {
\t{
\t\tSkinId = "Astronaut",
\t\tName = "Astronaut",
\t\tDescription = "",
\t\tRarity = "Legendary",
\t\tImageId = "rbxassetid://129333345351079",
\t\tIconImageId = "rbxassetid://129333345351079",
\t\tPreviewImageId = "rbxassetid://129333345351079",
\t\tCollection = "NPCSkins",
\t\tModelPath = { "NPCSkins", "MainHub", "Astronaut" },
\t\tPrice = nil,
\t\tEnabled = true,
\t\tShopVisible = false,
\t\tOwnedByDefault = false,
\t\tOwned = true,
\t\tEquipped = true,
\t\tLocked = false,
\t},
\t{
\t\tSkinId = "MurderKitten",
\t\tName = "MurderKitten",
\t\tDescription = "",
\t\tRarity = "Legendary",
\t\tImageId = "rbxassetid://80395771208314",
\t\tIconImageId = "rbxassetid://80395771208314",
\t\tPreviewImageId = "rbxassetid://80395771208314",
\t\tCollection = "NPCSkins",
\t\tModelPath = { "NPCSkins", "MainHub", "MurderKitten" },
\t\tPrice = nil,
\t\tEnabled = true,
\t\tShopVisible = false,
\t\tOwnedByDefault = false,
\t\tOwned = true,
\t\tEquipped = false,
\t\tLocked = false,
\t},
\t{
\t\tSkinId = "Cat",
\t\tName = "Cat",
\t\tDescription = "",
\t\tRarity = "Legendary",
\t\tImageId = "rbxassetid://76904147821003",
\t\tIconImageId = "rbxassetid://76904147821003",
\t\tPreviewImageId = "rbxassetid://76904147821003",
\t\tCollection = "NPCSkins",
\t\tModelPath = { "NPCSkins", "MainHub", "Cat" },
\t\tPrice = nil,
\t\tEnabled = true,
\t\tShopVisible = false,
\t\tOwnedByDefault = false,
\t\tOwned = true,
\t\tEquipped = false,
\t\tLocked = false,
\t},
\t{
\t\tSkinId = "Chef",
\t\tName = "Chef",
\t\tDescription = "",
\t\tRarity = "Legendary",
\t\tImageId = "rbxassetid://127883244163109",
\t\tIconImageId = "rbxassetid://127883244163109",
\t\tPreviewImageId = "rbxassetid://127883244163109",
\t\tCollection = "NPCSkins",
\t\tModelPath = { "NPCSkins", "MainHub", "Chef" },
\t\tPrice = nil,
\t\tEnabled = true,
\t\tShopVisible = false,
\t\tOwnedByDefault = false,
\t\tOwned = true,
\t\tEquipped = false,
\t\tLocked = false,
\t},
\t{
\t\tSkinId = "Overclock",
\t\tName = "Overclock",
\t\tDescription = "",
\t\tRarity = "Legendary",
\t\tImageId = "rbxassetid://138789250340947",
\t\tIconImageId = "rbxassetid://138789250340947",
\t\tPreviewImageId = "rbxassetid://138789250340947",
\t\tCollection = "NPCSkins",
\t\tModelPath = { "NPCSkins", "MainHub", "Overclock" },
\t\tPrice = nil,
\t\tEnabled = true,
\t\tShopVisible = false,
\t\tOwnedByDefault = false,
\t\tOwned = true,
\t\tEquipped = false,
\t\tLocked = false,
\t},
\t{
\t\tSkinId = "Professor",
\t\tName = "Professor",
\t\tDescription = "",
\t\tRarity = "Legendary",
\t\tImageId = "rbxassetid://84338306153696",
\t\tIconImageId = "rbxassetid://84338306153696",
\t\tPreviewImageId = "rbxassetid://84338306153696",
\t\tCollection = "NPCSkins",
\t\tModelPath = { "NPCSkins", "MainHub", "Professor" },
\t\tPrice = nil,
\t\tEnabled = true,
\t\tShopVisible = false,
\t\tOwnedByDefault = false,
\t\tOwned = true,
\t\tEquipped = false,
\t\tLocked = false,
\t},
}'''


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "update_mock_skins_npc_v2" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def find_table_end(text: str, start: int) -> int:
    brace_depth = 0
    in_string: str | None = None
    escape = False
    opened = False

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
            brace_depth += 1
            opened = True
        elif ch == "}":
            brace_depth -= 1
            if opened and brace_depth == 0:
                return i + 1

        i += 1

    raise RuntimeError("Could not find end of SKINS table")


def patch_skins(text: str) -> str:
    patterns = [
        r"local\s+SKINS\s*:\s*\{\s*SkinItem\s*\}\s*=\s*\{",
        r"local\s+SKINS\s*=\s*\{",
        r"local\s+MOCK_SKINS\s*:\s*\{\s*SkinItem\s*\}\s*=\s*\{",
        r"local\s+MOCK_SKINS\s*=\s*\{",
    ]

    match = None
    for pattern in patterns:
        match = re.search(pattern, text)
        if match is not None:
            break

    if match is None:
        raise RuntimeError("Could not find local SKINS / MOCK_SKINS table in MockInventory.lua")

    start = match.start()
    end = find_table_end(text, match.end() - 1)

    return text[:start] + SKINS_BLOCK + text[end:]


def patch_default_equipped(text: str) -> tuple[str, int]:
    # Current MockInventory.getDefaultEquippedSkinId iterates Equipped == true.
    # We set Astronaut.Equipped = true above, so this is only needed if a separate constant exists.
    new_text, count = re.subn(
        r'local\s+DEFAULT_EQUIPPED_SKIN_ID\s*=\s*"[^"]*"',
        'local DEFAULT_EQUIPPED_SKIN_ID = "Astronaut"',
        text,
        count=1,
    )
    return new_text, count


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
        description="Update Inventory SKINS mock data to supplied NPC skin definitions."
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
        after = patch_skins(before)
        after, equipped_count = patch_default_equipped(after)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("No files were changed.")
        return 1

    if before == after:
        print("No changes needed. SKINS already appear updated.")
        return 0

    print("Planned changes:")
    print("  - Replace local SKINS table with 6 NPCSkins entries:")
    print("    Astronaut, MurderKitten, Cat, Chef, Overclock, Professor")
    print("  - Set Astronaut.Equipped = true for the mock default preview")
    print("  - Keep UI fields: ImageId, Owned, Equipped, Locked")
    print("  - Add production-like fields: IconImageId, PreviewImageId, Collection, ModelPath, Price, Enabled, ShopVisible, OwnedByDefault")
    if equipped_count > 0:
        print('  - Updated DEFAULT_EQUIPPED_SKIN_ID to "Astronaut"')

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
    print("  3) If Luau type errors appear because SkinItem is too narrow, extend InventoryTypes.SkinItem with optional fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
