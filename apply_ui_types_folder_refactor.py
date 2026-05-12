from pathlib import Path
import shutil
import textwrap

ROOT = Path.cwd()
UI_MANAGER = ROOT / "src" / "client" / "UI" / "UIManager"
TYPES = UI_MANAGER / "UITypes"
COMPONENT_TYPES = TYPES / "ComponentTypes"
EFFECT_TYPES = TYPES / "EffectTypes"
MENU_TYPES = TYPES / "MenuTypes"

if not UI_MANAGER.exists():
    raise SystemExit("Run this script from the Arcadia-Vide repo root. Could not find src/client/UI/UIManager")

for folder in (TYPES, COMPONENT_TYPES, EFFECT_TYPES, MENU_TYPES):
    folder.mkdir(parents=True, exist_ok=True)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")

# -----------------------------------------------------------------------------
# Top-level/shared types
# -----------------------------------------------------------------------------
write(TYPES / "SharedTypes.lua", r'''
--!strict

-- Backward-compatible non-generic aliases for old modules.
export type Source = (() -> any) & ((any) -> ())
export type Reactive = any | (() -> any)

-- Stronger generic aliases for new/refactored modules.
export type SourceOf<T> = (() -> T) & ((T) -> ())
export type ReactiveOf<T> = T | (() -> T)

return {}
''')

write(TYPES / "StoreTypes.lua", r'''
--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>
export type MenuId = MenuIdTypes.MenuId

export type UIStore = {
	currentMenu: SourceOf<MenuId?>,
}

return {}
''')

write(TYPES / "ButtonTypes.lua", r'''
--!strict

local StoreTypes = require(script.Parent.StoreTypes)

export type UIStore = StoreTypes.UIStore

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
''')

# -----------------------------------------------------------------------------
# Menu types
# -----------------------------------------------------------------------------
write(MENU_TYPES / "MenuIdTypes.lua", r'''
--!strict

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
''')

simple_menus = {
    "SideKickTypes.lua": "SideKickMenuProps",
    "BoostersTypes.lua": "BoostersMenuProps",
    "ActivityTypes.lua": "ActivityMenuProps",
    "StatsTypes.lua": "StatsMenuProps",
    "QuestsTypes.lua": "QuestsMenuProps",
    "RewardsTypes.lua": "RewardsMenuProps",
    "ShopTypes.lua": "ShopMenuProps",
}

for filename, prop_name in simple_menus.items():
    write(MENU_TYPES / filename, f'''
--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type {prop_name} = {{
	store: StoreTypes.UIStore,
}}

return {{}}
''')

write(MENU_TYPES / "InventoryTypes.lua", r'''
--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type InventoryMenuProps = {
	store: StoreTypes.UIStore,
}

export type InventoryTabId = "Skins" | "Ranks" | "Quests"

export type SkinRarity =
	"Common"
	| "Uncommon"
	| "Rare"
	| "Epic"
	| "Legendary"
	| "Mythic"

export type SkinView = {
	SkinId: string,
	Name: string,
	ImageId: string,
	Rarity: SkinRarity,
	Description: string,
	Owned: boolean,
	Equipped: boolean,
	Locked: boolean,
}

export type InventoryTabDefinition = {
	id: InventoryTabId,
	label: string,
	hasAlert: boolean?,
	layoutOrder: number,
}

return {}
''')

write(MENU_TYPES / "AchievementTypes.lua", r'''
--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type AchievementsMenuProps = {
	store: StoreTypes.UIStore,
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

export type AchievementState = "Available" | "NotReady" | "Claimed"

return {}
''')

write(MENU_TYPES / "SettingsTypes.lua", r'''
--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type SettingsMenuProps = {
	store: StoreTypes.UIStore,
}

export type SettingsTab = "Volume" | "User" | "Game"

return {}
''')

write(MENU_TYPES / "init.lua", r'''
--!strict

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

export type InventoryTabId = InventoryTypes.InventoryTabId
export type SkinRarity = InventoryTypes.SkinRarity
export type SkinView = InventoryTypes.SkinView
export type InventoryTabDefinition = InventoryTypes.InventoryTabDefinition

export type SettingsTab = SettingsTypes.SettingsTab

export type AchievementCategory = AchievementTypes.AchievementCategory
export type AchievementState = AchievementTypes.AchievementState

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
''')

# -----------------------------------------------------------------------------
# Effect types
# -----------------------------------------------------------------------------
write(EFFECT_TYPES / "HoverUIScaleTypes.lua", r'''
--!strict

export type HoverUIScaleOptions = {
	idleScale: number?,
	hoverScale: number?,
	scaleTextConstraints: boolean?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
''')

write(EFFECT_TYPES / "PulseUIScaleTypes.lua", r'''
--!strict

export type PulseUIScaleOptions = {
	enabled: boolean?,
	idleScale: number?,
	pulseScale: number?,
	period: number?,
	phaseOffset: number?,
}

return {}
''')

write(EFFECT_TYPES / "FadeGuiObjectTypes.lua", r'''
--!strict

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
''')

write(EFFECT_TYPES / "SlideFadeCanvasGroupTypes.lua", r'''
--!strict

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
''')

write(EFFECT_TYPES / "SweepGradientKeypointTypes.lua", r'''
--!strict

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
''')

write(EFFECT_TYPES / "init.lua", r'''
--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local FadeGuiObjectTypes = require(script.FadeGuiObjectTypes)
local HoverUIScaleTypes = require(script.HoverUIScaleTypes)
local PulseUIScaleTypes = require(script.PulseUIScaleTypes)
local SlideFadeCanvasGroupTypes = require(script.SlideFadeCanvasGroupTypes)
local SweepGradientKeypointTypes = require(script.SweepGradientKeypointTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>

export type FadeGuiObjectOptions = FadeGuiObjectTypes.FadeGuiObjectOptions
export type HoverUIScaleOptions = HoverUIScaleTypes.HoverUIScaleOptions
export type PulseUIScaleOptions = PulseUIScaleTypes.PulseUIScaleOptions
export type SlideFadeCanvasGroupOptions = SlideFadeCanvasGroupTypes.SlideFadeCanvasGroupOptions
export type SweepGradientKeypointOptions = SweepGradientKeypointTypes.SweepGradientKeypointOptions

export type HoverScaleOptions = {
	scale: number?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

export type SpinOptions = {
	speed: number?,
}

export type SlideMenuOptions = {
	open: () -> boolean,
	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	duration: number?,
}

export type PulseStrokeOptions = {
	colorA: Color3?,
	colorB: Color3?,
	duration: number?,
}

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

export type PulseGradientOffsetOptions = {
	phase: (() -> number)?,
	phaseMultiplier: number?,
	minOffset: Vector2?,
	maxOffset: Vector2?,
}

export type PulseDriverOptions = {
	phase: SourceOf<number>,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

export type LiquidGradientOptions = {
	duration: number?,
	primaryColor: Color3?,
	secondaryColor: Color3?,
	disabledColor: Color3?,
	enabled: (() -> boolean)?,
}

return {
	FadeGuiObjectTypes = FadeGuiObjectTypes,
	HoverUIScaleTypes = HoverUIScaleTypes,
	PulseUIScaleTypes = PulseUIScaleTypes,
	SlideFadeCanvasGroupTypes = SlideFadeCanvasGroupTypes,
	SweepGradientKeypointTypes = SweepGradientKeypointTypes,
}
''')

# -----------------------------------------------------------------------------
# Component types
# -----------------------------------------------------------------------------
write(COMPONENT_TYPES / "ActionButtonTypes.lua", r'''
--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

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

export type GradientKeypoint = ActionButtonGradientKeypoint

export type ActionButtonGradientProps = {
	keypoints: ReactiveOf<{ ActionButtonGradientKeypoint }>?,
	rotation: ReactiveOf<number>?,
}

export type ActionButtonProps = {
	name: string?,
	text: Reactive?,
	iconText: Reactive?,
	variant: Reactive?,
	gradient: ActionButtonGradientProps?,
	strokeGradient: ActionButtonGradientProps?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,
	disabled: Reactive?,
	cornerRadius: Reactive?,
	textColor3: Reactive?,
	textTransparency: Reactive?,
	strokeColor: Reactive?,
	strokeThickness: Reactive?,
	strokeTransparency: Reactive?,
	hoverScale: Reactive?,
	hoverDuration: Reactive?,
	scaleTextConstraints: Reactive?,
	onClick: (() -> ())?,
}

return {}
''')

write(COMPONENT_TYPES / "TextTypes.lua", r'''
--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

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
	thickness: Reactive?,
	color: Reactive?,
	transparency: Reactive?,
	pulse: TextPulseStrokeProps?,
}

export type TextProps = {
	name: string?,
	text: Reactive?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	rotation: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	layoutOrder: Reactive?,
	backgroundTransparency: Reactive?,
	backgroundColor3: Reactive?,
	fontFace: Font?,
	textScaled: boolean?,
	textSize: Reactive?,
	minTextSize: number?,
	maxTextSize: number?,
	textColor3: Reactive?,
	textTransparency: Reactive?,
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
''')

write(COMPONENT_TYPES / "ImageTypes.lua", r'''
--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive

export type ImageGradientProps = {
	color: ColorSequence?,
	transparency: NumberSequence?,
	rotation: number?,
	offset: Vector2?,
}

export type ImageStrokeProps = {
	thickness: Reactive?,
	color: Reactive?,
	transparency: Reactive?,
	applyStrokeMode: Enum.ApplyStrokeMode?,
}

export type ImageProps = {
	name: string?,
	image: Reactive?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	rotation: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	layoutOrder: Reactive?,
	backgroundTransparency: Reactive?,
	backgroundColor3: Reactive?,
	imageColor3: Reactive?,
	imageTransparency: Reactive?,
	scaleType: Enum.ScaleType?,
	sliceCenter: Rect?,
	sliceScale: number?,
	cornerRadius: Reactive?,
	stroke: ImageStrokeProps?,
	gradient: ImageGradientProps?,
}

return {}
''')

write(COMPONENT_TYPES / "PanelTypes.lua", r'''
--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.Parent.MenuTypes.MenuIdTypes)

export type PanelProps = {
	store: StoreTypes.UIStore,
	menuId: MenuIdTypes.MenuId,
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
''')

write(COMPONENT_TYPES / "ScrollAreaTypes.lua", r'''
--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)
local EffectTypes = require(script.Parent.Parent.EffectTypes)

export type Reactive = SharedTypes.Reactive
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions

export type ScrollAreaLayoutKind = "Grid" | "List" | "None"
export type ScrollAreaChildren = Instance | { Instance } | (() -> Instance?) | (() -> { Instance })

export type ScrollAreaPaddingProps = {
	top: Reactive?,
	bottom: Reactive?,
	left: Reactive?,
	right: Reactive?,
}

export type ScrollAreaGridProps = {
	cellSize: Reactive?,
	cellPadding: Reactive?,
	fillDirection: Enum.FillDirection?,
	fillDirectionMaxCells: number?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
	startCorner: Enum.StartCorner?,
}

export type ScrollAreaListProps = {
	padding: Reactive?,
	fillDirection: Enum.FillDirection?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
}

export type ScrollAreaProps = {
	name: string?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	layoutOrder: Reactive?,
	layoutTween: TweenGuiObjectLayoutOptions?,
	backgroundTransparency: Reactive?,
	backgroundColor3: Reactive?,
	clipsDescendants: boolean?,
	syncGridCanvas: boolean?,
	canvasBottomSafetyScale: Reactive?,
	canvasHeightScale: Reactive?,
	canvasSize: Reactive?,
	automaticCanvasSize: Enum.AutomaticSize?,
	scrollingDirection: Enum.ScrollingDirection?,
	scrollingEnabled: Reactive?,
	scrollBarThickness: Reactive?,
	scrollBarImageColor3: Reactive?,
	scrollBarImageTransparency: Reactive?,
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
''')

write(COMPONENT_TYPES / "init.lua", r'''
--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local EffectTypes = require(script.Parent.EffectTypes)

local ActionButtonTypes = require(script.ActionButtonTypes)
local ImageTypes = require(script.ImageTypes)
local PanelTypes = require(script.PanelTypes)
local ScrollAreaTypes = require(script.ScrollAreaTypes)
local TextTypes = require(script.TextTypes)

export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>
export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>

export type ActionButtonProps = ActionButtonTypes.ActionButtonProps
export type ActionButtonVariant = ActionButtonTypes.ActionButtonVariant
export type ActionButtonGradientKeypoint = ActionButtonTypes.ActionButtonGradientKeypoint
export type GradientKeypoint = ActionButtonTypes.GradientKeypoint
export type ActionButtonGradientProps = ActionButtonTypes.ActionButtonGradientProps

export type ImageProps = ImageTypes.ImageProps
export type ImageStrokeProps = ImageTypes.ImageStrokeProps
export type ImageGradientProps = ImageTypes.ImageGradientProps

export type PanelProps = PanelTypes.PanelProps

export type ScrollAreaProps = ScrollAreaTypes.ScrollAreaProps
export type ScrollAreaPaddingProps = ScrollAreaTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ScrollAreaTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ScrollAreaTypes.ScrollAreaListProps
export type ScrollAreaLayoutKind = ScrollAreaTypes.ScrollAreaLayoutKind
export type ScrollAreaChildren = ScrollAreaTypes.ScrollAreaChildren

export type TextProps = TextTypes.TextProps
export type TextStrokeProps = TextTypes.TextStrokeProps
export type TextGradientProps = TextTypes.TextGradientProps
export type TextPulseStrokeProps = TextTypes.TextPulseStrokeProps

export type BackgroundProps = {
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
}

export type HeaderProps = {
	text: string | (() -> string)?,
}

export type ExitButtonProps = {
	onClick: (() -> ())?,
	position: UDim2?,
	size: UDim2?,
	anchorPoint: Vector2?,
}

export type GridCellSizeOptions = {
	columns: number,
	rowsVisible: number?,
	gap: number?,
	widthFill: number?,
	heightFill: number?,
}

export type ToggleSwitchProps = {
	name: string?,
	value: Source,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,
	disabled: Reactive?,
	onChanged: ((boolean) -> ())?,
	backgroundColor3: Reactive?,
	onBackgroundColor3: Reactive?,
	fillColor3: Reactive?,
	knobColor3: Reactive?,
	onKnobColor3: Reactive?,
	strokeColor3: Reactive?,
	backgroundTransparency: Reactive?,
	fillTransparency: Reactive?,
	strokeTransparency: Reactive?,
	strokeThickness: Reactive?,
	cornerRadius: Reactive?,
	knobSize: Reactive?,
	knobOffPosition: Reactive?,
	knobOnPosition: Reactive?,
	tweenDuration: number?,
}

export type ToggleButtonProps = {
	name: string?,
	value: Source,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,
	disabled: Reactive?,
	onChanged: ((boolean) -> ())?,
	textOn: Reactive?,
	textOff: Reactive?,
	fontFace: Reactive?,
	textColor3: Reactive?,
	onTextColor3: Reactive?,
	backgroundColor3: Reactive?,
	onBackgroundColor3: Reactive?,
	backgroundTransparency: Reactive?,
	gradient: Reactive?,
	onGradient: Reactive?,
	gradientRotation: Reactive?,
	strokeColor3: Reactive?,
	onStrokeColor3: Reactive?,
	strokeTransparency: Reactive?,
	strokeThickness: Reactive?,
	cornerRadius: Reactive?,
	aspectRatio: Reactive?,
	minTextSize: Reactive?,
	maxTextSize: Reactive?,
}

export type SliderProps = {
	name: string?,
	value: Source,
	min: number?,
	max: number?,
	step: number?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,
	disabled: Reactive?,
	dimmed: Reactive?,
	onChanged: ((number) -> ())?,
	backgroundColor3: Reactive?,
	fillColor3: Reactive?,
	fillGradient: Reactive?,
	fillGradientTransparency: Reactive?,
	fillGradientRotation: Reactive?,
	fillGradientOffset: Reactive?,
	fillGradientEffect: EffectTypes.LiquidGradientOptions?,
	knobColor3: Reactive?,
	dimmedKnobColor3: Reactive?,
	strokeColor3: Reactive?,
	backgroundTransparency: Reactive?,
	fillTransparency: Reactive?,
	dimmedFillTransparency: Reactive?,
	strokeTransparency: Reactive?,
	strokeThickness: Reactive?,
	cornerRadius: Reactive?,
	knobSize: Reactive?,
}

return {
	ActionButtonTypes = ActionButtonTypes,
	ImageTypes = ImageTypes,
	PanelTypes = PanelTypes,
	ScrollAreaTypes = ScrollAreaTypes,
	TextTypes = TextTypes,
}
''')

# -----------------------------------------------------------------------------
# Top-level compatibility aggregator
# -----------------------------------------------------------------------------
write(TYPES / "init.lua", r'''
--!strict

local SharedTypes = require(script.SharedTypes)
local StoreTypes = require(script.StoreTypes)
local ButtonTypes = require(script.ButtonTypes)
local ComponentTypes = require(script.ComponentTypes)
local EffectTypes = require(script.EffectTypes)
local MenuTypes = require(script.MenuTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>
export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

export type DeviceKind = "Desktop" | "Mobile" | "Tablet" | "Console"
export type MenuId = MenuTypes.MenuId
export type UIStore = StoreTypes.UIStore
export type SettingsTab = MenuTypes.SettingsTab

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

export type InventoryTabId = MenuTypes.InventoryTabId
export type SkinRarity = MenuTypes.SkinRarity
export type SkinView = MenuTypes.SkinView
export type InventoryTabDefinition = MenuTypes.InventoryTabDefinition
export type AchievementCategory = MenuTypes.AchievementCategory
export type AchievementState = MenuTypes.AchievementState

export type BackgroundProps = ComponentTypes.BackgroundProps
export type ExitButtonProps = ComponentTypes.ExitButtonProps
export type HeaderProps = ComponentTypes.HeaderProps
export type PanelProps = ComponentTypes.PanelProps
export type TextProps = ComponentTypes.TextProps
export type TextGradientProps = ComponentTypes.TextGradientProps
export type TextPulseStrokeProps = ComponentTypes.TextPulseStrokeProps
export type TextStrokeProps = ComponentTypes.TextStrokeProps
export type ScrollAreaLayoutKind = ComponentTypes.ScrollAreaLayoutKind
export type ScrollAreaChildren = ComponentTypes.ScrollAreaChildren
export type ScrollAreaPaddingProps = ComponentTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ComponentTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ComponentTypes.ScrollAreaListProps
export type ScrollAreaProps = ComponentTypes.ScrollAreaProps
export type ImageStrokeProps = ComponentTypes.ImageStrokeProps
export type ImageGradientProps = ComponentTypes.ImageGradientProps
export type ImageProps = ComponentTypes.ImageProps
export type ToggleSwitchProps = ComponentTypes.ToggleSwitchProps
export type ToggleButtonProps = ComponentTypes.ToggleButtonProps
export type SliderProps = ComponentTypes.SliderProps
export type GridCellSizeOptions = ComponentTypes.GridCellSizeOptions
export type ActionButtonVariant = ComponentTypes.ActionButtonVariant
export type ActionButtonGradientKeypoint = ComponentTypes.ActionButtonGradientKeypoint
export type ActionButtonGradientProps = ComponentTypes.ActionButtonGradientProps
export type ActionButtonProps = ComponentTypes.ActionButtonProps

export type HoverScaleOptions = EffectTypes.HoverScaleOptions
export type SpinOptions = EffectTypes.SpinOptions
export type SlideMenuOptions = EffectTypes.SlideMenuOptions
export type PulseStrokeOptions = EffectTypes.PulseStrokeOptions
export type HoverUIScaleOptions = EffectTypes.HoverUIScaleOptions
export type PulseUIScaleOptions = EffectTypes.PulseUIScaleOptions
export type TweenGuiObjectLayoutBounceOptions = EffectTypes.TweenGuiObjectLayoutBounceOptions
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions
export type SlideFadeCanvasGroupOptions = EffectTypes.SlideFadeCanvasGroupOptions
export type PulseDriverOptions = EffectTypes.PulseDriverOptions
export type SweepGradientKeypointOptions = EffectTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = EffectTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions
export type FadeGuiObjectOptions = EffectTypes.FadeGuiObjectOptions

return {
	SharedTypes = SharedTypes,
	StoreTypes = StoreTypes,
	ButtonTypes = ButtonTypes,
	ComponentTypes = ComponentTypes,
	EffectTypes = EffectTypes,
	MenuTypes = MenuTypes,
}
''')

# Remove legacy flat UITypes.lua. Keeping it beside UITypes/init.lua creates a Rojo name collision.
legacy_file = UI_MANAGER / "UITypes.lua"
if legacy_file.exists():
    backup_dir = ROOT / "_local_backups"
    backup_dir.mkdir(exist_ok=True)
    backup_file = backup_dir / "UITypes.lua.bak"
    shutil.copy2(legacy_file, backup_file)
    legacy_file.unlink()
    print(f"Backed up and removed legacy file: {legacy_file} -> {backup_file}")

print("UITypes folder refactor files written successfully.")
print("Next: run Rojo/Studio typecheck. If errors appear, paste the exact output.")
