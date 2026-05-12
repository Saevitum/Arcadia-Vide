--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local create = Vide.create

type Reactive<T> = Types.Reactive<T>
type ToggleButtonProps = Types.ToggleButtonProps

local DEFAULT_GRADIENT = ColorSequence.new({
	ColorSequenceKeypoint.new(0, Color3.fromRGB(0, 255, 8)),
	ColorSequenceKeypoint.new(0.55, Color3.fromRGB(0, 156, 3)),
	ColorSequenceKeypoint.new(1, Color3.fromRGB(0, 102, 2)),
})

local DEFAULT_ON_GRADIENT = ColorSequence.new({
	ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 44, 48)),
	ColorSequenceKeypoint.new(0.55, Color3.fromRGB(186, 32, 37)),
	ColorSequenceKeypoint.new(1, Color3.fromRGB(86, 15, 17)),
})

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function ToggleButton(props: ToggleButtonProps)
	local value = props.value

	return create("TextButton")({
		Name = props.name or "ToggleButton",

		Size = function()
			return read(props.size, UDim2.fromScale(1, 1))
		end,

		Position = function()
			return read(props.position, UDim2.fromScale(0, 0))
		end,

		AnchorPoint = function()
			return read(props.anchorPoint, Vector2.new(0, 0))
		end,

		Visible = function()
			return read(props.visible, true)
		end,

		LayoutOrder = function()
			return read(props.layoutOrder, 0)
		end,

		ZIndex = function()
			return read(props.zIndex, 1)
		end,

		Text = function()
			if value() then
				return read(props.textOn, "ON")
			end

			return read(props.textOff, "OFF")
		end,

		FontFace = function()
			return read(
				props.fontFace,
				Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal)
			)
		end,

		TextScaled = true,
		TextColor3 = function()
			if value() then
				return read(props.onTextColor3, Color3.fromRGB(18, 13, 24))
			end

			return read(props.textColor3, Color3.fromRGB(8, 18, 24))
		end,
		TextStrokeTransparency = 0.82,
		TextXAlignment = Enum.TextXAlignment.Center,
		TextYAlignment = Enum.TextYAlignment.Center,

		AutoButtonColor = false,
		Active = true,

		BackgroundColor3 = function()
			if value() then
				return read(props.onBackgroundColor3, Color3.fromRGB(255, 255, 255))
			end

			return read(props.backgroundColor3, Color3.fromRGB(255, 255, 255))
		end,

		BackgroundTransparency = function()
			return read(props.backgroundTransparency, 0)
		end,

		BorderSizePixel = 0,

		Activated = function()
			if read(props.disabled, false) then
				return
			end

			local nextValue = not value()
			value(nextValue)

			if props.onChanged ~= nil then
				props.onChanged(nextValue)
			end
		end,

		create("UIAspectRatioConstraint")({
			AspectRatio = function()
				return read(props.aspectRatio, 1)
			end,
			DominantAxis = Enum.DominantAxis.Height,
		}),

		create("UICorner")({
			CornerRadius = function()
				return read(props.cornerRadius, UDim.new(0.18, 0))
			end,
		}),

		create("UIGradient")({
			Rotation = function()
				return read(props.gradientRotation, 90)
			end,

			Color = function()
				if value() then
					return read(props.onGradient, DEFAULT_ON_GRADIENT)
				end

				return read(props.gradient, DEFAULT_GRADIENT)
			end,
		}),

		create("UIStroke")({
			Thickness = function()
				return read(props.strokeThickness, 2)
			end,

			Color = function()
				if value() then
					return read(props.onStrokeColor3, Color3.fromRGB(255, 83, 151))
				end

				return read(props.strokeColor3, Color3.fromRGB(0, 255, 238))
			end,

			Transparency = function()
				return read(props.strokeTransparency, 0.05)
			end,
		}),

		create("UITextSizeConstraint")({
			MinTextSize = function()
				return read(props.minTextSize, 7)
			end,

			MaxTextSize = function()
				return read(props.maxTextSize, 14)
			end,
		}),
	})
end

return ToggleButton
