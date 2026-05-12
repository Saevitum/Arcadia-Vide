--!strict

export type SweepGradientKeypointOptions = {
	phase: (() -> number)?,
	edgeColor: Color3?,
	middleColor: Color3?,
	alternateMiddleColor: Color3?,
	middleColors: { Color3 }?,
	onColorChanged: ((Color3) -> ())?,
	edgeTransparency: number?,
	middleTransparency: number?,
	changeColorEveryLoops: number?,
	loopsPerColor: number?,
	segmentDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	colorTweenDuration: number?,
	colorEasingStyle: Enum.EasingStyle?,
	colorEasingDirection: Enum.EasingDirection?,
}

return {}
