--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true
type ActivityButtonProps = Types.ActivityButtonProps

local create = Vide.create

local function ActivityButton(props: ActivityButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "ActivityButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://83551560338748",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Activity" then
				store.currentMenu(nil)
			else
				store.currentMenu("Activity")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return ActivityButton
