--!strict

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
