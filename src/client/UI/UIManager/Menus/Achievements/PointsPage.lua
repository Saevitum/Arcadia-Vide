--!strict

local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type PointsPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function PointsPage(props: PointsPageProps)
	return EmptyCategoryPage("Points", props.selectedTab, 3, "Points")
end

return PointsPage
