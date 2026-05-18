--!strict

local ComponentTypes = require(script.Parent.Parent.Parent.UITypes.ComponentTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)

export type InventoryTabId = MenuTypes.InventoryTabId
export type SkinItem = MenuTypes.SkinItem
export type SkinRarity = MenuTypes.SkinRarity
export type InventoryTabDefinition = ComponentTypes.TabDefinition<InventoryTabId>

local MockInventory = {}

local TABS: { InventoryTabDefinition } = {
	{
		id = "Skins",
		label = "SKINS",
		layoutOrder = 1,
		disabled = false,
		hasAlert = false,
	},

	{
		id = "Ranks",
		label = "RANKS",
		layoutOrder = 2,
		disabled = false,
		hasAlert = false,
	},

	{
		id = "Quests",
		label = "QUESTS",
		layoutOrder = 3,
		disabled = false,
		hasAlert = false,
	},
}

MockInventory.TABS = TABS

local SKINS: { SkinItem } = {
	{
		SkinId = "Astronaut",
		Name = "Astronaut",
		Description = "",
		Rarity = "Legendary",
		ImageId = "rbxassetid://129333345351079",
		IconImageId = "rbxassetid://129333345351079",
		PreviewImageId = "rbxassetid://129333345351079",
		Collection = "NPCSkins",
		ModelPath = { "NPCSkins", "MainHub", "Astronaut" },
		Price = nil,
		Enabled = true,
		ShopVisible = false,
		OwnedByDefault = false,
		Owned = true,
		Equipped = true,
		Locked = false,
	},
	{
		SkinId = "MurderKitten",
		Name = "MurderKitten",
		Description = "",
		Rarity = "Legendary",
		ImageId = "rbxassetid://80395771208314",
		IconImageId = "rbxassetid://80395771208314",
		PreviewImageId = "rbxassetid://80395771208314",
		Collection = "NPCSkins",
		ModelPath = { "NPCSkins", "MainHub", "MurderKitten" },
		Price = nil,
		Enabled = true,
		ShopVisible = false,
		OwnedByDefault = false,
		Owned = true,
		Equipped = false,
		Locked = false,
	},
	{
		SkinId = "Cat",
		Name = "Cat",
		Description = "",
		Rarity = "Legendary",
		ImageId = "rbxassetid://76904147821003",
		IconImageId = "rbxassetid://76904147821003",
		PreviewImageId = "rbxassetid://76904147821003",
		Collection = "NPCSkins",
		ModelPath = { "NPCSkins", "MainHub", "Cat" },
		Price = nil,
		Enabled = true,
		ShopVisible = false,
		OwnedByDefault = false,
		Owned = true,
		Equipped = false,
		Locked = false,
	},
	{
		SkinId = "Chef",
		Name = "Chef",
		Description = "",
		Rarity = "Legendary",
		ImageId = "rbxassetid://127883244163109",
		IconImageId = "rbxassetid://127883244163109",
		PreviewImageId = "rbxassetid://127883244163109",
		Collection = "NPCSkins",
		ModelPath = { "NPCSkins", "MainHub", "Chef" },
		Price = nil,
		Enabled = true,
		ShopVisible = false,
		OwnedByDefault = false,
		Owned = true,
		Equipped = false,
		Locked = false,
	},
	{
		SkinId = "Overclock",
		Name = "Overclock",
		Description = "",
		Rarity = "Legendary",
		ImageId = "rbxassetid://138789250340947",
		IconImageId = "rbxassetid://138789250340947",
		PreviewImageId = "rbxassetid://138789250340947",
		Collection = "NPCSkins",
		ModelPath = { "NPCSkins", "MainHub", "Overclock" },
		Price = nil,
		Enabled = true,
		ShopVisible = false,
		OwnedByDefault = false,
		Owned = true,
		Equipped = false,
		Locked = false,
	},
	{
		SkinId = "Professor",
		Name = "Professor",
		Description = "",
		Rarity = "Legendary",
		ImageId = "rbxassetid://84338306153696",
		IconImageId = "rbxassetid://84338306153696",
		PreviewImageId = "rbxassetid://84338306153696",
		Collection = "NPCSkins",
		ModelPath = { "NPCSkins", "MainHub", "Professor" },
		Price = nil,
		Enabled = true,
		ShopVisible = false,
		OwnedByDefault = false,
		Owned = true,
		Equipped = false,
		Locked = false,
	},
}

MockInventory.SKINS = SKINS

function MockInventory.getDefaultSkin(): SkinItem?
	return SKINS[1]
end

function MockInventory.getDefaultEquippedSkinId(): string?
	for _, skin in ipairs(SKINS) do
		if skin.Equipped then
			return skin.SkinId
		end
	end

	return nil
end

function MockInventory.findSkinById(skinId: string): SkinItem?
	for _, skin in ipairs(SKINS) do
		if skin.SkinId == skinId then
			return skin
		end
	end

	return nil
end

return MockInventory
