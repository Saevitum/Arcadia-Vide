--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

local action = Vide.action
local cleanup = Vide.cleanup

Vide.strict = true

export type PulseStrokeOptions = {
	colorA: Color3?,
	colorB: Color3?,
	duration: number?,
}

local function PulseStrokeColor(options: PulseStrokeOptions?)
	local resolved: PulseStrokeOptions = options or {}

	local colorA = resolved.colorA or Color3.fromRGB(255, 0, 255)
	local colorB = resolved.colorB or Color3.fromRGB(120, 1, 255)
	local duration = resolved.duration or 0.8

	return action(function(instance: Instance)
		if not instance:IsA("UIStroke") then
			return
		end

		local stroke = instance :: UIStroke

		local tweenInfo = TweenInfo.new(
			duration,
			Enum.EasingStyle.Sine,
			Enum.EasingDirection.InOut,
			-1, --  infinite
			true -- reverse (ping-pong)
		)

		local tween = TweenService:Create(stroke, tweenInfo, {
			Color = colorB,
		})

		stroke.Color = colorA
		tween:Play()

		cleanup(function()
			tween:Cancel()
		end)
	end)
end

return PulseStrokeColor
