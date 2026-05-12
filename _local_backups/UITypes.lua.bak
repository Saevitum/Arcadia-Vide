--!strict

export type DeviceKind = "Desktop" | "Mobile" | "Tablet" | "Console"

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

export type Source<T> = (() -> T) & ((T) -> ())
export type SettingsTab = "Volume" | "User" | "Game"

export type UIStore = {
	currentMenu: Source<MenuId?>,
}

export type ButtonBarProps = {
	store: UIStore,
}

export type SideKickMenuProps = {
	store: UIStore,
}

export type SideKickButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type BoostersMenuProps = {
	store: UIStore,
}

export type BoostersButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type ActivityButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type StatsMenuProps = {
	store: UIStore,
}

export type StatsButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type QuestsMenuProps = {
	store: UIStore,
}

export type QuestsButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type InventoryMenuProps = {
	store: UIStore,
}

export type InventoryButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type AchievementsMenuProps = {
	store: UIStore,
}

export type AchievementsButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type RewardsMenuProps = {
	store: UIStore,
}

export type RewardsButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type SettingsMenuProps = {
	store: UIStore,
}

export type SettingsButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type ShopMenuProps = {
	store: UIStore,
}

export type ShopButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

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

export type HoverScaleOptions = {
	scale: number?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

export type SpinOptions = {
	speed: number?,
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

export type Reactive<T> = T | (() -> T)

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

export type ImageStrokeProps = {
	thickness: Reactive<number>?,
	color: Reactive<Color3>?,
	transparency: Reactive<number>?,
	applyStrokeMode: Enum.ApplyStrokeMode?,
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

export type GridCellSizeOptions = {
	columns: number,
	rowsVisible: number?,

	gap: number?,

	-- 1 means use the full available ScrollArea width/height.
	-- Lower values intentionally leave empty breathing room.
	widthFill: number?,
	heightFill: number?,
}

export type HoverUIScaleOptions = {
	idleScale: number?,
	hoverScale: number?,
	scaleTextConstraints: boolean?,

	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
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

export type PulseDriverOptions = {
	phase: (() -> number) & ((number) -> ()),

	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

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

export type PulseGradientOffsetOptions = {
	phase: (() -> number)?,
	minOffset: Vector2?,
	maxOffset: Vector2?,
	phaseMultiplier: number?,
}

export type LiquidGradientOptions = {
	duration: number?,
	primaryColor: Color3?,
	secondaryColor: Color3?,
	disabledColor: Color3?,
	enabled: (() -> boolean)?,
}

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

export type ImageGradientProps = {
	color: ColorSequence?,
	transparency: NumberSequence?,
	rotation: number?,
	offset: Vector2?,
}

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

	variant: Reactive<ActionButtonVariant?>?,
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

export type ActivityMenuProps = {
	store: UIStore,
}

return {}
