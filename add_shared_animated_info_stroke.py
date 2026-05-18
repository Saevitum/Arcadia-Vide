#!/usr/bin/env python3
"""
Create a shared AnimatedInfoStroke component and use it in SideKicks + Inventory.

Run from the Arcadia-Vide repository root:

    python add_shared_animated_info_stroke.py --dry-run
    python add_shared_animated_info_stroke.py

Designed for:
    ac4a28e Inventory menu V7

Why this exists:
- The divider and the info-frame stroke were animated by different low-level systems.
- SideKicks divider is good and should remain the reference.
- The two info frames were manually duplicated and easy to desync/break.
- This patch creates one shared component:
      src/client/UI/UIManager/Components/AnimatedInfoStroke.lua
  and replaces both menu-specific info UIStroke blocks with it.

What it changes:
1) Adds:
   src/client/UI/UIManager/Components/AnimatedInfoStroke.lua

2) Exports it from:
   src/client/UI/UIManager/Components/init.lua

3) Replaces the root UIStroke + UIGradient block in:
   src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua
   src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua

4) Restores InventoryDivider to match SideKicks divider timing:
   - loopsPerColor = 3
   - segmentDuration = 1.2
   - colorTweenDuration = 0.45
   - Sine/InOut easing
   - SideKicks-like fade timing

Backups:
- Before writing, backups are created under:
  .patch_backups/shared_animated_info_stroke/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


COMPONENTS_INIT = Path("src/client/UI/UIManager/Components/init.lua")
ANIMATED_INFO_STROKE = Path("src/client/UI/UIManager/Components/AnimatedInfoStroke.lua")
SIDEKICK_INFO = Path("src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua")
INVENTORY_INFO = Path("src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua")
INVENTORY_INIT = Path("src/client/UI/UIManager/Menus/Inventory/init.lua")


ANIMATED_INFO_STROKE_SOURCE = """--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local create = Vide.create
local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

export type ColorMode = "StartAccent" | "EdgeAccent"

export type AnimatedInfoStrokeProps = {
\tname: string?,
\taccentColor: () -> Color3,
\tpulsePhase: (() -> number)?,

\tcolorMode: ColorMode?,
\twhiteColor: Color3?,

\tthickness: number?,
\tstrokeTransparency: number?,

\trotation: number?,
\tgradientTransparency: NumberSequence?,

\tminOffset: Vector2?,
\tmaxOffset: Vector2?,
\tdividerCyclesPerInfoPulse: number?,

\tcolorTweenDuration: number?,
\tcolorEasingStyle: Enum.EasingStyle?,
\tcolorEasingDirection: Enum.EasingDirection?,
}

local DEFAULT_WHITE = Color3.fromRGB(255, 255, 255)
local DEFAULT_MIN_OFFSET = Vector2.new(0, -0.35)
local DEFAULT_MAX_OFFSET = Vector2.new(0, 0)

local DEFAULT_GRADIENT_TRANSPARENCY = NumberSequence.new({
\tNumberSequenceKeypoint.new(0, 0),
\tNumberSequenceKeypoint.new(0.602, 0.828),
\tNumberSequenceKeypoint.new(1, 1),
})

local function lerpNumber(a: number, b: number, alpha: number): number
\treturn a + ((b - a) * alpha)
end

local function lerpVector2(a: Vector2, b: Vector2, alpha: number): Vector2
\treturn Vector2.new(
\t\tlerpNumber(a.X, b.X, alpha),
\t\tlerpNumber(a.Y, b.Y, alpha)
\t)
end

local function phaseToPingPongAlpha(phase: number): number
\tphase = phase % 1

\tif phase < 0.5 then
\t\treturn phase / 0.5
\tend

\treturn 1 - ((phase - 0.5) / 0.5)
end

local function buildColorSequence(colorMode: ColorMode, accentColor: Color3, whiteColor: Color3): ColorSequence
\tif colorMode == "StartAccent" then
\t\treturn ColorSequence.new({
\t\t\tColorSequenceKeypoint.new(0, accentColor),
\t\t\tColorSequenceKeypoint.new(1, whiteColor),
\t\t})
\tend

\treturn ColorSequence.new({
\t\tColorSequenceKeypoint.new(0, accentColor),
\t\tColorSequenceKeypoint.new(0.5, whiteColor),
\t\tColorSequenceKeypoint.new(1, accentColor),
\t})
end

local function AnimatedInfoStrokeGradient(props: AnimatedInfoStrokeProps)
\treturn action(function(instance: Instance)
\t\tif not instance:IsA("UIGradient") then
\t\t\treturn
\t\tend

\t\tlocal gradient = instance :: UIGradient

\t\tlocal colorMode: ColorMode = if props.colorMode ~= nil then props.colorMode else "EdgeAccent"
\t\tlocal whiteColor = props.whiteColor or DEFAULT_WHITE
\t\tlocal colorTweenDuration = props.colorTweenDuration or 0.45
\t\tlocal colorEasingStyle = props.colorEasingStyle or Enum.EasingStyle.Sine
\t\tlocal colorEasingDirection = props.colorEasingDirection or Enum.EasingDirection.InOut

\t\tlocal minOffset = props.minOffset or DEFAULT_MIN_OFFSET
\t\tlocal maxOffset = props.maxOffset or DEFAULT_MAX_OFFSET
\t\tlocal dividerCyclesPerInfoPulse = math.max(0.001, props.dividerCyclesPerInfoPulse or 3)

\t\tlocal activeColorTween: Tween? = nil
\t\tlocal alive = true

\t\tlocal colorDriver = Instance.new("Color3Value")
\t\tcolorDriver.Name = "AnimatedInfoStrokeColorDriver"
\t\tcolorDriver.Value = props.accentColor()

\t\tlocal function applyColor()
\t\t\tif not alive then
\t\t\t\treturn
\t\t\tend

\t\t\tgradient.Color = buildColorSequence(colorMode, colorDriver.Value, whiteColor)
\t\tend

\t\tlocal colorConnection = colorDriver:GetPropertyChangedSignal("Value"):Connect(applyColor)
\t\tapplyColor()

\t\tlocal function cancelColorTween()
\t\t\tif activeColorTween ~= nil then
\t\t\t\tactiveColorTween:Cancel()
\t\t\t\tactiveColorTween = nil
\t\t\tend
\t\tend

\t\t-- Smooth accent color changes.
\t\teffect(function()
\t\t\tlocal targetColor = props.accentColor()

\t\t\tif not alive then
\t\t\t\treturn
\t\t\tend

\t\t\tcancelColorTween()

\t\t\tif colorDriver.Value == targetColor then
\t\t\t\tapplyColor()
\t\t\t\treturn
\t\t\tend

\t\t\tlocal tween = TweenService:Create(
\t\t\t\tcolorDriver,
\t\t\t\tTweenInfo.new(colorTweenDuration, colorEasingStyle, colorEasingDirection),
\t\t\t\t{
\t\t\t\t\tValue = targetColor,
\t\t\t\t}
\t\t\t)

\t\t\tactiveColorTween = tween
\t\t\ttween:Play()
\t\tend)

\t\t-- Slow info-frame pulse. One info pulse can span multiple divider cycles.
\t\tlocal phaseSource = props.pulsePhase

\t\tif phaseSource ~= nil then
\t\t\tlocal lastRawPhase = math.clamp(phaseSource(), 0, 1)
\t\t\tlocal completedDividerCycles = 0

\t\t\teffect(function()
\t\t\t\tlocal rawPhase = math.clamp(phaseSource(), 0, 1)

\t\t\t\tif rawPhase < lastRawPhase then
\t\t\t\t\tcompletedDividerCycles += 1
\t\t\t\tend

\t\t\t\tlastRawPhase = rawPhase

\t\t\t\tlocal infoPhase = (completedDividerCycles + rawPhase) / dividerCyclesPerInfoPulse
\t\t\t\tlocal alpha = phaseToPingPongAlpha(infoPhase)

\t\t\t\tgradient.Offset = lerpVector2(maxOffset, minOffset, alpha)
\t\t\tend)
\t\tend

\t\tcleanup(function()
\t\t\talive = false
\t\t\tcancelColorTween()
\t\t\tcolorConnection:Disconnect()
\t\t\tcolorDriver:Destroy()
\t\tend)
\tend)
end

local function AnimatedInfoStroke(props: AnimatedInfoStrokeProps)
\tlocal colorMode: ColorMode = if props.colorMode ~= nil then props.colorMode else "EdgeAccent"
\tlocal whiteColor = props.whiteColor or DEFAULT_WHITE
\tlocal gradientTransparency = props.gradientTransparency or DEFAULT_GRADIENT_TRANSPARENCY

\treturn create("UIStroke")({
\t\tName = props.name or "AnimatedInfoStroke",
\t\tColor = whiteColor,
\t\tThickness = props.thickness or 2,
\t\tTransparency = props.strokeTransparency or 0,

\t\tcreate("UIGradient")({
\t\t\tRotation = props.rotation or 90,
\t\t\tOffset = props.maxOffset or DEFAULT_MAX_OFFSET,
\t\t\tColor = buildColorSequence(colorMode, props.accentColor(), whiteColor),
\t\t\tTransparency = gradientTransparency,

\t\t\tAnimatedInfoStrokeGradient(props),
\t\t}),
\t})
end

return AnimatedInfoStroke
"""


SIDEKICK_STROKE_CALL = """AnimatedInfoStroke({
\t\t\tname = "SideKickInfoStroke",
\t\t\taccentColor = props.accentColor,
\t\t\tpulsePhase = props.pulsePhase,
\t\t\tcolorMode = "StartAccent",
\t\t\twhiteColor = Color3.fromRGB(255, 255, 255),
\t\t\tthickness = 2,
\t\t\tstrokeTransparency = 0,
\t\t\trotation = 90,
\t\t\tgradientTransparency = NumberSequence.new({
\t\t\t\tNumberSequenceKeypoint.new(0, 0),
\t\t\t\tNumberSequenceKeypoint.new(0.602, 0.828),
\t\t\t\tNumberSequenceKeypoint.new(1, 1),
\t\t\t}),
\t\t\tminOffset = Vector2.new(0, -0.35),
\t\t\tmaxOffset = Vector2.new(0, 0),
\t\t\tdividerCyclesPerInfoPulse = 3,
\t\t\tcolorTweenDuration = 0.45,
\t\t\tcolorEasingStyle = Enum.EasingStyle.Sine,
\t\t\tcolorEasingDirection = Enum.EasingDirection.InOut,
\t\t}), """


INVENTORY_STROKE_CALL = """AnimatedInfoStroke({
\t\t\tname = "SelectedSkinInfoStroke",
\t\t\taccentColor = props.accentColor,
\t\t\tpulsePhase = props.pulsePhase,
\t\t\tcolorMode = "EdgeAccent",
\t\t\twhiteColor = Tokens.Colors.White,
\t\t\tthickness = 2,
\t\t\tstrokeTransparency = 0,
\t\t\trotation = 90,
\t\t\tgradientTransparency = Gradients.strokePulseTransparency(),
\t\t\tminOffset = Vector2.new(0, -0.35),
\t\t\tmaxOffset = Vector2.new(0, 0),
\t\t\tdividerCyclesPerInfoPulse = 3,
\t\t\tcolorTweenDuration = 0.45,
\t\t\tcolorEasingStyle = Enum.EasingStyle.Sine,
\t\t\tcolorEasingDirection = Enum.EasingDirection.InOut,
\t\t}), """


INVENTORY_DIVIDER_BLOCK = """create("Frame")({
\t\t\tName = "InventoryDivider",
\t\t\tSize = DIVIDER_SIZE,
\t\t\tPosition = DIVIDER_POSITION,
\t\t\tAnchorPoint = Vector2.new(0.5, 0.5),
\t\t\tBackgroundColor3 = Style.Tokens.Colors.White,
\t\t\tBackgroundTransparency = 1,
\t\t\tBorderSizePixel = 0,
\t\t\tZIndex = 22,

\t\t\tEffects.FadeGuiObject({
\t\t\t\topen = hasSelectedSkin,
\t\t\t\topenTransparency = 0,
\t\t\t\tclosedTransparency = 1,
\t\t\t\topenDuration = 3,
\t\t\t\tcloseDuration = 0.08,
\t\t\t\teasingStyle = Enum.EasingStyle.Quad,
\t\t\t\teasingDirection = Enum.EasingDirection.Out,
\t\t\t\thideWhenClosed = true,
\t\t\t}),

\t\t\tcreate("UIGradient")({
\t\t\t\tRotation = 90,
\t\t\t\tColor = ColorSequence.new({
\t\t\t\t\tColorSequenceKeypoint.new(0, Style.Tokens.Colors.White),
\t\t\t\t\tColorSequenceKeypoint.new(0.5, Style.Tokens.Colors.CyanBright),
\t\t\t\t\tColorSequenceKeypoint.new(1, Style.Tokens.Colors.White),
\t\t\t\t}),
\t\t\t\tTransparency = NumberSequence.new({
\t\t\t\t\tNumberSequenceKeypoint.new(0, 1),
\t\t\t\t\tNumberSequenceKeypoint.new(0.5, 0),
\t\t\t\t\tNumberSequenceKeypoint.new(1, 1),
\t\t\t\t}),

\t\t\t\tEffects.SweepGradientKeypoint({
\t\t\t\t\tphase = pulsePhase,
\t\t\t\t\tedgeColor = Style.Tokens.Colors.White,
\t\t\t\t\tmiddleColors = {
\t\t\t\t\t\tStyle.Tokens.Colors.CyanBright,
\t\t\t\t\t\tStyle.Tokens.Colors.Magenta,
\t\t\t\t\t\tStyle.Tokens.Colors.Red,
\t\t\t\t\t},
\t\t\t\t\tedgeTransparency = 1,
\t\t\t\t\tmiddleTransparency = 0,
\t\t\t\t\tloopsPerColor = 3,
\t\t\t\t\tsegmentDuration = 1.2,
\t\t\t\t\teasingStyle = Enum.EasingStyle.Sine,
\t\t\t\t\teasingDirection = Enum.EasingDirection.InOut,
\t\t\t\t\tcolorTweenDuration = 0.45,
\t\t\t\t\tcolorEasingStyle = Enum.EasingStyle.Sine,
\t\t\t\t\tcolorEasingDirection = Enum.EasingDirection.InOut,
\t\t\t\t\tonColorChanged = function(color: Color3)
\t\t\t\t\t\taccentColor(color)
\t\t\t\t\tend,
\t\t\t\t}),
\t\t\t}),
\t\t}), """


@dataclass(frozen=True)
class Patch:
    path: Path
    before: str
    after: str
    notes: list[str]


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


def export_component(text: str) -> tuple[str, str]:
    if "AnimatedInfoStroke" in text:
        return text, "Components/init.lua already exports AnimatedInfoStroke"

    marker = "ActionButton = require(script.ActionButton),"
    if marker in text:
        return (
            text.replace(
                marker,
                marker + " AnimatedInfoStroke = require(script.AnimatedInfoStroke),",
                1,
            ),
            "Exported AnimatedInfoStroke after ActionButton",
        )

    new_text, count = re.subn(
        r"return\s*\{",
        "return { AnimatedInfoStroke = require(script.AnimatedInfoStroke),",
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError("Could not export AnimatedInfoStroke from Components/init.lua")

    return new_text, "Exported AnimatedInfoStroke at start of Components/init.lua return table"


def ensure_local_component_alias(text: str, after_alias: str) -> tuple[str, str]:
    if "local AnimatedInfoStroke = Components.AnimatedInfoStroke" in text:
        return text, "AnimatedInfoStroke local alias already exists"

    if after_alias not in text:
        raise RuntimeError(f"Could not find alias marker: {after_alias}")

    return (
        text.replace(
            after_alias,
            after_alias + " local AnimatedInfoStroke = Components.AnimatedInfoStroke",
            1,
        ),
        "Added local AnimatedInfoStroke alias",
    )


def replace_root_stroke_block(text: str, frame_marker: str, replacement: str) -> tuple[str, str]:
    if "AnimatedInfoStroke({" in text:
        # If it already has the component, do not try to replace again.
        return text, "Root info stroke already appears to use AnimatedInfoStroke"

    start = text.find('create("UIStroke")({ Color =')
    if start == -1:
        # Inventory starts with Tokens.Colors.White; still same prefix contains Color =
        start = text.find('create("UIStroke")({ Color = Tokens.Colors.White')

    if start == -1:
        raise RuntimeError("Could not find root create(\"UIStroke\") block")

    marker_index = text.find(frame_marker, start)
    if marker_index == -1:
        raise RuntimeError(f"Could not find frame marker after root stroke: {frame_marker}")

    return text[:start] + replacement + text[marker_index:], "Replaced root UIStroke/UIGradient block with AnimatedInfoStroke"


def patch_sidekick_info(path: Path) -> Patch:
    before = read_text(path)
    after = before
    notes: list[str] = []

    after, note = ensure_local_component_alias(after, "local Image = Components.Image")
    notes.append(note)

    after, note = replace_root_stroke_block(
        after,
        'create("Frame")({ Name = "SideKickImage"',
        SIDEKICK_STROKE_CALL,
    )
    notes.append(note)

    return Patch(path, before, after, notes)


def patch_inventory_info(path: Path) -> Patch:
    before = read_text(path)
    after = before
    notes: list[str] = []

    after, note = ensure_local_component_alias(after, "local ActionButton = Components.ActionButton")
    notes.append(note)

    after, note = replace_root_stroke_block(
        after,
        'create("Frame")({ Name = "SkinImage"',
        INVENTORY_STROKE_CALL,
    )
    notes.append(note)

    return Patch(path, before, after, notes)


def patch_inventory_divider(path: Path) -> Patch:
    before = read_text(path)
    after = before
    notes: list[str] = []

    start = after.find('create("Frame")({ Name = "InventoryDivider"')
    if start == -1:
        # Idempotency check: formatted replacement already exists.
        if 'Name = "InventoryDivider"' in after and "loopsPerColor = 3" in after:
            return Patch(path, before, after, ["Inventory divider already appears patched"])
        raise RuntimeError("Could not find InventoryDivider frame")

    marker = "SkinsPage({"
    marker_index = after.find(marker, start)
    if marker_index == -1:
        raise RuntimeError("Could not find SkinsPage marker after InventoryDivider")

    after = after[:start] + INVENTORY_DIVIDER_BLOCK + after[marker_index:]
    notes.append("Replaced InventoryDivider block with SideKicks-matching SweepGradientKeypoint timing")

    return Patch(path, before, after, notes)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add shared AnimatedInfoStroke and restore matching info/divider effects."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backups before writing.")
    args = parser.parse_args()

    repo_root = Path.cwd()

    required = [COMPONENTS_INIT, SIDEKICK_INFO, INVENTORY_INFO, INVENTORY_INIT]
    missing = [path for path in required if not (repo_root / path).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from the Arcadia-Vide repository root.")
        return 1

    patches: list[Patch] = []

    component_path = repo_root / ANIMATED_INFO_STROKE
    component_before = read_text(component_path) if component_path.exists() else ""
    patches.append(
        Patch(
            ANIMATED_INFO_STROKE,
            component_before,
            ANIMATED_INFO_STROKE_SOURCE,
            ["Added/updated shared AnimatedInfoStroke component"],
        )
    )

    components_init_path = repo_root / COMPONENTS_INIT
    components_before = read_text(components_init_path)
    try:
        components_after, components_note = export_component(components_before)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        return 1

    patches.append(Patch(COMPONENTS_INIT, components_before, components_after, [components_note]))

    try:
        patches.append(patch_sidekick_info(repo_root / SIDEKICK_INFO))
        patches.append(patch_inventory_info(repo_root / INVENTORY_INFO))
        patches.append(patch_inventory_divider(repo_root / INVENTORY_INIT))
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("No files were changed. Your local files may differ from commit ac4a28e.")
        return 1

    changed = [patch for patch in patches if patch.before != patch.after]

    print("Patch notes:")
    for patch in patches:
        print(f"\n{patch.path}")
        for note in patch.notes:
            print(f"  - {note}")

    if not changed:
        print("\nNo changes needed. The shared AnimatedInfoStroke patch already appears applied.")
        return 0

    print("\nDiff:\n")
    for patch in changed:
        print(unified_diff(patch.path, patch.before, patch.after))

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "shared_animated_info_stroke" / timestamp

        for patch in changed:
            target = repo_root / patch.path
            if target.exists():
                backup_path = make_backup(target, backup_root)
                print(f"Backup created: {backup_path}")

    for patch in changed:
        target = repo_root / patch.path
        target.parent.mkdir(parents=True, exist_ok=True)
        write_text(target, patch.after)
        print(f"Updated: {patch.path}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Studio/Hoarcekat")
    print("  3) Test SideKicks divider, SideKicks info stroke, Inventory divider, Inventory info stroke")
    print("  4) If the info stroke pulse is too slow/fast, tune dividerCyclesPerInfoPulse in the two AnimatedInfoStroke calls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
