--!strict

export type SlideFadeCanvasGroupOptions = {
	open: () -> boolean,
	openPosition: UDim2,
	closedPosition: UDim2,
	openTransparency: number?,
	closedTransparency: number?,
	duration: number?,
	fadeDuration: number?,
	closeFadeDuration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	openEasingStyle: Enum.EasingStyle?,
	openEasingDirection: Enum.EasingDirection?,
	closeEasingStyle: Enum.EasingStyle?,
	closeEasingDirection: Enum.EasingDirection?,
	fadeEasingStyle: Enum.EasingStyle?,
	fadeEasingDirection: Enum.EasingDirection?,
	hideWhenClosed: boolean?,
}

return {}
