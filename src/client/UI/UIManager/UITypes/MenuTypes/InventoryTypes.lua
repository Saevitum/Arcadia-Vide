--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type Source<T> = SharedTypes.Source<T>
export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore

export type InventoryMenuProps = {
	store: UIStore,
}

export type InventoryTabId = "Skins" | "Ranks" | "Quests"

export type SkinRarity =
	"Common"
	| "Uncommon"
	| "Rare"
	| "Epic"
	| "Legendary"
	| "Mythic"

export type SkinItem = {
	SkinId: string,
	Name: string,
	ImageId: string,
	Rarity: SkinRarity,
	Description: string,
	Owned: boolean,
	Equipped: boolean,
	Locked: boolean,
}

return {}
