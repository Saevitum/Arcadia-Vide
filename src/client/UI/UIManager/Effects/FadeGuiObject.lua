--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local function FadeGuiObject(options: Types.FadeGuiObjectOptions)
	local duration = options.duration or 0.18
	local openDuration = options.openDuration or duration
	local closeDuration = options.closeDuration or duration

	local easingStyle = options.easingStyle or Enum.EasingStyle.Quad
	local easingDirection = options.easingDirection or Enum.EasingDirection.Out

	local openTransparency = options.openTransparency or 0
	local closedTransparency = options.closedTransparency or 1

	local hideWhenClosed = if options.hideWhenClosed == nil then true else options.hideWhenClosed

	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		local guiObject = instance :: GuiObject

		local activeTween: Tween? = nil
		local activeCompletedConnection: RBXScriptConnection? = nil
		local firstRun = true
		local runId = 0

		local function cancelActiveTween()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			if activeCompletedConnection ~= nil then
				activeCompletedConnection:Disconnect()
				activeCompletedConnection = nil
			end
		end

		effect(function()
			runId += 1
			local currentRunId = runId

			local isOpen = options.open()
			local targetTransparency = if isOpen then openTransparency else closedTransparency
			local tweenDuration = if isOpen then openDuration else closeDuration

			if firstRun then
				firstRun = false

				guiObject.BackgroundTransparency = targetTransparency
				guiObject.Visible = isOpen or not hideWhenClosed

				return
			end

			cancelActiveTween()

			guiObject.Visible = true

			local tween = TweenService:Create(guiObject, TweenInfo.new(tweenDuration, easingStyle, easingDirection), {
				BackgroundTransparency = targetTransparency,
			})

			activeTween = tween

			activeCompletedConnection = tween.Completed:Connect(function(playbackState: Enum.PlaybackState)
				if playbackState ~= Enum.PlaybackState.Completed then
					return
				end

				if currentRunId ~= runId then
					return
				end

				if not options.open() and hideWhenClosed then
					guiObject.Visible = false
				end
			end)

			tween:Play()
		end)

		cleanup(function()
			cancelActiveTween()
		end)
	end)
end

return FadeGuiObject
