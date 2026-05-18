#!/usr/bin/env python3
"""
Robust fix for fast/snappy info-frame stroke effects in SideKicks + Inventory.

Run from the Arcadia-Vide repository root:

    python fix_info_frame_effects_v2.py --dry-run
    python fix_info_frame_effects_v2.py

Designed after re-checking the current GitHub main / commit:
    8a4c067 Inventory menu V6

Problem this fixes:
- Both info frames still have:
      Effects.PulseGradientOffset({ phase = ..., phaseMultiplier = 3, ... })
  so the info-frame stroke pulses too fast.
- Both info frames still use:
      Color = function()
          local color = props.accentColor()
          return ColorSequence.new(...)
      end
  so the info-frame UIGradient color snaps immediately instead of tweening smoothly.
- The existing PulseGradientOffset only handles multipliers >= 1 correctly. It needs cycle
  tracking so phaseMultiplier = 1 / 3 means:
      divider does 3 full cycles while info frame does 1 full pulse.

What this script changes:
1) Rewrites:
   - src/client/UI/UIManager/Effects/PulseGradientOffset.lua
   with fractional phaseMultiplier support.

2) Adds:
   - src/client/UI/UIManager/Effects/TweenGradientAccentColor.lua
   a new effect that tweens a UIGradient accent color through a Color3Value.

3) Updates:
   - src/client/UI/UIManager/Effects/init.lua
   to export TweenGradientAccentColor.

4) Updates both info frames:
   - src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua
   - src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua

   It changes their PulseGradientOffset to:
      phaseMultiplier = 1 / 3

   It replaces reactive UIGradient.Color with:
      static initial ColorSequence
      + Effects.TweenGradientAccentColor(...)

Backups:
- Before writing, backups are created under:
  .patch_backups/info_frame_effects_v2/<timestamp>/
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


PULSE_GRADIENT_OFFSET_SOURCE = """--!strict

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

\t\tlocal phaseSource = if options ~= nil then options.phase else nil
\t\tif phaseSource ~= nil then
\t\t\tlocal phaseMultiplier = if options ~= nil and options.phaseMultiplier ~= nil then options.phaseMultiplier else 1

\t\t\t-- The shared PulseDriver is a repeating 0 -> 1 source.
\t\t\t-- A fractional multiplier such as 1 / 3 needs to continue across driver resets.
\t\t\t-- Example:
\t\t\t--   divider phase cycles: 0->1, 0->1, 0->1
\t\t\t--   info phase at 1/3:   0.................1
\t\t\tlocal lastRawPhase = math.clamp(phaseSource(), 0, 1)
\t\t\tlocal completedCycles = 0

\t\t\teffect(function()
\t\t\t\tlocal rawPhase = math.clamp(phaseSource(), 0, 1)

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

\t\tlocal function tweenTo(offset: Vector2): boolean
\t\t\tif not alive then
\t\t\t\treturn false
\t\t\tend

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

\t\t\tlocal playbackState = tween.Completed:Wait()

\t\t\tif activeTween == tween then
\t\t\t\tactiveTween = nil
\t\t\tend

\t\t\treturn alive and playbackState == Enum.PlaybackState.Completed
\t\tend

\t\ttask.spawn(function()
\t\t\twhile alive do
\t\t\t\tif not tweenTo(minOffset) then
\t\t\t\t\tbreak
\t\t\t\tend

\t\t\t\tif not tweenTo(maxOffset) then
\t\t\t\t\tbreak
\t\t\t\tend
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


TWEEN_GRADIENT_ACCENT_SOURCE = """--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

export type TweenGradientAccentColorOptions = {
\taccentColor: () -> Color3,
\tmode: "StartAccent" | "EdgeAccent"?,
\twhiteColor: Color3?,
\tduration: number?,
\teasingStyle: Enum.EasingStyle?,
\teasingDirection: Enum.EasingDirection?,
}

local DEFAULT_WHITE = Color3.fromRGB(255, 255, 255)

local function buildColorSequence(mode: "StartAccent" | "EdgeAccent", accentColor: Color3, whiteColor: Color3): ColorSequence
\tif mode == "EdgeAccent" then
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
\tlocal mode = options.mode or "StartAccent"
\tlocal whiteColor = options.whiteColor or DEFAULT_WHITE
\tlocal duration = options.duration or 0.45
\tlocal easingStyle = options.easingStyle or Enum.EasingStyle.Sine
\tlocal easingDirection = options.easingDirection or Enum.EasingDirection.InOut

\treturn action(function(instance: Instance)
\t\tif not instance:IsA("UIGradient") then
\t\t\treturn
\t\tend

\t\tlocal gradient = instance :: UIGradient
\t\tlocal colorDriver = Instance.new("Color3Value")
\t\tcolorDriver.Name = "TweenGradientAccentColorDriver"
\t\tcolorDriver.Value = options.accentColor()

\t\tlocal alive = true
\t\tlocal activeTween: Tween? = nil

\t\tlocal function applyColor(color: Color3)
\t\t\tgradient.Color = buildColorSequence(mode, color, whiteColor)
\t\tend

\t\tapplyColor(colorDriver.Value)

\t\tlocal connection = colorDriver:GetPropertyChangedSignal("Value"):Connect(function()
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


def export_tween_effect(text: str) -> tuple[str, str]:
    if "TweenGradientAccentColor" in text:
        return text, "Effects/init.lua already exports TweenGradientAccentColor"

    marker = "PulseGradientOffset = require(script.PulseGradientOffset),"
    insert = marker + " TweenGradientAccentColor = require(script.TweenGradientAccentColor),"

    if marker in text:
        return text.replace(marker, insert, 1), "Added TweenGradientAccentColor after PulseGradientOffset"

    # Fallback for either one-line or formatted return table.
    new_text, count = re.subn(
        r"return\s*\{",
        "return { TweenGradientAccentColor = require(script.TweenGradientAccentColor),",
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError("Could not insert TweenGradientAccentColor into Effects/init.lua")

    return new_text, "Added TweenGradientAccentColor at start of Effects/init.lua return table"


def set_phase_multiplier_one_third(text: str) -> tuple[str, int]:
    """
    Only patch phaseMultiplier entries in the target info files.
    """
    pattern = re.compile(
        r"phaseMultiplier\s*=\s*(?:\d+(?:\.\d+)?|1\s*/\s*3)\s*,"
    )
    return pattern.subn("phaseMultiplier = 1 / 3,", text)


def replace_sidekick_gradient_color(text: str) -> tuple[str, bool]:
    if "Effects.TweenGradientAccentColor" in text:
        return text, False

    pattern = re.compile(
        r"Color\s*=\s*function\(\)\s*"
        r"local\s+color\s*=\s*props\.accentColor\(\)\s*"
        r"return\s+ColorSequence\.new\(\{\s*"
        r"ColorSequenceKeypoint\.new\(0\s*,\s*color\)\s*,\s*"
        r"ColorSequenceKeypoint\.new\(1\s*,\s*Color3\.fromRGB\(255\s*,\s*255\s*,\s*255\)\)\s*,?\s*"
        r"\}\)\s*"
        r"end\s*,"
    )

    replacement = (
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
        "}),"
    )

    new_text, count = pattern.subn(replacement, text, count=1)

    if count != 1:
        return text, False

    return new_text, True


def replace_inventory_gradient_color(text: str) -> tuple[str, bool]:
    if "Effects.TweenGradientAccentColor" in text:
        return text, False

    pattern = re.compile(
        r"Color\s*=\s*function\(\)\s*"
        r"local\s+color\s*=\s*props\.accentColor\(\)\s*"
        r"return\s+ColorSequence\.new\(\{\s*"
        r"ColorSequenceKeypoint\.new\(0\s*,\s*color\)\s*,\s*"
        r"ColorSequenceKeypoint\.new\(0\.5\s*,\s*Tokens\.Colors\.White\)\s*,\s*"
        r"ColorSequenceKeypoint\.new\(1\s*,\s*color\)\s*,?\s*"
        r"\}\)\s*"
        r"end\s*,"
    )

    replacement = (
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
        "}),"
    )

    new_text, count = pattern.subn(replacement, text, count=1)

    if count != 1:
        return text, False

    return new_text, True


def patch_info_file(path: Path, kind: str) -> Patch:
    before = read_text(path)
    after, phase_count = set_phase_multiplier_one_third(before)

    notes = [f"Set phaseMultiplier to 1 / 3 ({phase_count} replacement(s))"]

    if kind == "sidekick":
        after2, color_patched = replace_sidekick_gradient_color(after)
        after = after2
        if color_patched:
            notes.append("Replaced SideKickInfo reactive UIGradient.Color with TweenGradientAccentColor")
        elif "Effects.TweenGradientAccentColor" in after:
            notes.append("SideKickInfo already has TweenGradientAccentColor")
        else:
            notes.append("WARNING: Could not find SideKickInfo UIGradient.Color block to patch")
    else:
        after2, color_patched = replace_inventory_gradient_color(after)
        after = after2
        if color_patched:
            notes.append("Replaced SelectedSkinInfo reactive UIGradient.Color with TweenGradientAccentColor")
        elif "Effects.TweenGradientAccentColor" in after:
            notes.append("SelectedSkinInfo already has TweenGradientAccentColor")
        else:
            notes.append("WARNING: Could not find SelectedSkinInfo UIGradient.Color block to patch")

    return Patch(path, before, after, notes)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Slow/smooth SideKicks + Inventory info-frame border effects."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backups before writing.")
    args = parser.parse_args()

    repo_root = Path.cwd()

    required = [
        PULSE_GRADIENT_OFFSET,
        EFFECTS_INIT,
        SIDEKICK_INFO,
        INVENTORY_INFO,
    ]

    missing = [path for path in required if not (repo_root / path).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from the Arcadia-Vide repository root.")
        return 1

    patches: list[Patch] = []

    pulse_path = repo_root / PULSE_GRADIENT_OFFSET
    pulse_before = read_text(pulse_path)
    patches.append(Patch(
        PULSE_GRADIENT_OFFSET,
        pulse_before,
        PULSE_GRADIENT_OFFSET_SOURCE,
        ["Rewrote PulseGradientOffset with cycle-aware fractional phaseMultiplier support"],
    ))

    tween_path = repo_root / TWEEN_GRADIENT_ACCENT
    tween_before = read_text(tween_path) if tween_path.exists() else ""
    patches.append(Patch(
        TWEEN_GRADIENT_ACCENT,
        tween_before,
        TWEEN_GRADIENT_ACCENT_SOURCE,
        ["Added/updated TweenGradientAccentColor effect"],
    ))

    effects_path = repo_root / EFFECTS_INIT
    effects_before = read_text(effects_path)
    try:
        effects_after, effects_note = export_tween_effect(effects_before)
    except RuntimeError as err:
        print(f"ERROR: {err}")
        return 1

    patches.append(Patch(EFFECTS_INIT, effects_before, effects_after, [effects_note]))

    patches.append(patch_info_file(repo_root / SIDEKICK_INFO, "sidekick"))
    patches.append(patch_info_file(repo_root / INVENTORY_INFO, "inventory"))

    warnings = [
        note
        for patch in patches
        for note in patch.notes
        if note.startswith("WARNING:")
    ]

    print("Patch notes:")
    for patch in patches:
        print(f"\n{patch.path}")
        for note in patch.notes:
            print(f"  - {note}")

    if warnings:
        print("\nERROR: One or more expected blocks could not be patched safely:")
        for warning in warnings:
            print(f"  - {warning}")
        print("\nNo files were changed. Upload the affected file if this happens again.")
        return 1

    changed = [patch for patch in patches if patch.before != patch.after]

    if not changed:
        print("\nNo changes needed. The patch already appears to be applied.")
        return 0

    print("\nDiff:\n")
    for patch in changed:
        print(unified_diff(patch.path, patch.before, patch.after))

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "info_frame_effects_v2" / timestamp

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
    print("  3) Watch the info frame for at least 3 divider cycles")
    print("  4) If 1/3 is too slow, change phaseMultiplier to 1 / 2 in both info files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
