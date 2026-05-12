--!strict

export type SweepGradientKeypointOptions = {
	edgeColor: Color3?,
	middleColor: Color3?,
	alternateMiddleColor: Color3?,
	middleColors: { Color3 }?,

	loopsPerColor: number?,
	changeColorEveryLoops: number?,

	edgeTransparency: number?,
	middleTransparency: number?,

	segmentDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,

	colorTweenDuration: number?,
	colorEasingStyle: Enum.EasingStyle?,
	colorEasingDirection: Enum.EasingDirection?,

	phase: (() -> number)?,
	onColorChanged: ((Color3) -> ())?,
}

return {}
