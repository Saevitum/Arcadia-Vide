--!strict

export type Requirement = {
	nodeId: string,
	minLevel: number,
}

export type NodeKind = "Group" | "Stat"

export type NodeDefinition = {
	id: string,
	kind: NodeKind,
	groupId: string,

	title: string,
	subtitle: string?,
	effectShort: string?,
	description: string?,

	maxLevel: number?,
	position: Vector2,

	-- If present, this stat renders as a mystery ? node until requirements are met.
	requires: { Requirement }?,
}

-- Flat-top hex honeycomb spacing for the current 148x148 rendered hex assets.
-- Neighbor positions are intentionally close so diagonal sides visually match.
local HX = 118
local HY = 68

-- Root category layout:
--       Economy
--  Skills     Stamina
local ECONOMY = Vector2.new(0, -HY)
local SKILLS = Vector2.new(-HX, 0)
local STAMINA = Vector2.new(HX, 0)

local nodes: { NodeDefinition } = {
	-- Category hubs. These are always visible at root.
	{
		id = "EconomyOpen",
		kind = "Group",
		groupId = "Economy",
		title = "Economy",
		subtitle = "Open",
		description = "Open the Economy tree.",
		position = ECONOMY,
	},
	{
		id = "SkillsOpen",
		kind = "Group",
		groupId = "Skills",
		title = "Skills",
		subtitle = "Open",
		description = "Open the Skills tree.",
		position = SKILLS,
	},
	{
		id = "StaminaOpen",
		kind = "Group",
		groupId = "Stamina",
		title = "Stamina",
		subtitle = "Open",
		description = "Open the Stamina tree.",
		position = STAMINA,
	},

	-- Economy cluster around EconomyOpen.
	-- First-tier known stats form a compact honeycomb around the red/yellow hub.
	{
		id = "MoneyBoost",
		kind = "Stat",
		groupId = "Economy",
		title = "Money",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Money per level.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(-HX, 0),
	},
	{
		id = "ExpBoost",
		kind = "Stat",
		groupId = "Economy",
		title = "EXP",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% EXP per level.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(-HX / 2, -HY),
	},
	{
		id = "PointsBoost",
		kind = "Stat",
		groupId = "Economy",
		title = "Points",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Points per level.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(HX / 2, -HY),
	},
	{
		id = "GemsBoost",
		kind = "Stat",
		groupId = "Economy",
		title = "Gems",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Gems per level.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(-HX / 2, HY),
	},
	{
		id = "Lucky",
		kind = "Stat",
		groupId = "Economy",
		title = "Lucky",
		effectShort = "+2%",
		description = "+2% Luck per level.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(HX / 2, HY),
	},

	-- Economy future nodes.
	-- They are visible as ? until the requirement is met, then become known Gray stat hexes.
	{
		id = "CoinIncome",
		kind = "Stat",
		groupId = "Economy",
		title = "Coin",
		subtitle = "Income",
		effectShort = "+5%",
		description = "Future economy upgrade.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(-HX * 1.5, -HY),
		requires = {
			{ nodeId = "MoneyBoost", minLevel = 1 },
		},
	},
	{
		id = "UltraLuck",
		kind = "Stat",
		groupId = "Economy",
		title = "Ultra",
		subtitle = "Luck",
		effectShort = "+5%",
		description = "Future luck upgrade.",
		maxLevel = 10,
		position = ECONOMY + Vector2.new(HX * 1.5, HY),
		requires = {
			{ nodeId = "Lucky", minLevel = 1 },
		},
	},

	-- Skills cluster around SkillsOpen.
	{
		id = "SkillHaste",
		kind = "Stat",
		groupId = "Skills",
		title = "Skill",
		subtitle = "Haste",
		effectShort = "-4%",
		description = "-4% Cooldown per level.",
		maxLevel = 10,
		position = SKILLS + Vector2.new(-HX, 0),
	},
	{
		id = "SkillPower",
		kind = "Stat",
		groupId = "Skills",
		title = "Skill",
		subtitle = "Power",
		effectShort = "+4%",
		description = "+4% Power per level.",
		maxLevel = 10,
		position = SKILLS + Vector2.new(-HX / 2, -HY),
	},
	{
		id = "SkillDuration",
		kind = "Stat",
		groupId = "Skills",
		title = "Skill",
		subtitle = "Duration",
		effectShort = "+0.5s",
		description = "+0.5 seconds Duration per level.",
		maxLevel = 10,
		position = SKILLS + Vector2.new(-HX / 2, HY),
	},
	{
		id = "SkillOverdrive",
		kind = "Stat",
		groupId = "Skills",
		title = "Skill",
		subtitle = "Overdrive",
		effectShort = "+5%",
		description = "Future skill upgrade.",
		maxLevel = 10,
		position = SKILLS + Vector2.new(-HX * 1.5, -HY),
		requires = {
			{ nodeId = "SkillPower", minLevel = 1 },
		},
	},

	-- Stamina cluster around StaminaOpen.
	{
		id = "MaxStamina",
		kind = "Stat",
		groupId = "Stamina",
		title = "Max",
		subtitle = "Stamina",
		effectShort = "+10",
		description = "+10 Max Stamina per level.",
		maxLevel = 10,
		position = STAMINA + Vector2.new(HX, 0),
	},
	{
		id = "StaminaRecovery",
		kind = "Stat",
		groupId = "Stamina",
		title = "Stamina",
		subtitle = "Regen",
		effectShort = "+1/s",
		description = "+1/sec Regen per level.",
		maxLevel = 10,
		position = STAMINA + Vector2.new(HX / 2, HY),
	},
	{
		id = "Endurance",
		kind = "Stat",
		groupId = "Stamina",
		title = "Endurance",
		effectShort = "+5%",
		description = "Future survival upgrade.",
		maxLevel = 10,
		position = STAMINA + Vector2.new(HX * 1.5, HY),
		requires = {
			{ nodeId = "MaxStamina", minLevel = 1 },
		},
	},
}

return {
	nodes = nodes,
}
