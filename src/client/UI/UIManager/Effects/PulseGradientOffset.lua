--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local DEFAULT_MIN_OFFSET = Vector2.new(0, -0.35)
local DEFAULT_MAX_OFFSET = Vector2.new(0, 0)

local function lerpNumber(a: number, b: number, alpha: number): number
	return a + ((b - a) * alpha)
end

local function lerpVector2(a: Vector2, b: Vector2, alpha: number): Vector2
	return Vector2.new(lerpNumber(a.X, b.X, alpha), lerpNumber(a.Y, b.Y, alpha))
end

local function PulseGradientOffset(options: Types.PulseGradientOffsetOptions?)
	local minOffset = if options ~= nil and options.minOffset ~= nil then options.minOffset else DEFAULT_MIN_OFFSET

	local maxOffset = if options ~= nil and options.maxOffset ~= nil then options.maxOffset else DEFAULT_MAX_OFFSET

	return action(function(instance: Instance)
		if not instance:IsA("UIGradient") then
			return
		end

		local gradient = instance :: UIGradient

		if options ~= nil and options.phase ~= nil then
			local phaseMultiplier = if options.phaseMultiplier ~= nil then options.phaseMultiplier else 1

			effect(function()
				local rawPhase = math.clamp(options.phase(), 0, 1)
				local phase = (rawPhase * phaseMultiplier) % 1

				local alpha: number

				if phase < 0.5 then
					alpha = phase / 0.5
				else
					alpha = 1 - ((phase - 0.5) / 0.5)
				end

				gradient.Offset = lerpVector2(maxOffset, minOffset, alpha)
			end)

			return
		end

		local alive = true
		local activeTween: Tween? = nil

		local function tweenTo(offset: Vector2)
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			local tween =
				TweenService:Create(gradient, TweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
					Offset = offset,
				})

			activeTween = tween
			tween:Play()
			tween.Completed:Wait()

			if activeTween == tween then
				activeTween = nil
			end
		end

		task.spawn(function()
			while alive do
				tweenTo(minOffset)

				if not alive then
					break
				end

				tweenTo(maxOffset)
			end
		end)

		cleanup(function()
			alive = false

			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end
		end)
	end)
end

return PulseGradientOffset
