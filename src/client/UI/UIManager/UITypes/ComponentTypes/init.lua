--!strict

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
