--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

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

export type GradientKeypoint = ActionButtonGradientKeypoint

export type ActionButtonGradientProps = {
	keypoints: ReactiveOf<{ ActionButtonGradientKeypoint }>?,
	rotation: ReactiveOf<number>?,
}

export type ActionButtonProps = {
	name: string?,
	text: Reactive?,
	iconText: Reactive?,
	variant: Reactive?,
	gradient: ActionButtonGradientProps?,
	strokeGradient: ActionButtonGradientProps?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	layoutOrder: Reactive?,
	zIndex: Reactive?,
	disabled: Reactive?,
	cornerRadius: Reactive?,
	textColor3: Reactive?,
	textTransparency: Reactive?,
	strokeColor: Reactive?,
	strokeThickness: Reactive?,
	strokeTransparency: Reactive?,
	hoverScale: Reactive?,
	hoverDuration: Reactive?,
	scaleTextConstraints: Reactive?,
	onClick: (() -> ())?,
}

return {}
