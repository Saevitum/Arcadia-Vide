--!strict

local SharedTypes = require(script.SharedTypes)
local DeviceTypes = require(script.DeviceTypes)
local StoreTypes = require(script.StoreTypes)
local ButtonTypes = require(script.ButtonTypes)

local ComponentTypes = require(script.ComponentTypes)
local EffectTypes = require(script.EffectTypes)
local MenuTypes = require(script.MenuTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>
export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

export type DeviceKind = DeviceTypes.DeviceKind

export type MenuId = MenuTypes.MenuId
export type UIStore = StoreTypes.UIStore

export type ButtonBarProps = ButtonTypes.ButtonBarProps
export type MenuButtonProps = ButtonTypes.MenuButtonProps
export type SideKickButtonProps = ButtonTypes.SideKickButtonProps
export type BoostersButtonProps = ButtonTypes.BoostersButtonProps
export type ActivityButtonProps = ButtonTypes.ActivityButtonProps
export type StatsButtonProps = ButtonTypes.StatsButtonProps
export type QuestsButtonProps = ButtonTypes.QuestsButtonProps
export type InventoryButtonProps = ButtonTypes.InventoryButtonProps
export type AchievementsButtonProps = ButtonTypes.AchievementsButtonProps
export type RewardsButtonProps = ButtonTypes.RewardsButtonProps
export type SettingsButtonProps = ButtonTypes.SettingsButtonProps
export type ShopButtonProps = ButtonTypes.ShopButtonProps

export type BackgroundProps = ComponentTypes.BackgroundProps
export type HeaderProps = ComponentTypes.HeaderProps
export type ExitButtonProps = ComponentTypes.ExitButtonProps
export type GridCellSizeOptions = ComponentTypes.GridCellSizeOptions

export type PanelProps = ComponentTypes.PanelProps
export type TextProps = ComponentTypes.TextProps
export type TextStrokeProps = ComponentTypes.TextStrokeProps
export type TextGradientProps = ComponentTypes.TextGradientProps

export type ImageProps = ComponentTypes.ImageProps
export type ImageStrokeProps = ComponentTypes.ImageStrokeProps
export type ImageGradientProps = ComponentTypes.ImageGradientProps

export type ScrollAreaProps = ComponentTypes.ScrollAreaProps
export type ScrollAreaPaddingProps = ComponentTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ComponentTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ComponentTypes.ScrollAreaListProps
export type ScrollAreaLayoutKind = ComponentTypes.ScrollAreaLayoutKind

export type ActionButtonProps = ComponentTypes.ActionButtonProps
export type ActionButtonVariant = ComponentTypes.ActionButtonVariant
export type GradientKeypoint = ComponentTypes.GradientKeypoint

export type SliderProps = ComponentTypes.SliderProps
export type ToggleButtonProps = ComponentTypes.ToggleButtonProps
export type ToggleSwitchProps = ComponentTypes.ToggleSwitchProps

export type HoverScaleOptions = EffectTypes.HoverScaleOptions
export type HoverUIScaleOptions = EffectTypes.HoverUIScaleOptions
export type SlideMenuOptions = EffectTypes.SlideMenuOptions
export type SpinOptions = EffectTypes.SpinOptions
export type PulseStrokeOptions = EffectTypes.PulseStrokeOptions
export type SweepGradientKeypointOptions = EffectTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = EffectTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions
export type PulseDriverOptions = EffectTypes.PulseDriverOptions
export type PulseUIScaleOptions = EffectTypes.PulseUIScaleOptions
export type FadeGuiObjectOptions = EffectTypes.FadeGuiObjectOptions
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions
export type TweenGuiObjectLayoutBounceOptions = EffectTypes.TweenGuiObjectLayoutBounceOptions
export type SlideFadeCanvasGroupOptions = EffectTypes.SlideFadeCanvasGroupOptions

export type SideKickMenuProps = MenuTypes.SideKickMenuProps
export type BoostersMenuProps = MenuTypes.BoostersMenuProps
export type ActivityMenuProps = MenuTypes.ActivityMenuProps
export type StatsMenuProps = MenuTypes.StatsMenuProps
export type QuestsMenuProps = MenuTypes.QuestsMenuProps
export type InventoryMenuProps = MenuTypes.InventoryMenuProps
export type AchievementsMenuProps = MenuTypes.AchievementsMenuProps
export type RewardsMenuProps = MenuTypes.RewardsMenuProps
export type SettingsMenuProps = MenuTypes.SettingsMenuProps
export type ShopMenuProps = MenuTypes.ShopMenuProps

export type InventoryTabId = MenuTypes.InventoryTabId
export type SkinRarity = MenuTypes.SkinRarity
export type SkinView = MenuTypes.SkinView
export type InventoryTabDefinition = MenuTypes.InventoryTabDefinition

export type SettingsTab = MenuTypes.SettingsTab
export type AchievementCategory = MenuTypes.AchievementCategory
export type AchievementState = MenuTypes.AchievementState

return {
	SharedTypes = SharedTypes,
	DeviceTypes = DeviceTypes,
	StoreTypes = StoreTypes,
	ButtonTypes = ButtonTypes,

	ComponentTypes = ComponentTypes,
	EffectTypes = EffectTypes,
	MenuTypes = MenuTypes,
}
