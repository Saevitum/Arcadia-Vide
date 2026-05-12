--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type SettingsMenuProps = {
	store: StoreTypes.UIStore,
}

export type SettingsTab = "Volume" | "User" | "Game"

return {}
