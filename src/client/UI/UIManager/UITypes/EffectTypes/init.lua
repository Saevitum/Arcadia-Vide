--!strict

local SharedTypes = require(script.Parent.SharedTypes)

local HoverScaleTypes = require(script.HoverScaleTypes)
local SpinTypes = require(script.SpinTypes)
local HoverUIScaleTypes = require(script.HoverUIScaleTypes)
local TweenGuiObjectLayoutTypes = require(script.TweenGuiObjectLayoutTypes)
local SlideFadeCanvasGroupTypes = require(script.SlideFadeCanvasGroupTypes)
local PulseDriverTypes = require(script.PulseDriverTypes)
local SweepGradientKeypointTypes = require(script.SweepGradientKeypointTypes)
local PulseGradientOffsetTypes = require(script.PulseGradientOffsetTypes)
local LiquidGradientTypes = require(script.LiquidGradientTypes)
local FadeGuiObjectTypes = require(script.FadeGuiObjectTypes)
local PulseUIScaleTypes = require(script.PulseUIScaleTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type HoverScaleOptions = HoverScaleTypes.HoverScaleOptions
export type SpinOptions = SpinTypes.SpinOptions
export type HoverUIScaleOptions = HoverUIScaleTypes.HoverUIScaleOptions
export type TweenGuiObjectLayoutBounceOptions = TweenGuiObjectLayoutTypes.TweenGuiObjectLayoutBounceOptions
export type TweenGuiObjectLayoutOptions = TweenGuiObjectLayoutTypes.TweenGuiObjectLayoutOptions
export type SlideFadeCanvasGroupOptions = SlideFadeCanvasGroupTypes.SlideFadeCanvasGroupOptions
export type PulseDriverOptions = PulseDriverTypes.PulseDriverOptions
export type SweepGradientKeypointOptions = SweepGradientKeypointTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = PulseGradientOffsetTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = LiquidGradientTypes.LiquidGradientOptions
export type FadeGuiObjectOptions = FadeGuiObjectTypes.FadeGuiObjectOptions
export type PulseUIScaleOptions = PulseUIScaleTypes.PulseUIScaleOptions

return {
	HoverScaleTypes = HoverScaleTypes,
	SpinTypes = SpinTypes,
	HoverUIScaleTypes = HoverUIScaleTypes,
	TweenGuiObjectLayoutTypes = TweenGuiObjectLayoutTypes,
	SlideFadeCanvasGroupTypes = SlideFadeCanvasGroupTypes,
	PulseDriverTypes = PulseDriverTypes,
	SweepGradientKeypointTypes = SweepGradientKeypointTypes,
	PulseGradientOffsetTypes = PulseGradientOffsetTypes,
	LiquidGradientTypes = LiquidGradientTypes,
	FadeGuiObjectTypes = FadeGuiObjectTypes,
	PulseUIScaleTypes = PulseUIScaleTypes,
}
