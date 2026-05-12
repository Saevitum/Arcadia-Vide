--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type RewardsMenuProps = {
	store: StoreTypes.UIStore,
}

export type RewardState = "Claimed" | "Locked" | "Available"

return {}
