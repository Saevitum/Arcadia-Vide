--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Components)

local GameSettingsPage = require(script.GameSettingsPage)
local TabStrip = require(script.TabStrip)
local UserSettingsPage = require(script.UserSettingsPage)
local VolumeSettingsPage = require(script.VolumeSettingsPage)

Vide.strict = true

local create = Vide.create
local source = Vide.source

local Panel = Components.Panel

type Source<T> = Types.Source<T>
type SettingsTab = Types.SettingsTab

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

			TabStrip({
				selectedTab = selectedTab,
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
