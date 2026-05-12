--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true
type StatsButtonProps = Types.StatsButtonProps

local create = Vide.create

local function StatsButton(props: StatsButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "StatsButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://91694042782086",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Stats" then
				store.currentMenu(nil)
			else
				store.currentMenu("Stats")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return StatsButton
