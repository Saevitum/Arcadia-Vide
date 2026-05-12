--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create
local action = Vide.action

type TextProps = Types.TextProps
type TextStrokeProps = Types.TextStrokeProps
type Reactive<T> = Types.Reactive<T>

local DEFAULT_FONT = Font.fromEnum(Enum.Font.Michroma)

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function getStrokeAction(stroke: TextStrokeProps?)
	if stroke == nil or stroke.pulse == nil then
		return action(function(_instance: Instance) end)
	end

	local pulse = stroke.pulse

	return Effects.PulseStrokeColor({
		colorA = pulse.colorA,
		colorB = pulse.colorB,
		duration = pulse.duration,
	})
end

local function Text(props: TextProps?)
	local resolvedProps: TextProps = props or {}

	local gradient = resolvedProps.gradient
	local stroke = resolvedProps.stroke

	return create("TextLabel")({
		Name = resolvedProps.name or "Text",

		Size = function()
			return read(resolvedProps.size, UDim2.fromScale(1, 1))
		end,

		Position = function()
			return read(resolvedProps.position, UDim2.fromScale(0, 0))
		end,

		AnchorPoint = function()
			return read(resolvedProps.anchorPoint, Vector2.new(0, 0))
		end,

		Rotation = function()
			return read(resolvedProps.rotation, 0)
		end,

		Visible = function()
			return read(resolvedProps.visible, true)
		end,

		ZIndex = function()
			return read(resolvedProps.zIndex, 1)
		end,

		LayoutOrder = function()
			return read(resolvedProps.layoutOrder, 0)
		end,

		BackgroundTransparency = function()
			return read(resolvedProps.backgroundTransparency, 1)
		end,

		BackgroundColor3 = function()
			return read(resolvedProps.backgroundColor3, Color3.fromRGB(255, 255, 255))
		end,

		BorderSizePixel = 0,

		Text = function()
			return read(resolvedProps.text, "")
		end,

		FontFace = resolvedProps.fontFace or DEFAULT_FONT,

		TextScaled = if resolvedProps.textScaled == nil then true else resolvedProps.textScaled,

		TextSize = function()
			return read(resolvedProps.textSize, 14)
		end,

		TextColor3 = function()
			return read(resolvedProps.textColor3, Color3.fromRGB(255, 255, 255))
		end,

		TextTransparency = function()
			return read(resolvedProps.textTransparency, 0)
		end,

		TextXAlignment = resolvedProps.textXAlignment or Enum.TextXAlignment.Center,
		TextYAlignment = resolvedProps.textYAlignment or Enum.TextYAlignment.Center,

		RichText = resolvedProps.richText or false,
		TextWrapped = if resolvedProps.textWrapped == nil then true else resolvedProps.textWrapped,
		TextTruncate = resolvedProps.textTruncate or Enum.TextTruncate.None,
		LineHeight = resolvedProps.lineHeight or 1,
		AutomaticSize = resolvedProps.automaticSize or Enum.AutomaticSize.None,

		create("UITextSizeConstraint")({
			MinTextSize = resolvedProps.minTextSize or 8,
			MaxTextSize = resolvedProps.maxTextSize or 36,
		}),

		create("UIGradient")({
			Enabled = gradient ~= nil,
			Color = if gradient ~= nil and gradient.color ~= nil
				then gradient.color
				else ColorSequence.new(Color3.fromRGB(255, 255, 255)),

			Transparency = if gradient ~= nil and gradient.transparency ~= nil
				then gradient.transparency
				else NumberSequence.new(0),

			Rotation = if gradient ~= nil and gradient.rotation ~= nil then gradient.rotation else 0,

			Offset = if gradient ~= nil and gradient.offset ~= nil then gradient.offset else Vector2.new(0, 0),
		}),

		create("UIStroke")({
			Enabled = stroke ~= nil,

			Thickness = function()
				if stroke == nil then
					return 0
				end

				return read(stroke.thickness, 1)
			end,

			Color = function()
				if stroke == nil then
					return Color3.fromRGB(255, 255, 255)
				end

				return read(stroke.color, Color3.fromRGB(255, 255, 255))
			end,

			Transparency = function()
				if stroke == nil then
					return 1
				end

				return read(stroke.transparency, 0)
			end,

			getStrokeAction(stroke),
		}),
	})
end

return Text
