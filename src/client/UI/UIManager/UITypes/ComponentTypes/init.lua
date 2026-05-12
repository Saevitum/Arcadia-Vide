--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local PanelTypes = require(script.PanelTypes)
local TextTypes = require(script.TextTypes)
local ImageTypes = require(script.ImageTypes)
local ScrollAreaTypes = require(script.ScrollAreaTypes)
local ActionButtonTypes = require(script.ActionButtonTypes)
local InputTypes = require(script.InputTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type BackgroundProps = PanelTypes.BackgroundProps
export type ExitButtonProps = PanelTypes.ExitButtonProps
export type HeaderProps = PanelTypes.HeaderProps
export type PanelProps = PanelTypes.PanelProps

export type TextGradientProps = TextTypes.TextGradientProps
export type TextPulseStrokeProps = TextTypes.TextPulseStrokeProps
export type TextStrokeProps = TextTypes.TextStrokeProps
export type TextProps = TextTypes.TextProps

export type ImageStrokeProps = ImageTypes.ImageStrokeProps
export type ImageGradientProps = ImageTypes.ImageGradientProps
export type ImageProps = ImageTypes.ImageProps

export type ScrollAreaLayoutKind = ScrollAreaTypes.ScrollAreaLayoutKind
export type ScrollAreaChildren = ScrollAreaTypes.ScrollAreaChildren
export type ScrollAreaPaddingProps = ScrollAreaTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ScrollAreaTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ScrollAreaTypes.ScrollAreaListProps
export type GridCellSizeOptions = ScrollAreaTypes.GridCellSizeOptions
export type ScrollAreaProps = ScrollAreaTypes.ScrollAreaProps

export type ActionButtonVariant = ActionButtonTypes.ActionButtonVariant
export type ActionButtonGradientKeypoint = ActionButtonTypes.ActionButtonGradientKeypoint
export type ActionButtonGradientProps = ActionButtonTypes.ActionButtonGradientProps
export type ActionButtonProps = ActionButtonTypes.ActionButtonProps

export type ToggleSwitchProps = InputTypes.ToggleSwitchProps
export type ToggleButtonProps = InputTypes.ToggleButtonProps
export type SliderProps = InputTypes.SliderProps

return {
	PanelTypes = PanelTypes,
	TextTypes = TextTypes,
	ImageTypes = ImageTypes,
	ScrollAreaTypes = ScrollAreaTypes,
	ActionButtonTypes = ActionButtonTypes,
	InputTypes = InputTypes,
}
