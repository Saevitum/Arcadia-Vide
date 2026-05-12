--!strict

local StoreTypes = require(script.Parent.StoreTypes)

export type UIStore = StoreTypes.UIStore

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
