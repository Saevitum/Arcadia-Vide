--!strict

export type Requirement = { nodeId: string, minLevel: number }
export type NodeKind = "Group" | "Stat" | "Mystery"
export type NodeDefinition = {
	id: string,
	kind: NodeKind,
	groupId: string?,
	title: string,
	subtitle: string?,
	description: string?,
	effectText: string?,
	maxLevel: number?,
	position: Vector2,
	visibleWhenGroupOpen: string?,
	visibleWhen: { Requirement }?,
}
export type ConnectionDefinition = { from: string, to: string }

local nodes: { NodeDefinition } = {
	{ id = "EconomyOpen", kind = "Group", groupId = "Economy", title = "Economy", subtitle = "Open", description = "Open the Economy branch.", position = Vector2.new(-430, -80) },
	{ id = "SkillsOpen", kind = "Group", groupId = "Skills", title = "Skills", subtitle = "Open", description = "Open the Skills branch.", position = Vector2.new(430, -80) },
	{ id = "StaminaOpen", kind = "Group", groupId = "Stamina", title = "Stamina", subtitle = "Open", description = "Open the Stamina branch.", position = Vector2.new(0, 270) },

	{ id = "MoneyBoost", kind = "Stat", groupId = "Economy", title = "Money", subtitle = "Boost", description = "Increase money gained.", effectText = "+3% Money per level", maxLevel = 10, position = Vector2.new(-700, -80), visibleWhenGroupOpen = "Economy" },
	{ id = "ExpBoost", kind = "Stat", groupId = "Economy", title = "EXP", subtitle = "Boost", description = "Increase experience gained.", effectText = "+3% EXP per level", maxLevel = 10, position = Vector2.new(-560, -260), visibleWhenGroupOpen = "Economy" },
	{ id = "GemsBoost", kind = "Stat", groupId = "Economy", title = "Gems", subtitle = "Boost", description = "Increase gems gained.", effectText = "+3% Gems per level", maxLevel = 10, position = Vector2.new(-560, 100), visibleWhenGroupOpen = "Economy" },
	{ id = "PointsBoost", kind = "Stat", groupId = "Economy", title = "Points", subtitle = "Boost", description = "Increase points gained.", effectText = "+3% Points per level", maxLevel = 10, position = Vector2.new(-300, -260), visibleWhenGroupOpen = "Economy" },
	{ id = "Lucky", kind = "Stat", groupId = "Economy", title = "Lucky", description = "Increase luck.", effectText = "+2% Luck per level", maxLevel = 10, position = Vector2.new(-300, 100), visibleWhenGroupOpen = "Economy" },

	{ id = "SkillHaste", kind = "Stat", groupId = "Skills", title = "Skill", subtitle = "Haste", description = "Reduce skill cooldowns.", effectText = "-4% Cooldown per level", maxLevel = 10, position = Vector2.new(700, -80), visibleWhenGroupOpen = "Skills" },
	{ id = "SkillPower", kind = "Stat", groupId = "Skills", title = "Skill", subtitle = "Power", description = "Increase skill power.", effectText = "+4% Power per level", maxLevel = 10, position = Vector2.new(560, -260), visibleWhenGroupOpen = "Skills" },
	{ id = "SkillDuration", kind = "Stat", groupId = "Skills", title = "Skill", subtitle = "Duration", description = "Increase skill duration.", effectText = "+0.5s Duration per level", maxLevel = 10, position = Vector2.new(560, 100), visibleWhenGroupOpen = "Skills" },

	{ id = "MaxStamina", kind = "Stat", groupId = "Stamina", title = "Max", subtitle = "Stamina", description = "Increase maximum stamina.", effectText = "+10 Stamina per level", maxLevel = 10, position = Vector2.new(-170, 500), visibleWhenGroupOpen = "Stamina" },
	{ id = "StaminaRecovery", kind = "Stat", groupId = "Stamina", title = "Stamina", subtitle = "Recovery", description = "Increase stamina regeneration.", effectText = "+1/sec Regen per level", maxLevel = 10, position = Vector2.new(170, 500), visibleWhenGroupOpen = "Stamina" },

	{ id = "FutureIncome", kind = "Mystery", groupId = "Economy", title = "?", description = "Unknown economy upgrade.", position = Vector2.new(-850, -260), visibleWhenGroupOpen = "Economy", visibleWhen = { { nodeId = "MoneyBoost", minLevel = 1 } } },
	{ id = "FutureLuck", kind = "Mystery", groupId = "Economy", title = "?", description = "Unknown luck upgrade.", position = Vector2.new(-160, 290), visibleWhenGroupOpen = "Economy", visibleWhen = { { nodeId = "Lucky", minLevel = 1 } } },
	{ id = "FutureSkill", kind = "Mystery", groupId = "Skills", title = "?", description = "Unknown skill upgrade.", position = Vector2.new(850, -260), visibleWhenGroupOpen = "Skills", visibleWhen = { { nodeId = "SkillPower", minLevel = 1 } } },
	{ id = "FutureSurvival", kind = "Mystery", groupId = "Stamina", title = "?", description = "Unknown survival upgrade.", position = Vector2.new(0, 710), visibleWhenGroupOpen = "Stamina", visibleWhen = { { nodeId = "MaxStamina", minLevel = 1 } } },
}

local connections: { ConnectionDefinition } = {
	{ from = "EconomyOpen", to = "MoneyBoost" }, { from = "EconomyOpen", to = "ExpBoost" }, { from = "EconomyOpen", to = "GemsBoost" }, { from = "EconomyOpen", to = "PointsBoost" }, { from = "EconomyOpen", to = "Lucky" },
	{ from = "MoneyBoost", to = "FutureIncome" }, { from = "Lucky", to = "FutureLuck" },
	{ from = "SkillsOpen", to = "SkillHaste" }, { from = "SkillsOpen", to = "SkillPower" }, { from = "SkillsOpen", to = "SkillDuration" }, { from = "SkillPower", to = "FutureSkill" },
	{ from = "StaminaOpen", to = "MaxStamina" }, { from = "StaminaOpen", to = "StaminaRecovery" }, { from = "MaxStamina", to = "FutureSurvival" },
}

return { nodes = nodes, connections = connections }
