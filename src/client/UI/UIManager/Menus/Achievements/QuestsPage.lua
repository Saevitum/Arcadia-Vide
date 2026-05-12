--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type QuestsPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function QuestsPage(props: QuestsPageProps)
	return EmptyCategoryPage("Quests", props.selectedTab, 8, "Quests")
end

return QuestsPage
