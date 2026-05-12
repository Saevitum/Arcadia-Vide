--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.MenuIdTypes)

local SideKickTypes = require(script.SideKickTypes)
local BoostersTypes = require(script.BoostersTypes)
local ActivityTypes = require(script.ActivityTypes)
local StatsTypes = require(script.StatsTypes)
local QuestsTypes = require(script.QuestsTypes)
local InventoryTypes = require(script.InventoryTypes)
local AchievementTypes = require(script.AchievementTypes)
local RewardsTypes = require(script.RewardsTypes)
local SettingsTypes = require(script.SettingsTypes)
local ShopTypes = require(script.ShopTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>

export type MenuId = MenuIdTypes.MenuId

export type SideKickMenuProps = SideKickTypes.SideKickMenuProps
export type BoostersMenuProps = BoostersTypes.BoostersMenuProps
export type ActivityMenuProps = ActivityTypes.ActivityMenuProps
export type StatsMenuProps = StatsTypes.StatsMenuProps
export type QuestsMenuProps = QuestsTypes.QuestsMenuProps
export type InventoryMenuProps = InventoryTypes.InventoryMenuProps
export type AchievementsMenuProps = AchievementTypes.AchievementsMenuProps
export type RewardsMenuProps = RewardsTypes.RewardsMenuProps
export type SettingsMenuProps = SettingsTypes.SettingsMenuProps
export type ShopMenuProps = ShopTypes.ShopMenuProps

export type SettingsTab = SettingsTypes.SettingsTab
export type InventoryTabId = InventoryTypes.InventoryTabId
export type SkinRarity = InventoryTypes.SkinRarity
export type SkinItem = InventoryTypes.SkinItem
export type AchievementCategory = AchievementTypes.AchievementCategory

return {
	MenuIdTypes = MenuIdTypes,

	SideKickTypes = SideKickTypes,
	BoostersTypes = BoostersTypes,
	ActivityTypes = ActivityTypes,
	StatsTypes = StatsTypes,
	QuestsTypes = QuestsTypes,
	InventoryTypes = InventoryTypes,
	AchievementTypes = AchievementTypes,
	RewardsTypes = RewardsTypes,
	SettingsTypes = SettingsTypes,
	ShopTypes = ShopTypes,
}
