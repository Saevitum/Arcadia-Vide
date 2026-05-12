--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local function overshootUDim2(current: UDim2, target: UDim2, amount: number): UDim2
	return UDim2.new(
		target.X.Scale + ((target.X.Scale - current.X.Scale) * amount),
		target.X.Offset + math.round((target.X.Offset - current.X.Offset) * amount),

		target.Y.Scale + ((target.Y.Scale - current.Y.Scale) * amount),
		target.Y.Offset + math.round((target.Y.Offset - current.Y.Offset) * amount)
	)
end

local function shouldUseBounce(bounce: Types.TweenGuiObjectLayoutBounceOptions?, isOpen: boolean): boolean
	if bounce == nil then
		return false
	end

	if bounce.enabled == false then
		return false
	end

	if isOpen and bounce.open == false then
		return false
	end

	if not isOpen and bounce.close == false then
		return false
	end

	return true
end

local function TweenGuiObjectLayout(options: Types.TweenGuiObjectLayoutOptions)
	local duration = options.duration or 0.3

	local fallbackEasingStyle = options.easingStyle or Enum.EasingStyle.Quad
	local fallbackEasingDirection = options.easingDirection or Enum.EasingDirection.Out

	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		local guiObject = instance :: GuiObject

		local activeTweens: { Tween } = {}
		local activeCompletedConnection: RBXScriptConnection? = nil

		local firstRun = true
		local runId = 0

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

			local goal: { [string]: any } = {}
			local hasGoal = false

			if options.targetSize ~= nil then
				goal.Size = options.targetSize()
				hasGoal = true
			end

			if options.targetPosition ~= nil then
				goal.Position = options.targetPosition()
				hasGoal = true
			end

			if not hasGoal then
				return
			end

			local isOpen = if options.isOpen ~= nil then options.isOpen() else true

			if firstRun then
				firstRun = false

				if goal.Size ~= nil then
					guiObject.Size = goal.Size
				end

				if goal.Position ~= nil then
					guiObject.Position = goal.Position
				end

				return
			end

			cancelActiveTweens()

			local bounce = options.bounce

			if shouldUseBounce(bounce, isOpen) then
				local resolvedBounce = bounce :: Types.TweenGuiObjectLayoutBounceOptions

				local overshootAmount = resolvedBounce.overshoot or 0.08
				local firstDuration = resolvedBounce.firstDuration or (duration * 0.62)
				local settleDuration = resolvedBounce.settleDuration or (duration * 0.38)

				local overshootGoal: { [string]: any } = {}

				if goal.Size ~= nil then
					overshootGoal.Size = overshootUDim2(guiObject.Size, goal.Size, overshootAmount)
				end

				if goal.Position ~= nil then
					overshootGoal.Position = overshootUDim2(guiObject.Position, goal.Position, overshootAmount)
				end

				local firstTweenInfo = TweenInfo.new(
					firstDuration,
					resolvedBounce.firstEasingStyle or Enum.EasingStyle.Quad,
					resolvedBounce.firstEasingDirection or Enum.EasingDirection.Out
				)

				local settleTweenInfo = TweenInfo.new(
					settleDuration,
					resolvedBounce.settleEasingStyle or Enum.EasingStyle.Quad,
					resolvedBounce.settleEasingDirection or Enum.EasingDirection.Out
				)

				local firstTween = TweenService:Create(guiObject, firstTweenInfo, overshootGoal)
				local settleTween = TweenService:Create(guiObject, settleTweenInfo, goal)

				table.insert(activeTweens, firstTween)
				table.insert(activeTweens, settleTween)

				activeCompletedConnection = firstTween.Completed:Connect(function(playbackState: Enum.PlaybackState)
					if playbackState ~= Enum.PlaybackState.Completed then
						return
					end

					if currentRunId ~= runId then
						return
					end

					settleTween:Play()
				end)

				firstTween:Play()
				return
			end

			local easingStyle = if isOpen
				then options.openEasingStyle or fallbackEasingStyle
				else options.closeEasingStyle or fallbackEasingStyle

			local easingDirection = if isOpen
				then options.openEasingDirection or fallbackEasingDirection
				else options.closeEasingDirection or fallbackEasingDirection

			local tween = TweenService:Create(guiObject, TweenInfo.new(duration, easingStyle, easingDirection), goal)

			table.insert(activeTweens, tween)
			tween:Play()
		end)

		cleanup(function()
			cancelActiveTweens()
		end)
	end)
end

return TweenGuiObjectLayout
