--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local MIN_KEYPOINT_TIME = 0.001
local MAX_KEYPOINT_TIME = 0.999
local CENTER_KEYPOINT_TIME = 0.5

local function phaseToMiddleTime(phase: number): number
	phase = math.clamp(phase, 0, 1)

	if phase < (1 / 3) then
		local alpha = phase / (1 / 3)
		return 0.5 + (0.5 * alpha)
	end

	if phase < (2 / 3) then
		local alpha = (phase - (1 / 3)) / (1 / 3)
		return 1 - alpha
	end

	local alpha = (phase - (2 / 3)) / (1 / 3)
	return 0 + (0.5 * alpha)
end
local function getSafeKeypointTime(value: number): number
	return math.clamp(value, MIN_KEYPOINT_TIME, MAX_KEYPOINT_TIME)
end

local function buildColorSequence(edgeColor: Color3, middleColor: Color3, middleTime: number): ColorSequence
	return ColorSequence.new({
		ColorSequenceKeypoint.new(0, edgeColor),
		ColorSequenceKeypoint.new(getSafeKeypointTime(middleTime), middleColor),
		ColorSequenceKeypoint.new(1, edgeColor),
	})
end

local function buildTransparencySequence(
	edgeTransparency: number,
	middleTransparency: number,
	middleTime: number
): NumberSequence
	return NumberSequence.new({
		NumberSequenceKeypoint.new(0, edgeTransparency),
		NumberSequenceKeypoint.new(getSafeKeypointTime(middleTime), middleTransparency),
		NumberSequenceKeypoint.new(1, edgeTransparency),
	})
end

local function SweepGradientKeypoint(options: Types.SweepGradientKeypointOptions?)
	local edgeColor = if options ~= nil and options.edgeColor ~= nil
		then options.edgeColor
		else Color3.fromRGB(255, 255, 255)

	local middleColor = if options ~= nil and options.middleColor ~= nil
		then options.middleColor
		else Color3.fromRGB(0, 229, 255)

	local alternateMiddleColor = if options ~= nil and options.alternateMiddleColor ~= nil
		then options.alternateMiddleColor
		else Color3.fromRGB(255, 0, 255)

	local middleColors = if options ~= nil
			and options.middleColors ~= nil
			and #options.middleColors > 0
		then options.middleColors
		else {
			middleColor,
			alternateMiddleColor,
			Color3.fromRGB(255, 153, 0),
		}

	local loopsPerColor = math.max(
		1,
		if options ~= nil and options.loopsPerColor ~= nil
			then options.loopsPerColor
			elseif options ~= nil and options.changeColorEveryLoops ~= nil then options.changeColorEveryLoops
			else 3
	)

	local edgeTransparency = if options ~= nil and options.edgeTransparency ~= nil then options.edgeTransparency else 1

	local middleTransparency = if options ~= nil and options.middleTransparency ~= nil
		then options.middleTransparency
		else 0

	local changeColorEveryLoops = math.max(
		1,
		if options ~= nil and options.changeColorEveryLoops ~= nil then options.changeColorEveryLoops else 3
	)

	local segmentDuration = if options ~= nil and options.segmentDuration ~= nil then options.segmentDuration else 1.2

	local easingStyle = if options ~= nil and options.easingStyle ~= nil
		then options.easingStyle
		else Enum.EasingStyle.Sine

	local easingDirection = if options ~= nil and options.easingDirection ~= nil
		then options.easingDirection
		else Enum.EasingDirection.InOut

	local colorTweenDuration = if options ~= nil and options.colorTweenDuration ~= nil
		then options.colorTweenDuration
		else 0.45

	local colorEasingStyle = if options ~= nil and options.colorEasingStyle ~= nil
		then options.colorEasingStyle
		else Enum.EasingStyle.Sine

	local colorEasingDirection = if options ~= nil and options.colorEasingDirection ~= nil
		then options.colorEasingDirection
		else Enum.EasingDirection.InOut

	return action(function(instance: Instance)
		if not instance:IsA("UIGradient") then
			return
		end

		local gradient = instance :: UIGradient

		local timeDriver = Instance.new("NumberValue")
		timeDriver.Name = "SweepGradientTimeDriver"
		timeDriver.Value = CENTER_KEYPOINT_TIME

		local colorDriver = Instance.new("Color3Value")
		colorDriver.Name = "SweepGradientColorDriver"
		colorDriver.Value = middleColor

		local alive = true
		local activeTimeTween: Tween? = nil
		local activeColorTween: Tween? = nil

		local function applyGradient()
			if not alive then
				return
			end

			local middleTime = timeDriver.Value
			local currentMiddleColor = colorDriver.Value

			if options ~= nil and options.onColorChanged ~= nil then
				options.onColorChanged(currentMiddleColor)
			end

			gradient.Color = buildColorSequence(edgeColor, currentMiddleColor, middleTime)
			gradient.Transparency = buildTransparencySequence(edgeTransparency, middleTransparency, middleTime)
		end

		local timeChangedConnection = timeDriver:GetPropertyChangedSignal("Value"):Connect(applyGradient)
		local colorChangedConnection = colorDriver:GetPropertyChangedSignal("Value"):Connect(applyGradient)

		local function cancelTimeTween()
			if activeTimeTween ~= nil then
				activeTimeTween:Cancel()
				activeTimeTween = nil
			end
		end

		local function cancelColorTween()
			if activeColorTween ~= nil then
				activeColorTween:Cancel()
				activeColorTween = nil
			end
		end

		local function tweenTimeTo(targetValue: number): boolean
			if not alive then
				return false
			end

			cancelTimeTween()

			local tween =
				TweenService:Create(timeDriver, TweenInfo.new(segmentDuration, easingStyle, easingDirection), {
					Value = targetValue,
				})

			activeTimeTween = tween
			tween:Play()

			local playbackState = tween.Completed:Wait()

			if activeTimeTween == tween then
				activeTimeTween = nil
			end

			return alive and playbackState == Enum.PlaybackState.Completed
		end

		local function startColorTweenTo(targetColor: Color3)
			if not alive then
				return
			end

			if colorDriver.Value == targetColor then
				return
			end

			cancelColorTween()

			local tween = TweenService:Create(
				colorDriver,
				TweenInfo.new(colorTweenDuration, colorEasingStyle, colorEasingDirection),
				{
					Value = targetColor,
				}
			)

			activeColorTween = tween
			tween:Play()
		end

		if options ~= nil and options.phase ~= nil then
			local lastPhase = options.phase()
			local completedLoops = 0
			local currentColorIndex = 1

			colorDriver.Value = middleColors[currentColorIndex]
			applyGradient()

			effect(function()
				local phase = math.clamp(options.phase(), 0, 1)

				-- Detect phase reset: 1 -> 0 means one divider cycle completed.
				if phase < lastPhase then
					completedLoops += 1

					if completedLoops % loopsPerColor == 0 then
						currentColorIndex += 1

						if currentColorIndex > #middleColors then
							currentColorIndex = 1
						end

						startColorTweenTo(middleColors[currentColorIndex])
					end
				end

				lastPhase = phase

				timeDriver.Value = phaseToMiddleTime(phase)
			end)

			cleanup(function()
				alive = false

				cancelTimeTween()
				cancelColorTween()

				timeChangedConnection:Disconnect()
				colorChangedConnection:Disconnect()

				timeDriver:Destroy()
				colorDriver:Destroy()
			end)

			return
		end

		task.spawn(function()
			local completedLoops = 0
			local currentColorIndex = 1

			colorDriver.Value = middleColors[currentColorIndex]
			applyGradient()

			while alive do
				if not tweenTimeTo(MAX_KEYPOINT_TIME) then
					break
				end

				if not tweenTimeTo(MIN_KEYPOINT_TIME) then
					break
				end

				completedLoops += 1

				if completedLoops % loopsPerColor == 0 then
					currentColorIndex += 1

					if currentColorIndex > #middleColors then
						currentColorIndex = 1
					end

					startColorTweenTo(middleColors[currentColorIndex])
				end

				if not tweenTimeTo(CENTER_KEYPOINT_TIME) then
					break
				end
			end
		end)

		cleanup(function()
			alive = false

			cancelTimeTween()
			cancelColorTween()

			timeChangedConnection:Disconnect()
			colorChangedConnection:Disconnect()

			timeDriver:Destroy()
			colorDriver:Destroy()
		end)
	end)
end

return SweepGradientKeypoint
