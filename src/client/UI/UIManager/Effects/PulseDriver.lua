--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.EffectTypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup

local function PulseDriver(options: Types.PulseDriverOptions)
	local duration = options.duration or 1.2
	local easingStyle = options.easingStyle or Enum.EasingStyle.Sine
	local easingDirection = options.easingDirection or Enum.EasingDirection.InOut

	return action(function(_instance: Instance)
		local driver = Instance.new("NumberValue")
		driver.Name = "PulseDriver"
		driver.Value = 0

		local alive = true
		local activeTween: Tween? = nil

		local connection = driver:GetPropertyChangedSignal("Value"):Connect(function()
			options.phase(driver.Value)
		end)

		local function cancelTween()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end
		end

		local function tweenTo(value: number): boolean
			if not alive then
				return false
			end

			cancelTween()

			local tween = TweenService:Create(driver, TweenInfo.new(duration, easingStyle, easingDirection), {
				Value = value,
			})

			activeTween = tween
			tween:Play()

			local playbackState = tween.Completed:Wait()

			if activeTween == tween then
				activeTween = nil
			end

			return alive and playbackState == Enum.PlaybackState.Completed
		end

		task.spawn(function()
			options.phase(0)

			while alive do
				driver.Value = 0
				options.phase(0)

				if not tweenTo(1) then
					break
				end
			end
		end)

		cleanup(function()
			alive = false
			cancelTween()
			connection:Disconnect()
			driver:Destroy()
		end)
	end)
end

return PulseDriver
