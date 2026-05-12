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
