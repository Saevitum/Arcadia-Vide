--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local action = Vide.action

export type PulseUIScaleOptions = {
	enabled: boolean?,

	idleScale: number?,
	pulseScale: number?,

	period: number?,
	phaseOffset: number?,
}

local DEFAULT_IDLE_SCALE = 1
local DEFAULT_PULSE_SCALE = 1.025
local DEFAULT_PERIOD = 1.8

local TAU = math.pi * 2

local function PulseUIScale(options: PulseUIScaleOptions?)
	return action(function(instance: Instance)
		if not instance:IsA("GuiObject") then
			return
		end

		if options ~= nil and options.enabled == false then
			return
		end

		local idleScale = if options ~= nil and options.idleScale ~= nil then options.idleScale else DEFAULT_IDLE_SCALE

		local pulseScale = if options ~= nil and options.pulseScale ~= nil
			then options.pulseScale
			else DEFAULT_PULSE_SCALE

		local period = if options ~= nil and options.period ~= nil then options.period else DEFAULT_PERIOD

		local phaseOffset = if options ~= nil and options.phaseOffset ~= nil then options.phaseOffset else 0

		local existingScale = instance:FindFirstChild("PulseUIScale")

		if existingScale ~= nil then
			existingScale:Destroy()
		end

		local uiScale = Instance.new("UIScale")
		uiScale.Name = "PulseUIScale"
		uiScale.Scale = idleScale
		uiScale.Parent = instance

		local amplitude = pulseScale - idleScale
		local startTime = os.clock()

		local connection = RunService.RenderStepped:Connect(function()
			if uiScale.Parent == nil then
				return
			end

			local elapsed = os.clock() - startTime
			local phase = ((elapsed / period) + phaseOffset) * TAU

			-- 0 → 1 → 0 smooth breathing curve.
			local alpha = (math.sin(phase - (math.pi / 2)) + 1) * 0.5

			uiScale.Scale = idleScale + (amplitude * alpha)
		end)

		return function()
			connection:Disconnect()
			uiScale:Destroy()
		end
	end)
end

return PulseUIScale
