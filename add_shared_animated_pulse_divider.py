#!/usr/bin/env python3
# Shared AnimatedPulseDivider + repaired info-stroke sync patch.
#
# Run from the Arcadia-Vide repository root:
#   python add_shared_animated_pulse_divider.py --dry-run
#   python add_shared_animated_pulse_divider.py
#
# Designed for:
#   5e6375e Inventory menu V8
#
# What it does:
# 1) Adds Components/AnimatedPulseDivider.lua.
# 2) Exports AnimatedPulseDivider from Components/init.lua.
# 3) Replaces SideKicks' SideKickDivider with AnimatedPulseDivider.
# 4) Rewrites Inventory/init.lua into a clean single-content structure:
#      InventoryContent
#        PulseDriverHost
#        InventoryTabStrip
#        AnimatedPulseDivider
#        SkinsPage
#        SelectedSkinInfo
#        RanksPage
#        QuestsPage
#    This removes the duplicate/malformed InventoryDivider blocks.
# 5) Cleans leftover duplicate old info-stroke fragments after AnimatedInfoStroke in:
#      SideKickInfo.lua
#      SelectedSkinInfo.lua
# 6) Sets both info frames to:
#      dividerCyclesPerInfoPulse = 2
#    so the info-frame pulse is faster than the previous 3:1 but still slower than the divider.
#
# Backups:
#   .patch_backups/shared_animated_pulse_divider/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


COMPONENTS_INIT = Path("src/client/UI/UIManager/Components/init.lua")
ANIMATED_PULSE_DIVIDER = Path("src/client/UI/UIManager/Components/AnimatedPulseDivider.lua")
SIDEKICKS_INIT = Path("src/client/UI/UIManager/Menus/SideKicks/init.luau")
SIDEKICK_INFO = Path("src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua")
INVENTORY_INIT = Path("src/client/UI/UIManager/Menus/Inventory/init.lua")
INVENTORY_INFO = Path("src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua")


ANIMATED_PULSE_DIVIDER_SOURCE = """--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create

export type AnimatedPulseDividerProps = {
\tname: string?,
\topen: () -> boolean,
\tphase: () -> number,

\tsize: UDim2,
\tposition: UDim2,
\tanchorPoint: Vector2?,
\tzIndex: number?,

\tbackgroundColor3: Color3?,

\tedgeColor: Color3?,
\tmiddleColors: { Color3 }?,
\tonColorChanged: ((Color3) -> ())?,

\trotation: number?,

\topenDuration: number?,
\tcloseDuration: number?,

\tloopsPerColor: number?,
\tsegmentDuration: number?,
\tcolorTweenDuration: number?,

\teasingStyle: Enum.EasingStyle?,
\teasingDirection: Enum.EasingDirection?,
\tcolorEasingStyle: Enum.EasingStyle?,
\tcolorEasingDirection: Enum.EasingDirection?,
}

local DEFAULT_EDGE_COLOR = Color3.fromRGB(255, 255, 255)
local DEFAULT_MIDDLE_COLORS = {
\tColor3.fromRGB(0, 229, 255),
\tColor3.fromRGB(255, 0, 255),
\tColor3.fromRGB(255, 0, 60),
}

local function AnimatedPulseDivider(props: AnimatedPulseDividerProps)
\tlocal edgeColor = props.edgeColor or DEFAULT_EDGE_COLOR
\tlocal middleColors = props.middleColors or DEFAULT_MIDDLE_COLORS
\tlocal easingStyle = props.easingStyle or Enum.EasingStyle.Sine
\tlocal easingDirection = props.easingDirection or Enum.EasingDirection.InOut
\tlocal colorEasingStyle = props.colorEasingStyle or Enum.EasingStyle.Sine
\tlocal colorEasingDirection = props.colorEasingDirection or Enum.EasingDirection.InOut

\treturn create("Frame")({
\t\tName = props.name or "AnimatedPulseDivider",
\t\tSize = props.size,
\t\tPosition = props.position,
\t\tAnchorPoint = props.anchorPoint or Vector2.new(0.5, 0.5),
\t\tVisible = false,
\t\tBackgroundColor3 = props.backgroundColor3 or edgeColor,
\t\tBackgroundTransparency = 1,
\t\tBorderSizePixel = 0,
\t\tZIndex = props.zIndex or 16,

\t\tEffects.FadeGuiObject({
\t\t\topen = props.open,
\t\t\topenTransparency = 0,
\t\t\tclosedTransparency = 1,
\t\t\topenDuration = props.openDuration or 3,
\t\t\tcloseDuration = props.closeDuration or 0.08,
\t\t\teasingStyle = Enum.EasingStyle.Quad,
\t\t\teasingDirection = Enum.EasingDirection.Out,
\t\t\thideWhenClosed = true,
\t\t}),

\t\tcreate("UIGradient")({
\t\t\tRotation = props.rotation or 90,
\t\t\tColor = ColorSequence.new({
\t\t\t\tColorSequenceKeypoint.new(0, edgeColor),
\t\t\t\tColorSequenceKeypoint.new(0.5, middleColors[1]),
\t\t\t\tColorSequenceKeypoint.new(1, edgeColor),
\t\t\t}),
\t\t\tTransparency = NumberSequence.new({
\t\t\t\tNumberSequenceKeypoint.new(0, 1),
\t\t\t\tNumberSequenceKeypoint.new(0.5, 0),
\t\t\t\tNumberSequenceKeypoint.new(1, 1),
\t\t\t}),

\t\t\tEffects.SweepGradientKeypoint({
\t\t\t\tphase = props.phase,
\t\t\t\tedgeColor = edgeColor,
\t\t\t\tmiddleColors = middleColors,
\t\t\t\tedgeTransparency = 1,
\t\t\t\tmiddleTransparency = 0,

\t\t\t\t-- Reference timing from the good SideKicks divider.
\t\t\t\tloopsPerColor = props.loopsPerColor or 3,
\t\t\t\tsegmentDuration = props.segmentDuration or 1.2,
\t\t\t\teasingStyle = easingStyle,
\t\t\t\teasingDirection = easingDirection,
\t\t\t\tcolorTweenDuration = props.colorTweenDuration or 0.45,
\t\t\t\tcolorEasingStyle = colorEasingStyle,
\t\t\t\tcolorEasingDirection = colorEasingDirection,

\t\t\t\tonColorChanged = props.onColorChanged,
\t\t\t}),
\t\t}),
\t})
end

return AnimatedPulseDivider
"""


INVENTORY_INIT_SOURCE = """--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local SharedTypes = require(script.Parent.Parent.UITypes.SharedTypes)
local Components = require(script.Parent.Parent.Components)
local Tabs = require(script.Parent.Parent.Components.Tabs)
local Effects = require(script.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Style)

local MockInventory = require(script.MockInventory)
local SkinsPage = require(script.SkinsPage)
local RanksPage = require(script.RanksPage)
local QuestsPage = require(script.QuestsPage)
local SelectedSkinInfo = require(script.SelectedSkinInfo)

Vide.strict = true

local create = Vide.create
local source = Vide.source

local Panel = Components.Panel
local AnimatedPulseDivider = Components.AnimatedPulseDivider

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = Types.InventoryTabId
type SkinItem = Types.SkinItem

local TAB_STYLE = Style.Tabs.Presets.CyberThreeTabs

local TAB_STRIP_SIZE = UDim2.fromScale(0.42, 0.06)
local TAB_STRIP_POSITION = UDim2.fromScale(0.5, 0.23)

local DIVIDER_SIZE = UDim2.fromScale(0.0015, 0.5)
local DIVIDER_POSITION = UDim2.fromScale(0.636, 0.55)

local function InventoryMenu(props: Types.InventoryMenuProps)
\tlocal selectedTab: Source<InventoryTabId> = source("Skins" :: InventoryTabId)
\tlocal selectedSkin: Source<SkinItem?> = source(nil :: SkinItem?)
\tlocal selectedSkinId: Source<string?> = source(nil :: string?)
\tlocal equippedSkinId: Source<string?> = source(MockInventory.getDefaultEquippedSkinId())

\tlocal pulsePhase: Source<number> = source(0)
\tlocal accentColor: Source<Color3> = source(Style.Tokens.Colors.CyanBright)

\tlocal function hasSelectedSkin(): boolean
\t\treturn selectedTab() == "Skins" and selectedSkin() ~= nil
\tend

\tlocal function selectSkin(skin: SkinItem)
\t\tif selectedSkinId() == skin.SkinId then
\t\t\tselectedSkin(nil)
\t\t\tselectedSkinId(nil)
\t\t\treturn
\t\tend

\t\tselectedSkin(skin)
\t\tselectedSkinId(skin.SkinId)
\tend

\tlocal function equipSkin(skin: SkinItem)
\t\tequippedSkinId(skin.SkinId)
\tend

\treturn Panel({
\t\tname = "InventoryMenu",
\t\tstore = props.store,
\t\tmenuId = "Inventory",
\t\ttitle = "INVENTORY",

\t\tcontent = create("Frame")({
\t\t\tName = "InventoryContent",
\t\t\tSize = UDim2.fromScale(1, 1),
\t\t\tPosition = UDim2.fromScale(0, 0),
\t\t\tAnchorPoint = Vector2.new(0, 0),
\t\t\tBackgroundTransparency = 1,
\t\t\tBorderSizePixel = 0,
\t\t\tZIndex = 11,

\t\t\tcreate("Frame")({
\t\t\t\tName = "PulseDriverHost",
\t\t\t\tSize = UDim2.fromScale(0, 0),
\t\t\t\tBackgroundTransparency = 1,
\t\t\t\tVisible = false,

\t\t\t\tEffects.PulseDriver({
\t\t\t\t\tphase = pulsePhase,
\t\t\t\t\tduration = 3.6,
\t\t\t\t\teasingStyle = Enum.EasingStyle.Sine,
\t\t\t\t\teasingDirection = Enum.EasingDirection.InOut,
\t\t\t\t}),
\t\t\t}),

\t\t\tTabs.TabStrip({
\t\t\t\tname = "InventoryTabStrip",
\t\t\t\ttabs = MockInventory.TABS :: any,
\t\t\t\tselectedTab = selectedTab,
\t\t\t\tsize = TAB_STRIP_SIZE,
\t\t\t\tposition = TAB_STRIP_POSITION,
\t\t\t\tanchorPoint = Vector2.new(0.5, 0.5),
\t\t\t\tcellSize = UDim2.fromScale(0.3, 0.7),
\t\t\t\tcellPadding = UDim2.fromScale(0.035, 0),
\t\t\t\tfillDirectionMaxCells = 3,
\t\t\t\tstyle = TAB_STYLE,
\t\t\t\tzIndex = 21,
\t\t\t}),

\t\t\tAnimatedPulseDivider({
\t\t\t\tname = "InventoryDivider",
\t\t\t\topen = hasSelectedSkin,
\t\t\t\tphase = pulsePhase,
\t\t\t\tsize = DIVIDER_SIZE,
\t\t\t\tposition = DIVIDER_POSITION,
\t\t\t\tanchorPoint = Vector2.new(0.5, 0.5),
\t\t\t\tzIndex = 22,
\t\t\t\tbackgroundColor3 = Style.Tokens.Colors.White,
\t\t\t\tedgeColor = Style.Tokens.Colors.White,
\t\t\t\tmiddleColors = {
\t\t\t\t\tStyle.Tokens.Colors.CyanBright,
\t\t\t\t\tStyle.Tokens.Colors.Magenta,
\t\t\t\t\tStyle.Tokens.Colors.Red,
\t\t\t\t},
\t\t\t\tonColorChanged = function(color: Color3)
\t\t\t\t\taccentColor(color)
\t\t\t\tend,
\t\t\t}),

\t\t\tSkinsPage({
\t\t\t\tselectedTab = selectedTab,
\t\t\t\tselectedSkin = selectedSkin,
\t\t\t\tselectedSkinId = selectedSkinId,
\t\t\t\tequippedSkinId = equippedSkinId,
\t\t\t\tonSelectSkin = selectSkin,
\t\t\t}),

\t\t\tSelectedSkinInfo({
\t\t\t\tselectedTab = selectedTab,
\t\t\t\tselectedSkin = selectedSkin,
\t\t\t\tequippedSkinId = equippedSkinId,
\t\t\t\taccentColor = accentColor,
\t\t\t\tpulsePhase = pulsePhase,
\t\t\t\tonEquip = equipSkin,
\t\t\t}),

\t\t\tRanksPage({
\t\t\t\tselectedTab = selectedTab,
\t\t\t}),

\t\t\tQuestsPage({
\t\t\t\tselectedTab = selectedTab,
\t\t\t}),
\t\t}),
\t})
end

return InventoryMenu
"""


SIDEKICK_DIVIDER_CALL = """AnimatedPulseDivider({
\t\t\t\tname = "SideKickDivider",
\t\t\t\topen = function()
\t\t\t\t\treturn selectedSideKick() ~= nil
\t\t\t\tend,
\t\t\t\tphase = pulsePhase,
\t\t\t\tsize = UDim2.fromScale(0.0015, 0.5),
\t\t\t\tposition = UDim2.fromScale(0.639, 0.49),
\t\t\t\tanchorPoint = Vector2.new(0.5, 0.5),
\t\t\t\tzIndex = 16,
\t\t\t\tbackgroundColor3 = Color3.fromRGB(255, 255, 255),
\t\t\t\tedgeColor = Color3.fromRGB(255, 255, 255),
\t\t\t\tmiddleColors = {
\t\t\t\t\tColor3.fromRGB(0, 229, 255),
\t\t\t\t\tColor3.fromRGB(255, 0, 255),
\t\t\t\t\tColor3.fromRGB(255, 0, 60),
\t\t\t\t},
\t\t\t\tonColorChanged = function(color: Color3)
\t\t\t\t\tdividerColor(color)
\t\t\t\tend,
\t\t\t}), """


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
            end_preview = min(len(text), start + 2000)
            preview = text[start:end_preview]
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
    if "AnimatedPulseDivider" in text:
        return text, "Components/init.lua already exports AnimatedPulseDivider"

    marker = "AnimatedInfoStroke = require(script.AnimatedInfoStroke),"
    if marker in text:
        return (
            text.replace(
                marker,
                marker + " AnimatedPulseDivider = require(script.AnimatedPulseDivider),",
                1,
            ),
            "Exported AnimatedPulseDivider after AnimatedInfoStroke",
        )

    marker = "ActionButton = require(script.ActionButton),"
    if marker in text:
        return (
            text.replace(
                marker,
                marker + " AnimatedPulseDivider = require(script.AnimatedPulseDivider),",
                1,
            ),
            "Exported AnimatedPulseDivider after ActionButton fallback",
        )

    new_text, count = re.subn(
        r"return\s*\{",
        "return { AnimatedPulseDivider = require(script.AnimatedPulseDivider),",
        text,
        count=1,
    )

    if count != 1:
        raise RuntimeError("Could not export AnimatedPulseDivider from Components/init.lua")

    return new_text, "Exported AnimatedPulseDivider at start of Components/init.lua return table"


def ensure_sidekick_alias(text: str) -> tuple[str, str]:
    if "local AnimatedPulseDivider = Components.AnimatedPulseDivider" in text:
        return text, "SideKicks already has AnimatedPulseDivider alias"

    marker = "local ScrollArea = Components.ScrollArea"
    if marker not in text:
        raise RuntimeError("Could not find local ScrollArea alias in SideKicks/init.luau")

    return (
        text.replace(marker, marker + " local AnimatedPulseDivider = Components.AnimatedPulseDivider", 1),
        "Added AnimatedPulseDivider alias in SideKicks/init.luau",
    )


def replace_sidekick_divider(text: str) -> tuple[str, str]:
    if 'AnimatedPulseDivider({' in text and 'name = "SideKickDivider"' in text:
        return text, "SideKickDivider already uses AnimatedPulseDivider"

    start, end = find_create_expression(text, "Frame", 0, "SideKickDivider")
    return (
        text[:start] + SIDEKICK_DIVIDER_CALL + text[end:],
        "Replaced SideKickDivider frame with AnimatedPulseDivider",
    )


def clean_info_file(text: str, label: str) -> tuple[str, list[str]]:
    notes: list[str] = []

    if "AnimatedInfoStroke({" not in text:
        notes.append(f"{label}: no AnimatedInfoStroke call found")
        return text, notes

    start = text.find("AnimatedInfoStroke({")
    stroke_end = include_trailing_comma(text, find_balanced_expression_end(text, start))

    # Remove leftover broken raw table from older patch:
    #   ({ Color = ..., Thickness = ..., create("UIGradient")(...), }),
    search_start = stroke_end
    raw_match = re.search(r"\(\s*\{\s*Color\s*=", text[search_start:search_start + 1500])
    if raw_match is not None:
        raw_start = search_start + raw_match.start()
        raw_end = include_trailing_comma(text, find_balanced_expression_end(text, raw_start))
        text = text[:raw_start] + text[raw_end:]
        notes.append(f"{label}: removed leftover duplicate raw old UIStroke table")
    else:
        notes.append(f"{label}: no leftover raw old UIStroke table found")

    # Speed up info pulse from 3 divider cycles to 2.
    text, count = re.subn(
        r"dividerCyclesPerInfoPulse\s*=\s*[-+]?\d*\.?\d+\s*,",
        "dividerCyclesPerInfoPulse = 2,",
        text,
        count=1,
    )

    if count == 1:
        notes.append(f"{label}: set dividerCyclesPerInfoPulse = 2")
    else:
        notes.append(f"{label}: dividerCyclesPerInfoPulse not found")

    return text, notes


def patch_sidekicks_init(path: Path) -> Patch:
    before = read_text(path)
    after = before
    notes: list[str] = []

    after, note = ensure_sidekick_alias(after)
    notes.append(note)

    after, note = replace_sidekick_divider(after)
    notes.append(note)

    return Patch(path, before, after, notes)


def patch_info(path: Path, label: str) -> Patch:
    before = read_text(path)
    after, notes = clean_info_file(before, label)
    return Patch(path, before, after, notes)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add shared AnimatedPulseDivider and sync divider/info effects."
    )
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backups before writing.")
    args = parser.parse_args()

    repo_root = Path.cwd()

    required = [COMPONENTS_INIT, SIDEKICKS_INIT, SIDEKICK_INFO, INVENTORY_INIT, INVENTORY_INFO]
    missing = [path for path in required if not (repo_root / path).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from the Arcadia-Vide repository root.")
        return 1

    patches: list[Patch] = []

    # Add component file.
    component_path = repo_root / ANIMATED_PULSE_DIVIDER
    component_before = read_text(component_path) if component_path.exists() else ""
    patches.append(
        Patch(
            ANIMATED_PULSE_DIVIDER,
            component_before,
            ANIMATED_PULSE_DIVIDER_SOURCE,
            ["Added/updated shared AnimatedPulseDivider component"],
        )
    )

    # Export component.
    components_init_path = repo_root / COMPONENTS_INIT
    components_before = read_text(components_init_path)

    try:
        components_after, components_note = export_component(components_before)
        patches.append(Patch(COMPONENTS_INIT, components_before, components_after, [components_note]))

        # SideKicks divider becomes shared.
        patches.append(patch_sidekicks_init(repo_root / SIDEKICKS_INIT))

        # Inventory init is currently structurally malformed/duplicated, so rewrite cleanly.
        inventory_before = read_text(repo_root / INVENTORY_INIT)
        patches.append(
            Patch(
                INVENTORY_INIT,
                inventory_before,
                INVENTORY_INIT_SOURCE,
                ["Rewrote Inventory/init.lua cleanly with one InventoryContent and shared AnimatedPulseDivider"],
            )
        )

        # Clean duplicate raw stroke fragments and speed info pulse.
        patches.append(patch_info(repo_root / SIDEKICK_INFO, "SideKickInfo"))
        patches.append(patch_info(repo_root / INVENTORY_INFO, "SelectedSkinInfo"))

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
        print("\nNo changes needed.")
        return 0

    print("\nDiff:\n")
    for patch in changed:
        print(unified_diff(patch.path, patch.before, patch.after))

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "shared_animated_pulse_divider" / timestamp

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
    print("  2) Run your type/lint checks")
    print("  3) Refresh Studio/Hoarcekat")
    print("  4) Test both menus for:")
    print("     - divider animation identical")
    print("     - divider color and info frame color change together")
    print("     - info frame pulse visible at dividerCyclesPerInfoPulse = 2")
    print("  5) If the info pulse is still too slow, set dividerCyclesPerInfoPulse = 1.5 in both info files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
