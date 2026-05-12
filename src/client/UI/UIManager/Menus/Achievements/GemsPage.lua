--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type GemsPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function GemsPage(props: GemsPageProps)
	return EmptyCategoryPage("Gems", props.selectedTab, 2, "Gems")
end

return GemsPage
