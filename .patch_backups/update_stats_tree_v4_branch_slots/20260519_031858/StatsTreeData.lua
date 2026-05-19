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

-- Full-step honeycomb spacing for the current 148x148 rendered hex assets.
-- These are the same offsets that make the 3 root category hubs line up correctly.
local HEX_DX = 118
local HEX_DY = 68

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

local function P(origin: Vector2, x: number, y: number): Vector2
	return origin + Vector2.new(x * HEX_DX, y * HEX_DY)
end

local function step(origin: Vector2, direction: Vector2, tier: number): Vector2
	return P(origin, direction.X * tier, direction.Y * tier)
end

-- Root category hubs:
--          Economy
--     Skills      Stamina
local ECONOMY = Vector2.new(0, -HEX_DY)
local SKILLS = Vector2.new(-HEX_DX, 0)
local STAMINA = Vector2.new(HEX_DX, 0)

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
	-- Economy branches.
	{
		groupId = "Economy",
		branchId = "MoneyBoost",
		title = "Money",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Money per tier.",
		origin = ECONOMY,
		direction = Vector2.new(-2, 0),
	},
	{
		groupId = "Economy",
		branchId = "ExpBoost",
		title = "EXP",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% EXP per tier.",
		origin = ECONOMY,
		direction = Vector2.new(-1, -1),
	},
	{
		groupId = "Economy",
		branchId = "PointsBoost",
		title = "Points",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Points per tier.",
		origin = ECONOMY,
		direction = Vector2.new(1, -1),
	},
	{
		groupId = "Economy",
		branchId = "GemsBoost",
		title = "Gems",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Gems per tier.",
		origin = ECONOMY,
		direction = Vector2.new(-1, 1),
	},
	{
		groupId = "Economy",
		branchId = "Lucky",
		title = "Lucky",
		effectShort = "+2%",
		description = "+2% Luck per tier.",
		origin = ECONOMY,
		direction = Vector2.new(1, 1),
	},

	-- Skills branches.
	{
		groupId = "Skills",
		branchId = "SkillHaste",
		title = "Skill",
		subtitle = "Haste",
		effectShort = "-4%",
		description = "-4% Cooldown per tier.",
		origin = SKILLS,
		direction = Vector2.new(-2, 0),
	},
	{
		groupId = "Skills",
		branchId = "SkillPower",
		title = "Skill",
		subtitle = "Power",
		effectShort = "+4%",
		description = "+4% Power per tier.",
		origin = SKILLS,
		direction = Vector2.new(-1, -1),
	},
	{
		groupId = "Skills",
		branchId = "SkillDuration",
		title = "Skill",
		subtitle = "Duration",
		effectShort = "+0.5s",
		description = "+0.5 seconds Duration per tier.",
		origin = SKILLS,
		direction = Vector2.new(-1, 1),
	},

	-- Stamina branches.
	{
		groupId = "Stamina",
		branchId = "MaxStamina",
		title = "Max",
		subtitle = "Stamina",
		effectShort = "+10",
		description = "+10 Max Stamina per tier.",
		origin = STAMINA,
		direction = Vector2.new(2, 0),
	},
	{
		groupId = "Stamina",
		branchId = "StaminaRecovery",
		title = "Stamina",
		subtitle = "Regen",
		effectShort = "+1/s",
		description = "+1/sec Regen per tier.",
		origin = STAMINA,
		direction = Vector2.new(1, 1),
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
			position = step(branch.origin, branch.direction, tier),
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
