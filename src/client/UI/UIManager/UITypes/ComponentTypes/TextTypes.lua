--!strict

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
