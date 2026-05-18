#!/usr/bin/env python3
"""
Fix Luau type errors introduced by fix_inventory_v4_ui.py.

Run from the Arcadia-Vide repo root:
    python fix_inventory_type_errors.py --dry-run
    python fix_inventory_type_errors.py

Or pass the repo path explicitly:
    python fix_inventory_type_errors.py --repo C:\\path\\to\\Arcadia-Vide

What this fixes:
  - Re-parameterizes Source<T> / Reactive<T> aliases in touched files.
  - Gives Inventory SkinCard / SelectedSkinInfo props concrete source types.
  - Rewrites TabsTypes.lua with generic-safe tab prop types.
  - Fixes TabButton.lua's generic Reactive<T> usage.
  - Fixes TabButton.lua's TabVisualStateStyle | {} missing-key errors by resolving styles through typed fallbacks.
  - Backs up changed files under .patch_backups/ before writing.
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


TABS_TYPES_LUA = r'''--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type TabDefinition = {
	id: any,
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

export type TabButtonProps = {
	tab: TabDefinition,
	selectedTab: Source<any>,
	style: TabButtonStyle?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	onTabSelected: ((any) -> ())?,
}

export type TabStripProps = {
	tabs: { TabDefinition },
	selectedTab: Source<any>,
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
	onTabSelected: ((any) -> ())?,
}

return {}
'''


RESOLVE_STYLE_FUNCTION = r'''local function resolveStyle(style: TabVisualStateStyle?, fallback: TabVisualStateStyle?): ResolvedStyle
	local styleAny = (style or {}) :: any
	local fallbackAny = (fallback or {}) :: any

	return {
		backgroundColor = styleAny.backgroundColor or fallbackAny.backgroundColor or Color3.fromRGB(255, 255, 255),
		backgroundTransparency = if styleAny.backgroundTransparency ~= nil then styleAny.backgroundTransparency elseif fallbackAny.backgroundTransparency ~= nil then fallbackAny.backgroundTransparency else 0,
		gradient = styleAny.gradient or fallbackAny.gradient or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		gradientRotation = if styleAny.gradientRotation ~= nil then styleAny.gradientRotation elseif fallbackAny.gradientRotation ~= nil then fallbackAny.gradientRotation else 0,
		strokeColor = styleAny.strokeColor or fallbackAny.strokeColor or Color3.fromRGB(255, 255, 255),
		strokeTransparency = if styleAny.strokeTransparency ~= nil then styleAny.strokeTransparency elseif fallbackAny.strokeTransparency ~= nil then fallbackAny.strokeTransparency else 0,
		strokeThickness = if styleAny.strokeThickness ~= nil then styleAny.strokeThickness elseif fallbackAny.strokeThickness ~= nil then fallbackAny.strokeThickness else 1,
		strokeGradient = styleAny.strokeGradient or fallbackAny.strokeGradient or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		strokeGradientRotation = if styleAny.strokeGradientRotation ~= nil then styleAny.strokeGradientRotation elseif fallbackAny.strokeGradientRotation ~= nil then fallbackAny.strokeGradientRotation else 0,
		textColor = styleAny.textColor or fallbackAny.textColor or Color3.fromRGB(255, 255, 255),
		textTransparency = if styleAny.textTransparency ~= nil then styleAny.textTransparency elseif fallbackAny.textTransparency ~= nil then fallbackAny.textTransparency else 0,
		glossColor = styleAny.glossColor or fallbackAny.glossColor or Color3.fromRGB(255, 255, 255),
		glossBackgroundTransparency = if styleAny.glossBackgroundTransparency ~= nil then styleAny.glossBackgroundTransparency elseif fallbackAny.glossBackgroundTransparency ~= nil then fallbackAny.glossBackgroundTransparency else 0,
		glossTransparency = styleAny.glossTransparency or fallbackAny.glossTransparency or NumberSequence.new({
			NumberSequenceKeypoint.new(0, 1),
			NumberSequenceKeypoint.new(0.5, 0.75),
			NumberSequenceKeypoint.new(1, 0),
		}),
	}
end
'''


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


class Patcher:
    def __init__(self, repo: Path, dry_run: bool = False, backup: bool = True) -> None:
        self.repo = repo
        self.dry_run = dry_run
        self.backup = backup
        self.changed: list[str] = []
        self.skipped: list[str] = []
        self.backup_dir: Path | None = None

    def rel(self, rel_path: str) -> Path:
        return self.repo / rel_path

    def ensure_repo(self) -> None:
        required = [
            "default.project.json",
            "src/client/UI/UIManager/init.lua",
            "src/client/UI/UIManager/Menus/Inventory/init.lua",
        ]
        missing = [path for path in required if not self.rel(path).exists()]
        if missing:
            raise SystemExit(
                "This does not look like the Arcadia-Vide repo root. Missing:\n  - "
                + "\n  - ".join(missing)
            )

    def make_backup_dir(self) -> Path:
        if self.backup_dir is None:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.backup_dir = self.repo / ".patch_backups" / f"fix_inventory_type_errors_{stamp}"
            if not self.dry_run:
                self.backup_dir.mkdir(parents=True, exist_ok=True)
        return self.backup_dir

    def backup_file(self, path: Path) -> None:
        if not self.backup or self.dry_run:
            return
        backup_root = self.make_backup_dir()
        target = backup_root / path.relative_to(self.repo)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    def save_if_changed(self, rel_path: str, old: str, new: str, reason: str) -> None:
        old = normalize_newlines(old)
        new = normalize_newlines(new).rstrip() + "\n"

        if old == new:
            self.skipped.append(f"{rel_path} (already up to date/no match for {reason})")
            return

        print(f"\n--- {rel_path}: {reason}")
        if self.dry_run:
            diff = difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            )
            for index, line in enumerate(diff):
                if index >= 260:
                    print("... diff truncated ...")
                    break
                print(line)
        else:
            path = self.rel(rel_path)
            self.backup_file(path)
            path.write_text(new, encoding="utf-8")

        self.changed.append(rel_path)

    def patch_file(self, rel_path: str, transform, reason: str) -> None:
        path = self.rel(rel_path)
        if not path.exists():
            self.skipped.append(f"{rel_path} (missing)")
            return
        old = normalize_newlines(path.read_text(encoding="utf-8"))
        new = transform(old)
        self.save_if_changed(rel_path, old, new, reason)

    def write_file(self, rel_path: str, content: str, reason: str) -> None:
        path = self.rel(rel_path)
        if not path.exists():
            self.skipped.append(f"{rel_path} (missing)")
            return
        old = normalize_newlines(path.read_text(encoding="utf-8"))
        self.save_if_changed(rel_path, old, content, reason)

    def patch_component_types_init(self) -> None:
        def transform(text: str) -> str:
            text = text.replace(
                "export type Source = SharedTypes.Source",
                "export type Source<T> = SharedTypes.Source<T>",
            )
            text = text.replace(
                "export type Reactive = SharedTypes.Reactive",
                "export type Reactive<T> = SharedTypes.Reactive<T>",
            )
            return text

        self.patch_file(
            "src/client/UI/UIManager/UITypes/ComponentTypes/init.lua",
            transform,
            "make exported Source/Reactive aliases generic-safe",
        )

    def patch_skin_card(self) -> None:
        def transform(text: str) -> str:
            text = text.replace(
                "type Source = SharedTypes.Source",
                "type Source<T> = SharedTypes.Source<T>",
            )
            text = re.sub(
                r"selectedSkinId:\s*Source,",
                "selectedSkinId: Source<string?>,",
                text,
            )
            text = re.sub(
                r"equippedSkinId:\s*Source,",
                "equippedSkinId: Source<string?>,",
                text,
            )
            return text

        self.patch_file(
            "src/client/UI/UIManager/Menus/Inventory/SkinCard.lua",
            transform,
            "parameterize Source<T> in SkinCard props",
        )

    def patch_selected_skin_info(self) -> None:
        def transform(text: str) -> str:
            text = text.replace(
                "type Source = SharedTypes.Source",
                "type Source<T> = SharedTypes.Source<T>",
            )
            replacements = {
                r"selectedTab:\s*Source,": "selectedTab: Source<InventoryTabId>,",
                r"selectedSkin:\s*Source,": "selectedSkin: Source<SkinItem?>,",
                r"equippedSkinId:\s*Source,": "equippedSkinId: Source<string?>,",
                r"accentColor:\s*Source,": "accentColor: Source<Color3>,",
                r"pulsePhase:\s*Source,": "pulsePhase: Source<number>,",
            }
            for pattern, replacement in replacements.items():
                text = re.sub(pattern, replacement, text)
            return text

        self.patch_file(
            "src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua",
            transform,
            "parameterize Source<T> in SelectedSkinInfo props",
        )

    def patch_tab_button(self) -> None:
        def transform(text: str) -> str:
            text = text.replace(
                "type Reactive = Types.Reactive",
                "type Source<T> = Types.Source<T>\ntype Reactive<T> = Types.Reactive<T>",
            )
            text = text.replace(
                "local function readReactive<T>(value: Reactive?, fallback: T): T",
                "local function readReactive<T>(value: Reactive<T>?, fallback: T): T",
            )
            text = text.replace(
                "hovered: Types.Source",
                "hovered: Source<boolean>",
            )

            # Make all empty-style fallbacks explicitly TabVisualStateStyle, avoiding TabVisualStateStyle | {} unions.
            text = text.replace(
                "return buttonStyle.disabled or buttonStyle.default or {}",
                "return (buttonStyle.disabled or buttonStyle.default or {}) :: TabVisualStateStyle",
            )
            text = text.replace(
                "return buttonStyle.selected or buttonStyle.default or {}",
                "return (buttonStyle.selected or buttonStyle.default or {}) :: TabVisualStateStyle",
            )
            text = text.replace(
                "return buttonStyle.hover or buttonStyle.default or {}",
                "return (buttonStyle.hover or buttonStyle.default or {}) :: TabVisualStateStyle",
            )
            text = text.replace(
                "return buttonStyle.default or {}",
                "return (buttonStyle.default or {}) :: TabVisualStateStyle",
            )
            text = text.replace(
                "local fallbackStyle = buttonStyle.default or DEFAULT_BUTTON_STYLE.default or {}",
                "local fallbackStyle = (buttonStyle.default or DEFAULT_BUTTON_STYLE.default or {}) :: TabVisualStateStyle",
            )

            # Replace the resolveStyle function with an any-backed resolver. The public types stay strict;
            # this avoids Luau treating fallback or {} as an unsafe union and reporting every optional key.
            pattern = (
                r"local function resolveStyle\(style: TabVisualStateStyle, fallback: TabVisualStateStyle\?\): ResolvedStyle"
                r".*?\nend\n\nlocal function colorAt"
            )
            replacement = RESOLVE_STYLE_FUNCTION + "\nlocal function colorAt"
            text, count = re.subn(pattern, replacement, text, flags=re.DOTALL)

            # If the function was already partially edited to accept TabVisualStateStyle?, still replace it.
            if count == 0:
                pattern_optional = (
                    r"local function resolveStyle\(style: TabVisualStateStyle\?, fallback: TabVisualStateStyle\?\): ResolvedStyle"
                    r".*?\nend\n\nlocal function colorAt"
                )
                text = re.sub(pattern_optional, replacement, text, flags=re.DOTALL)

            return text

        self.patch_file(
            "src/client/UI/UIManager/Components/Tabs/TabButton.lua",
            transform,
            "fix generic Reactive<T> and style fallback type errors",
        )

    def patch(self) -> None:
        self.ensure_repo()
        self.patch_component_types_init()
        self.patch_skin_card()
        self.patch_selected_skin_info()
        self.write_file(
            "src/client/UI/UIManager/UITypes/ComponentTypes/TabsTypes.lua",
            TABS_TYPES_LUA,
            "rewrite tab component types with concrete generic usage",
        )
        self.patch_tab_button()

    def report(self) -> None:
        print("\nPatch summary")
        print("=============")
        if self.changed:
            print("Changed files:")
            for item in self.changed:
                print(f"  - {item}")
        else:
            print("No files changed.")

        if self.skipped:
            print("\nSkipped/no-op files:")
            for item in self.skipped:
                print(f"  - {item}")

        if self.backup and not self.dry_run and self.backup_dir is not None:
            print(f"\nBackups saved to: {self.backup_dir}")

        print("\nNext recommended commands:")
        print("  git diff")
        print("  selene src")
        print("\nThen refresh Studio's type checker. If Studio still shows stale errors, close/reopen the affected scripts or restart Studio.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fix Inventory V4 UI Luau type errors.")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Path to Arcadia-Vide repo root. Defaults to current directory.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create .patch_backups copies before writing.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo = args.repo.expanduser().resolve()
    patcher = Patcher(repo=repo, dry_run=args.dry_run, backup=not args.no_backup)

    try:
        patcher.patch()
        patcher.report()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
