--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local SharedTypes = require(script.Parent.Parent.UITypes.SharedTypes)
local ComponentTypes = require(script.Parent.Parent.UITypes.ComponentTypes)

local Components = require(script.Parent.Parent.Components)
local Tabs = require(script.Parent.Parent.Components.Tabs)
local Style = require(script.Parent.Parent.Style)

local GameSettingsPage = require(script.GameSettingsPage)
local UserSettingsPage = require(script.UserSettingsPage)
local VolumeSettingsPage = require(script.VolumeSettingsPage)

Vide.strict = true

local create = Vide.create
local source = Vide.source

local Panel = Components.Panel

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab
type TabDefinition<T> = ComponentTypes.TabDefinition<T>

local SETTINGS_TABS: { TabDefinition<SettingsTab> } = {
	{
		id = "Volume",
		label = "VOLUME",
		layoutOrder = 1,
		disabled = false,
		hasAlert = false,
	},

	{
		id = "User",
		label = "USER",
		layoutOrder = 2,
		disabled = false,
		hasAlert = false,
	},

	{
		id = "Game",
		label = "GAME",
		layoutOrder = 3,
		disabled = false,
		hasAlert = false,
	},
}

local TAB_LAYOUT = Style.Tabs.Layouts.SettingsThree
local TAB_STYLE = Style.Tabs.Presets.SettingsPink

local function SettingsMenu(props: Types.SettingsMenuProps)
	local selectedTab: Source<SettingsTab> = source("Volume" :: SettingsTab)

	local masterVolume: Source<number> = source(75)
	local sfxVolume: Source<number> = source(80)
	local musicVolume: Source<number> = source(65)

	local masterMuted: Source<boolean> = source(false)
	local sfxMuted: Source<boolean> = source(false)
	local musicMuted: Source<boolean> = source(false)

	local hideYourRank: Source<boolean> = source(false)
	local hideOthersRank: Source<boolean> = source(false)
	local hideYourNameplate: Source<boolean> = source(false)
	local hideOthersNameplate: Source<boolean> = source(false)

	local hidePopups: Source<boolean> = source(false)
	local disableVFX: Source<boolean> = source(false)
	local disableCameraShake: Source<boolean> = source(false)

	return Panel({
		name = "SettingsMenu",
		store = props.store,
		menuId = "Settings",
		title = "SETTINGS",

		content = create("Frame")({
			Name = "SettingsContent",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			Tabs.TabStrip({
				name = "SettingsTabStrip",

				tabs = SETTINGS_TABS,
				selectedTab = selectedTab,

				size = TAB_LAYOUT.size,
				position = TAB_LAYOUT.position,
				anchorPoint = TAB_LAYOUT.anchorPoint,

				cellSize = TAB_LAYOUT.cellSize,
				cellPadding = TAB_LAYOUT.cellPadding,
				fillDirectionMaxCells = TAB_LAYOUT.fillDirectionMaxCells,

				style = TAB_STYLE,
				zIndex = 21,
			}),

			VolumeSettingsPage({
				selectedTab = selectedTab,
				masterVolume = masterVolume,
				sfxVolume = sfxVolume,
				musicVolume = musicVolume,
				masterMuted = masterMuted,
				sfxMuted = sfxMuted,
				musicMuted = musicMuted,
			}),

			UserSettingsPage({
				selectedTab = selectedTab,
				hideYourRank = hideYourRank,
				hideOthersRank = hideOthersRank,
				hideYourNameplate = hideYourNameplate,
				hideOthersNameplate = hideOthersNameplate,
			}),

			GameSettingsPage({
				selectedTab = selectedTab,
				hidePopups = hidePopups,
				disableVFX = disableVFX,
				disableCameraShake = disableCameraShake,
			}),
		}),
	})
end

return SettingsMenu
