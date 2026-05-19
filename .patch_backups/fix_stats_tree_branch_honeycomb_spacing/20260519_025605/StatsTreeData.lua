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

-- Flat-top hex honeycomb spacing.
-- Adjust these two values only if you want the global gap tighter or wider.
local HEX_STEP_X = 118
local HEX_STEP_Y = 68

-- Build a consistent honeycomb lattice.
-- Basis vectors:
--   east      = ( HEX_STEP_X, 0 )
--   southEast = ( HEX_STEP_X/2, HEX_STEP_Y )
-- This lets every node live on the same hex grid.
local function H(origin: Vector2, q: number, r: number): Vector2
	return origin + Vector2.new(
		(q * HEX_STEP_X) + (r * (HEX_STEP_X / 2)),
		r * HEX_STEP_Y
	)
end

-- Root layout:
--          Economy
--     Skills      Stamina
--
-- These are already in honeycomb relation and now ALL child nodes follow the same system.
local ECONOMY = Vector2.new(0, -HEX_STEP_Y)
local SKILLS = Vector2.new(-HEX_STEP_X, 0)
local STAMINA = Vector2.new(HEX_STEP_X, 0)

local nodes: { NodeDefinition } = {
	-- Root category hubs.
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

	-- ============================================================
	-- ECONOMY BRANCH (all nodes on same honeycomb lattice)
	-- ============================================================
	{
		id = "MoneyBoost",
		kind = "Stat",
		groupId = "Economy",
		title = "Money",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Money per level.",
		maxLevel = 10,
		position = H(ECONOMY, -1, 0),
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
		position = H(ECONOMY, 0, -1),
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
		position = H(ECONOMY, 1, -1),
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
		position = H(ECONOMY, -1, 1),
	},
	{
		id = "Lucky",
		kind = "Stat",
		groupId = "Economy",
		title = "Lucky",
		effectShort = "+2%",
		description = "+2% Luck per level.",
		maxLevel = 10,
		position = H(ECONOMY, 0, 1),
	},
	{
		id = "CoinIncome",
		kind = "Stat",
		groupId = "Economy",
		title = "Coin",
		subtitle = "Income",
		effectShort = "+5%",
		description = "Future economy upgrade.",
		maxLevel = 10,
		position = H(ECONOMY, -2, 0),
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
		position = H(ECONOMY, 0, 2),
		requires = {
			{ nodeId = "Lucky", minLevel = 1 },
		},
	},

	-- ============================================================
	-- SKILLS BRANCH (same honeycomb structure)
	-- ============================================================
	{
		id = "SkillHaste",
		kind = "Stat",
		groupId = "Skills",
		title = "Skill",
		subtitle = "Haste",
		effectShort = "-4%",
		description = "-4% Cooldown per level.",
		maxLevel = 10,
		position = H(SKILLS, -1, 0),
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
		position = H(SKILLS, 0, -1),
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
		position = H(SKILLS, -1, 1),
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
		position = H(SKILLS, -1, -1),
		requires = {
			{ nodeId = "SkillPower", minLevel = 1 },
		},
	},

	-- ============================================================
	-- STAMINA BRANCH (same honeycomb structure)
	-- ============================================================
	{
		id = "MaxStamina",
		kind = "Stat",
		groupId = "Stamina",
		title = "Max",
		subtitle = "Stamina",
		effectShort = "+10",
		description = "+10 Max Stamina per level.",
		maxLevel = 10,
		position = H(STAMINA, 1, 0),
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
		position = H(STAMINA, 0, 1),
	},
	{
		id = "Endurance",
		kind = "Stat",
		groupId = "Stamina",
		title = "Endurance",
		effectShort = "+5%",
		description = "Future survival upgrade.",
		maxLevel = 10,
		position = H(STAMINA, 1, 1),
		requires = {
			{ nodeId = "MaxStamina", minLevel = 1 },
		},
	},
}

return {
	nodes = nodes,
}
