--!strict

local ComponentTypes = require(script.Parent.Parent.Parent.UITypes.ComponentTypes)

export type AchievementCategory =
	"Money"
	| "Gems"
	| "Points"
	| "Wins"
	| "Level"
	| "Playtime"
	| "Login"
	| "Quests"
	| "SideKicks"
	| "Placeholder"

export type AchievementState = "Available" | "NotReady" | "Claimed"

export type MockAchievement = {
	Id: string,
	Category: AchievementCategory,

	Title: string,
	TaskText: string,
	ProgressText: string,

	State: AchievementState,
}

export type AchievementTabDefinition = ComponentTypes.TabDefinition<AchievementCategory>

local MockAchievements = {}

local TABS: { AchievementTabDefinition } = {
	{
		id = "Money",
		label = "Money",
		hasAlert = true,
		layoutOrder = 1,
	},
	{
		id = "Gems",
		label = "Gems",
		layoutOrder = 2,
	},
	{
		id = "Points",
		label = "Points",
		layoutOrder = 3,
	},
	{
		id = "Wins",
		label = "Wins",
		layoutOrder = 4,
	},
	{
		id = "Level",
		label = "Level",
		layoutOrder = 5,
	},
	{
		id = "Playtime",
		label = "Playtime",
		hasAlert = true,
		layoutOrder = 6,
	},
	{
		id = "Login",
		label = "Login",
		layoutOrder = 7,
	},
	{
		id = "Quests",
		label = "Quests",
		layoutOrder = 8,
	},
	{
		id = "SideKicks",
		label = "SideKicks",
		layoutOrder = 9,
	},
	{
		id = "Placeholder",
		label = "Placeholder",
		layoutOrder = 10,
	},
}

MockAchievements.TABS = TABS

MockAchievements.BY_CATEGORY = {
	Money = {
		{
			Id = "PocketChange",
			Category = "Money",
			Title = "Pocket Change",
			TaskText = "Have 5,000 Money",
			ProgressText = "5000/5000",
			State = "Available",
		},
		{
			Id = "GettingRich",
			Category = "Money",
			Title = "Getting Rich",
			TaskText = "Have 50,000 Money",
			ProgressText = "16264/50000",
			State = "NotReady",
		},
		{
			Id = "MoneyBags",
			Category = "Money",
			Title = "Money Bags",
			TaskText = "Have 500,000 Money",
			ProgressText = "16264/500000",
			State = "NotReady",
		},
		{
			Id = "Millionaire",
			Category = "Money",
			Title = "Millionaire",
			TaskText = "Have 5,000,000 Money",
			ProgressText = "16264/5000000",
			State = "NotReady",
		},
	} :: { MockAchievement },

	Gems = {} :: { MockAchievement },
	Points = {} :: { MockAchievement },
	Wins = {} :: { MockAchievement },
	Level = {} :: { MockAchievement },
	Playtime = {} :: { MockAchievement },
	Login = {} :: { MockAchievement },
	Quests = {} :: { MockAchievement },
	SideKicks = {} :: { MockAchievement },
	Placeholder = {} :: { MockAchievement },
}

return MockAchievements
