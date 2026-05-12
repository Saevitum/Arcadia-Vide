--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

local action = Vide.action
local effect = Vide.effect
local cleanup = Vide.cleanup

Vide.strict = true

export type Source<T> = (() -> T) & ((T) -> ())

export type SlideMenuOptions = {
	open: () -> boolean,
	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	duration: number?,
}

local function SlideMenu(options: SlideMenuOptions)
	local openSource = options.open

	local openPosition = options.openPosition or UDim2.fromScale(0.5, 0.5)
	local enterPosition = options.enterPosition or UDim2.fromScale(1.5, 0.5)
	local exitPosition = options.exitPosition or UDim2.fromScale(-0.5, 0.5)
	local duration = options.duration or 0.45

	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		local gui = instance :: GuiObject
		local activeTween: Tween? = nil
		local didMount = false

		gui.Visible = openSource()
		gui.Position = if openSource() then openPosition else enterPosition

		effect(function()
			local isOpen = openSource()

			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			if not didMount and not isOpen then
				gui.Visible = false
				gui.Position = enterPosition
				didMount = true
				return
			end

			didMount = true

			if isOpen then
				gui.Visible = true
				gui.Position = enterPosition
			end

			local targetPosition = if isOpen then openPosition else exitPosition

			local tween = TweenService:Create(
				gui,
				TweenInfo.new(
					duration,
					if isOpen then Enum.EasingStyle.Back else Enum.EasingStyle.Quad,
					Enum.EasingDirection.Out
				),
				{
					Position = targetPosition,
				}
			)

			activeTween = tween

			local completedConnection = tween.Completed:Connect(function(playbackState)
				if activeTween ~= tween then
					return
				end

				if playbackState == Enum.PlaybackState.Completed and not isOpen then
					gui.Visible = false
				end
			end)

			tween:Play()

			return function()
				completedConnection:Disconnect()

				if activeTween == tween then
					local tweenToCancel = activeTween
					activeTween = nil

					if tweenToCancel ~= nil then
						tweenToCancel:Cancel()
					end
				end
			end
		end)

		cleanup(function()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end
		end)
	end)
end

return SlideMenu
