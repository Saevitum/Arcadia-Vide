--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Effects)
local Types = require(script.Parent.Parent.UITypes.ButtonTypes)

Vide.strict = true
type QuestsButtonProps = Types.QuestsButtonProps

local create = Vide.create

local function QuestsButton(props: QuestsButtonProps)
	local store = props.store

	return create("ImageButton")({
		Name = "QuestsButton",
		LayoutOrder = props.layoutOrder or 1,

		Size = UDim2.fromScale(0.08, 1),

		BackgroundTransparency = 1,
		Image = "rbxassetid://112007764203708",

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
		}),

		Activated = function()
			if store.currentMenu() == "Quests" then
				store.currentMenu(nil)
			else
				store.currentMenu("Quests")
			end
		end,

		Effects.HoverScale({
			scale = 1.12,
			duration = 0.12,
		}),
	})
end

return QuestsButton
