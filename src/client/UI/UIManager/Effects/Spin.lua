--!strict

local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Types = require(script.Parent.Parent.UITypes.EffectTypes)
local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup

local function Spin(options: Types.SpinOptions?)
	local resolvedOptions: Types.SpinOptions = options or {}
	local speed: number = resolvedOptions.speed or 180

	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		local guiObject = instance :: GuiObject

		local connection = RunService.RenderStepped:Connect(function(dt: number)
			guiObject.Rotation = (guiObject.Rotation + dt * speed) % 360
		end)

		cleanup(function()
			connection:Disconnect()
		end)
	end)
end

return Spin
