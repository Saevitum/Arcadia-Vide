--!strict

export type PulseUIScaleOptions = {
	open: (() -> boolean)?,
	enabled: (() -> boolean)?,
	idleScale: number?,
	minScale: number?,
	maxScale: number?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
