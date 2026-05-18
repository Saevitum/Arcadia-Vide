--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Source = SharedTypes.Source
export type Reactive = SharedTypes.Reactive

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
	selectedTab: Source,
	style: TabButtonStyle?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	onTabSelected: ((any) -> ())?,
}

export type TabStripProps = {
	tabs: { TabDefinition },
	selectedTab: Source,
	style: TabStripStyle?,
	name: string?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	cellSize: Reactive?,
	cellPadding: Reactive?,
	fillDirectionMaxCells: Reactive?,
	onTabSelected: ((any) -> ())?,
}

return {}
