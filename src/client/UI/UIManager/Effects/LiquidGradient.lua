--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.EffectTypes)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup

local TAU = math.pi * 2

local function LiquidGradient(options: Types.LiquidGradientOptions?)
	local duration = if options ~= nil and options.duration ~= nil then math.max(options.duration, 0.05) else 4
	local primaryColor = if options ~= nil and options.primaryColor ~= nil
		then options.primaryColor
		else Color3.fromRGB(0, 255, 238)
	local secondaryColor = if options ~= nil and options.secondaryColor ~= nil
		then options.secondaryColor
		else Color3.fromRGB(255, 0, 255)
	local disabledColor = if options ~= nil and options.disabledColor ~= nil
		then options.disabledColor
		else Color3.fromRGB(55, 60, 70)

	return action(function(instance: Instance)
		if not instance:IsA("UIGradient") then
			return
		end

		local gradient = instance :: UIGradient
		local startTime = os.clock()

		gradient.Offset = Vector2.new(0, 0)
		gradient.Rotation = 0

		local connection = RunService.Heartbeat:Connect(function()
			if options ~= nil and options.enabled ~= nil and not options.enabled() then
				gradient.Color = ColorSequence.new(disabledColor)
				return
			end

			local phase = ((os.clock() - startTime) / duration) % 1
			local alpha = (math.sin((phase * TAU) - (math.pi / 2)) + 1) / 2

			gradient.Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, primaryColor:Lerp(secondaryColor, alpha)),
				ColorSequenceKeypoint.new(1, secondaryColor:Lerp(primaryColor, alpha)),
			})
		end)

		cleanup(function()
			connection:Disconnect()
		end)
	end)
end

return LiquidGradient
