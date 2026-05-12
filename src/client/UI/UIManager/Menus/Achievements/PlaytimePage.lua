--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type PlaytimePageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function PlaytimePage(props: PlaytimePageProps)
	return EmptyCategoryPage("Playtime", props.selectedTab, 6, "Playtime")
end

return PlaytimePage
