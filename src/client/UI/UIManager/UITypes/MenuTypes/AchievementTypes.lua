--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type AchievementsMenuProps = {
	store: StoreTypes.UIStore,
}

export type AchievementCategory =
	"Money"
	| "Gems"
	| "Points"
	| "Wins"
	| "Level"
	| "Playtime"
	| "Login"
	| "Quests"
	| "SideKicks"
	| "Placeholder"

export type AchievementState = "Available" | "NotReady" | "Claimed"

return {}
