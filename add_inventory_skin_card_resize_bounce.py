#!/usr/bin/env python3
# Add bouncy Inventory SkinCard grid cell-size animation.
#
# Run from the Arcadia-Vide repository root:
#   python add_inventory_skin_card_resize_bounce.py --dry-run
#   python add_inventory_skin_card_resize_bounce.py
#
# Target:
#   src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua
#
# Why:
# - SkinsScrollArea.layoutTween already uses the same SideKicks-like bounce config.
# - But SkinCard cell size still changes through a reactive UIGridLayout.CellSize function.
# - That means the ScrollArea frame can bounce, while the SkinCards themselves can still
#   snap/smooth-resize differently when selectedSkin changes.
#
# This patch:
# - Adds a local animatedCellSize source inside SkinsPage().
# - Tweens that source with the same SideKicks bounce timings:
#     firstDuration = 0.22
#     settleDuration = 0.16
#     overshoot = 0.09
#     Quint.Out -> Quint.Out
# - Changes grid.cellSize to read animatedCellSize instead of directly switching between
#   GRID_FULL_CELL_SIZE and GRID_DETAIL_CELL_SIZE.
#
# Final sizes are unchanged:
# - GRID_FULL_CELL_SIZE
# - GRID_DETAIL_CELL_SIZE
#
# Backup:
#   .patch_backups/add_inventory_skin_card_resize_bounce/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua")


ANIMATED_CELL_SIZE_BLOCK = """local animatedCellSize = source(GRID_FULL_CELL_SIZE)
\tlocal cellSizeDriver = Instance.new("Vector3Value")
\tcellSizeDriver.Name = "SkinInventoryCellSizeDriver"
\tcellSizeDriver.Value = Vector3.new(GRID_FULL_CELL_SIZE.X.Scale, GRID_FULL_CELL_SIZE.Y.Scale, 0)

\tlocal activeCellSizeTweens: { Tween } = {}
\tlocal activeCellSizeConnection: RBXScriptConnection? = nil
\tlocal firstCellSizeRun = true
\tlocal cellSizeRunId = 0

\tlocal function cancelCellSizeTweens()
\t\tfor _, tween in ipairs(activeCellSizeTweens) do
\t\t\ttween:Cancel()
\t\tend

\t\ttable.clear(activeCellSizeTweens)

\t\tif activeCellSizeConnection ~= nil then
\t\t\tactiveCellSizeConnection:Disconnect()
\t\t\tactiveCellSizeConnection = nil
\t\tend
\tend

\tlocal function setAnimatedCellSizeFromDriver()
\t\tlocal value = cellSizeDriver.Value
\t\tanimatedCellSize(UDim2.fromScale(value.X, value.Y))
\tend

\tlocal cellSizeChangedConnection = cellSizeDriver:GetPropertyChangedSignal("Value"):Connect(setAnimatedCellSizeFromDriver)
\tsetAnimatedCellSizeFromDriver()

\teffect(function()
\t\tcellSizeRunId += 1
\t\tlocal currentRunId = cellSizeRunId

\t\tlocal target = if hasSelectedSkin(props) then GRID_DETAIL_CELL_SIZE else GRID_FULL_CELL_SIZE
\t\tlocal targetValue = Vector3.new(target.X.Scale, target.Y.Scale, 0)

\t\tif firstCellSizeRun then
\t\t\tfirstCellSizeRun = false
\t\t\tcellSizeDriver.Value = targetValue
\t\t\tsetAnimatedCellSizeFromDriver()
\t\t\treturn
\t\tend

\t\tcancelCellSizeTweens()

\t\tlocal currentValue = cellSizeDriver.Value
\t\tlocal overshootAmount = 0.09
\t\tlocal overshootValue = Vector3.new(
\t\t\ttargetValue.X + ((targetValue.X - currentValue.X) * overshootAmount),
\t\t\ttargetValue.Y + ((targetValue.Y - currentValue.Y) * overshootAmount),
\t\t\t0
\t\t)

\t\tlocal firstTween = TweenService:Create(
\t\t\tcellSizeDriver,
\t\t\tTweenInfo.new(0.22, Enum.EasingStyle.Quint, Enum.EasingDirection.Out),
\t\t\t{
\t\t\t\tValue = overshootValue,
\t\t\t}
\t\t)

\t\tlocal settleTween = TweenService:Create(
\t\t\tcellSizeDriver,
\t\t\tTweenInfo.new(0.16, Enum.EasingStyle.Quint, Enum.EasingDirection.Out),
\t\t\t{
\t\t\t\tValue = targetValue,
\t\t\t}
\t\t)

\t\ttable.insert(activeCellSizeTweens, firstTween)
\t\ttable.insert(activeCellSizeTweens, settleTween)

\t\tactiveCellSizeConnection = firstTween.Completed:Connect(function(playbackState: Enum.PlaybackState)
\t\t\tif playbackState ~= Enum.PlaybackState.Completed then
\t\t\t\treturn
\t\t\tend

\t\t\tif currentRunId ~= cellSizeRunId then
\t\t\t\treturn
\t\t\tend

\t\t\tsettleTween:Play()
\t\tend)

\t\tfirstTween:Play()
\tend)

\tcleanup(function()
\t\tcancelCellSizeTweens()
\t\tcellSizeChangedConnection:Disconnect()
\t\tcellSizeDriver:Destroy()
\tend)

\t"""


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "add_inventory_skin_card_resize_bounce" / timestamp
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


def ensure_services_and_vide_aliases(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    new_text = text

    if "local TweenService = game:GetService(\"TweenService\")" not in new_text:
        marker = "local ReplicatedStorage = game:GetService(\"ReplicatedStorage\")"
        if marker not in new_text:
            raise RuntimeError("Could not find ReplicatedStorage service declaration")
        new_text = new_text.replace(
            marker,
            marker + " local TweenService = game:GetService(\"TweenService\")",
            1,
        )
        notes.append("Added TweenService service")

    if "local source = Vide.source" not in new_text:
        marker = "local create = Vide.create"
        if marker not in new_text:
            raise RuntimeError("Could not find local create = Vide.create")
        new_text = new_text.replace(
            marker,
            marker + " local source = Vide.source",
            1,
        )
        notes.append("Added local source = Vide.source")

    if "local effect = Vide.effect" not in new_text:
        marker = "local create = Vide.create"
        if marker not in new_text:
            raise RuntimeError("Could not find local create = Vide.create for effect insertion")
        new_text = new_text.replace(
            marker,
            marker + " local effect = Vide.effect",
            1,
        )
        notes.append("Added local effect = Vide.effect")

    if "local cleanup = Vide.cleanup" not in new_text:
        marker = "local create = Vide.create"
        if marker not in new_text:
            raise RuntimeError("Could not find local create = Vide.create for cleanup insertion")
        new_text = new_text.replace(
            marker,
            marker + " local cleanup = Vide.cleanup",
            1,
        )
        notes.append("Added local cleanup = Vide.cleanup")

    return new_text, notes


def insert_animated_cell_size_block(text: str) -> tuple[str, str]:
    if "SkinInventoryCellSizeDriver" in text:
        return text, "Animated cell-size driver already exists"

    marker = "local function SkinsPage(props: SkinsPageProps) return create(\"CanvasGroup\")"
    if marker not in text:
        raise RuntimeError("Could not find compact SkinsPage function return marker")

    replacement = "local function SkinsPage(props: SkinsPageProps) " + ANIMATED_CELL_SIZE_BLOCK + "return create(\"CanvasGroup\")"

    return text.replace(marker, replacement, 1), "Inserted animated cell-size source/tween block inside SkinsPage()"


def replace_grid_cell_size(text: str) -> tuple[str, str]:
    old = "cellSize = function() if hasSelectedSkin(props) then return GRID_DETAIL_CELL_SIZE end return GRID_FULL_CELL_SIZE end,"
    new = "cellSize = function() return animatedCellSize() end,"

    if new in text:
        return text, "grid.cellSize already reads animatedCellSize"

    if old not in text:
        pattern = re.compile(
            r"cellSize\s*=\s*function\(\)\s*"
            r"if\s+hasSelectedSkin\(props\)\s+then\s+return\s+GRID_DETAIL_CELL_SIZE\s+end\s*"
            r"return\s+GRID_FULL_CELL_SIZE\s*"
            r"end\s*,",
            re.DOTALL,
        )
        text2, count = pattern.subn(new, text, count=1)
        if count != 1:
            raise RuntimeError("Could not find grid.cellSize full/detail function to replace")
        return text2, "Replaced grid.cellSize full/detail function with animatedCellSize fallback"

    return text.replace(old, new, 1), "Replaced grid.cellSize full/detail function with animatedCellSize"


def patch_text(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    new_text, alias_notes = ensure_services_and_vide_aliases(text)
    notes.extend(alias_notes)

    new_text, note = insert_animated_cell_size_block(new_text)
    notes.append(note)

    new_text, note = replace_grid_cell_size(new_text)
    notes.append(note)

    return new_text, notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Animate Inventory SkinCard grid CellSize with SideKicks-like bounce."
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
    print("  3) Select and deselect a SkinCard.")
    print("  4) The ScrollArea should still bounce, and SkinCards should now resize with a matching overshoot/settle bounce.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
