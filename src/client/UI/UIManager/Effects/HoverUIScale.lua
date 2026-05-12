--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Types = require(script.Parent.Parent.UITypes)
local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup

type TextConstraintState = {
	constraint: UITextSizeConstraint,
	maxTextSize: number,
}

local function findOrCreateUIScale(gui: GuiObject): UIScale
	local existing = gui:FindFirstChild("HoverUIScale")

	if existing ~= nil and existing:IsA("UIScale") then
		return existing
	end

	local uiScale = Instance.new("UIScale")
	uiScale.Name = "HoverUIScale"
	uiScale.Scale = 1
	uiScale.Parent = gui

	return uiScale
end

local function HoverUIScale(options: Types.HoverUIScaleOptions?)
	local resolvedOptions: Types.HoverUIScaleOptions = options or {}

	local idleScale = resolvedOptions.idleScale or 1
	local hoverScale = resolvedOptions.hoverScale or 1.06
	local scaleTextConstraints = resolvedOptions.scaleTextConstraints or false

	local duration = resolvedOptions.duration or 0.12
	local easingStyle = resolvedOptions.easingStyle or Enum.EasingStyle.Quad
	local easingDirection = resolvedOptions.easingDirection or Enum.EasingDirection.Out

	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		local gui = instance :: GuiObject
		local uiScale = findOrCreateUIScale(gui)

		local activeTween: Tween? = nil
		local activeTextTweens: { Tween } = {}
		local textConstraints: { TextConstraintState } = {}
		local descendantAddedConn: RBXScriptConnection? = nil

		local function addTextConstraint(descendant: Instance)
			if not scaleTextConstraints then
				return
			end

			if not descendant:IsA("UITextSizeConstraint") then
				return
			end

			local constraint = descendant :: UITextSizeConstraint

			for _, state in ipairs(textConstraints) do
				if state.constraint == constraint then
					return
				end
			end

			table.insert(textConstraints, {
				constraint = constraint,
				maxTextSize = constraint.MaxTextSize,
			})
		end

		if scaleTextConstraints then
			for _, descendant in ipairs(gui:GetDescendants()) do
				addTextConstraint(descendant)
			end

			descendantAddedConn = gui.DescendantAdded:Connect(addTextConstraint)
		end

		local function tweenTo(targetScale: number)
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			for _, tween in ipairs(activeTextTweens) do
				tween:Cancel()
			end

			table.clear(activeTextTweens)

			local tweenInfo = TweenInfo.new(duration, easingStyle, easingDirection)
			local textScale = if idleScale ~= 0 then targetScale / idleScale else targetScale

			local tween = TweenService:Create(uiScale, tweenInfo, {
				Scale = targetScale,
			})

			activeTween = tween
			tween:Play()

			for _, state in ipairs(textConstraints) do
				local textTween = TweenService:Create(state.constraint, tweenInfo, {
					MaxTextSize = state.maxTextSize * textScale,
				})

				table.insert(activeTextTweens, textTween)
				textTween:Play()
			end
		end

		local enterConn = gui.MouseEnter:Connect(function()
			tweenTo(hoverScale)
		end)

		local leaveConn = gui.MouseLeave:Connect(function()
			tweenTo(idleScale)
		end)

		cleanup(function()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			for _, tween in ipairs(activeTextTweens) do
				tween:Cancel()
			end

			table.clear(activeTextTweens)

			for _, state in ipairs(textConstraints) do
				state.constraint.MaxTextSize = state.maxTextSize
			end

			if descendantAddedConn ~= nil then
				descendantAddedConn:Disconnect()
				descendantAddedConn = nil
			end

			enterConn:Disconnect()
			leaveConn:Disconnect()
		end)
	end)
end

return HoverUIScale
