--!strict

local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local MockAchievements = require(script.Parent.MockAchievements)
local EmptyCategoryPage = require(script.Parent.EmptyCategoryPage)

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type LoginPageProps = {
	selectedTab: Source<AchievementCategory>,
}

local function LoginPage(props: LoginPageProps)
	return EmptyCategoryPage("Login", props.selectedTab, 7, "Login")
end

return LoginPage
