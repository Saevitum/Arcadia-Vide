--!strict

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
