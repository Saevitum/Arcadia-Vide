--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type LevelPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function LevelPage(props: LevelPageProps)
	return EmptyCategoryPage("Level", props.selectedTab, 5, "Level")
end

return LevelPage
