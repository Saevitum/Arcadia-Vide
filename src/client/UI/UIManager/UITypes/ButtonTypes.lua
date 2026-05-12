--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local StoreTypes = require(script.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore
export type MenuId = MenuIdTypes.MenuId

export type ButtonBarProps = {
	store: UIStore,
}

export type MenuButtonProps = {
	store: UIStore,
	layoutOrder: number?,
}

export type SideKickButtonProps = MenuButtonProps
export type BoostersButtonProps = MenuButtonProps
export type ActivityButtonProps = MenuButtonProps
export type StatsButtonProps = MenuButtonProps
export type QuestsButtonProps = MenuButtonProps
export type InventoryButtonProps = MenuButtonProps
export type AchievementsButtonProps = MenuButtonProps
export type RewardsButtonProps = MenuButtonProps
export type SettingsButtonProps = MenuButtonProps
export type ShopButtonProps = MenuButtonProps

return {}
