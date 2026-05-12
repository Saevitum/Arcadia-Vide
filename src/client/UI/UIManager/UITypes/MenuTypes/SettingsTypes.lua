--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore

export type SettingsMenuProps = {
	store: UIStore,
}

export type SettingsTab = "Volume" | "User" | "Game"

return {}
