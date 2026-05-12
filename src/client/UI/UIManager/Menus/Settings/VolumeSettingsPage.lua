--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local SettingsPage = require(script.Parent.SettingsPage)
local VolumeSettingRow = require(script.Parent.VolumeSettingRow)

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type VolumeSettingsPageProps = {
	selectedTab: Source<SettingsTab>,
	masterVolume: Source<number>,
	sfxVolume: Source<number>,
	musicVolume: Source<number>,
	masterMuted: Source<boolean>,
	sfxMuted: Source<boolean>,
	musicMuted: Source<boolean>,
}

local function VolumeSettingsPage(props: VolumeSettingsPageProps)
	return SettingsPage({
		tab = "Volume",
		selectedTab = props.selectedTab,
		layoutOrder = 1,
		zIndex = 20,
		children = {
			VolumeSettingRow({ name = "MasterVolumeRow", label = "Master Volume", description = "Controls every sound in the game.", value = props.masterVolume, muted = props.masterMuted, layoutOrder = 1, zIndex = 24 }),
			VolumeSettingRow({ name = "SFXVolumeRow", label = "SFX Volume", description = "Controls interface and gameplay sounds.", value = props.sfxVolume, muted = props.sfxMuted, layoutOrder = 2, zIndex = 24 }),
			VolumeSettingRow({ name = "MusicVolumeRow", label = "Music Volume", description = "Controls background music.", value = props.musicVolume, muted = props.musicMuted, layoutOrder = 3, zIndex = 24 }),
		},
	})
end

return VolumeSettingsPage
