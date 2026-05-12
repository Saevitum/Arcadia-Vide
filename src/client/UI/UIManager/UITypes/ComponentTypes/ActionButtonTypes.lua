--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive<T> = SharedTypes.Reactive<T>

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
	variant: Reactive<ActionButtonVariant>?,
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

return {}
