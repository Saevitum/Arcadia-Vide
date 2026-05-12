--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes.ButtonTypes)

Vide.strict = true
type ShopButtonProps = Types.ShopButtonProps

local create = Vide.create

local function ShopButton(props: ShopButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "ShopButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://87927985019199",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Shop" then
				store.currentMenu(nil)
			else
				store.currentMenu("Shop")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return ShopButton
