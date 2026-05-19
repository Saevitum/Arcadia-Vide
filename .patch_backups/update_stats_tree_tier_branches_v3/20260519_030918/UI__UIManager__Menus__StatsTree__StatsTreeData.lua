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

-- Full-step honeycomb spacing for the current 148x148 rendered hex assets.
-- The important rule:
--   diagonal neighbors use the SAME offset as the working root layout.
--
-- Root layout:
--          Economy
--     Skills      Stamina
--
-- If the global gap needs tuning, adjust only these two values.
local HEX_DX = 118
local HEX_DY = 68

local function P(origin: Vector2, x: number, y: number): Vector2
	return origin + Vector2.new(x * HEX_DX, y * HEX_DY)
end

-- Root category hubs.
local ECONOMY = Vector2.new(0, -HEX_DY)
local SKILLS = Vector2.new(-HEX_DX, 0)
local STAMINA = Vector2.new(HEX_DX, 0)

local nodes: { NodeDefinition } = {
	-- ============================================================
	-- ROOT CATEGORY HUBS
	-- ============================================================
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
	-- ECONOMY BRANCH
	-- Same full honeycomb neighbor pattern around EconomyOpen:
	--              EXP       Points
	--       Money     Economy
	--              Gems      Lucky
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
		position = P(ECONOMY, -2, 0),
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
		position = P(ECONOMY, -1, -1),
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
		position = P(ECONOMY, 1, -1),
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
		position = P(ECONOMY, -1, 1),
	},
	{
		id = "Lucky",
		kind = "Stat",
		groupId = "Economy",
		title = "Lucky",
		effectShort = "+2%",
		description = "+2% Luck per level.",
		maxLevel = 10,
		position = P(ECONOMY, 1, 1),
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
		position = P(ECONOMY, -3, -1),
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
		position = P(ECONOMY, 2, 2),
		requires = {
			{ nodeId = "Lucky", minLevel = 1 },
		},
	},

	-- ============================================================
	-- SKILLS BRANCH
	-- Uses the same full honeycomb offsets around SkillsOpen.
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
		position = P(SKILLS, -2, 0),
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
		position = P(SKILLS, -1, -1),
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
		position = P(SKILLS, -1, 1),
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
		position = P(SKILLS, -3, -1),
		requires = {
			{ nodeId = "SkillPower", minLevel = 1 },
		},
	},

	-- ============================================================
	-- STAMINA BRANCH
	-- Uses the same full honeycomb offsets around StaminaOpen.
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
		position = P(STAMINA, 2, 0),
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
		position = P(STAMINA, 1, 1),
	},
	{
		id = "Endurance",
		kind = "Stat",
		groupId = "Stamina",
		title = "Endurance",
		effectShort = "+5%",
		description = "Future survival upgrade.",
		maxLevel = 10,
		position = P(STAMINA, 3, 1),
		requires = {
			{ nodeId = "MaxStamina", minLevel = 1 },
		},
	},
}

return {
	nodes = nodes,
}
