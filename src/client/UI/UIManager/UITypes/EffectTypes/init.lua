--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local FadeGuiObjectTypes = require(script.FadeGuiObjectTypes)
local HoverUIScaleTypes = require(script.HoverUIScaleTypes)
local PulseUIScaleTypes = require(script.PulseUIScaleTypes)
local SlideFadeCanvasGroupTypes = require(script.SlideFadeCanvasGroupTypes)
local SweepGradientKeypointTypes = require(script.SweepGradientKeypointTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>

export type FadeGuiObjectOptions = FadeGuiObjectTypes.FadeGuiObjectOptions
export type HoverUIScaleOptions = HoverUIScaleTypes.HoverUIScaleOptions
export type PulseUIScaleOptions = PulseUIScaleTypes.PulseUIScaleOptions
export type SlideFadeCanvasGroupOptions = SlideFadeCanvasGroupTypes.SlideFadeCanvasGroupOptions
export type SweepGradientKeypointOptions = SweepGradientKeypointTypes.SweepGradientKeypointOptions

export type HoverScaleOptions = {
	scale: number?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

export type SpinOptions = {
	speed: number?,
}

export type SlideMenuOptions = {
	open: () -> boolean,
	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	duration: number?,
}

export type PulseStrokeOptions = {
	colorA: Color3?,
	colorB: Color3?,
	duration: number?,
}

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

export type PulseGradientOffsetOptions = {
	phase: (() -> number)?,
	phaseMultiplier: number?,
	minOffset: Vector2?,
	maxOffset: Vector2?,
}

export type PulseDriverOptions = {
	phase: SourceOf<number>,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

export type LiquidGradientOptions = {
	duration: number?,
	primaryColor: Color3?,
	secondaryColor: Color3?,
	disabledColor: Color3?,
	enabled: (() -> boolean)?,
}

return {
	FadeGuiObjectTypes = FadeGuiObjectTypes,
	HoverUIScaleTypes = HoverUIScaleTypes,
	PulseUIScaleTypes = PulseUIScaleTypes,
	SlideFadeCanvasGroupTypes = SlideFadeCanvasGroupTypes,
	SweepGradientKeypointTypes = SweepGradientKeypointTypes,
}
