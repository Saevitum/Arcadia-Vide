#!/usr/bin/env python3
"""
Restore/slow SideKicks + Inventory pulse timing and make Inventory open/close motion match SideKicks.

Run from the Arcadia-Vide repository root:

    python restore_inventory_sidekick_effects.py --dry-run
    python restore_inventory_sidekick_effects.py

Targets current repo around:
    8a4c067 Inventory menu V6

What this changes:

1) Slows the info-frame UIStroke pulse in BOTH menus
   - SideKicks/SideKickInfo.lua
   - Inventory/SelectedSkinInfo.lua

   Changes:
       phaseMultiplier = 3
   to:
       phaseMultiplier = 1

   Reason:
   PulseDriver already runs at duration = 3.6.
   phaseMultiplier = 3 makes the info stroke pulse 3 times inside that cycle, which looks too fast.
   phaseMultiplier = 1 restores the slower "one info pulse per full driver cycle" behavior.

2) Makes Inventory divider color sweep timing match SideKicks more closely
   - Inventory/init.lua

   Changes:
       loopsPerColor = 1 -> loopsPerColor = 3
       colorTweenDuration = 0.22 -> colorTweenDuration = 0.45

   Also adds the same Sine easing options SideKicks uses for the sweep/color tween.

3) Makes Inventory divider fade match SideKicks
   - Inventory/init.lua

   Changes InventoryDivider FadeGuiObject from quick duration-only fade to:
       openDuration = 3
       closeDuration = 0.08
       easingStyle = Enum.EasingStyle.Quad
       easingDirection = Enum.EasingDirection.Out

4) Makes Inventory SkinsScrollArea layout tween match SideKicks' poppy/bouncy feel
   - Inventory/SkinsPage.lua

   Replaces the Inventory layoutTween timing/easing/bounce block with the SideKicks-style values:
       duration = 0.38
       easingStyle = Enum.EasingStyle.Quint
       easingDirection = Enum.EasingDirection.Out
       overshoot = 0.09
       firstDuration = 0.22
       settleDuration = 0.16
       Quint.Out / Quint.Out

Backups:
- Before writing, backups are created under:
  .patch_backups/restore_inventory_sidekick_effects/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SIDEKICK_INFO = Path("src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua")
INVENTORY_INFO = Path("src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua")
INVENTORY_INIT = Path("src/client/UI/UIManager/Menus/Inventory/init.lua")
INVENTORY_SKINS = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")


@dataclass(frozen=True)
class PatchResult:
    path: Path
    before: str
    after: str
    notes: list[str]


def make_backup(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    safe_name = "__".join(path.parts[-5:])
    backup_path = backup_root / safe_name
    shutil.copy2(path, backup_path)
    return backup_path


def normalize_info_pulse_multiplier(text: str) -> tuple[str, int]:
    """
    Target PulseGradientOffset phaseMultiplier in info frames.
    We intentionally patch all phaseMultiplier assignments in these two info files,
    because these files only use it for the info-frame UIStroke pulse.
    """
    new_text, count = re.subn(
        r"phaseMultiplier\s*=\s*3\s*,",
        "phaseMultiplier = 1,",
        text,
    )
    return new_text, count


def patch_inventory_sweep_timing(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    new_text = text

    if "loopsPerColor = 1" in new_text:
        new_text = new_text.replace("loopsPerColor = 1,", "loopsPerColor = 3,", 1)
        notes.append("Inventory divider loopsPerColor: 1 -> 3")

    if "colorTweenDuration = 0.22" in new_text:
        new_text = new_text.replace("colorTweenDuration = 0.22,", "colorTweenDuration = 0.45,", 1)
        notes.append("Inventory divider colorTweenDuration: 0.22 -> 0.45")

    # Add SideKicks-like motion easing after loopsPerColor if missing in this file's sweep options.
    sweep_start = new_text.find("Effects.SweepGradientKeypoint({")
    if sweep_start != -1:
        sweep_context = new_text[sweep_start:sweep_start + 900]

        if "segmentDuration" not in sweep_context:
            new_text = new_text.replace(
                "loopsPerColor = 3,",
                (
                    "loopsPerColor = 3, "
                    "segmentDuration = 1.2, "
                    "easingStyle = Enum.EasingStyle.Sine, "
                    "easingDirection = Enum.EasingDirection.InOut,"
                ),
                1,
            )
            notes.append("Inventory divider added SideKicks-like segmentDuration/easing")

        # Recompute because text may have changed.
        sweep_start = new_text.find("Effects.SweepGradientKeypoint({")
        sweep_context = new_text[sweep_start:sweep_start + 1100]

        if "colorEasingStyle" not in sweep_context:
            new_text = new_text.replace(
                "colorTweenDuration = 0.45,",
                (
                    "colorTweenDuration = 0.45, "
                    "colorEasingStyle = Enum.EasingStyle.Sine, "
                    "colorEasingDirection = Enum.EasingDirection.InOut,"
                ),
                1,
            )
            notes.append("Inventory divider added SideKicks-like color easing")

    return new_text, notes


def patch_inventory_divider_fade(text: str) -> tuple[str, list[str]]:
    """
    Replace the InventoryDivider FadeGuiObject block with SideKicks-style fade timing.

    Handles the current minified one-line style.
    """
    notes: list[str] = []
    pattern = re.compile(
        r"Effects\.FadeGuiObject\(\{\s*"
        r"open\s*=\s*hasSelectedSkin\s*,\s*"
        r"openTransparency\s*=\s*0\s*,\s*"
        r"closedTransparency\s*=\s*1\s*,\s*"
        r"(?:duration\s*=\s*[-+]?\d*\.?\d+\s*,\s*)?"
        r"(?:openDuration\s*=\s*[-+]?\d*\.?\d+\s*,\s*)?"
        r"(?:closeDuration\s*=\s*[-+]?\d*\.?\d+\s*,\s*)?"
        r"(?:easingStyle\s*=\s*Enum\.EasingStyle\.[A-Za-z]+\s*,\s*)?"
        r"(?:easingDirection\s*=\s*Enum\.EasingDirection\.[A-Za-z]+\s*,\s*)?"
        r"hideWhenClosed\s*=\s*true\s*,?\s*"
        r"\}\)"
    )

    replacement = (
        "Effects.FadeGuiObject({ "
        "open = hasSelectedSkin, "
        "openTransparency = 0, "
        "closedTransparency = 1, "
        "openDuration = 3, "
        "closeDuration = 0.08, "
        "easingStyle = Enum.EasingStyle.Quad, "
        "easingDirection = Enum.EasingDirection.Out, "
        "hideWhenClosed = true, "
        "})"
    )

    new_text, count = pattern.subn(replacement, text, count=1)
    if count == 1:
        notes.append("InventoryDivider FadeGuiObject now matches SideKicks-style open/close fade timing")
    else:
        # Not fatal: user may have edited the block manually.
        notes.append("WARNING: InventoryDivider FadeGuiObject block was not found; skipped fade timing patch")

    return new_text, notes


def patch_inventory_layout_tween(text: str) -> tuple[str, list[str]]:
    """
    Replace SkinsPage layoutTween timing/easing/bounce block with SideKicks-style settings.
    """
    notes: list[str] = []

    target_size = (
        "targetSize = function() "
        "if hasSelectedSkin(props) then return PAGE_DETAIL_SIZE end "
        "return PAGE_FULL_SIZE end,"
    )
    target_position = (
        "targetPosition = function() "
        "if hasSelectedSkin(props) then return PAGE_DETAIL_POSITION end "
        "return PAGE_FULL_POSITION end,"
    )

    replacement = (
        "layoutTween = { "
        "isOpen = function() return hasSelectedSkin(props) end, "
        f"{target_size} "
        f"{target_position} "
        "duration = 0.38, "
        "easingStyle = Enum.EasingStyle.Quint, "
        "easingDirection = Enum.EasingDirection.Out, "
        "bounce = { "
        "overshoot = 0.09, "
        "firstDuration = 0.22, "
        "settleDuration = 0.16, "
        "firstEasingStyle = Enum.EasingStyle.Quint, "
        "firstEasingDirection = Enum.EasingDirection.Out, "
        "settleEasingStyle = Enum.EasingStyle.Quint, "
        "settleEasingDirection = Enum.EasingDirection.Out, "
        "}, "
        "}, "
        "scrollBarThickness ="
    )

    # Current minified pattern in SkinsPage.lua.
    pattern = re.compile(
        r"layoutTween\s*=\s*\{\s*"
        r"isOpen\s*=\s*function\(\)\s*return\s+hasSelectedSkin\(props\)\s*end\s*,\s*"
        r"targetSize\s*=\s*function\(\)\s*if\s+hasSelectedSkin\(props\)\s*then\s*return\s+PAGE_DETAIL_SIZE\s*end\s*return\s+PAGE_FULL_SIZE\s*end\s*,\s*"
        r"targetPosition\s*=\s*function\(\)\s*if\s+hasSelectedSkin\(props\)\s*then\s*return\s+PAGE_DETAIL_POSITION\s*end\s*return\s+PAGE_FULL_POSITION\s*end\s*,\s*"
        r".*?"
        r"\}\s*,\s*scrollBarThickness\s*=",
        re.DOTALL,
    )

    new_text, count = pattern.subn(replacement, text, count=1)

    if count == 1:
        notes.append("SkinsPage layoutTween now uses SideKicks-style Quint bounce settings")
    else:
        notes.append("WARNING: SkinsPage layoutTween block was not found; skipped layout tween patch")

    return new_text, notes


def patch_file(path: Path) -> PatchResult:
    before = path.read_text(encoding="utf-8")
    after = before
    notes: list[str] = []

    if path == SIDEKICK_INFO or path == INVENTORY_INFO:
        after, count = normalize_info_pulse_multiplier(after)
        if count > 0:
            notes.append(f"Info pulse phaseMultiplier: 3 -> 1 ({count} replacement(s))")
        else:
            notes.append("No phaseMultiplier = 3 found; info pulse may already be slowed")

    elif path == INVENTORY_INIT:
        after, sweep_notes = patch_inventory_sweep_timing(after)
        notes.extend(sweep_notes)

        after, fade_notes = patch_inventory_divider_fade(after)
        notes.extend(fade_notes)

    elif path == INVENTORY_SKINS:
        after, layout_notes = patch_inventory_layout_tween(after)
        notes.extend(layout_notes)

    return PatchResult(path=path, before=before, after=after, notes=notes)


def print_diff(result: PatchResult) -> None:
    diff = difflib.unified_diff(
        result.before.splitlines(keepends=True),
        result.after.splitlines(keepends=True),
        fromfile=f"{result.path} (before)",
        tofile=f"{result.path} (after)",
    )
    print("".join(diff))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restore slower SideKicks/Inventory pulse timing and SideKicks-like Inventory bounce."
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
    targets = [SIDEKICK_INFO, INVENTORY_INFO, INVENTORY_INIT, INVENTORY_SKINS]

    missing = [target for target in targets if not (repo_root / target).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from the Arcadia-Vide repository root.")
        return 1

    results = [patch_file(repo_root / target) for target in targets]
    changed = [result for result in results if result.before != result.after]

    print("Patch notes:")
    for result in results:
        print(f"\n{result.path}")
        for note in result.notes:
            print(f"  - {note}")

    if not changed:
        print("\nNo file changes needed.")
        return 0

    print("\nDiff:\n")
    for result in changed:
        print_diff(result)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "restore_inventory_sidekick_effects" / timestamp
        for result in changed:
            backup_path = make_backup(result.path, backup_root)
            print(f"Backup created: {backup_path}")

    for result in changed:
        result.path.write_text(result.after, encoding="utf-8")
        print(f"Updated: {result.path}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Hoarcekat/Studio")
    print("  3) Test SideKicks and Inventory selected/open + deselect/close transitions")
    print("  4) If the info pulse is now too slow, set only phaseMultiplier back to 2, not 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
