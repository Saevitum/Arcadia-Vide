#!/usr/bin/env python3
# V2 robust shared AnimatedInfoStroke patch.
#
# Run from the Arcadia-Vide repository root:
#     python add_shared_animated_info_stroke_v2.py --dry-run
#     python add_shared_animated_info_stroke_v2.py
#
# This version does NOT depend on exact one-line text blocks.
# It finds and replaces the first root create("UIStroke") expression in:
# - Menus/SideKicks/SideKickInfo.lua
# - Menus/Inventory/SelectedSkinInfo.lua
#
# It also replaces the InventoryDivider frame with a SideKicks-matching divider config.
#
# Designed for current local state after:
# - ac4a28e Inventory menu V7
# - previous TweenGradientAccentColor / PulseGradientOffset patch attempts
#
# Backups:
# - .patch_backups/shared_animated_info_stroke_v2/<timestamp>/

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

\t\tlocal alive = true
\t\tlocal activeColorTween: Tween? = nil

\t\tlocal colorDriver = Instance.new("Color3Value")
\t\tcolorDriver.Name = "AnimatedInfoStrokeColorDriver"
\t\tcolorDriver.Value = props.accentColor()

\t\tlocal function applyColor(color: Color3)
\t\t\tif not alive then
\t\t\t\treturn
\t\t\tend

\t\t\tgradient.Color = buildColorSequence(colorMode, color, whiteColor)
\t\tend

\t\tapplyColor(colorDriver.Value)

\t\tlocal colorConnection = colorDriver:GetPropertyChangedSignal("Value"):Connect(function()
\t\t\tapplyColor(colorDriver.Value)
\t\tend)

\t\tlocal function cancelColorTween()
\t\t\tif activeColorTween ~= nil then
\t\t\t\tactiveColorTween:Cancel()
\t\t\t\tactiveColorTween = nil
\t\t\tend
\t\tend

\t\t-- Smoothly follow divider accent color changes.
\t\teffect(function()
\t\t\tlocal targetColor = props.accentColor()

\t\t\tif not alive then
\t\t\t\treturn
\t\t\tend

\t\t\tcancelColorTween()

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

\t\t-- Slow info-frame offset pulse. With dividerCyclesPerInfoPulse = 3:
\t\t-- divider cycles 3 times while the info border completes 1 full ping-pong pulse.
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
\tlocal maxOffset = props.maxOffset or DEFAULT_MAX_OFFSET

\treturn create("UIStroke")({
\t\tName = props.name or "AnimatedInfoStroke",
\t\tColor = whiteColor,
\t\tThickness = props.thickness or 2,
\t\tTransparency = props.strokeTransparency or 0,

\t\tcreate("UIGradient")({
\t\t\tRotation = props.rotation or 90,
\t\t\tOffset = maxOffset,
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


def include_trailing_comma(text: str, end: int) -> int:
    i = end
    while i < len(text) and text[i].isspace():
        i += 1

    if i < len(text) and text[i] == ",":
        return i + 1

    return end


def find_create_expression(text: str, class_name: str, after_index: int = 0, name: str | None = None) -> tuple[int, int]:
    pattern = re.compile(rf'create\s*\(\s*"{re.escape(class_name)}"\s*\)\s*\(\s*\{{')
    for match in pattern.finditer(text, after_index):
        start = match.start()

        if name is not None:
            preview = text[start:start + 1200]
            if re.search(rf'Name\s*=\s*"{re.escape(name)}"', preview) is None:
                continue

        end = find_balanced_expression_end(text, start)
        end = include_trailing_comma(text, end)
        return start, end

    label = f'create("{class_name}")'
    if name is not None:
        label += f' with Name = "{name}"'
    raise RuntimeError(f"Could not find {label}")


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


def ensure_alias(text: str, alias_after_regex: str) -> tuple[str, str]:
    if "local AnimatedInfoStroke = Components.AnimatedInfoStroke" in text:
        return text, "AnimatedInfoStroke local alias already exists"

    match = re.search(alias_after_regex, text)
    if match is None:
        marker = "Vide.strict = true"
        if marker not in text:
            raise RuntimeError("Could not find a safe place to insert AnimatedInfoStroke alias")
        return (
            text.replace(
                marker,
                marker + " local AnimatedInfoStroke = Components.AnimatedInfoStroke",
                1,
            ),
            "Added AnimatedInfoStroke alias after Vide.strict fallback",
        )

    insert_at = match.end()
    return (
        text[:insert_at] + " local AnimatedInfoStroke = Components.AnimatedInfoStroke" + text[insert_at:],
        "Added local AnimatedInfoStroke alias",
    )


def patch_root_info_stroke(text: str, replacement: str, label: str) -> tuple[str, str]:
    if "AnimatedInfoStroke({" in text:
        return text, f"{label}: already uses AnimatedInfoStroke"

    start, end = find_create_expression(text, "UIStroke", 0)
    return text[:start] + replacement + text[end:], f"{label}: replaced first/root UIStroke expression"


def patch_sidekick_info(path: Path) -> Patch:
    before = read_text(path)
    after = before
    notes: list[str] = []

    after, note = ensure_alias(after, r"local\s+Image\s*=\s*Components\.Image")
    notes.append(note)

    after, note = patch_root_info_stroke(after, SIDEKICK_STROKE_CALL, "SideKickInfo")
    notes.append(note)

    return Patch(path, before, after, notes)


def patch_inventory_info(path: Path) -> Patch:
    before = read_text(path)
    after = before
    notes: list[str] = []

    after, note = ensure_alias(after, r"local\s+ActionButton\s*=\s*Components\.ActionButton")
    notes.append(note)

    after, note = patch_root_info_stroke(after, INVENTORY_STROKE_CALL, "SelectedSkinInfo")
    notes.append(note)

    return Patch(path, before, after, notes)


def patch_inventory_divider(path: Path) -> Patch:
    before = read_text(path)
    after = before

    start, end = find_create_expression(after, "Frame", 0, "InventoryDivider")
    after = after[:start] + INVENTORY_DIVIDER_BLOCK + after[end:]

    return Patch(
        path,
        before,
        after,
        ["Replaced InventoryDivider frame with SideKicks-matching SweepGradientKeypoint timing"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add shared AnimatedInfoStroke and patch both info frames robustly."
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
        patches.append(Patch(COMPONENTS_INIT, components_before, components_after, [components_note]))

        patches.append(patch_sidekick_info(repo_root / SIDEKICK_INFO))
        patches.append(patch_inventory_info(repo_root / INVENTORY_INFO))
        patches.append(patch_inventory_divider(repo_root / INVENTORY_INIT))
    except RuntimeError as err:
        print(f"ERROR: {err}")
        print("No files were changed.")
        return 1

    changed = [patch for patch in patches if patch.before != patch.after]

    print("Patch notes:")
    for patch in patches:
        print(f"\n{patch.path}")
        for note in patch.notes:
            print(f"  - {note}")

    if not changed:
        print("\nNo changes needed. Shared AnimatedInfoStroke already appears applied.")
        return 0

    print("\nDiff:\n")
    for patch in changed:
        print(unified_diff(patch.path, patch.before, patch.after))

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "shared_animated_info_stroke_v2" / timestamp

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
    print("  3) Test: SideKicks divider, SideKicks info stroke, Inventory divider, Inventory info stroke")
    print("  4) If the info stroke is too slow/fast, tune dividerCyclesPerInfoPulse in the AnimatedInfoStroke calls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
