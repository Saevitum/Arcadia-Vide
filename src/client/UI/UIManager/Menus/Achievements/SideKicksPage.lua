--!strict

local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type SideKicksPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function SideKicksPage(props: SideKicksPageProps)
	return EmptyCategoryPage("SideKicks", props.selectedTab, 9, "SideKicks")
end

return SideKicksPage
