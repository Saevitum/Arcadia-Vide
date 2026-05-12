--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Effects = require(script.Parent.Parent.Effects)
local Layout = require(script.Parent.Parent.Layout)

Vide.strict = true
local create = Vide.create

type ExitButtonProps = Types.ExitButtonProps

local function ExitButton(props: ExitButtonProps?)
	local resolvedProps: ExitButtonProps = props or {}

	return create("ImageButton")({
		Name = "ExitButton",

		AnchorPoint = resolvedProps.anchorPoint or Vector2.new(0.5, 0.5),
		Position = resolvedProps.position or UDim2.fromScale(0.92, 0.217),
		Size = resolvedProps.size or Layout.GetExitButtonSize(),

		BackgroundTransparency = 1,
		Image = "rbxassetid://79330223886044",

		Activated = function()
			local onClick = resolvedProps.onClick

			if onClick ~= nil then
				onClick()
			end
		end,

		Effects.Spin({
			speed = 22.5,
		}),

		Effects.HoverScale({
			scale = 1.1,
			duration = 0.12,
		}),
	})
end

return ExitButton
