--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Style = require(script.Parent.Parent.Parent.Style)
local SettingsPage = require(script.Parent.SettingsPage)
local ToggleSettingRow = require(script.Parent.ToggleSettingRow)

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type GameSettingsPageProps = {
	selectedTab: Source<SettingsTab>,
	hidePopups: Source<boolean>,
	disableVFX: Source<boolean>,
	disableCameraShake: Source<boolean>,
}

local GAME_TOGGLE_LAYOUT = Style.Controls.Settings.Layouts.GameToggleRow

local function GameSettingsPage(props: GameSettingsPageProps)
	return SettingsPage({
		tab = "Game",
		selectedTab = props.selectedTab,
		layoutOrder = 3,
		zIndex = 20,
		children = {
			ToggleSettingRow({ name = "HidePopupsRow", label = "Hide Popups", description = "Reduce non-critical popup messages.", value = props.hidePopups, layoutOrder = 1, zIndex = 24, layout = GAME_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "DisableVFXRow", label = "Disable VFX", description = "Reduce visual effects intensity.", value = props.disableVFX, layoutOrder = 2, zIndex = 24, layout = GAME_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "DisableCameraShakeRow", label = "Disable Camera Shake", description = "Turn off camera shake effects.", value = props.disableCameraShake, layoutOrder = 3, zIndex = 24, layout = GAME_TOGGLE_LAYOUT }),
		},
	})
end

return GameSettingsPage
