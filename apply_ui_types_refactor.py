#!/usr/bin/env python3
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / "src" / "client" / "UI" / "UIManager" / "UITypes"

FILES = {
"SharedTypes.lua": """--!strict

-- Compatibility aliases for current modules that still use `Types.Source`
-- and `Types.Reactive` without generic parameters.
export type Source = (() -> any) & ((any) -> ())
export type Reactive = any

-- Preferred typed aliases for new/refactored modules.
export type SourceOf<T> = (() -> T) & ((T) -> ())
export type ReactiveOf<T> = T | (() -> T)

export type VoidCallback = () -> ()
export type CleanupCallback = () -> ()

return {}
""",

"StoreTypes.lua": """--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type SourceOf<T> = SharedTypes.SourceOf<T>
export type MenuId = MenuIdTypes.MenuId

export type UIStore = {
	currentMenu: SourceOf<MenuId?>,
}

return {}
""",

"ButtonTypes.lua": """--!strict

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
""",

"DeviceTypes.lua": """--!strict

export type DeviceKind = "Desktop" | "Mobile" | "Tablet" | "Console"

return {}
""",

"ComponentTypes/ActionButtonTypes.lua": """--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

export type ActionButtonVariant =
	"Green"
	| "OrangeYellow"
	| "Blue"
	| "Purple"
	| "Yellow"
	| "Orange"
	| "Red"
	| "Red2"
	| "Red3"
	| "Disabled"
	| "Dark"

export type GradientKeypoint = {
	time: number,
	color: Color3,
}

export type ActionButtonGradientProps = {
	keypoints: Reactive?,
	rotation: Reactive?,
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
""",

"ComponentTypes/TextTypes.lua": """--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive

export type TextGradientProps = {
	color: ColorSequence?,
	transparency: NumberSequence?,
	rotation: number?,
	offset: Vector2?,
}

export type TextStrokePulseProps = {
	colorA: Color3?,
	colorB: Color3?,
	duration: number?,
}

export type TextStrokeProps = {
	thickness: Reactive?,
	color: Reactive?,
	transparency: Reactive?,
	pulse: TextStrokePulseProps?,
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
""",

"ComponentTypes/ImageTypes.lua": """--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive

export type ImageStrokeProps = {
	thickness: Reactive?,
	color: Reactive?,
	transparency: Reactive?,
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
""",

"ComponentTypes/PanelTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.Parent.MenuTypes.MenuIdTypes)

export type UIStore = StoreTypes.UIStore
export type MenuId = MenuIdTypes.MenuId

export type PanelProps = {
	name: string?,
	store: UIStore,
	menuId: MenuId,
	title: string?,

	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	zIndex: number?,
	aspectRatio: number?,

	content: Instance?,

	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	slideDuration: number?,

	exitButtonSize: UDim2?,
	exitButtonPosition: UDim2?,
	exitButtonAnchorPoint: Vector2?,
}

return {}
""",

"ComponentTypes/ScrollAreaTypes.lua": """--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive

export type ScrollAreaLayoutKind = "Grid" | "List" | "None"

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

	backgroundTransparency: Reactive?,
	backgroundColor3: Reactive?,
	clipsDescendants: boolean?,

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

	layoutTween: any?,
	syncGridCanvas: boolean?,
	canvasBottomSafetyScale: Reactive?,

	children: any?,
}

return {}
""",

"ComponentTypes/init.lua": """--!strict

local SharedTypes = require(script.Parent.SharedTypes)

local ActionButtonTypes = require(script.ActionButtonTypes)
local ImageTypes = require(script.ImageTypes)
local PanelTypes = require(script.PanelTypes)
local ScrollAreaTypes = require(script.ScrollAreaTypes)
local TextTypes = require(script.TextTypes)

export type Reactive = SharedTypes.Reactive
export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>

export type ActionButtonProps = ActionButtonTypes.ActionButtonProps
export type ActionButtonVariant = ActionButtonTypes.ActionButtonVariant
export type GradientKeypoint = ActionButtonTypes.GradientKeypoint

export type ImageProps = ImageTypes.ImageProps
export type ImageStrokeProps = ImageTypes.ImageStrokeProps
export type ImageGradientProps = ImageTypes.ImageGradientProps

export type PanelProps = PanelTypes.PanelProps

export type ScrollAreaProps = ScrollAreaTypes.ScrollAreaProps
export type ScrollAreaPaddingProps = ScrollAreaTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ScrollAreaTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ScrollAreaTypes.ScrollAreaListProps
export type ScrollAreaLayoutKind = ScrollAreaTypes.ScrollAreaLayoutKind

export type TextProps = TextTypes.TextProps
export type TextStrokeProps = TextTypes.TextStrokeProps
export type TextGradientProps = TextTypes.TextGradientProps

export type BackgroundProps = {
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
}

export type HeaderProps = {
	text: string?,
}

export type ExitButtonProps = {
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	onClick: (() -> ())?,
}

export type GridCellSizeOptions = {
	columns: number,
	rowsVisible: number?,
	gap: number?,
	widthFill: number?,
	heightFill: number?,
}

export type SliderProps = {
	name: string?,
	value: SourceOf<number>,

	min: number?,
	max: number?,
	step: number?,

	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,

	backgroundColor3: Reactive?,
	backgroundTransparency: Reactive?,
	dimmed: Reactive?,
	disabled: Reactive?,

	cornerRadius: Reactive?,
	strokeThickness: Reactive?,
	strokeColor3: Reactive?,
	strokeTransparency: Reactive?,

	fillColor3: Reactive?,
	fillTransparency: Reactive?,
	dimmedFillTransparency: Reactive?,
	fillGradient: Reactive?,
	fillGradientTransparency: Reactive?,
	fillGradientRotation: Reactive?,
	fillGradientOffset: Reactive?,
	fillGradientEffect: any?,

	knobSize: Reactive?,
	knobColor3: Reactive?,
	dimmedKnobColor3: Reactive?,

	onChanged: ((number) -> ())?,
}

export type ToggleButtonProps = {
	name: string?,
	value: SourceOf<boolean>,

	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,

	textOn: Reactive?,
	textOff: Reactive?,
	fontFace: Reactive?,
	minTextSize: Reactive?,
	maxTextSize: Reactive?,

	textColor3: Reactive?,
	onTextColor3: Reactive?,

	backgroundColor3: Reactive?,
	onBackgroundColor3: Reactive?,
	backgroundTransparency: Reactive?,

	gradient: Reactive?,
	onGradient: Reactive?,
	gradientRotation: Reactive?,

	strokeThickness: Reactive?,
	strokeColor3: Reactive?,
	onStrokeColor3: Reactive?,
	strokeTransparency: Reactive?,

	cornerRadius: Reactive?,
	aspectRatio: Reactive?,

	disabled: Reactive?,
	onChanged: ((boolean) -> ())?,
}

export type ToggleSwitchProps = {
	name: string?,
	value: SourceOf<boolean>,

	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,

	backgroundColor3: Reactive?,
	onBackgroundColor3: Reactive?,
	backgroundTransparency: Reactive?,

	cornerRadius: Reactive?,
	strokeThickness: Reactive?,
	strokeColor3: Reactive?,
	strokeTransparency: Reactive?,

	fillColor3: Reactive?,
	fillTransparency: Reactive?,

	knobSize: Reactive?,
	knobColor3: Reactive?,
	onKnobColor3: Reactive?,
	knobOnPosition: Reactive?,
	knobOffPosition: Reactive?,
	tweenDuration: number?,

	disabled: Reactive?,
	onChanged: ((boolean) -> ())?,
}

return {
	ActionButtonTypes = ActionButtonTypes,
	ImageTypes = ImageTypes,
	PanelTypes = PanelTypes,
	ScrollAreaTypes = ScrollAreaTypes,
	TextTypes = TextTypes,
}
""",

"EffectTypes/HoverUIScaleTypes.lua": """--!strict

export type HoverUIScaleOptions = {
	idleScale: number?,
	hoverScale: number?,
	scaleTextConstraints: boolean?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
""",

"EffectTypes/SlideFadeCanvasGroupTypes.lua": """--!strict

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
""",

"EffectTypes/SweepGradientKeypointTypes.lua": """--!strict

export type SweepGradientKeypointOptions = {
	edgeColor: Color3?,
	middleColor: Color3?,
	alternateMiddleColor: Color3?,
	middleColors: { Color3 }?,

	loopsPerColor: number?,
	changeColorEveryLoops: number?,

	edgeTransparency: number?,
	middleTransparency: number?,

	segmentDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,

	colorTweenDuration: number?,
	colorEasingStyle: Enum.EasingStyle?,
	colorEasingDirection: Enum.EasingDirection?,

	phase: (() -> number)?,
	onColorChanged: ((Color3) -> ())?,
}

return {}
""",

"EffectTypes/FadeGuiObjectTypes.lua": """--!strict

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
""",

"EffectTypes/PulseUIScaleTypes.lua": """--!strict

export type PulseUIScaleOptions = {
	enabled: boolean?,
	idleScale: number?,
	pulseScale: number?,
	period: number?,
	phaseOffset: number?,
}

return {}
""",

"EffectTypes/init.lua": """--!strict

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
""",

"MenuTypes/MenuIdTypes.lua": """--!strict

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
""",

"MenuTypes/SideKickTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type UIStore = StoreTypes.UIStore

export type SideKickMenuProps = {
	store: UIStore,
}

export type SideKickRarity =
	"Common"
	| "Uncommon"
	| "Rare"
	| "Epic"
	| "Legendary"
	| "Mythic"

export type SideKickType = "Passive" | "Active"

export type SideKickView = {
	SideKickId: string,
	Name: string,
	Description: string,
	Rarity: SideKickRarity,
	Type: SideKickType,
	ImageId: string,
	TransparentImageId: string?,
	ModelPath: string?,
	Skill: string?,
	BasePower: number,
	VirtualMachine: string?,
}

return {}
""",

"MenuTypes/BoostersTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type BoostersMenuProps = {
	store: StoreTypes.UIStore,
}

return {}
""",

"MenuTypes/ActivityTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type ActivityMenuProps = {
	store: StoreTypes.UIStore,
}

export type ActivityRow = {
	label: string,
	value: string,
}

return {}
""",

"MenuTypes/StatsTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type StatsMenuProps = {
	store: StoreTypes.UIStore,
}

return {}
""",

"MenuTypes/QuestsTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type QuestsMenuProps = {
	store: StoreTypes.UIStore,
}

return {}
""",

"MenuTypes/InventoryTypes.lua": """--!strict

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
""",

"MenuTypes/AchievementTypes.lua": """--!strict

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
""",

"MenuTypes/RewardsTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type RewardsMenuProps = {
	store: StoreTypes.UIStore,
}

export type RewardState = "Claimed" | "Locked" | "Available"

return {}
""",

"MenuTypes/SettingsTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type SettingsMenuProps = {
	store: StoreTypes.UIStore,
}

export type SettingsTab = "Volume" | "User" | "Game"

return {}
""",

"MenuTypes/ShopTypes.lua": """--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type ShopMenuProps = {
	store: StoreTypes.UIStore,
}

return {}
""",

"MenuTypes/init.lua": """--!strict

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
""",

"init.lua": """--!strict

local SharedTypes = require(script.SharedTypes)
local DeviceTypes = require(script.DeviceTypes)
local StoreTypes = require(script.StoreTypes)
local ButtonTypes = require(script.ButtonTypes)

local ComponentTypes = require(script.ComponentTypes)
local EffectTypes = require(script.EffectTypes)
local MenuTypes = require(script.MenuTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>
export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

export type DeviceKind = DeviceTypes.DeviceKind

export type MenuId = MenuTypes.MenuId
export type UIStore = StoreTypes.UIStore

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
export type HeaderProps = ComponentTypes.HeaderProps
export type ExitButtonProps = ComponentTypes.ExitButtonProps
export type GridCellSizeOptions = ComponentTypes.GridCellSizeOptions

export type PanelProps = ComponentTypes.PanelProps
export type TextProps = ComponentTypes.TextProps
export type TextStrokeProps = ComponentTypes.TextStrokeProps
export type TextGradientProps = ComponentTypes.TextGradientProps

export type ImageProps = ComponentTypes.ImageProps
export type ImageStrokeProps = ComponentTypes.ImageStrokeProps
export type ImageGradientProps = ComponentTypes.ImageGradientProps

export type ScrollAreaProps = ComponentTypes.ScrollAreaProps
export type ScrollAreaPaddingProps = ComponentTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ComponentTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ComponentTypes.ScrollAreaListProps
export type ScrollAreaLayoutKind = ComponentTypes.ScrollAreaLayoutKind

export type ActionButtonProps = ComponentTypes.ActionButtonProps
export type ActionButtonVariant = ComponentTypes.ActionButtonVariant
export type GradientKeypoint = ComponentTypes.GradientKeypoint

export type SliderProps = ComponentTypes.SliderProps
export type ToggleButtonProps = ComponentTypes.ToggleButtonProps
export type ToggleSwitchProps = ComponentTypes.ToggleSwitchProps

export type HoverScaleOptions = EffectTypes.HoverScaleOptions
export type HoverUIScaleOptions = EffectTypes.HoverUIScaleOptions
export type SlideMenuOptions = EffectTypes.SlideMenuOptions
export type SpinOptions = EffectTypes.SpinOptions
export type PulseStrokeOptions = EffectTypes.PulseStrokeOptions
export type SweepGradientKeypointOptions = EffectTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = EffectTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions
export type PulseDriverOptions = EffectTypes.PulseDriverOptions
export type PulseUIScaleOptions = EffectTypes.PulseUIScaleOptions
export type FadeGuiObjectOptions = EffectTypes.FadeGuiObjectOptions
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions
export type TweenGuiObjectLayoutBounceOptions = EffectTypes.TweenGuiObjectLayoutBounceOptions
export type SlideFadeCanvasGroupOptions = EffectTypes.SlideFadeCanvasGroupOptions

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

export type SettingsTab = MenuTypes.SettingsTab
export type AchievementCategory = MenuTypes.AchievementCategory
export type AchievementState = MenuTypes.AchievementState

return {
	SharedTypes = SharedTypes,
	DeviceTypes = DeviceTypes,
	StoreTypes = StoreTypes,
	ButtonTypes = ButtonTypes,

	ComponentTypes = ComponentTypes,
	EffectTypes = EffectTypes,
	MenuTypes = MenuTypes,
}
""",
}

def main():
    if not BASE.exists():
        raise SystemExit(f"Cannot find {BASE}. Run this from the Arcadia-Vide repo root.")

    for relative, content in FILES.items():
        path = BASE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {path.relative_to(ROOT)}")

    print("\nDone. Now run your typechecker/Studio sync and commit the changes.")

if __name__ == "__main__":
    main()
