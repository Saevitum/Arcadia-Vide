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
