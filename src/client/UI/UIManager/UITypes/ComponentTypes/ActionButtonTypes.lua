--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

export type ActionButtonVariant =
	"Green"
	| "OrangeYellow"
	| "Blue"
	| "Purple"
	| "Yellow"
	| "Orange"
	| "Red"
	| "Red2"
	| "Red3"
	| "Disabled"
	| "Dark"

export type GradientKeypoint = {
	time: number,
	color: Color3,
}

export type ActionButtonGradientProps = {
	keypoints: Reactive?,
	rotation: Reactive?,
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
