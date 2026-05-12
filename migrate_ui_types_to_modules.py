#!/usr/bin/env python3
"""
Migrates UIManager/UITypes.lua to a folder-based typed system and updates existing
UI modules to require the grouped type modules.

Run from the repo root:

    python migrate_ui_types_to_modules.py

Then check Roblox Studio + VSCode diagnostics before committing.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO_ROOT = Path.cwd()
UI_MANAGER = REPO_ROOT / "src" / "client" / "UI" / "UIManager"
UITYPES_DIR = UI_MANAGER / "UITypes"
BACKUP_DIR = REPO_ROOT / "_local_backups"

HEADER = "--!strict\n\n"


def write_lua(relative: str, body: str) -> None:
    path = UITYPES_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = HEADER + body.strip() + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)}")


def backup_and_remove_old_flat_file() -> None:
    old_file = UI_MANAGER / "UITypes.lua"
    if not old_file.exists():
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / "UITypes.lua.bak"

    if backup.exists():
        i = 2
        while (BACKUP_DIR / f"UITypes.lua.bak.{i}").exists():
            i += 1
        backup = BACKUP_DIR / f"UITypes.lua.bak.{i}"

    shutil.copy2(old_file, backup)
    old_file.unlink()
    print(f"backed up old UITypes.lua -> {backup.relative_to(REPO_ROOT)}")
    print("removed old flat src/client/UI/UIManager/UITypes.lua")


def write_type_modules() -> None:
    # Root / shared
    write_lua("SharedTypes.lua", """
export type Source<T> = (() -> T) & ((T) -> ())
export type Reactive<T> = T | (() -> T)

return {}
""")

    write_lua("DeviceTypes.lua", """
export type DeviceKind = "Desktop" | "Mobile" | "Tablet" | "Console"

return {}
""")

    write_lua("MenuTypes/MenuIdTypes.lua", """
export type MenuId =
	"SideKicks"
	| "Boosters"
	| "Stats"
	| "Quests"
	| "Inventory"
	| "Achievements"
	| "Activity"
	| "Rewards"
	| "Settings"
	| "Shop"

return {}
""")

    write_lua("StoreTypes.lua", """
local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type Source<T> = SharedTypes.Source<T>
export type MenuId = MenuIdTypes.MenuId

export type UIStore = {
	currentMenu: Source<MenuId?>,
}

return {}
""")

    write_lua("ButtonTypes.lua", """
local SharedTypes = require(script.Parent.SharedTypes)
local StoreTypes = require(script.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore
export type MenuId = MenuIdTypes.MenuId

export type ButtonBarProps = {
	store: UIStore,
}

export type MenuButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type SideKickButtonProps = MenuButtonProps
export type BoostersButtonProps = MenuButtonProps
export type ActivityButtonProps = MenuButtonProps
export type StatsButtonProps = MenuButtonProps
export type QuestsButtonProps = MenuButtonProps
export type InventoryButtonProps = MenuButtonProps
export type AchievementsButtonProps = MenuButtonProps
export type RewardsButtonProps = MenuButtonProps
export type SettingsButtonProps = MenuButtonProps
export type ShopButtonProps = MenuButtonProps

return {}
""")

    # Component types
    write_lua("ComponentTypes/PanelTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.Parent.MenuTypes.MenuIdTypes)

export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore
export type MenuId = MenuIdTypes.MenuId

export type BackgroundProps = {
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
}

export type ExitButtonProps = {
	onClick: (() -> ())?,
	position: UDim2?,
	size: UDim2?,
	anchorPoint: Vector2?,
}

export type HeaderProps = {
	text: string | (() -> string)?,
}

export type PanelProps = {
	store: UIStore,
	menuId: MenuId,
	name: string?,
	title: string | (() -> string)?,
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	zIndex: number?,
	aspectRatio: number?,
	exitButtonSize: UDim2?,
	exitButtonPosition: UDim2?,
	exitButtonAnchorPoint: Vector2?,
	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	slideDuration: number?,
	content: Instance?,
}

return {}
""")

    write_lua("ComponentTypes/TextTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive<T> = SharedTypes.Reactive<T>

export type TextGradientProps = {
	color: ColorSequence?,
	transparency: NumberSequence?,
	rotation: number?,
	offset: Vector2?,
}

export type TextPulseStrokeProps = {
	colorA: Color3?,
	colorB: Color3?,
	duration: number?,
}

export type TextStrokeProps = {
	thickness: Reactive<number>?,
	color: Reactive<Color3>?,
	transparency: Reactive<number>?,
	pulse: TextPulseStrokeProps?,
}

export type TextProps = {
	name: string?,
	text: Reactive<string>?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	rotation: Reactive<number>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	layoutOrder: Reactive<number>?,
	backgroundTransparency: Reactive<number>?,
	backgroundColor3: Reactive<Color3>?,
	fontFace: Font?,
	textScaled: boolean?,
	textSize: Reactive<number>?,
	minTextSize: number?,
	maxTextSize: number?,
	textColor3: Reactive<Color3>?,
	textTransparency: Reactive<number>?,
	textXAlignment: Enum.TextXAlignment?,
	textYAlignment: Enum.TextYAlignment?,
	richText: boolean?,
	textWrapped: boolean?,
	textTruncate: Enum.TextTruncate?,
	lineHeight: number?,
	automaticSize: Enum.AutomaticSize?,
	gradient: TextGradientProps?,
	stroke: TextStrokeProps?,
}

return {}
""")

    write_lua("ComponentTypes/ImageTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive<T> = SharedTypes.Reactive<T>

export type ImageStrokeProps = {
	thickness: Reactive<number>?,
	color: Reactive<Color3>?,
	transparency: Reactive<number>?,
	applyStrokeMode: Enum.ApplyStrokeMode?,
}

export type ImageGradientProps = {
	color: ColorSequence?,
	transparency: NumberSequence?,
	rotation: number?,
	offset: Vector2?,
}

export type ImageProps = {
	name: string?,
	image: Reactive<string>?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	rotation: Reactive<number>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	layoutOrder: Reactive<number>?,
	backgroundTransparency: Reactive<number>?,
	backgroundColor3: Reactive<Color3>?,
	imageColor3: Reactive<Color3>?,
	imageTransparency: Reactive<number>?,
	scaleType: Enum.ScaleType?,
	sliceCenter: Rect?,
	sliceScale: number?,
	cornerRadius: Reactive<UDim>?,
	stroke: ImageStrokeProps?,
	gradient: ImageGradientProps?,
}

return {}
""")

    write_lua("ComponentTypes/ScrollAreaTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)
local EffectTypes = require(script.Parent.Parent.EffectTypes)

export type Reactive<T> = SharedTypes.Reactive<T>
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions

export type ScrollAreaLayoutKind = "Grid" | "List" | "None"
export type ScrollAreaChildren = Instance | { Instance } | (() -> Instance?) | (() -> { Instance })

export type ScrollAreaPaddingProps = {
	top: Reactive<UDim>?,
	bottom: Reactive<UDim>?,
	left: Reactive<UDim>?,
	right: Reactive<UDim>?,
}

export type ScrollAreaGridProps = {
	cellSize: Reactive<UDim2>?,
	cellPadding: Reactive<UDim2>?,
	fillDirection: Enum.FillDirection?,
	fillDirectionMaxCells: number?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
	startCorner: Enum.StartCorner?,
}

export type ScrollAreaListProps = {
	padding: Reactive<UDim>?,
	fillDirection: Enum.FillDirection?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
}

export type GridCellSizeOptions = {
	columns: number,
	rowsVisible: number?,
	gap: number?,
	widthFill: number?,
	heightFill: number?,
}

export type ScrollAreaProps = {
	name: string?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	layoutOrder: Reactive<number>?,
	layoutTween: TweenGuiObjectLayoutOptions?,
	backgroundTransparency: Reactive<number>?,
	backgroundColor3: Reactive<Color3>?,
	clipsDescendants: boolean?,
	syncGridCanvas: boolean?,
	canvasBottomSafetyScale: Reactive<number>?,
	canvasHeightScale: Reactive<number>?,
	canvasSize: Reactive<UDim2>?,
	automaticCanvasSize: Enum.AutomaticSize?,
	scrollingDirection: Enum.ScrollingDirection?,
	scrollingEnabled: Reactive<boolean>?,
	scrollBarThickness: Reactive<number>?,
	scrollBarImageColor3: Reactive<Color3>?,
	scrollBarImageTransparency: Reactive<number>?,
	elasticBehavior: Enum.ElasticBehavior?,
	verticalScrollBarInset: Enum.ScrollBarInset?,
	horizontalScrollBarInset: Enum.ScrollBarInset?,
	padding: ScrollAreaPaddingProps?,
	layoutKind: ScrollAreaLayoutKind?,
	grid: ScrollAreaGridProps?,
	list: ScrollAreaListProps?,
	children: ScrollAreaChildren?,
}

return {}
""")

    write_lua("ComponentTypes/ActionButtonTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive<T> = SharedTypes.Reactive<T>

export type ActionButtonVariant =
	"CyanGreen"
	| "Blue"
	| "Purple"
	| "Yellow"
	| "Orange"
	| "Red"
	| "Dark"
	| "Disabled"
	| "OrangeYellow"
	| "Red2"
	| "Red3"
	| "Green"

export type ActionButtonGradientKeypoint = {
	time: number,
	color: Color3,
}

export type ActionButtonGradientProps = {
	keypoints: Reactive<{ ActionButtonGradientKeypoint }>?,
	rotation: Reactive<number>?,
}

export type ActionButtonProps = {
	name: string?,
	text: Reactive<string>?,
	iconText: Reactive<string>?,
	variant: Reactive<ActionButtonVariant>?,
	gradient: ActionButtonGradientProps?,
	strokeGradient: ActionButtonGradientProps?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	layoutOrder: Reactive<number>?,
	zIndex: Reactive<number>?,
	disabled: Reactive<boolean>?,
	cornerRadius: Reactive<UDim>?,
	textColor3: Reactive<Color3>?,
	textTransparency: Reactive<number>?,
	strokeColor: Reactive<Color3>?,
	strokeThickness: Reactive<number>?,
	strokeTransparency: Reactive<number>?,
	hoverScale: Reactive<number>?,
	hoverDuration: Reactive<number>?,
	scaleTextConstraints: Reactive<boolean>?,
	onClick: (() -> ())?,
}

return {}
""")

    write_lua("ComponentTypes/InputTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)
local EffectTypes = require(script.Parent.Parent.EffectTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions

export type ToggleSwitchProps = {
	name: string?,
	value: Source<boolean>,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	layoutOrder: Reactive<number>?,
	zIndex: Reactive<number>?,
	disabled: Reactive<boolean>?,
	onChanged: ((boolean) -> ())?,
	backgroundColor3: Reactive<Color3>?,
	onBackgroundColor3: Reactive<Color3>?,
	fillColor3: Reactive<Color3>?,
	knobColor3: Reactive<Color3>?,
	onKnobColor3: Reactive<Color3>?,
	strokeColor3: Reactive<Color3>?,
	backgroundTransparency: Reactive<number>?,
	fillTransparency: Reactive<number>?,
	strokeTransparency: Reactive<number>?,
	strokeThickness: Reactive<number>?,
	cornerRadius: Reactive<UDim>?,
	knobSize: Reactive<UDim2>?,
	knobOffPosition: Reactive<UDim2>?,
	knobOnPosition: Reactive<UDim2>?,
	tweenDuration: number?,
}

export type ToggleButtonProps = {
	name: string?,
	value: Source<boolean>,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	layoutOrder: Reactive<number>?,
	zIndex: Reactive<number>?,
	disabled: Reactive<boolean>?,
	onChanged: ((boolean) -> ())?,
	textOn: Reactive<string>?,
	textOff: Reactive<string>?,
	fontFace: Reactive<Font>?,
	textColor3: Reactive<Color3>?,
	onTextColor3: Reactive<Color3>?,
	backgroundColor3: Reactive<Color3>?,
	onBackgroundColor3: Reactive<Color3>?,
	backgroundTransparency: Reactive<number>?,
	gradient: Reactive<ColorSequence>?,
	onGradient: Reactive<ColorSequence>?,
	gradientRotation: Reactive<number>?,
	strokeColor3: Reactive<Color3>?,
	onStrokeColor3: Reactive<Color3>?,
	strokeTransparency: Reactive<number>?,
	strokeThickness: Reactive<number>?,
	cornerRadius: Reactive<UDim>?,
	aspectRatio: Reactive<number>?,
	minTextSize: Reactive<number>?,
	maxTextSize: Reactive<number>?,
}

export type SliderProps = {
	name: string?,
	value: Source<number>,
	min: number?,
	max: number?,
	step: number?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	layoutOrder: Reactive<number>?,
	zIndex: Reactive<number>?,
	disabled: Reactive<boolean>?,
	dimmed: Reactive<boolean>?,
	onChanged: ((number) -> ())?,
	backgroundColor3: Reactive<Color3>?,
	fillColor3: Reactive<Color3>?,
	fillGradient: Reactive<ColorSequence>?,
	fillGradientTransparency: Reactive<NumberSequence>?,
	fillGradientRotation: Reactive<number>?,
	fillGradientOffset: Reactive<Vector2>?,
	fillGradientEffect: LiquidGradientOptions?,
	knobColor3: Reactive<Color3>?,
	dimmedKnobColor3: Reactive<Color3>?,
	strokeColor3: Reactive<Color3>?,
	backgroundTransparency: Reactive<number>?,
	fillTransparency: Reactive<number>?,
	dimmedFillTransparency: Reactive<number>?,
	strokeTransparency: Reactive<number>?,
	strokeThickness: Reactive<number>?,
	cornerRadius: Reactive<UDim>?,
	knobSize: Reactive<UDim2>?,
}

return {}
""")

    write_lua("ComponentTypes/init.lua", """
local SharedTypes = require(script.Parent.SharedTypes)
local PanelTypes = require(script.PanelTypes)
local TextTypes = require(script.TextTypes)
local ImageTypes = require(script.ImageTypes)
local ScrollAreaTypes = require(script.ScrollAreaTypes)
local ActionButtonTypes = require(script.ActionButtonTypes)
local InputTypes = require(script.InputTypes)

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

return {
	PanelTypes = PanelTypes,
	TextTypes = TextTypes,
	ImageTypes = ImageTypes,
	ScrollAreaTypes = ScrollAreaTypes,
	ActionButtonTypes = ActionButtonTypes,
	InputTypes = InputTypes,
}
""")

    # Effect types
    write_lua("EffectTypes/HoverScaleTypes.lua", """
export type HoverScaleOptions = {
	scale: number?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
""")

    write_lua("EffectTypes/SpinTypes.lua", """
export type SpinOptions = {
	speed: number?,
}

return {}
""")

    write_lua("EffectTypes/HoverUIScaleTypes.lua", """
export type HoverUIScaleOptions = {
	idleScale: number?,
	hoverScale: number?,
	scaleTextConstraints: boolean?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
""")

    write_lua("EffectTypes/TweenGuiObjectLayoutTypes.lua", """
export type TweenGuiObjectLayoutBounceOptions = {
	enabled: boolean?,
	open: boolean?,
	close: boolean?,
	overshoot: number?,
	firstDuration: number?,
	settleDuration: number?,
	firstEasingStyle: Enum.EasingStyle?,
	firstEasingDirection: Enum.EasingDirection?,
	settleEasingStyle: Enum.EasingStyle?,
	settleEasingDirection: Enum.EasingDirection?,
}

export type TweenGuiObjectLayoutOptions = {
	isOpen: (() -> boolean)?,
	targetSize: (() -> UDim2)?,
	targetPosition: (() -> UDim2)?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	openEasingStyle: Enum.EasingStyle?,
	openEasingDirection: Enum.EasingDirection?,
	closeEasingStyle: Enum.EasingStyle?,
	closeEasingDirection: Enum.EasingDirection?,
	bounce: TweenGuiObjectLayoutBounceOptions?,
}

return {}
""")

    write_lua("EffectTypes/SlideFadeCanvasGroupTypes.lua", """
export type SlideFadeCanvasGroupOptions = {
	open: () -> boolean,
	openPosition: UDim2,
	closedPosition: UDim2,
	openTransparency: number?,
	closedTransparency: number?,
	duration: number?,
	fadeDuration: number?,
	closeFadeDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	openEasingStyle: Enum.EasingStyle?,
	openEasingDirection: Enum.EasingDirection?,
	closeEasingStyle: Enum.EasingStyle?,
	closeEasingDirection: Enum.EasingDirection?,
	fadeEasingStyle: Enum.EasingStyle?,
	fadeEasingDirection: Enum.EasingDirection?,
	hideWhenClosed: boolean?,
}

return {}
""")

    write_lua("EffectTypes/PulseDriverTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Source<T> = SharedTypes.Source<T>

export type PulseDriverOptions = {
	phase: Source<number>,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
""")

    write_lua("EffectTypes/SweepGradientKeypointTypes.lua", """
export type SweepGradientKeypointOptions = {
	phase: (() -> number)?,
	edgeColor: Color3?,
	middleColor: Color3?,
	alternateMiddleColor: Color3?,
	middleColors: { Color3 }?,
	onColorChanged: ((Color3) -> ())?,
	edgeTransparency: number?,
	middleTransparency: number?,
	changeColorEveryLoops: number?,
	loopsPerColor: number?,
	segmentDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	colorTweenDuration: number?,
	colorEasingStyle: Enum.EasingStyle?,
	colorEasingDirection: Enum.EasingDirection?,
}

return {}
""")

    write_lua("EffectTypes/PulseGradientOffsetTypes.lua", """
export type PulseGradientOffsetOptions = {
	phase: (() -> number)?,
	minOffset: Vector2?,
	maxOffset: Vector2?,
	phaseMultiplier: number?,
}

return {}
""")

    write_lua("EffectTypes/LiquidGradientTypes.lua", """
export type LiquidGradientOptions = {
	duration: number?,
	primaryColor: Color3?,
	secondaryColor: Color3?,
	disabledColor: Color3?,
	enabled: (() -> boolean)?,
}

return {}
""")

    write_lua("EffectTypes/FadeGuiObjectTypes.lua", """
export type FadeGuiObjectOptions = {
	open: () -> boolean,
	openTransparency: number?,
	closedTransparency: number?,
	duration: number?,
	openDuration: number?,
	closeDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	hideWhenClosed: boolean?,
}

return {}
""")

    write_lua("EffectTypes/PulseUIScaleTypes.lua", """
export type PulseUIScaleOptions = {
	open: (() -> boolean)?,
	enabled: (() -> boolean)?,
	idleScale: number?,
	minScale: number?,
	maxScale: number?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
""")

    write_lua("EffectTypes/init.lua", """
local SharedTypes = require(script.Parent.SharedTypes)

local HoverScaleTypes = require(script.HoverScaleTypes)
local SpinTypes = require(script.SpinTypes)
local HoverUIScaleTypes = require(script.HoverUIScaleTypes)
local TweenGuiObjectLayoutTypes = require(script.TweenGuiObjectLayoutTypes)
local SlideFadeCanvasGroupTypes = require(script.SlideFadeCanvasGroupTypes)
local PulseDriverTypes = require(script.PulseDriverTypes)
local SweepGradientKeypointTypes = require(script.SweepGradientKeypointTypes)
local PulseGradientOffsetTypes = require(script.PulseGradientOffsetTypes)
local LiquidGradientTypes = require(script.LiquidGradientTypes)
local FadeGuiObjectTypes = require(script.FadeGuiObjectTypes)
local PulseUIScaleTypes = require(script.PulseUIScaleTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type HoverScaleOptions = HoverScaleTypes.HoverScaleOptions
export type SpinOptions = SpinTypes.SpinOptions
export type HoverUIScaleOptions = HoverUIScaleTypes.HoverUIScaleOptions
export type TweenGuiObjectLayoutBounceOptions = TweenGuiObjectLayoutTypes.TweenGuiObjectLayoutBounceOptions
export type TweenGuiObjectLayoutOptions = TweenGuiObjectLayoutTypes.TweenGuiObjectLayoutOptions
export type SlideFadeCanvasGroupOptions = SlideFadeCanvasGroupTypes.SlideFadeCanvasGroupOptions
export type PulseDriverOptions = PulseDriverTypes.PulseDriverOptions
export type SweepGradientKeypointOptions = SweepGradientKeypointTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = PulseGradientOffsetTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = LiquidGradientTypes.LiquidGradientOptions
export type FadeGuiObjectOptions = FadeGuiObjectTypes.FadeGuiObjectOptions
export type PulseUIScaleOptions = PulseUIScaleTypes.PulseUIScaleOptions

return {
	HoverScaleTypes = HoverScaleTypes,
	SpinTypes = SpinTypes,
	HoverUIScaleTypes = HoverUIScaleTypes,
	TweenGuiObjectLayoutTypes = TweenGuiObjectLayoutTypes,
	SlideFadeCanvasGroupTypes = SlideFadeCanvasGroupTypes,
	PulseDriverTypes = PulseDriverTypes,
	SweepGradientKeypointTypes = SweepGradientKeypointTypes,
	PulseGradientOffsetTypes = PulseGradientOffsetTypes,
	LiquidGradientTypes = LiquidGradientTypes,
	FadeGuiObjectTypes = FadeGuiObjectTypes,
	PulseUIScaleTypes = PulseUIScaleTypes,
}
""")

    # Menu types
    simple_menus = [
        ("SideKickTypes.lua", "SideKickMenuProps"),
        ("BoostersTypes.lua", "BoostersMenuProps"),
        ("ActivityTypes.lua", "ActivityMenuProps"),
        ("StatsTypes.lua", "StatsMenuProps"),
        ("QuestsTypes.lua", "QuestsMenuProps"),
        ("RewardsTypes.lua", "RewardsMenuProps"),
        ("ShopTypes.lua", "ShopMenuProps"),
    ]

    for filename, prop_name in simple_menus:
        write_lua(f"MenuTypes/{filename}", f"""
local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type UIStore = StoreTypes.UIStore

export type {prop_name} = {{
	store: UIStore,
}}

return {{}}
""")

    write_lua("MenuTypes/InventoryTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore

export type InventoryMenuProps = {
	store: UIStore,
}

export type InventoryTabId = "Skins" | "Ranks" | "Quests"

export type SkinRarity =
	"Common"
	| "Uncommon"
	| "Rare"
	| "Epic"
	| "Legendary"
	| "Mythic"

export type SkinItem = {
	SkinId: string,
	Name: string,
	ImageId: string,
	Rarity: SkinRarity,
	Description: string,
	Owned: boolean,
	Equipped: boolean,
	Locked: boolean,
}

return {}
""")

    write_lua("MenuTypes/AchievementTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore

export type AchievementsMenuProps = {
	store: UIStore,
}

export type AchievementCategory =
	"Money"
	| "Gems"
	| "Points"
	| "Wins"
	| "Level"
	| "Playtime"
	| "Login"
	| "Quests"
	| "SideKicks"
	| "Placeholder"

return {}
""")

    write_lua("MenuTypes/SettingsTypes.lua", """
local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore

export type SettingsMenuProps = {
	store: UIStore,
}

export type SettingsTab = "Volume" | "User" | "Game"

return {}
""")

    write_lua("MenuTypes/init.lua", """
local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.MenuIdTypes)

local SideKickTypes = require(script.SideKickTypes)
local BoostersTypes = require(script.BoostersTypes)
local ActivityTypes = require(script.ActivityTypes)
local StatsTypes = require(script.StatsTypes)
local QuestsTypes = require(script.QuestsTypes)
local InventoryTypes = require(script.InventoryTypes)
local AchievementTypes = require(script.AchievementTypes)
local RewardsTypes = require(script.RewardsTypes)
local SettingsTypes = require(script.SettingsTypes)
local ShopTypes = require(script.ShopTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type MenuId = MenuIdTypes.MenuId

export type SideKickMenuProps = SideKickTypes.SideKickMenuProps
export type BoostersMenuProps = BoostersTypes.BoostersMenuProps
export type ActivityMenuProps = ActivityTypes.ActivityMenuProps
export type StatsMenuProps = StatsTypes.StatsMenuProps
export type QuestsMenuProps = QuestsTypes.QuestsMenuProps
export type InventoryMenuProps = InventoryTypes.InventoryMenuProps
export type AchievementsMenuProps = AchievementTypes.AchievementsMenuProps
export type RewardsMenuProps = RewardsTypes.RewardsMenuProps
export type SettingsMenuProps = SettingsTypes.SettingsMenuProps
export type ShopMenuProps = ShopTypes.ShopMenuProps

export type SettingsTab = SettingsTypes.SettingsTab
export type InventoryTabId = InventoryTypes.InventoryTabId
export type SkinRarity = InventoryTypes.SkinRarity
export type SkinItem = InventoryTypes.SkinItem
export type AchievementCategory = AchievementTypes.AchievementCategory

return {
	MenuIdTypes = MenuIdTypes,

	SideKickTypes = SideKickTypes,
	BoostersTypes = BoostersTypes,
	ActivityTypes = ActivityTypes,
	StatsTypes = StatsTypes,
	QuestsTypes = QuestsTypes,
	InventoryTypes = InventoryTypes,
	AchievementTypes = AchievementTypes,
	RewardsTypes = RewardsTypes,
	SettingsTypes = SettingsTypes,
	ShopTypes = ShopTypes,
}
""")

    # Top-level UITypes convenience aggregator. Existing code should no longer target this,
    # but keeping it makes ad-hoc imports convenient.
    write_lua("init.lua", """
local SharedTypes = require(script.SharedTypes)
local DeviceTypes = require(script.DeviceTypes)
local StoreTypes = require(script.StoreTypes)
local ButtonTypes = require(script.ButtonTypes)
local ComponentTypes = require(script.ComponentTypes)
local EffectTypes = require(script.EffectTypes)
local MenuTypes = require(script.MenuTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type DeviceKind = DeviceTypes.DeviceKind
export type UIStore = StoreTypes.UIStore
export type MenuId = MenuTypes.MenuId

export type ButtonBarProps = ButtonTypes.ButtonBarProps
export type MenuButtonProps = ButtonTypes.MenuButtonProps
export type SideKickButtonProps = ButtonTypes.SideKickButtonProps
export type BoostersButtonProps = ButtonTypes.BoostersButtonProps
export type ActivityButtonProps = ButtonTypes.ActivityButtonProps
export type StatsButtonProps = ButtonTypes.StatsButtonProps
export type QuestsButtonProps = ButtonTypes.QuestsButtonProps
export type InventoryButtonProps = ButtonTypes.InventoryButtonProps
export type AchievementsButtonProps = ButtonTypes.AchievementsButtonProps
export type RewardsButtonProps = ButtonTypes.RewardsButtonProps
export type SettingsButtonProps = ButtonTypes.SettingsButtonProps
export type ShopButtonProps = ButtonTypes.ShopButtonProps

export type BackgroundProps = ComponentTypes.BackgroundProps
export type ExitButtonProps = ComponentTypes.ExitButtonProps
export type HeaderProps = ComponentTypes.HeaderProps
export type PanelProps = ComponentTypes.PanelProps
export type TextProps = ComponentTypes.TextProps
export type ImageProps = ComponentTypes.ImageProps
export type ScrollAreaProps = ComponentTypes.ScrollAreaProps
export type ActionButtonProps = ComponentTypes.ActionButtonProps
export type ToggleSwitchProps = ComponentTypes.ToggleSwitchProps
export type ToggleButtonProps = ComponentTypes.ToggleButtonProps
export type SliderProps = ComponentTypes.SliderProps

export type HoverScaleOptions = EffectTypes.HoverScaleOptions
export type SpinOptions = EffectTypes.SpinOptions
export type HoverUIScaleOptions = EffectTypes.HoverUIScaleOptions
export type TweenGuiObjectLayoutBounceOptions = EffectTypes.TweenGuiObjectLayoutBounceOptions
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions
export type SlideFadeCanvasGroupOptions = EffectTypes.SlideFadeCanvasGroupOptions
export type PulseDriverOptions = EffectTypes.PulseDriverOptions
export type SweepGradientKeypointOptions = EffectTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = EffectTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions
export type FadeGuiObjectOptions = EffectTypes.FadeGuiObjectOptions
export type PulseUIScaleOptions = EffectTypes.PulseUIScaleOptions

export type SideKickMenuProps = MenuTypes.SideKickMenuProps
export type BoostersMenuProps = MenuTypes.BoostersMenuProps
export type ActivityMenuProps = MenuTypes.ActivityMenuProps
export type StatsMenuProps = MenuTypes.StatsMenuProps
export type QuestsMenuProps = MenuTypes.QuestsMenuProps
export type InventoryMenuProps = MenuTypes.InventoryMenuProps
export type AchievementsMenuProps = MenuTypes.AchievementsMenuProps
export type RewardsMenuProps = MenuTypes.RewardsMenuProps
export type SettingsMenuProps = MenuTypes.SettingsMenuProps
export type ShopMenuProps = MenuTypes.ShopMenuProps
export type SettingsTab = MenuTypes.SettingsTab
export type InventoryTabId = MenuTypes.InventoryTabId
export type SkinRarity = MenuTypes.SkinRarity
export type SkinItem = MenuTypes.SkinItem
export type AchievementCategory = MenuTypes.AchievementCategory

return {
	SharedTypes = SharedTypes,
	DeviceTypes = DeviceTypes,
	StoreTypes = StoreTypes,
	ButtonTypes = ButtonTypes,
	ComponentTypes = ComponentTypes,
	EffectTypes = EffectTypes,
	MenuTypes = MenuTypes,
}
""")


def grouped_type_module_for(path: Path) -> str | None:
    rel = path.relative_to(UI_MANAGER)
    parts = rel.parts

    # Skip the new type modules themselves.
    if parts and parts[0] == "UITypes":
        return None

    name = path.name

    if name == "Store.lua":
        return "StoreTypes"

    if name == "Device.lua" or name == "Layout.lua":
        return "DeviceTypes"

    if name == "init.lua" and path.parent == UI_MANAGER:
        return "StoreTypes"

    if "Components" in parts:
        return "ComponentTypes"

    if "Effects" in parts:
        return "EffectTypes"

    if "Buttons" in parts:
        return "ButtonTypes"

    if "Menus" in parts:
        return "MenuTypes"

    if "Hoarcekat" in parts:
        return "StoreTypes"

    return None


def update_type_imports_in_code() -> None:
    if not UI_MANAGER.exists():
        raise SystemExit(f"UIManager folder not found: {UI_MANAGER}")

    lua_files = sorted(
        list(UI_MANAGER.rglob("*.lua")) + list(UI_MANAGER.rglob("*.luau"))
    )

    changed = 0

    for path in lua_files:
        if "UITypes" in path.relative_to(UI_MANAGER).parts:
            continue

        group = grouped_type_module_for(path)
        if group is None:
            continue

        text = path.read_text(encoding="utf-8")
        original = text

        # Change only requires that currently point to the old UITypes module.
        # Keeps the local variable name as `Types`, so the rest of the file needs
        # very little rewriting.
        #
        # Example:
        # local Types = require(script.Parent.Parent.UITypes)
        # -> local Types = require(script.Parent.Parent.UITypes.MenuTypes)
        pattern = re.compile(
            r"local\s+Types\s*=\s*require\((?P<expr>[^)]*?\.UITypes)\)"
        )

        def repl(match: re.Match[str]) -> str:
            expr = match.group("expr")
            if f".UITypes.{group}" in expr:
                return match.group(0)
            if ".UITypes." in expr:
                # Already migrated to some child type module. Leave it alone.
                return match.group(0)
            return f"local Types = require({expr}.{group})"

        text = pattern.sub(repl, text)

        # Generic naming cleanup.
        text = text.replace("Types.SourceOf<", "Types.Source<")
        text = text.replace("Types.ReactiveOf<", "Types.Reactive<")

        # Old non-generic local aliases become concrete any-typed aliases.
        # This avoids breaking files that still annotate fields as `Source`.
        text = re.sub(
            r"type\s+Source\s*=\s*Types\.Source(?![\w<])",
            "type Source = Types.Source<any>",
            text,
        )
        text = re.sub(
            r"type\s+Reactive\s*=\s*Types\.Reactive(?![\w<])",
            "type Reactive = Types.Reactive<any>",
            text,
        )

        # Existing generic aliases are valid once Types.Source<T> exists.
        text = re.sub(
            r"type\s+Source\s*<\s*T\s*>\s*=\s*Types\.SourceOf\s*<\s*T\s*>",
            "type Source<T> = Types.Source<T>",
            text,
        )
        text = re.sub(
            r"type\s+Reactive\s*<\s*T\s*>\s*=\s*Types\.ReactiveOf\s*<\s*T\s*>",
            "type Reactive<T> = Types.Reactive<T>",
            text,
        )

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"updated imports in {path.relative_to(REPO_ROOT)}")

    print(f"updated {changed} code files")


def main() -> None:
    if not UI_MANAGER.exists():
        raise SystemExit(
            "Could not find src/client/UI/UIManager. Run this script from the repo root."
        )

    UITYPES_DIR.mkdir(parents=True, exist_ok=True)

    write_type_modules()
    update_type_imports_in_code()
    backup_and_remove_old_flat_file()

    print("\nDone.")
    print("Next steps:")
    print("  1. Run git diff and inspect the changes.")
    print("  2. Sync/open Roblox Studio and check type errors.")
    print("  3. Check VSCode diagnostics.")
    print("  4. If clean: git add . && git commit -m \"Refactor UI types into modules\"")


if __name__ == "__main__":
    main()
