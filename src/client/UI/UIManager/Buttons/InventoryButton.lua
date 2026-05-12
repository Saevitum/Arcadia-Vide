--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes.ButtonTypes)

Vide.strict = true
type InventoryButtonProps = Types.InventoryButtonProps

local create = Vide.create

local function InventoryButton(props: InventoryButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "InventoryButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://74412862253699",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Inventory" then
				store.currentMenu(nil)
			else
				store.currentMenu("Inventory")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return InventoryButton
