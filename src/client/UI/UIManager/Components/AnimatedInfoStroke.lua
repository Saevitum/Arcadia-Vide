--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local create = Vide.create
local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

export type ColorMode = "StartAccent" | "EdgeAccent"

export type AnimatedInfoStrokeProps = {
	name: string?,
	accentColor: () -> Color3,
	pulsePhase: (() -> number)?,

	colorMode: ColorMode?,
	whiteColor: Color3?,

	thickness: number?,
	strokeTransparency: number?,

	rotation: number?,
	gradientTransparency: NumberSequence?,

	minOffset: Vector2?,
	maxOffset: Vector2?,
	dividerCyclesPerInfoPulse: number?,

	colorTweenDuration: number?,
	colorEasingStyle: Enum.EasingStyle?,
	colorEasingDirection: Enum.EasingDirection?,
}

local DEFAULT_WHITE = Color3.fromRGB(255, 255, 255)
local DEFAULT_MIN_OFFSET = Vector2.new(0, -0.35)
local DEFAULT_MAX_OFFSET = Vector2.new(0, 0)

local DEFAULT_GRADIENT_TRANSPARENCY = NumberSequence.new({
	NumberSequenceKeypoint.new(0, 0),
	NumberSequenceKeypoint.new(0.602, 0.828),
	NumberSequenceKeypoint.new(1, 1),
})

local function lerpNumber(a: number, b: number, alpha: number): number
	return a + ((b - a) * alpha)
end

local function lerpVector2(a: Vector2, b: Vector2, alpha: number): Vector2
	return Vector2.new(
		lerpNumber(a.X, b.X, alpha),
		lerpNumber(a.Y, b.Y, alpha)
	)
end

local function phaseToPingPongAlpha(phase: number): number
	phase = phase % 1

	if phase < 0.5 then
		return phase / 0.5
	end

	return 1 - ((phase - 0.5) / 0.5)
end

local function buildColorSequence(colorMode: ColorMode, accentColor: Color3, whiteColor: Color3): ColorSequence
	if colorMode == "StartAccent" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, accentColor),
			ColorSequenceKeypoint.new(1, whiteColor),
		})
	end

	return ColorSequence.new({
		ColorSequenceKeypoint.new(0, accentColor),
		ColorSequenceKeypoint.new(0.5, whiteColor),
		ColorSequenceKeypoint.new(1, accentColor),
	})
end

local function AnimatedInfoStrokeGradient(props: AnimatedInfoStrokeProps)
	return action(function(instance: Instance)
		if not instance:IsA("UIGradient") then
			return
		end

		local gradient = instance :: UIGradient

		local colorMode: ColorMode = if props.colorMode ~= nil then props.colorMode else "EdgeAccent"
		local whiteColor = props.whiteColor or DEFAULT_WHITE
		local colorTweenDuration = props.colorTweenDuration or 0.45
		local colorEasingStyle = props.colorEasingStyle or Enum.EasingStyle.Sine
		local colorEasingDirection = props.colorEasingDirection or Enum.EasingDirection.InOut

		local minOffset = props.minOffset or DEFAULT_MIN_OFFSET
		local maxOffset = props.maxOffset or DEFAULT_MAX_OFFSET
		local dividerCyclesPerInfoPulse = math.max(0.001, props.dividerCyclesPerInfoPulse or 3)

		local alive = true
		local activeColorTween: Tween? = nil

		local colorDriver = Instance.new("Color3Value")
		colorDriver.Name = "AnimatedInfoStrokeColorDriver"
		colorDriver.Value = props.accentColor()

		local function applyColor(color: Color3)
			if not alive then
				return
			end

			gradient.Color = buildColorSequence(colorMode, color, whiteColor)
		end

		applyColor(colorDriver.Value)

		local colorConnection = colorDriver:GetPropertyChangedSignal("Value"):Connect(function()
			applyColor(colorDriver.Value)
		end)

		local function cancelColorTween()
			if activeColorTween ~= nil then
				activeColorTween:Cancel()
				activeColorTween = nil
			end
		end

		-- Smoothly follow divider accent color changes.
		effect(function()
			local targetColor = props.accentColor()

			if not alive then
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
		end)

		-- Slow info-frame offset pulse. With dividerCyclesPerInfoPulse = 3:
		-- divider cycles 3 times while the info border completes 1 full ping-pong pulse.
		local phaseSource = props.pulsePhase

		if phaseSource ~= nil then
			local lastRawPhase = math.clamp(phaseSource(), 0, 1)
			local completedDividerCycles = 0

			effect(function()
				local rawPhase = math.clamp(phaseSource(), 0, 1)

				if rawPhase < lastRawPhase then
					completedDividerCycles += 1
				end

				lastRawPhase = rawPhase

				local infoPhase = (completedDividerCycles + rawPhase) / dividerCyclesPerInfoPulse
				local alpha = phaseToPingPongAlpha(infoPhase)

				gradient.Offset = lerpVector2(maxOffset, minOffset, alpha)
			end)
		end

		cleanup(function()
			alive = false
			cancelColorTween()
			colorConnection:Disconnect()
			colorDriver:Destroy()
		end)
	end)
end

local function AnimatedInfoStroke(props: AnimatedInfoStrokeProps)
	local colorMode: ColorMode = if props.colorMode ~= nil then props.colorMode else "EdgeAccent"
	local whiteColor = props.whiteColor or DEFAULT_WHITE
	local gradientTransparency = props.gradientTransparency or DEFAULT_GRADIENT_TRANSPARENCY
	local maxOffset = props.maxOffset or DEFAULT_MAX_OFFSET

	return create("UIStroke")({
		Name = props.name or "AnimatedInfoStroke",
		Color = whiteColor,
		Thickness = props.thickness or 2,
		Transparency = props.strokeTransparency or 0,

		create("UIGradient")({
			Rotation = props.rotation or 90,
			Offset = maxOffset,
			Color = buildColorSequence(colorMode, props.accentColor(), whiteColor),
			Transparency = gradientTransparency,

			AnimatedInfoStrokeGradient(props),
		}),
	})
end

return AnimatedInfoStroke
