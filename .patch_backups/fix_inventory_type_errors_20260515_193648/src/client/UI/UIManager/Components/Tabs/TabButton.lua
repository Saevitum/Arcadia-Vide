--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)
local Types = require(script.Parent.Parent.Parent.UITypes.ComponentTypes)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

type TabButtonProps = Types.TabButtonProps
type TabButtonStyle = Types.TabButtonStyle
type TabVisualStateStyle = Types.TabVisualStateStyle
type Reactive = Types.Reactive

local DEFAULT_BUTTON_STYLE: TabButtonStyle = Style.Tabs.Presets.CyberDefault.button :: TabButtonStyle

local function readReactive<T>(value: Reactive?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function mergeButtonStyle(style: TabButtonStyle?): TabButtonStyle
	return Style.Tabs.merge(DEFAULT_BUTTON_STYLE, style or {}) :: TabButtonStyle
end

local function isSelected(props: TabButtonProps): boolean
	return (props.selectedTab() :: any) == (props.tab.id :: any)
end

local function isDisabled(props: TabButtonProps): boolean
	return props.tab.disabled == true
end

local function getStateStyle(
	props: TabButtonProps,
	buttonStyle: TabButtonStyle,
	hovered: Types.Source
): TabVisualStateStyle
	if isDisabled(props) then
		return buttonStyle.disabled or buttonStyle.default or {}
	end

	if isSelected(props) then
		return buttonStyle.selected or buttonStyle.default or {}
	end

	if hovered() then
		return buttonStyle.hover or buttonStyle.default or {}
	end

	return buttonStyle.default or {}
end

type ResolvedStyle = {
	backgroundColor: Color3,
	backgroundTransparency: number,
	gradient: ColorSequence,
	gradientRotation: number,
	strokeColor: Color3,
	strokeTransparency: number,
	strokeThickness: number,
	strokeGradient: ColorSequence,
	strokeGradientRotation: number,
	textColor: Color3,
	textTransparency: number,
	glossColor: Color3,
	glossBackgroundTransparency: number,
	glossTransparency: NumberSequence,
}

local function resolveStyle(style: TabVisualStateStyle, fallback: TabVisualStateStyle?): ResolvedStyle
	local fallbackStyle = fallback or {}
	local styleAny = style :: any
	local fallbackAny = fallbackStyle :: any

	return {
		backgroundColor = style.backgroundColor or fallbackStyle.backgroundColor or Color3.fromRGB(255, 255, 255),
		backgroundTransparency = if style.backgroundTransparency ~= nil then style.backgroundTransparency elseif fallbackStyle.backgroundTransparency ~= nil then fallbackStyle.backgroundTransparency else 0,
		gradient = style.gradient or fallbackStyle.gradient or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		gradientRotation = if style.gradientRotation ~= nil then style.gradientRotation elseif fallbackStyle.gradientRotation ~= nil then fallbackStyle.gradientRotation else 0,
		strokeColor = style.strokeColor or fallbackStyle.strokeColor or Color3.fromRGB(255, 255, 255),
		strokeTransparency = if style.strokeTransparency ~= nil then style.strokeTransparency elseif fallbackStyle.strokeTransparency ~= nil then fallbackStyle.strokeTransparency else 0,
		strokeThickness = if style.strokeThickness ~= nil then style.strokeThickness elseif fallbackStyle.strokeThickness ~= nil then fallbackStyle.strokeThickness else 1,
		strokeGradient = style.strokeGradient or fallbackStyle.strokeGradient or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		strokeGradientRotation = if style.strokeGradientRotation ~= nil then style.strokeGradientRotation elseif fallbackStyle.strokeGradientRotation ~= nil then fallbackStyle.strokeGradientRotation else 0,
		textColor = style.textColor or fallbackStyle.textColor or Color3.fromRGB(255, 255, 255),
		textTransparency = if style.textTransparency ~= nil then style.textTransparency elseif fallbackStyle.textTransparency ~= nil then fallbackStyle.textTransparency else 0,
		glossColor = style.glossColor or fallbackStyle.glossColor or Color3.fromRGB(255, 255, 255),
		glossBackgroundTransparency = if styleAny.glossBackgroundTransparency ~= nil then styleAny.glossBackgroundTransparency elseif fallbackAny.glossBackgroundTransparency ~= nil then fallbackAny.glossBackgroundTransparency else 0,
		glossTransparency = style.glossTransparency or fallbackStyle.glossTransparency or NumberSequence.new({
			NumberSequenceKeypoint.new(0, 1),
			NumberSequenceKeypoint.new(0.5, 0.75),
			NumberSequenceKeypoint.new(1, 0),
		}),
	}
end

local function colorAt(sequence: ColorSequence, time: number): Color3
	local keypoints = sequence.Keypoints

	if #keypoints == 0 then
		return Color3.fromRGB(255, 255, 255)
	end

	if time <= keypoints[1].Time then
		return keypoints[1].Value
	end

	for index = 2, #keypoints do
		local previous = keypoints[index - 1]
		local current = keypoints[index]

		if time <= current.Time then
			local span = current.Time - previous.Time
			local alpha = if span <= 0 then 0 else (time - previous.Time) / span
			return previous.Value:Lerp(current.Value, math.clamp(alpha, 0, 1))
		end
	end

	return keypoints[#keypoints].Value
end

local function numberAt(sequence: NumberSequence, time: number): number
	local keypoints = sequence.Keypoints

	if #keypoints == 0 then
		return 0
	end

	if time <= keypoints[1].Time then
		return keypoints[1].Value
	end

	for index = 2, #keypoints do
		local previous = keypoints[index - 1]
		local current = keypoints[index]

		if time <= current.Time then
			local span = current.Time - previous.Time
			local alpha = if span <= 0 then 0 else (time - previous.Time) / span
			return previous.Value + ((current.Value - previous.Value) * math.clamp(alpha, 0, 1))
		end
	end

	return keypoints[#keypoints].Value
end

local function collectSequenceTimes(colorA: ColorSequence?, colorB: ColorSequence?, numberA: NumberSequence?, numberB: NumberSequence?): { number }
	local times: { number } = { 0, 1 }

	local function add(time: number)
		local clamped = math.clamp(time, 0, 1)

		for _, existing in ipairs(times) do
			if math.abs(existing - clamped) < 0.001 then
				return
			end
		end

		table.insert(times, clamped)
	end

	local function addColor(sequence: ColorSequence?)
		if sequence == nil then
			return
		end

		for _, keypoint in ipairs(sequence.Keypoints) do
			add(keypoint.Time)
		end
	end

	local function addNumber(sequence: NumberSequence?)
		if sequence == nil then
			return
		end

		for _, keypoint in ipairs(sequence.Keypoints) do
			add(keypoint.Time)
		end
	end

	addColor(colorA)
	addColor(colorB)
	addNumber(numberA)
	addNumber(numberB)
	table.sort(times)

	return times
end

local function lerpColorSequence(fromSequence: ColorSequence, toSequence: ColorSequence, alpha: number): ColorSequence
	local keypoints: { ColorSequenceKeypoint } = {}

	for _, time in ipairs(collectSequenceTimes(fromSequence, toSequence, nil, nil)) do
		table.insert(keypoints, ColorSequenceKeypoint.new(time, colorAt(fromSequence, time):Lerp(colorAt(toSequence, time), alpha)))
	end

	return ColorSequence.new(keypoints)
end

local function lerpNumberSequence(fromSequence: NumberSequence, toSequence: NumberSequence, alpha: number): NumberSequence
	local keypoints: { NumberSequenceKeypoint } = {}

	for _, time in ipairs(collectSequenceTimes(nil, nil, fromSequence, toSequence)) do
		local value = numberAt(fromSequence, time) + ((numberAt(toSequence, time) - numberAt(fromSequence, time)) * alpha)
		table.insert(keypoints, NumberSequenceKeypoint.new(time, math.clamp(value, 0, 1)))
	end

	return NumberSequence.new(keypoints)
end

local function lerpNumber(fromValue: number, toValue: number, alpha: number): number
	return fromValue + ((toValue - fromValue) * alpha)
end

local function findDirectChildOfClass(parent: Instance, className: string): Instance?
	for _, child in ipairs(parent:GetChildren()) do
		if child.ClassName == className then
			return child
		end
	end

	return nil
end

local function captureStyle(button: TextButton, fallback: ResolvedStyle): ResolvedStyle
	local gradient = findDirectChildOfClass(button, "UIGradient") :: UIGradient?
	local stroke = findDirectChildOfClass(button, "UIStroke") :: UIStroke?
	local strokeGradient: UIGradient? = if stroke ~= nil then stroke:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local gloss = button:FindFirstChild("Gloss") :: Frame?
	local glossGradient: UIGradient? = if gloss ~= nil then gloss:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local label = button:FindFirstChild("Label") :: TextLabel?

	return {
		backgroundColor = button.BackgroundColor3,
		backgroundTransparency = button.BackgroundTransparency,
		gradient = if gradient ~= nil then gradient.Color else fallback.gradient,
		gradientRotation = if gradient ~= nil then gradient.Rotation else fallback.gradientRotation,
		strokeColor = if stroke ~= nil then stroke.Color else fallback.strokeColor,
		strokeTransparency = if stroke ~= nil then stroke.Transparency else fallback.strokeTransparency,
		strokeThickness = if stroke ~= nil then stroke.Thickness else fallback.strokeThickness,
		strokeGradient = if strokeGradient ~= nil then strokeGradient.Color else fallback.strokeGradient,
		strokeGradientRotation = if strokeGradient ~= nil then strokeGradient.Rotation else fallback.strokeGradientRotation,
		textColor = if label ~= nil then label.TextColor3 else fallback.textColor,
		textTransparency = if label ~= nil then label.TextTransparency else fallback.textTransparency,
		glossColor = if gloss ~= nil then gloss.BackgroundColor3 else fallback.glossColor,
		glossBackgroundTransparency = if gloss ~= nil then gloss.BackgroundTransparency else fallback.glossBackgroundTransparency,
		glossTransparency = if glossGradient ~= nil then glossGradient.Transparency else fallback.glossTransparency,
	}
end

local function applyStyle(button: TextButton, fromStyle: ResolvedStyle, toStyle: ResolvedStyle, alpha: number)
	local gradient = findDirectChildOfClass(button, "UIGradient") :: UIGradient?
	local stroke = findDirectChildOfClass(button, "UIStroke") :: UIStroke?
	local strokeGradient: UIGradient? = if stroke ~= nil then stroke:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local gloss = button:FindFirstChild("Gloss") :: Frame?
	local glossGradient: UIGradient? = if gloss ~= nil then gloss:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local label = button:FindFirstChild("Label") :: TextLabel?

	button.BackgroundColor3 = fromStyle.backgroundColor:Lerp(toStyle.backgroundColor, alpha)
	button.BackgroundTransparency = lerpNumber(fromStyle.backgroundTransparency, toStyle.backgroundTransparency, alpha)

	if gradient ~= nil then
		gradient.Color = lerpColorSequence(fromStyle.gradient, toStyle.gradient, alpha)
		gradient.Rotation = lerpNumber(fromStyle.gradientRotation, toStyle.gradientRotation, alpha)
	end

	if stroke ~= nil then
		stroke.Color = fromStyle.strokeColor:Lerp(toStyle.strokeColor, alpha)
		stroke.Transparency = lerpNumber(fromStyle.strokeTransparency, toStyle.strokeTransparency, alpha)
		stroke.Thickness = lerpNumber(fromStyle.strokeThickness, toStyle.strokeThickness, alpha)
	end

	if strokeGradient ~= nil then
		strokeGradient.Color = lerpColorSequence(fromStyle.strokeGradient, toStyle.strokeGradient, alpha)
		strokeGradient.Rotation = lerpNumber(fromStyle.strokeGradientRotation, toStyle.strokeGradientRotation, alpha)
	end

	if gloss ~= nil then
		gloss.BackgroundColor3 = fromStyle.glossColor:Lerp(toStyle.glossColor, alpha)
		gloss.BackgroundTransparency = lerpNumber(fromStyle.glossBackgroundTransparency, toStyle.glossBackgroundTransparency, alpha)
	end

	if glossGradient ~= nil then
		glossGradient.Transparency = lerpNumberSequence(fromStyle.glossTransparency, toStyle.glossTransparency, alpha)
	end

	if label ~= nil then
		label.TextColor3 = fromStyle.textColor:Lerp(toStyle.textColor, alpha)
		label.TextTransparency = lerpNumber(fromStyle.textTransparency, toStyle.textTransparency, alpha)
	end
end

local function AnimateTabStyle(options: {
	getStyle: () -> TabVisualStateStyle,
	fallbackStyle: TabVisualStateStyle?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
})
	local duration = options.duration or 0.18
	local easingStyle = options.easingStyle or Enum.EasingStyle.Sine
	local easingDirection = options.easingDirection or Enum.EasingDirection.InOut

	return action(function(instance: Instance)
		if not instance:IsA("TextButton") then
			return
		end

		local button = instance :: TextButton
		local activeTween: Tween? = nil
		local activeDriver: NumberValue? = nil
		local activeConnection: RBXScriptConnection? = nil
		local firstRun = true

		local function cancelActiveTween()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			if activeConnection ~= nil then
				activeConnection:Disconnect()
				activeConnection = nil
			end

			if activeDriver ~= nil then
				activeDriver:Destroy()
				activeDriver = nil
			end
		end

		effect(function()
			local targetStyle = resolveStyle(options.getStyle(), options.fallbackStyle)

			if firstRun then
				firstRun = false
				applyStyle(button, targetStyle, targetStyle, 1)
				return
			end

			cancelActiveTween()

			local startStyle = captureStyle(button, targetStyle)
			local driver = Instance.new("NumberValue")
			driver.Name = "TabStyleTweenDriver"
			driver.Value = 0

			activeDriver = driver
			activeConnection = driver:GetPropertyChangedSignal("Value"):Connect(function()
				applyStyle(button, startStyle, targetStyle, math.clamp(driver.Value, 0, 1))
			end)

			local tween = TweenService:Create(driver, TweenInfo.new(duration, easingStyle, easingDirection), {
				Value = 1,
			})

			activeTween = tween
			tween:Play()
		end)

		cleanup(function()
			cancelActiveTween()
		end)
	end)
end

local function TabButton(props: TabButtonProps)
	local hovered = source(false)
	local buttonStyle = mergeButtonStyle(props.style)
	local fallbackStyle = buttonStyle.default or DEFAULT_BUTTON_STYLE.default or {}

	local function currentStyle(): TabVisualStateStyle
		return getStateStyle(props, buttonStyle, hovered)
	end

	local initialStyle = resolveStyle(currentStyle(), fallbackStyle)

	local function activate()
		if isDisabled(props) then
			return
		end

		if props.onTabSelected ~= nil then
			props.onTabSelected(props.tab.id)
			return
		end

		props.selectedTab(props.tab.id)
	end

	return create("TextButton")({
		Name = "Tab_" .. props.tab.label,
		Size = function()
			return readReactive(props.size, UDim2.fromScale(1, 1))
		end,
		Position = function()
			return readReactive(props.position, UDim2.fromScale(0, 0))
		end,
		AnchorPoint = function()
			return readReactive(props.anchorPoint, Vector2.new(0, 0))
		end,
		Visible = function()
			return readReactive(props.visible, true)
		end,
		LayoutOrder = props.tab.layoutOrder or 0,
		ZIndex = function()
			return readReactive(props.zIndex, 1)
		end,
		Text = "",
		AutoButtonColor = false,
		ClipsDescendants = true,
		BorderSizePixel = 0,
		BackgroundColor3 = initialStyle.backgroundColor,
		BackgroundTransparency = initialStyle.backgroundTransparency,

		Activated = activate,
		MouseEnter = function()
			hovered(true)
		end,
		MouseLeave = function()
			hovered(false)
		end,

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = buttonStyle.hoverScale or 1,
			duration = buttonStyle.hoverDuration or 0.12,
			scaleTextConstraints = true,
		}),

		AnimateTabStyle({
			getStyle = currentStyle,
			fallbackStyle = fallbackStyle,
			duration = (buttonStyle :: any).transitionDuration or Style.Tokens.Timing.Default,
			easingStyle = (buttonStyle :: any).transitionEasingStyle or Enum.EasingStyle.Sine,
			easingDirection = (buttonStyle :: any).transitionEasingDirection or Enum.EasingDirection.InOut,
		}),

		create("UICorner")({
			CornerRadius = buttonStyle.cornerRadius or UDim.new(0.16, 0),
		}),

		create("UIGradient")({
			Color = initialStyle.gradient,
			Rotation = initialStyle.gradientRotation,
		}),

		create("UIStroke")({
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
			Color = initialStyle.strokeColor,
			Transparency = initialStyle.strokeTransparency,
			Thickness = initialStyle.strokeThickness,

			create("UIGradient")({
				Color = initialStyle.strokeGradient,
				Rotation = initialStyle.strokeGradientRotation,
			}),
		}),

		create("Frame")({
			Name = "Gloss",
			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundColor3 = initialStyle.glossColor,
			BackgroundTransparency = initialStyle.glossBackgroundTransparency,
			BorderSizePixel = 0,
			ZIndex = function()
				return readReactive(props.zIndex, 1) + 1
			end,

			create("UICorner")({
				CornerRadius = buttonStyle.cornerRadius or UDim.new(0.16, 0),
			}),

			create("UIGradient")({
				Rotation = 90,
				Transparency = initialStyle.glossTransparency,
			}),
		}),

		create("TextLabel")({
			Name = "Label",
			Size = UDim2.fromScale(0.9, 0.68),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Text = props.tab.label,
			TextScaled = true,
			TextWrapped = false,
			TextXAlignment = Enum.TextXAlignment.Center,
			TextYAlignment = Enum.TextYAlignment.Center,
			FontFace = buttonStyle.fontFace or Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),
			TextColor3 = initialStyle.textColor,
			TextTransparency = initialStyle.textTransparency,
			ZIndex = function()
				return readReactive(props.zIndex, 1) + 2
			end,

			create("UITextSizeConstraint")({
				MinTextSize = buttonStyle.minTextSize or 7,
				MaxTextSize = buttonStyle.maxTextSize or 17,
			}),

			create("UIStroke")({
				ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual,
				Color = buttonStyle.textStrokeColor or Color3.fromRGB(0, 0, 0),
				Transparency = buttonStyle.textStrokeTransparency or 0.55,
				Thickness = buttonStyle.textStrokeThickness or 1,
			}),
		}),
	})
end

return TabButton
