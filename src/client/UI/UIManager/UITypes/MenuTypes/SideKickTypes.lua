--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type UIStore = StoreTypes.UIStore

export type SideKickMenuProps = {
	store: UIStore,
}

export type SideKickRarity =
	"Common"
	| "Uncommon"
	| "Rare"
	| "Epic"
	| "Legendary"
	| "Mythic"

export type SideKickType = "Passive" | "Active"

export type SideKickView = {
	SideKickId: string,
	Name: string,
	Description: string,
	Rarity: SideKickRarity,
	Type: SideKickType,
	ImageId: string,
	TransparentImageId: string?,
	ModelPath: string?,
	Skill: string?,
	BasePower: number,
	VirtualMachine: string?,
}

return {}
