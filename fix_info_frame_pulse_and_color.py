#!/usr/bin/env python3
"""
Slow/smooth info-frame pulse + color transition for SideKicks and Inventory.

Run from the Arcadia-Vide repository root:

    python fix_info_frame_pulse_and_color.py --dry-run
    python fix_info_frame_pulse_and_color.py

Designed around current git:
    8a4c067 Inventory menu V6

What this fixes:
1) Info-frame border pulse is too fast in both SideKicks and Inventory.
   - Changes info UIGradient offset pulse from phaseMultiplier = 3 to phaseMultiplier = 1 / 3.
   - Updates PulseGradientOffset.lua so fractional multipliers work across PulseDriver cycles.
   - Result: divider completes 3 cycles while the info frame completes 1 slower pulse.

2) Info-frame color change feels instant/snappy.
   - Adds Effects/TweenGradientAccentColor.lua.
   - Adds it to Effects/init.lua.
   - Replaces reactive UIGradient.Color bindings on:
       SideKicks/SideKickInfo.lua
       Inventory/SelectedSkinInfo.lua
     with a tween-driven gradient color effect.
   - Result: when accentColor changes, the info-frame UIStroke gradient color tweens smoothly.

Backups:
- Before writing, backups are created under:
  .patch_backups/info_frame_pulse_and_color/<timestamp>/
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


PULSE_GRADIENT_OFFSET = Path("src/client/UI/UIManager/Effects/PulseGradientOffset.lua")
TWEEN_GRADIENT_ACCENT = Path("src/client/UI/UIManager/Effects/TweenGradientAccentColor.lua")
EFFECTS_INIT = Path("src/client/UI/UIManager/Effects/init.lua")

SIDEKICK_INFO = Path("src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua")
INVENTORY_INFO = Path("src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua")


NEW_PULSE_GRADIENT_OFFSET = """--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.EffectTypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local DEFAULT_MIN_OFFSET = Vector2.new(0, -0.35)
local DEFAULT_MAX_OFFSET = Vector2.new(0, 0)

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

local function PulseGradientOffset(options: Types.PulseGradientOffsetOptions?)
\tlocal minOffset = if options ~= nil and options.minOffset ~= nil then options.minOffset else DEFAULT_MIN_OFFSET
\tlocal maxOffset = if options ~= nil and options.maxOffset ~= nil then options.maxOffset else DEFAULT_MAX_OFFSET

\treturn action(function(instance: Instance)
\t\tif not instance:IsA("UIGradient") then
\t\t\treturn
\t\tend

\t\tlocal gradient = instance :: UIGradient

\t\tif options ~= nil and options.phase ~= nil then
\t\t\tlocal phaseMultiplier = if options.phaseMultiplier ~= nil then options.phaseMultiplier else 1

\t\t\t-- Important:
\t\t\t-- The shared PulseDriver phase is a repeating 0 -> 1 cycle.
\t\t\t-- For multipliers below 1, rawPhase * multiplier would only ever move through
\t\t\t-- part of the pulse, then snap back on phase reset.
\t\t\t-- We keep a cycle counter so phaseMultiplier = 1 / 3 means:
\t\t\t--   one full info-frame pulse over three divider cycles.
\t\t\tlocal lastRawPhase = math.clamp(options.phase(), 0, 1)
\t\t\tlocal completedCycles = 0

\t\t\teffect(function()
\t\t\t\tlocal rawPhase = math.clamp(options.phase(), 0, 1)

\t\t\t\tif rawPhase < lastRawPhase then
\t\t\t\t\tcompletedCycles += 1
\t\t\t\tend

\t\t\t\tlastRawPhase = rawPhase

\t\t\t\tlocal continuousPhase = (completedCycles + rawPhase) * phaseMultiplier
\t\t\t\tlocal alpha = phaseToPingPongAlpha(continuousPhase)

\t\t\t\tgradient.Offset = lerpVector2(maxOffset, minOffset, alpha)
\t\t\tend)

\t\t\treturn
\t\tend

\t\tlocal alive = true
\t\tlocal activeTween: Tween? = nil

\t\tlocal function tweenTo(offset: Vector2)
\t\t\tif activeTween ~= nil then
\t\t\t\tactiveTween:Cancel()
\t\t\t\tactiveTween = nil
\t\t\tend

\t\t\tlocal tween = TweenService:Create(
\t\t\t\tgradient,
\t\t\t\tTweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut),
\t\t\t\t{
\t\t\t\t\tOffset = offset,
\t\t\t\t}
\t\t\t)

\t\t\tactiveTween = tween
\t\t\ttween:Play()
\t\t\ttween.Completed:Wait()

\t\t\tif activeTween == tween then
\t\t\t\tactiveTween = nil
\t\t\tend
\t\tend

\t\ttask.spawn(function()
\t\t\twhile alive do
\t\t\t\ttweenTo(minOffset)

\t\t\t\tif not alive then
\t\t\t\t\tbreak
\t\t\t\tend

\t\t\t\ttweenTo(maxOffset)
\t\t\tend
\t\tend)

\t\tcleanup(function()
\t\t\talive = false

\t\t\tif activeTween ~= nil then
\t\t\t\tactiveTween:Cancel()
\t\t\t\tactiveTween = nil
\t\t\tend
\t\tend)
\tend)
end

return PulseGradientOffset
"""


NEW_TWEEN_GRADIENT_ACCENT = """--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

export type TweenGradientAccentColorOptions = {
\taccentColor: () -> Color3,
\tmode: \"StartAccent\" | \"EdgeAccent\"?,
\twhiteColor: Color3?,
\tduration: number?,
\teasingStyle: Enum.EasingStyle?,
\teasingDirection: Enum.EasingDirection?,
}

local DEFAULT_WHITE = Color3.fromRGB(255, 255, 255)

local function buildColorSequence(mode: string?, accentColor: Color3, whiteColor: Color3): ColorSequence
\tif mode == \"EdgeAccent\" then
\t\treturn ColorSequence.new({
\t\t\tColorSequenceKeypoint.new(0, accentColor),
\t\t\tColorSequenceKeypoint.new(0.5, whiteColor),
\t\t\tColorSequenceKeypoint.new(1, accentColor),
\t\t})
\tend

\treturn ColorSequence.new({
\t\tColorSequenceKeypoint.new(0, accentColor),
\t\tColorSequenceKeypoint.new(1, whiteColor),
\t})
end

local function TweenGradientAccentColor(options: TweenGradientAccentColorOptions)
\tlocal mode = options.mode or \"StartAccent\"
\tlocal whiteColor = options.whiteColor or DEFAULT_WHITE
\tlocal duration = options.duration or 0.45
\tlocal easingStyle = options.easingStyle or Enum.EasingStyle.Sine
\tlocal easingDirection = options.easingDirection or Enum.EasingDirection.InOut

\treturn action(function(instance: Instance)
\t\tif not instance:IsA(\"UIGradient\") then
\t\t\treturn
\t\tend

\t\tlocal gradient = instance :: UIGradient
\t\tlocal colorDriver = Instance.new(\"Color3Value\")
\t\tcolorDriver.Name = \"TweenGradientAccentColorDriver\"
\t\tcolorDriver.Value = options.accentColor()

\t\tlocal alive = true
\t\tlocal activeTween: Tween? = nil

\t\tlocal function applyColor(color: Color3)
\t\t\tgradient.Color = buildColorSequence(mode, color, whiteColor)
\t\tend

\t\tapplyColor(colorDriver.Value)

\t\tlocal connection = colorDriver:GetPropertyChangedSignal(\"Value\"):Connect(function()
\t\t\tapplyColor(colorDriver.Value)
\t\tend)

\t\tlocal function cancelTween()
\t\t\tif activeTween ~= nil then
\t\t\t\tactiveTween:Cancel()
\t\t\t\tactiveTween = nil
\t\t\tend
\t\tend

\t\teffect(function()
\t\t\tlocal targetColor = options.accentColor()

\t\t\tif not alive then
\t\t\t\treturn
\t\t\tend

\t\t\tcancelTween()

\t\t\tlocal tween = TweenService:Create(
\t\t\t\tcolorDriver,
\t\t\t\tTweenInfo.new(duration, easingStyle, easingDirection),
\t\t\t\t{
\t\t\t\t\tValue = targetColor,
\t\t\t\t}
\t\t\t)

\t\t\tactiveTween = tween
\t\t\ttween:Play()
\t\tend)

\t\tcleanup(function()
\t\t\talive = false
\t\t\tcancelTween()
\t\t\tconnection:Disconnect()
\t\t\tcolorDriver:Destroy()
\t\tend)
\tend)
end

return TweenGradientAccentColor
"""


@dataclass(frozen=True)
class FilePatch:
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def replace_all_phase_multiplier(text: str) -> tuple[str, int]:
    # Patch any old info-frame setting, whether previous scripts left it at 3, 1, or another simple number.
    pattern = re.compile(r"phaseMultiplier\s*=\s*(?:\d+(?:\.\d+)?|1\s*/\s*3)\s*,")
    return pattern.subn("phaseMultiplier = 1 / 3,", text)


def patch_effects_init(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    if "TweenGradientAccentColor" in text:
        return text, ["Effects/init.lua already exports TweenGradientAccentColor"]

    # Current init.lua is one-line table style. Insert after PulseGradientOffset for stable ordering.
    if "PulseGradientOffset = require(script.PulseGradientOffset)," in text:
        text = text.replace(
            "PulseGradientOffset = require(script.PulseGradientOffset),",
            "PulseGradientOffset = require(script.PulseGradientOffset), TweenGradientAccentColor = require(script.TweenGradientAccentColor),",
            1,
        )
        notes.append("Added TweenGradientAccentColor export after PulseGradientOffset")
        return text, notes

    # Fallback: insert before final closing brace in return table.
    text, count = re.subn(r"}\s*$", " TweenGradientAccentColor = require(script.TweenGradientAccentColor), }", text, count=1)
    if count != 1:
        raise RuntimeError("Could not patch Effects/init.lua export table")

    notes.append("Added TweenGradientAccentColor export at end of Effects/init.lua")
    return text, notes


def patch_sidekick_info(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    text, phase_count = replace_all_phase_multiplier(text)
    notes.append(f"SideKickInfo phaseMultiplier set to 1 / 3 ({phase_count} replacement(s))")

    if "Effects.TweenGradientAccentColor" in text:
        notes.append("SideKickInfo already has TweenGradientAccentColor")
        return text, notes

    old_color = (
        "Color = function() local color = props.accentColor() return ColorSequence.new({ "
        "ColorSequenceKeypoint.new(0, color), ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 255, 255)), "
        "}) end, Rotation = 90,"
    )

    new_color = (
        "Color = ColorSequence.new({ "
        "ColorSequenceKeypoint.new(0, props.accentColor()), "
        "ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 255, 255)), "
        "}), "
        "Effects.TweenGradientAccentColor({ "
        "accentColor = props.accentColor, "
        "mode = \"StartAccent\", "
        "duration = 0.45, "
        "easingStyle = Enum.EasingStyle.Sine, "
        "easingDirection = Enum.EasingDirection.InOut, "
        "}), "
        "Rotation = 90,"
    )

    if old_color not in text:
        raise RuntimeError(
            "Could not find SideKickInfo reactive UIGradient.Color block. "
            "The file may have changed; patch manually."
        )

    text = text.replace(old_color, new_color, 1)
    notes.append("SideKickInfo UIGradient.Color now tweens accent color smoothly")
    return text, notes


def patch_inventory_info(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    text, phase_count = replace_all_phase_multiplier(text)
    notes.append(f"SelectedSkinInfo phaseMultiplier set to 1 / 3 ({phase_count} replacement(s))")

    if "Effects.TweenGradientAccentColor" in text:
        notes.append("SelectedSkinInfo already has TweenGradientAccentColor")
        return text, notes

    old_color = (
        "Color = function() local color = props.accentColor() return ColorSequence.new({ "
        "ColorSequenceKeypoint.new(0, color), ColorSequenceKeypoint.new(0.5, Tokens.Colors.White), "
        "ColorSequenceKeypoint.new(1, color), }) end, Rotation = 90,"
    )

    new_color = (
        "Color = ColorSequence.new({ "
        "ColorSequenceKeypoint.new(0, props.accentColor()), "
        "ColorSequenceKeypoint.new(0.5, Tokens.Colors.White), "
        "ColorSequenceKeypoint.new(1, props.accentColor()), "
        "}), "
        "Effects.TweenGradientAccentColor({ "
        "accentColor = props.accentColor, "
        "mode = \"EdgeAccent\", "
        "whiteColor = Tokens.Colors.White, "
        "duration = 0.45, "
        "easingStyle = Enum.EasingStyle.Sine, "
        "easingDirection = Enum.EasingDirection.InOut, "
        "}), "
        "Rotation = 90,"
    )

    if old_color not in text:
        raise RuntimeError(
            "Could not find SelectedSkinInfo reactive UIGradient.Color block. "
            "The file may have changed; patch manually."
        )

    text = text.replace(old_color, new_color, 1)
    notes.append("SelectedSkinInfo UIGradient.Color now tweens accent color smoothly")
    return text, notes


def diff(path: Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"{path} (before)",
            tofile=f"{path} (after)",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix fast info-frame pulse and snapping info-frame gradient color."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backups before writing.")
    args = parser.parse_args()

    repo_root = Path.cwd()

    required = [PULSE_GRADIENT_OFFSET, EFFECTS_INIT, SIDEKICK_INFO, INVENTORY_INFO]
    missing = [path for path in required if not (repo_root / path).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from the Arcadia-Vide repository root.")
        return 1

    patches: list[FilePatch] = []

    # 1) Rewrite PulseGradientOffset.lua with fractional-cycle-safe phase support.
    pulse_path = repo_root / PULSE_GRADIENT_OFFSET
    pulse_before = read(pulse_path)
    patches.append(
        FilePatch(
            PULSE_GRADIENT_OFFSET,
            pulse_before,
            NEW_PULSE_GRADIENT_OFFSET,
            ["PulseGradientOffset now supports fractional phaseMultiplier across repeated PulseDriver cycles"],
        )
    )

    # 2) Add TweenGradientAccentColor.lua.
    tween_path = repo_root / TWEEN_GRADIENT_ACCENT
    tween_before = read(tween_path) if tween_path.exists() else ""
    patches.append(
        FilePatch(
            TWEEN_GRADIENT_ACCENT,
            tween_before,
            NEW_TWEEN_GRADIENT_ACCENT,
            ["Added TweenGradientAccentColor effect"],
        )
    )

    # 3) Export the new effect.
    effects_path = repo_root / EFFECTS_INIT
    effects_before = read(effects_path)
    try:
        effects_after, effects_notes = patch_effects_init(effects_before)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        return 1

    patches.append(FilePatch(EFFECTS_INIT, effects_before, effects_after, effects_notes))

    # 4) Patch SideKickInfo + SelectedSkinInfo.
    sidekick_path = repo_root / SIDEKICK_INFO
    sidekick_before = read(sidekick_path)
    inventory_path = repo_root / INVENTORY_INFO
    inventory_before = read(inventory_path)

    try:
        sidekick_after, sidekick_notes = patch_sidekick_info(sidekick_before)
        inventory_after, inventory_notes = patch_inventory_info(inventory_before)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        return 1

    patches.append(FilePatch(SIDEKICK_INFO, sidekick_before, sidekick_after, sidekick_notes))
    patches.append(FilePatch(INVENTORY_INFO, inventory_before, inventory_after, inventory_notes))

    changed = [patch for patch in patches if patch.before != patch.after]

    print("Patch notes:")
    for patch in patches:
        print(f"\n{patch.path}")
        for note in patch.notes:
            print(f"  - {note}")

    if not changed:
        print("\nNo changes needed. The patch already appears to be applied.")
        return 0

    print("\nDiff:\n")
    for patch in changed:
        print(diff(patch.path, patch.before, patch.after))

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "info_frame_pulse_and_color" / timestamp

        for patch in changed:
            target = repo_root / patch.path
            if target.exists():
                backup = make_backup(target, backup_root)
                print(f"Backup created: {backup}")

    for patch in changed:
        target = repo_root / patch.path
        target.parent.mkdir(parents=True, exist_ok=True)
        write(target, patch.after)
        print(f"Updated: {patch.path}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Hoarcekat/Studio")
    print("  3) Test SideKicks and Inventory info-frame stroke pulse/color")
    print("  4) If one info pulse per 3 divider cycles is too slow, change phaseMultiplier to 1 / 2 in both info files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
