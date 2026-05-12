--!strict

export type TweenGuiObjectLayoutBounceOptions = {
	enabled: boolean?,
	open: boolean?,
	close: boolean?,
	overshoot: number?,
	firstDuration: number?,
	settleDuration: number?,
	firstEasingStyle: Enum.EasingStyle?,
	firstEasingDirection: Enum.EasingDirection?,
	settleEasingStyle: Enum.EasingStyle?,
	settleEasingDirection: Enum.EasingDirection?,
}

export type TweenGuiObjectLayoutOptions = {
	isOpen: (() -> boolean)?,
	targetSize: (() -> UDim2)?,
	targetPosition: (() -> UDim2)?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	openEasingStyle: Enum.EasingStyle?,
	openEasingDirection: Enum.EasingDirection?,
	closeEasingStyle: Enum.EasingStyle?,
	closeEasingDirection: Enum.EasingDirection?,
	bounce: TweenGuiObjectLayoutBounceOptions?,
}

return {}
