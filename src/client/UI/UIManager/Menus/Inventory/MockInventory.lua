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
		SkinId = "skin_cyber_runner",
		Name = "Cyber Runner",
		ImageId = "rbxassetid://13415286900",
		Rarity = "Common",
		Description = "A lightweight runner suit built for speed, agility, and clean neon movement trails.",
		Owned = true,
		Equipped = true,
		Locked = false,
	},

	{
		SkinId = "skin_neon_hacker",
		Name = "Neon Hacker",
		ImageId = "rbxassetid://13415241367",
		Rarity = "Uncommon",
		Description = "A neon-coded street outfit with reactive cyan panels and encrypted visor glow.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_void_agent",
		Name = "Void Agent",
		ImageId = "rbxassetid://14608383463",
		Rarity = "Rare",
		Description = "A dark tactical avatar prototype designed for stealth movement through Arcadia sectors.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_pulse_knight",
		Name = "Pulse Knight",
		ImageId = "rbxassetid://13414458532",
		Rarity = "Epic",
		Description = "A premium armored skin with magenta pulse lines and reinforced cyber plating.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_arc_light",
		Name = "Arc Light",
		ImageId = "rbxassetid://13414468097",
		Rarity = "Legendary",
		Description = "A radiant Arcadia champion skin powered by a high-density cyber core.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_singularity",
		Name = "Singularity",
		ImageId = "rbxassetid://13415034457",
		Rarity = "Mythic",
		Description = "A forbidden prototype that bends light around its frame and leaves unstable energy scars.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_grid_nomad",
		Name = "Grid Nomad",
		ImageId = "rbxassetid://13415286900",
		Rarity = "Common",
		Description = "A clean utility skin for new runners entering the grid for the first time.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_metro_jumper",
		Name = "Metro Jumper",
		ImageId = "rbxassetid://13415241367",
		Rarity = "Uncommon",
		Description = "A streetwear-inspired skin used by platform racers in the lower Arcadia routes.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_redline",
		Name = "Redline",
		ImageId = "rbxassetid://14608383463",
		Rarity = "Rare",
		Description = "A high-risk racing skin with red warning trims and aggressive combat-sport styling.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_starforged",
		Name = "Starforged",
		ImageId = "rbxassetid://13414458532",
		Rarity = "Epic",
		Description = "A refined space-tech skin forged for elite dashers and late-cycle progression.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_overseer",
		Name = "Overseer",
		ImageId = "rbxassetid://13414468097",
		Rarity = "Legendary",
		Description = "A commanding premium skin with heavy black plating and controlled neon emission.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_eclipse",
		Name = "Eclipse",
		ImageId = "rbxassetid://13415034457",
		Rarity = "Mythic",
		Description = "A rare eclipse-class avatar silhouette made for special events and high prestige.",
		Owned = false,
		Equipped = false,
		Locked = true,
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
