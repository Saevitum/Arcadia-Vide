--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes.ButtonTypes)

Vide.strict = true

type BoostersButtonProps = Types.BoostersButtonProps

local create = Vide.create

local function BoostersButton(props: BoostersButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "BoostersButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://124776708759760",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Boosters" then
				store.currentMenu(nil)
			else
				store.currentMenu("Boosters")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return BoostersButton
