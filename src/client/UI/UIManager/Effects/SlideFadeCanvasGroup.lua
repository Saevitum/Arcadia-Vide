--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.EffectTypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local function SlideFadeCanvasGroup(options: Types.SlideFadeCanvasGroupOptions)
	local duration = options.duration or 0.3
	local fadeDuration = options.fadeDuration or 0.16
	local closeFadeDuration = options.closeFadeDuration or 0.1

	local easingStyle = options.easingStyle or Enum.EasingStyle.Quad
	local easingDirection = options.easingDirection or Enum.EasingDirection.Out

	local openTransparency = options.openTransparency or 0
	local closedTransparency = options.closedTransparency or 1
	local hideWhenClosed = if options.hideWhenClosed == nil then true else options.hideWhenClosed

	return action(function(instance: Instance)
		if not instance:IsA("CanvasGroup") then
			return
		end

		local canvasGroup = instance :: CanvasGroup

		local activeTweens: { Tween } = {}
		local activeCompletedConnection: RBXScriptConnection? = nil

		local firstRun = true
		local runId = 0

		local originalStrokeTransparency: { [UIStroke]: number } = {}

		local function collectStrokes()
			for _, descendant in ipairs(canvasGroup:GetDescendants()) do
				if descendant:IsA("UIStroke") then
					local stroke = descendant :: UIStroke

					if originalStrokeTransparency[stroke] == nil then
						originalStrokeTransparency[stroke] = stroke.Transparency
					end
				end
			end
		end

		local function setStrokeTransparency(isOpen: boolean)
			collectStrokes()

			for stroke, originalTransparency in pairs(originalStrokeTransparency) do
				if stroke.Parent ~= nil then
					stroke.Transparency = if isOpen then originalTransparency else 1
				end
			end
		end

		local function cancelActiveTweens()
			for _, tween in ipairs(activeTweens) do
				tween:Cancel()
			end

			table.clear(activeTweens)

			if activeCompletedConnection ~= nil then
				activeCompletedConnection:Disconnect()
				activeCompletedConnection = nil
			end
		end

		effect(function()
			runId += 1
			local currentRunId = runId

			local isOpen = options.open()

			local targetPosition = if isOpen then options.openPosition else options.closedPosition
			local targetGroupTransparency = if isOpen then openTransparency else closedTransparency

			collectStrokes()

			if firstRun then
				firstRun = false

				canvasGroup.Position = targetPosition
				canvasGroup.GroupTransparency = targetGroupTransparency
				canvasGroup.Visible = isOpen or not hideWhenClosed

				setStrokeTransparency(isOpen)

				return
			end

			cancelActiveTweens()

			canvasGroup.Visible = true

			local positionEasingStyle = if isOpen
				then options.openEasingStyle or easingStyle
				else options.closeEasingStyle or easingStyle

			local positionEasingDirection = if isOpen
				then options.openEasingDirection or easingDirection
				else options.closeEasingDirection or easingDirection

			local fadeEasingStyle = options.fadeEasingStyle or Enum.EasingStyle.Quad
			local fadeEasingDirection = options.fadeEasingDirection or Enum.EasingDirection.Out

			local positionTweenInfo = TweenInfo.new(duration, positionEasingStyle, positionEasingDirection)

			local currentFadeDuration = if isOpen then fadeDuration else closeFadeDuration

			local fadeTweenInfo = TweenInfo.new(currentFadeDuration, fadeEasingStyle, fadeEasingDirection)

			local positionTween = TweenService:Create(canvasGroup, positionTweenInfo, {
				Position = targetPosition,
			})

			local fadeTween = TweenService:Create(canvasGroup, fadeTweenInfo, {
				GroupTransparency = targetGroupTransparency,
			})

			table.insert(activeTweens, positionTween)
			table.insert(activeTweens, fadeTween)

			for stroke, originalTransparency in pairs(originalStrokeTransparency) do
				if stroke.Parent ~= nil then
					local strokeTween = TweenService:Create(stroke, fadeTweenInfo, {
						Transparency = if isOpen then originalTransparency else 1,
					})

					table.insert(activeTweens, strokeTween)
				end
			end

			activeCompletedConnection = positionTween.Completed:Connect(function(playbackState: Enum.PlaybackState)
				if playbackState ~= Enum.PlaybackState.Completed then
					return
				end

				if currentRunId ~= runId then
					return
				end

				if not options.open() and hideWhenClosed then
					canvasGroup.Visible = false
				end
			end)

			for _, tween in ipairs(activeTweens) do
				tween:Play()
			end
		end)

		cleanup(function()
			cancelActiveTweens()
			table.clear(originalStrokeTransparency)
		end)
	end)
end

return SlideFadeCanvasGroup
