--!strict

export type FadeGuiObjectOptions = {
	open: () -> boolean,
	openTransparency: number?,
	closedTransparency: number?,
	duration: number?,
	openDuration: number?,
	closeDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	hideWhenClosed: boolean?,
}

return {}
