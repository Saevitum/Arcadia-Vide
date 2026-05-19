--!strict

export type NodeKind = "Group" | "Stat"

export type NodeDefinition = {
	id: string,
	kind: NodeKind,
	groupId: string,

	title: string,
	subtitle: string?,
	effectShort: string?,
	description: string?,

	position: Vector2,

	-- Tier branch metadata. Stat nodes are generated from BranchDefinition.
	branchId: string?,
	tier: number?,
	maxTier: number?,
}

type BranchDefinition = {
	groupId: string,
	branchId: string,

	title: string,
	subtitle: string?,
	effectShort: string,
	description: string,

	origin: Vector2,
	direction: Vector2,
	maxTier: number?,
}

-- Change this later if the stat cap changes.
local MAX_TIER = 10

-- Visual honeycomb spacing for the current 148x148 rendered hex assets.
--
-- The category root triangle already looked correct with:
--   Economy -> Skills  = SW
--   Economy -> Stamina = SE
--
-- Branches use the same neighbor slots around their category hub.
-- Horizontal branches need their own spacing so they do not feel too far away.
local DIAGONAL_X = 118
local DIAGONAL_Y = 68
local HORIZONTAL_X = 180

local DIRECTIONS = {
	NW = Vector2.new(-DIAGONAL_X, -DIAGONAL_Y),
	NE = Vector2.new(DIAGONAL_X, -DIAGONAL_Y),
	W = Vector2.new(-HORIZONTAL_X, 0),
	E = Vector2.new(HORIZONTAL_X, 0),
	SW = Vector2.new(-DIAGONAL_X, DIAGONAL_Y),
	SE = Vector2.new(DIAGONAL_X, DIAGONAL_Y),
}

local ROMAN: { [number]: string } = {
	[1] = "I",
	[2] = "II",
	[3] = "III",
	[4] = "IV",
	[5] = "V",
	[6] = "VI",
	[7] = "VII",
	[8] = "VIII",
	[9] = "IX",
	[10] = "X",
}

local function roman(value: number): string
	return ROMAN[value] or tostring(value)
end

local function branchPosition(origin: Vector2, direction: Vector2, tier: number): Vector2
	return origin + (direction * tier)
end

-- Root category hubs:
--          Economy
--     Skills      Stamina
local ECONOMY = Vector2.new(0, -DIAGONAL_Y)
local SKILLS = ECONOMY + DIRECTIONS.SW
local STAMINA = ECONOMY + DIRECTIONS.SE

local nodes: { NodeDefinition } = {
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
}

local branches: { BranchDefinition } = {
	-- ============================================================
	-- ECONOMY
	-- First-tier subtypes populate the ring around Economy.
	-- Each subtype then continues outward from that ring slot.
	-- ============================================================
	{
		groupId = "Economy",
		branchId = "MoneyBoost",
		title = "Money",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Money per tier.",
		origin = ECONOMY,
		direction = DIRECTIONS.W,
	},
	{
		groupId = "Economy",
		branchId = "ExpBoost",
		title = "EXP",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% EXP per tier.",
		origin = ECONOMY,
		direction = DIRECTIONS.NW,
	},
	{
		groupId = "Economy",
		branchId = "PointsBoost",
		title = "Points",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Points per tier.",
		origin = ECONOMY,
		direction = DIRECTIONS.NE,
	},
	{
		groupId = "Economy",
		branchId = "GemsBoost",
		title = "Gems",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Gems per tier.",
		origin = ECONOMY,
		direction = DIRECTIONS.SW,
	},
	{
		groupId = "Economy",
		branchId = "Lucky",
		title = "Lucky",
		effectShort = "+2%",
		description = "+2% Luck per tier.",
		origin = ECONOMY,
		direction = DIRECTIONS.SE,
	},

	-- ============================================================
	-- SKILLS
	-- First-tier subtypes populate slots around Skills.
	-- ============================================================
	{
		groupId = "Skills",
		branchId = "SkillHaste",
		title = "Skill",
		subtitle = "Haste",
		effectShort = "-4%",
		description = "-4% Cooldown per tier.",
		origin = SKILLS,
		direction = DIRECTIONS.W,
	},
	{
		groupId = "Skills",
		branchId = "SkillPower",
		title = "Skill",
		subtitle = "Power",
		effectShort = "+4%",
		description = "+4% Power per tier.",
		origin = SKILLS,
		direction = DIRECTIONS.NW,
	},
	{
		groupId = "Skills",
		branchId = "SkillDuration",
		title = "Skill",
		subtitle = "Duration",
		effectShort = "+0.5s",
		description = "+0.5 seconds Duration per tier.",
		origin = SKILLS,
		direction = DIRECTIONS.SW,
	},

	-- ============================================================
	-- STAMINA
	-- Only two current subtype branches, but still uses ring slots.
	-- ============================================================
	{
		groupId = "Stamina",
		branchId = "MaxStamina",
		title = "Max",
		subtitle = "Stamina",
		effectShort = "+10",
		description = "+10 Max Stamina per tier.",
		origin = STAMINA,
		direction = DIRECTIONS.E,
	},
	{
		groupId = "Stamina",
		branchId = "StaminaRecovery",
		title = "Stamina",
		subtitle = "Regen",
		effectShort = "+1/s",
		description = "+1/sec Regen per tier.",
		origin = STAMINA,
		direction = DIRECTIONS.SE,
	},
}

for _, branch in ipairs(branches) do
	local maxTier = branch.maxTier or MAX_TIER

	for tier = 1, maxTier do
		local tierRoman = roman(tier)

		table.insert(nodes, {
			id = branch.branchId .. "_" .. tostring(tier),
			kind = "Stat",
			groupId = branch.groupId,
			title = branch.title,
			subtitle = if branch.subtitle ~= nil then branch.subtitle .. " " .. tierRoman else tierRoman,
			effectShort = branch.effectShort,
			description = branch.description,
			position = branchPosition(branch.origin, branch.direction, tier),
			branchId = branch.branchId,
			tier = tier,
			maxTier = maxTier,
		})
	end
end

return {
	nodes = nodes,
	maxTier = MAX_TIER,
}
