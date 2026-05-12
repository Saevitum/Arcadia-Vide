--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Style = require(script.Parent.Parent.Parent.Style)
local SettingsPage = require(script.Parent.SettingsPage)
local ToggleSettingRow = require(script.Parent.ToggleSettingRow)

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type UserSettingsPageProps = {
	selectedTab: Source<SettingsTab>,
	hideYourRank: Source<boolean>,
	hideOthersRank: Source<boolean>,
	hideYourNameplate: Source<boolean>,
	hideOthersNameplate: Source<boolean>,
}

local USER_TOGGLE_LAYOUT = Style.Controls.Settings.Layouts.UserToggleRow

local function UserSettingsPage(props: UserSettingsPageProps)
	return SettingsPage({
		tab = "User",
		selectedTab = props.selectedTab,
		layoutOrder = 2,
		zIndex = 20,
		children = {
			ToggleSettingRow({ name = "HideYourRankRow", label = "Hide Your Rank", description = "Other players will not see your rank.", value = props.hideYourRank, layoutOrder = 1, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "HideOthersRankRow", label = "Hide Others Rank", description = "You will not see other player ranks.", value = props.hideOthersRank, layoutOrder = 2, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "HideYourNameplateRow", label = "Hide Your Nameplate", description = "Your nameplate is hidden from view.", value = props.hideYourNameplate, layoutOrder = 3, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "HideOthersNameplateRow", label = "Hide Others Nameplate", description = "You will not see other players nameplate.", value = props.hideOthersNameplate, layoutOrder = 4, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
		},
	})
end

return UserSettingsPage
