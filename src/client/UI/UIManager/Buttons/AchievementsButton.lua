--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true
type AchievementsButtonProps = Types.AchievementsButtonProps

local create = Vide.create

local function AchievementsButton(props: AchievementsButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "AchievementsButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://138929566469644",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Achievements" then
				store.currentMenu(nil)
			else
				store.currentMenu("Achievements")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return AchievementsButton
