--!strict

local SharedTypes = require(script.SharedTypes)
local DeviceTypes = require(script.DeviceTypes)
local StoreTypes = require(script.StoreTypes)
local ButtonTypes = require(script.ButtonTypes)
local ComponentTypes = require(script.ComponentTypes)
local EffectTypes = require(script.EffectTypes)
local MenuTypes = require(script.MenuTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type DeviceKind = DeviceTypes.DeviceKind
export type UIStore = StoreTypes.UIStore
export type MenuId = MenuTypes.MenuId

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
export type ExitButtonProps = ComponentTypes.ExitButtonProps
export type HeaderProps = ComponentTypes.HeaderProps
export type PanelProps = ComponentTypes.PanelProps
export type TextProps = ComponentTypes.TextProps
export type ImageProps = ComponentTypes.ImageProps
export type ScrollAreaProps = ComponentTypes.ScrollAreaProps
export type ActionButtonProps = ComponentTypes.ActionButtonProps
export type ToggleSwitchProps = ComponentTypes.ToggleSwitchProps
export type ToggleButtonProps = ComponentTypes.ToggleButtonProps
export type SliderProps = ComponentTypes.SliderProps

export type HoverScaleOptions = EffectTypes.HoverScaleOptions
export type SpinOptions = EffectTypes.SpinOptions
export type HoverUIScaleOptions = EffectTypes.HoverUIScaleOptions
export type TweenGuiObjectLayoutBounceOptions = EffectTypes.TweenGuiObjectLayoutBounceOptions
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions
export type SlideFadeCanvasGroupOptions = EffectTypes.SlideFadeCanvasGroupOptions
export type PulseDriverOptions = EffectTypes.PulseDriverOptions
export type SweepGradientKeypointOptions = EffectTypes.SweepGradientKeypointOptions
export type PulseGradientOffsetOptions = EffectTypes.PulseGradientOffsetOptions
export type LiquidGradientOptions = EffectTypes.LiquidGradientOptions
export type FadeGuiObjectOptions = EffectTypes.FadeGuiObjectOptions
export type PulseUIScaleOptions = EffectTypes.PulseUIScaleOptions

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
export type SettingsTab = MenuTypes.SettingsTab
export type InventoryTabId = MenuTypes.InventoryTabId
export type SkinRarity = MenuTypes.SkinRarity
export type SkinItem = MenuTypes.SkinItem
export type AchievementCategory = MenuTypes.AchievementCategory

return {
	SharedTypes = SharedTypes,
	DeviceTypes = DeviceTypes,
	StoreTypes = StoreTypes,
	ButtonTypes = ButtonTypes,
	ComponentTypes = ComponentTypes,
	EffectTypes = EffectTypes,
	MenuTypes = MenuTypes,
}
