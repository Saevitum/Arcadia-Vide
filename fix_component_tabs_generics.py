#!/usr/bin/env python3
"""
Fix remaining Luau tab generic type errors after Inventory menu V5 patches.

Target errors:
  ComponentTypes.lua/init.lua:
    Generic type 'TabDefinition' expects 0 type arguments, but 1 is specified
    Generic type 'TabButtonProps' expects 0 type arguments, but 1 is specified
    Generic type 'TabStripProps' expects 0 type arguments, but 1 is specified

Cause:
  ComponentTypes exports tab wrapper types with <T>, but ComponentTypes/TabsTypes.lua
  currently defines the underlying tab types as non-generic. This script normalizes the
  tab type chain so TabsTypes, ComponentTypes, root UITypes, TabButton, and TabStrip
  all agree on the same generic API.

Run from the repository root:
  python fix_component_tabs_generics.py --dry-run
  python fix_component_tabs_generics.py
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


TABS_TYPES_CONTENT = '''--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type TabDefinition<T> = {
	id: T,
	label: string,
	layoutOrder: number?,
	disabled: boolean?,
	hasAlert: boolean?,
}

export type TabPadding = {
	top: UDim?,
	bottom: UDim?,
	left: UDim?,
	right: UDim?,
}

export type TabVisualStateStyle = {
	backgroundColor: Color3?,
	backgroundTransparency: number?,
	gradient: ColorSequence?,
	gradientRotation: number?,
	strokeColor: Color3?,
	strokeTransparency: number?,
	strokeThickness: number?,
	strokeGradient: ColorSequence?,
	strokeGradientRotation: number?,
	textColor: Color3?,
	textTransparency: number?,
	glossColor: Color3?,
	glossBackgroundTransparency: number?,
	glossTransparency: NumberSequence?,
}

export type TabButtonStyle = {
	cornerRadius: UDim?,
	fontFace: Font?,
	minTextSize: number?,
	maxTextSize: number?,
	hoverScale: number?,
	hoverDuration: number?,
	transitionDuration: number?,
	transitionEasingStyle: Enum.EasingStyle?,
	transitionEasingDirection: Enum.EasingDirection?,
	textStrokeColor: Color3?,
	textStrokeTransparency: number?,
	textStrokeThickness: number?,
	default: TabVisualStateStyle?,
	hover: TabVisualStateStyle?,
	selected: TabVisualStateStyle?,
	disabled: TabVisualStateStyle?,
}

export type TabStripStyle = {
	backgroundColor: Color3?,
	backgroundTransparency: number?,
	cellSize: UDim2?,
	cellPadding: UDim2?,
	fillDirectionMaxCells: number?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	padding: TabPadding?,
	button: TabButtonStyle?,
}

export type TabButtonProps<T> = {
	tab: TabDefinition<T>,
	selectedTab: Source<T>,
	style: TabButtonStyle?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	onTabSelected: ((T) -> ())?,
}

export type TabStripProps<T> = {
	tabs: { TabDefinition<T> },
	selectedTab: Source<T>,
	style: TabStripStyle?,
	name: string?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	cellSize: Reactive<UDim2>?,
	cellPadding: Reactive<UDim2>?,
	fillDirectionMaxCells: Reactive<number>?,
	onTabSelected: ((T) -> ())?,
}

return {}
'''


COMPONENT_TYPES_INIT_CONTENT = '''--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local PanelTypes = require(script.PanelTypes)
local TextTypes = require(script.TextTypes)
local ImageTypes = require(script.ImageTypes)
local ScrollAreaTypes = require(script.ScrollAreaTypes)
local ActionButtonTypes = require(script.ActionButtonTypes)
local InputTypes = require(script.InputTypes)
local TabsTypes = require(script.TabsTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type BackgroundProps = PanelTypes.BackgroundProps
export type ExitButtonProps = PanelTypes.ExitButtonProps
export type HeaderProps = PanelTypes.HeaderProps
export type PanelProps = PanelTypes.PanelProps

export type TextGradientProps = TextTypes.TextGradientProps
export type TextPulseStrokeProps = TextTypes.TextPulseStrokeProps
export type TextStrokeProps = TextTypes.TextStrokeProps
export type TextProps = TextTypes.TextProps

export type ImageStrokeProps = ImageTypes.ImageStrokeProps
export type ImageGradientProps = ImageTypes.ImageGradientProps
export type ImageProps = ImageTypes.ImageProps

export type ScrollAreaLayoutKind = ScrollAreaTypes.ScrollAreaLayoutKind
export type ScrollAreaChildren = ScrollAreaTypes.ScrollAreaChildren
export type ScrollAreaPaddingProps = ScrollAreaTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ScrollAreaTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ScrollAreaTypes.ScrollAreaListProps
export type GridCellSizeOptions = ScrollAreaTypes.GridCellSizeOptions
export type ScrollAreaProps = ScrollAreaTypes.ScrollAreaProps

export type ActionButtonVariant = ActionButtonTypes.ActionButtonVariant
export type ActionButtonGradientKeypoint = ActionButtonTypes.ActionButtonGradientKeypoint
export type ActionButtonGradientProps = ActionButtonTypes.ActionButtonGradientProps
export type ActionButtonProps = ActionButtonTypes.ActionButtonProps

export type ToggleSwitchProps = InputTypes.ToggleSwitchProps
export type ToggleButtonProps = InputTypes.ToggleButtonProps
export type SliderProps = InputTypes.SliderProps

export type TabDefinition<T> = TabsTypes.TabDefinition<T>
export type TabPadding = TabsTypes.TabPadding
export type TabVisualStateStyle = TabsTypes.TabVisualStateStyle
export type TabButtonStyle = TabsTypes.TabButtonStyle
export type TabStripStyle = TabsTypes.TabStripStyle
export type TabButtonProps<T> = TabsTypes.TabButtonProps<T>
export type TabStripProps<T> = TabsTypes.TabStripProps<T>

return {
	PanelTypes = PanelTypes,
	TextTypes = TextTypes,
	ImageTypes = ImageTypes,
	ScrollAreaTypes = ScrollAreaTypes,
	ActionButtonTypes = ActionButtonTypes,
	InputTypes = InputTypes,
	TabsTypes = TabsTypes,
}
'''


SHARED_TYPES_CONTENT = '''--!strict

export type Source<T> = (() -> T) & ((T) -> ())
export type Reactive<T> = T | (() -> T)

return {}
'''


@dataclass(frozen=True)
class Change:
    path: Path
    before: str
    after: str


def repo_root_from(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "default.project.json").exists() and (candidate / "src").exists():
            return candidate
    return current


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def write_if_changed(path: Path, after: str, dry_run: bool, backup_root: Path, changes: list[Change]) -> None:
    before = normalize_newlines(read_text(path)) if path.exists() else ""
    after = normalize_newlines(after)
    if before == after:
        return
    changes.append(Change(path, before, after))
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup_path = backup_root / path.relative_to(repo_root)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
    path.write_text(after, encoding="utf-8", newline="\n")


def patch_root_ui_types(text: str) -> str:
    text = normalize_newlines(text)

    # Keep existing file shape, but repair the shared generic aliases if needed.
    text = re.sub(r"export type Source\s*=\s*SharedTypes\.Source", "export type Source<T> = SharedTypes.Source<T>", text)
    text = re.sub(r"export type Reactive\s*=\s*SharedTypes\.Reactive", "export type Reactive<T> = SharedTypes.Reactive<T>", text)

    tab_exports = '''export type TabDefinition<T> = ComponentTypes.TabDefinition<T>
export type TabPadding = ComponentTypes.TabPadding
export type TabVisualStateStyle = ComponentTypes.TabVisualStateStyle
export type TabButtonStyle = ComponentTypes.TabButtonStyle
export type TabStripStyle = ComponentTypes.TabStripStyle
export type TabButtonProps<T> = ComponentTypes.TabButtonProps<T>
export type TabStripProps<T> = ComponentTypes.TabStripProps<T>
'''

    # Remove old tab exports regardless of generic/non-generic form.
    tab_names = (
        "TabDefinition",
        "TabPadding",
        "TabVisualStateStyle",
        "TabButtonStyle",
        "TabStripStyle",
        "TabButtonProps",
        "TabStripProps",
    )
    for name in tab_names:
        text = re.sub(rf"^export type {name}(?:<[^>]+>)?\s*=\s*[^\n]+\n", "", text, flags=re.MULTILINE)

    # Insert after SliderProps when possible; otherwise before the first Effect type export.
    if "export type SliderProps = ComponentTypes.SliderProps\n" in text:
        text = text.replace(
            "export type SliderProps = ComponentTypes.SliderProps\n",
            "export type SliderProps = ComponentTypes.SliderProps\n" + tab_exports,
            1,
        )
    else:
        text = text.replace("export type HoverScaleOptions", tab_exports + "export type HoverScaleOptions", 1)

    # Add ComponentTypes table already exists; no return-table edit needed for type aliases.
    return text


def patch_tabbutton_file(text: str) -> str:
    text = normalize_newlines(text)
    text = re.sub(r"type TabButtonProps\s*=\s*Types\.TabButtonProps(?!<)", "type TabButtonProps = Types.TabButtonProps<string>", text)
    return text


def patch_tabstrip_file(text: str) -> str:
    text = normalize_newlines(text)
    text = re.sub(r"type TabStripProps\s*=\s*Types\.TabStripProps(?!<)", "type TabStripProps<T> = Types.TabStripProps<T>", text)
    return text


def print_diff(change: Change) -> None:
    rel = change.path.relative_to(repo_root)
    print(f"\n--- {rel}")
    print(f"+++ {rel}")
    diff = difflib.unified_diff(
        change.before.splitlines(),
        change.after.splitlines(),
        fromfile=str(rel),
        tofile=str(rel),
        lineterm="",
        n=3,
    )
    for line in diff:
        print(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix tab generic type alias mismatch in Arcadia-Vide.")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repo root. Defaults to current directory.")
    args = parser.parse_args()

    global repo_root
    repo_root = repo_root_from(args.root)

    files = {
        "shared": repo_root / "src/client/UI/UIManager/UITypes/SharedTypes.lua",
        "tabs_types": repo_root / "src/client/UI/UIManager/UITypes/ComponentTypes/TabsTypes.lua",
        "component_init": repo_root / "src/client/UI/UIManager/UITypes/ComponentTypes/init.lua",
        "root_ui_types": repo_root / "src/client/UI/UIManager/UITypes/init.lua",
        "tab_button": repo_root / "src/client/UI/UIManager/Components/Tabs/TabButton.lua",
        "tab_strip": repo_root / "src/client/UI/UIManager/Components/Tabs/TabStrip.lua",
    }

    required = ["tabs_types", "component_init"]
    missing = [str(files[key].relative_to(repo_root)) for key in required if not files[key].exists()]
    if missing:
        print("Could not find required files. Run this script from the repo root, or pass --root.", file=sys.stderr)
        for item in missing:
            print(f"  missing: {item}", file=sys.stderr)
        return 1

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = repo_root / ".patch_backups" / f"fix_component_tabs_generics_{stamp}"
    changes: list[Change] = []

    # Rewrite the small type definition modules to a known-good generic shape.
    if files["shared"].exists():
        write_if_changed(files["shared"], SHARED_TYPES_CONTENT, args.dry_run, backup_root, changes)
    write_if_changed(files["tabs_types"], TABS_TYPES_CONTENT, args.dry_run, backup_root, changes)
    write_if_changed(files["component_init"], COMPONENT_TYPES_INIT_CONTENT, args.dry_run, backup_root, changes)

    # Root UITypes is patched rather than fully rewritten to preserve any local additions.
    if files["root_ui_types"].exists():
        before = read_text(files["root_ui_types"])
        after = patch_root_ui_types(before)
        write_if_changed(files["root_ui_types"], after, args.dry_run, backup_root, changes)

    # Guard against the earlier single-line fix being missing after merges/reverts.
    if files["tab_button"].exists():
        before = read_text(files["tab_button"])
        after = patch_tabbutton_file(before)
        write_if_changed(files["tab_button"], after, args.dry_run, backup_root, changes)

    if files["tab_strip"].exists():
        before = read_text(files["tab_strip"])
        after = patch_tabstrip_file(before)
        write_if_changed(files["tab_strip"], after, args.dry_run, backup_root, changes)

    if not changes:
        print("No changes needed. The tab generic type chain already looks consistent.")
        return 0

    if args.dry_run:
        print(f"Dry run: {len(changes)} file(s) would change.")
        for change in changes:
            print_diff(change)
        return 0

    print(f"Patched {len(changes)} file(s).")
    print(f"Backups saved under: {backup_root.relative_to(repo_root)}")
    print("\nRecommended checks:")
    print("  git diff")
    print("  selene src")
    print("  then refresh Roblox Studio type checking")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
