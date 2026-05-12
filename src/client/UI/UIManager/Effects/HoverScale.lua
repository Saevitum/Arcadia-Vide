--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Types = require(script.Parent.Parent.UITypes)
local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true
local action = Vide.action
local cleanup = Vide.cleanup

local function scaleUDim2(size: UDim2, scale: number): UDim2
	return UDim2.new(size.X.Scale * scale, size.X.Offset * scale, size.Y.Scale * scale, size.Y.Offset * scale)
end

local function HoverScale(options: Types.HoverScaleOptions?)
	local resolvedOptions: Types.HoverScaleOptions = options or {}

	local scale: number = resolvedOptions.scale or 1.1
	local duration: number = resolvedOptions.duration or 0.12
	local easingStyle: Enum.EasingStyle = resolvedOptions.easingStyle or Enum.EasingStyle.Quad
	local easingDirection: Enum.EasingDirection = resolvedOptions.easingDirection or Enum.EasingDirection.Out

	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		local gui = instance :: GuiObject

		local originalSize: UDim2 = gui.Size
		local hoverSize: UDim2 = scaleUDim2(originalSize, scale)

		local activeTween: Tween? = nil

		local function tweenTo(targetSize: UDim2)
			if activeTween ~= nil then
				activeTween:Cancel()
			end

			local tween = TweenService:Create(gui, TweenInfo.new(duration, easingStyle, easingDirection), {
				Size = targetSize,
			})

			activeTween = tween
			tween:Play()
		end

		local enterConn = gui.MouseEnter:Connect(function()
			tweenTo(hoverSize)
		end)

		local leaveConn = gui.MouseLeave:Connect(function()
			tweenTo(originalSize)
		end)

		cleanup(function()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			enterConn:Disconnect()
			leaveConn:Disconnect()
		end)
	end)
end

return HoverScale
