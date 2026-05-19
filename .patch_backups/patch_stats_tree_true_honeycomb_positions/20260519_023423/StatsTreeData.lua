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

local nodes: { NodeDefinition } = {
	-- Category hubs. These are always available at the root view.
	-- Honeycomb triangle:
	-- Economy = top, Skills = bottom-left, Stamina = bottom-right.
	{
		id = "EconomyOpen",
		kind = "Group",
		groupId = "Economy",
		title = "Economy",
		subtitle = "Open",
		description = "Open the Economy tree.",
		position = Vector2.new(0, -135),
	},
	{
		id = "SkillsOpen",
		kind = "Group",
		groupId = "Skills",
		title = "Skills",
		subtitle = "Open",
		description = "Open the Skills tree.",
		position = Vector2.new(-78, 0),
	},
	{
		id = "StaminaOpen",
		kind = "Group",
		groupId = "Stamina",
		title = "Stamina",
		subtitle = "Open",
		description = "Open the Stamina tree.",
		position = Vector2.new(78, 0),
	},

	-- Economy: first-tier nodes are known immediately after opening Economy.
	{
		id = "MoneyBoost",
		kind = "Stat",
		groupId = "Economy",
		title = "Money",
		subtitle = "Boost",
		effectShort = "+3%",
		description = "+3% Money per level.",
		maxLevel = 10,
		position = Vector2.new(-156, -135),
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
		position = Vector2.new(-78, -270),
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
		position = Vector2.new(78, -270),
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
		position = Vector2.new(-78, 0),
	},
	{
		id = "Lucky",
		kind = "Stat",
		groupId = "Economy",
		title = "Lucky",
		effectShort = "+2%",
		description = "+2% Luck per level.",
		maxLevel = 10,
		position = Vector2.new(78, 0),
	},

	-- Economy future nodes. They start as ? and turn into known Gray stats.
	{
		id = "CoinIncome",
		kind = "Stat",
		groupId = "Economy",
		title = "Coin",
		subtitle = "Income",
		effectShort = "+5%",
		description = "Future economy upgrade.",
		maxLevel = 10,
		position = Vector2.new(-312, -270),
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
		position = Vector2.new(234, 0),
		requires = {
			{ nodeId = "Lucky", minLevel = 1 },
		},
	},

	-- Skills.
	{
		id = "SkillHaste",
		kind = "Stat",
		groupId = "Skills",
		title = "Skill",
		subtitle = "Haste",
		effectShort = "-4%",
		description = "-4% Cooldown per level.",
		maxLevel = 10,
		position = Vector2.new(-234, 0),
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
		position = Vector2.new(-156, -135),
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
		position = Vector2.new(-156, 135),
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
		position = Vector2.new(-312, -135),
		requires = {
			{ nodeId = "SkillPower", minLevel = 1 },
		},
	},

	-- Stamina.
	{
		id = "MaxStamina",
		kind = "Stat",
		groupId = "Stamina",
		title = "Max",
		subtitle = "Stamina",
		effectShort = "+10",
		description = "+10 Max Stamina per level.",
		maxLevel = 10,
		position = Vector2.new(234, 0),
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
		position = Vector2.new(156, 135),
	},
	{
		id = "Endurance",
		kind = "Stat",
		groupId = "Stamina",
		title = "Endurance",
		effectShort = "+5%",
		description = "Future survival upgrade.",
		maxLevel = 10,
		position = Vector2.new(312, 135),
		requires = {
			{ nodeId = "MaxStamina", minLevel = 1 },
		},
	},
}

return {
	nodes = nodes,
}
