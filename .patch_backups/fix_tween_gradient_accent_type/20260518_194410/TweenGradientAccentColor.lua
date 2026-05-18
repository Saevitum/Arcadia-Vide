--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

export type TweenGradientAccentColorOptions = {
	accentColor: () -> Color3,
	mode: "StartAccent" | "EdgeAccent"?,
	whiteColor: Color3?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

local DEFAULT_WHITE = Color3.fromRGB(255, 255, 255)

local function buildColorSequence(mode: "StartAccent" | "EdgeAccent", accentColor: Color3, whiteColor: Color3): ColorSequence
	if mode == "EdgeAccent" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, accentColor),
			ColorSequenceKeypoint.new(0.5, whiteColor),
			ColorSequenceKeypoint.new(1, accentColor),
		})
	end

	return ColorSequence.new({
		ColorSequenceKeypoint.new(0, accentColor),
		ColorSequenceKeypoint.new(1, whiteColor),
	})
end

local function TweenGradientAccentColor(options: TweenGradientAccentColorOptions)
	local mode = options.mode or "StartAccent"
	local whiteColor = options.whiteColor or DEFAULT_WHITE
	local duration = options.duration or 0.45
	local easingStyle = options.easingStyle or Enum.EasingStyle.Sine
	local easingDirection = options.easingDirection or Enum.EasingDirection.InOut

	return action(function(instance: Instance)
		if not instance:IsA("UIGradient") then
			return
		end

		local gradient = instance :: UIGradient
		local colorDriver = Instance.new("Color3Value")
		colorDriver.Name = "TweenGradientAccentColorDriver"
		colorDriver.Value = options.accentColor()

		local alive = true
		local activeTween: Tween? = nil

		local function applyColor(color: Color3)
			gradient.Color = buildColorSequence(mode, color, whiteColor)
		end

		applyColor(colorDriver.Value)

		local connection = colorDriver:GetPropertyChangedSignal("Value"):Connect(function()
			applyColor(colorDriver.Value)
		end)

		local function cancelTween()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end
		end

		effect(function()
			local targetColor = options.accentColor()

			if not alive then
				return
			end

			cancelTween()

			local tween = TweenService:Create(
				colorDriver,
				TweenInfo.new(duration, easingStyle, easingDirection),
				{
					Value = targetColor,
				}
			)

			activeTween = tween
			tween:Play()
		end)

		cleanup(function()
			alive = false
			cancelTween()
			connection:Disconnect()
			colorDriver:Destroy()
		end)
	end)
end

return TweenGradientAccentColor
