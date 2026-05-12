--!strict

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
