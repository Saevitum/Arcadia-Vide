--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type InventoryMenuProps = {
	store: StoreTypes.UIStore,
}

export type InventoryTabId = "Skins" | "Ranks" | "Quests"

export type SkinRarity =
	"Common"
	| "Uncommon"
	| "Rare"
	| "Epic"
	| "Legendary"
	| "Mythic"

export type SkinView = {
	SkinId: string,
	Name: string,
	ImageId: string,
	Rarity: SkinRarity,
	Description: string,

	Owned: boolean,
	Equipped: boolean,
	Locked: boolean,
}

export type InventoryTabDefinition = {
	id: InventoryTabId,
	label: string,
	hasAlert: boolean?,
	layoutOrder: number,
}

return {}
