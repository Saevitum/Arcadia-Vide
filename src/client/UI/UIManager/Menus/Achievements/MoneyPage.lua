--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)

local MockAchievements = require(script.Parent.MockAchievements)
local AchievementPage = require(script.Parent.AchievementPage)
local AchievementRow = require(script.Parent.AchievementRow)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory
type MockAchievement = MockAchievements.MockAchievement

export type MoneyPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function MoneyPage(props: MoneyPageProps)
	local rows: { Instance } = {}

	for index, achievement in ipairs(MockAchievements.BY_CATEGORY.Money) do
		table.insert(
			rows,
			AchievementRow({
				achievement = achievement,
				layoutOrder = index,
				zIndex = 24,

				onCollect = function(collected: MockAchievement)
					print(`Achievement collect clicked: {collected.Id}`)
				end,
			})
		)
	end

	return AchievementPage({
		tab = "Money",
		selectedTab = props.selectedTab,
		layoutOrder = 1,
		zIndex = 20,
		children = rows,
	})
end

return MoneyPage
