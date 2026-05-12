--!strict

local SharedTypes = require(script.SharedTypes)
local StoreTypes = require(script.StoreTypes)
local ButtonTypes = require(script.ButtonTypes)
local ComponentTypes = require(script.ComponentTypes)
local EffectTypes = require(script.EffectTypes)
local MenuTypes = require(script.MenuTypes)

export type Source = SharedTypes.Source
export type SourceOf<T> = SharedTypes.SourceOf<T>
export type Reactive = SharedTypes.Reactive
export type ReactiveOf<T> = SharedTypes.ReactiveOf<T>

export type DeviceKind = "Desktop" | "Mobile" | "Tablet" | "Console"
export type MenuId = MenuTypes.MenuId
export type UIStore = StoreTypes.UIStore
export type SettingsTab = MenuTypes.SettingsTab

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
export type AchievementCategory = MenuTypes.AchievementCategory
export type AchievementState = MenuTypes.AchievementState

export type BackgroundProps = ComponentTypes.BackgroundProps
export type ExitButtonProps = ComponentTypes.ExitButtonProps
export type HeaderProps = ComponentTypes.HeaderProps
export type PanelProps = ComponentTypes.PanelProps
export type TextProps = ComponentTypes.TextProps
export type TextGradientProps = ComponentTypes.TextGradientProps
export type TextPulseStrokeProps = ComponentTypes.TextPulseStrokeProps
export type TextStrokeProps = ComponentTypes.TextStrokeProps
export type ScrollAreaLayoutKind = ComponentTypes.ScrollAreaLayoutKind
export type ScrollAreaChildren = ComponentTypes.ScrollAreaChildren
export type ScrollAreaPaddingProps = ComponentTypes.ScrollAreaPaddingProps
export type ScrollAreaGridProps = ComponentTypes.ScrollAreaGridProps
export type ScrollAreaListProps = ComponentTypes.ScrollAreaListProps
export type ScrollAreaProps = ComponentTypes.ScrollAreaProps
export type ImageStrokeProps = ComponentTypes.ImageStrokeProps
export type ImageGradientProps = ComponentTypes.ImageGradientProps
export type ImageProps = ComponentTypes.ImageProps
export type ToggleSwitchProps = ComponentTypes.ToggleSwitchProps
export type ToggleButtonProps = ComponentTypes.ToggleButtonProps
export type SliderProps = ComponentTypes.SliderProps
export type GridCellSizeOptions = ComponentTypes.GridCellSizeOptions
export type ActionButtonVariant = ComponentTypes.ActionButtonVariant
export type ActionButtonGradientKeypoint = ComponentTypes.ActionButtonGradientKeypoint
export type ActionButtonGradientProps = ComponentTypes.ActionButtonGradientProps
export type ActionButtonProps = ComponentTypes.ActionButtonProps

export type HoverScaleOptions = EffectTypes.HoverScaleOptions
export type SpinOptions = EffectTypes.SpinOptions
export type SlideMenuOptions = EffectTypes.SlideMenuOptions
export type PulseStrokeOptions = EffectTypes.PulseStrokeOptions
export type HoverUIScaleOptions = EffectTypes.HoverUIScaleOptions
export type PulseUIScaleOptions = EffectTypes.PulseUIScaleOptions
export type TweenGuiObjectLayoutBounceOptions = EffectTypes.TweenGuiObjectLayoutBounceOptions
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions
export type SlideFadeCanvasGroupOptions = EffectTypes.SlideFadeCanvasGroupOptions
export type PulseDriverOptions = EffectTypes.PulseDriverOptions
export type SweepGradientKeypointOptions = EffectTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = EffectTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions
export type FadeGuiObjectOptions = EffectTypes.FadeGuiObjectOptions

return {
	SharedTypes = SharedTypes,
	StoreTypes = StoreTypes,
	ButtonTypes = ButtonTypes,
	ComponentTypes = ComponentTypes,
	EffectTypes = EffectTypes,
	MenuTypes = MenuTypes,
}
