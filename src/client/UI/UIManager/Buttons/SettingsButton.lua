--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true
type SettingsButtonProps = Types.SettingsButtonProps

local create = Vide.create

local function SettingsButton(props: SettingsButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "SettingsButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://87462171475713",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Settings" then
				store.currentMenu(nil)
			else
				store.currentMenu("Settings")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return SettingsButton
