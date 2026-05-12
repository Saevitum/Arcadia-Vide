--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type WinsPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function WinsPage(props: WinsPageProps)
	return EmptyCategoryPage("Wins", props.selectedTab, 4, "Wins")
end

return WinsPage
