--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create

type ToggleSwitchProps = Types.ToggleSwitchProps
type Reactive<T> = Types.Reactive<T>

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function ToggleSwitch(props: ToggleSwitchProps)
	local value = props.value

	return create("TextButton")({
		Name = props.name or "ToggleSwitch",

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

		Text = "",
		AutoButtonColor = false,
		Active = true,

		BackgroundColor3 = function()
			if value() then
				return read(props.onBackgroundColor3, Color3.fromRGB(5, 46, 55))
			end

			return read(props.backgroundColor3, Color3.fromRGB(9, 13, 22))
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

		create("UICorner")({
			CornerRadius = function()
				return read(props.cornerRadius, UDim.new(0.5, 0))
			end,
		}),

		create("UIStroke")({
			Thickness = function()
				return read(props.strokeThickness, 2)
			end,

			Color = function()
				return read(props.strokeColor3, Color3.fromRGB(0, 255, 238))
			end,

			Transparency = function()
				return read(props.strokeTransparency, 0)
			end,
		}),

		create("Frame")({
			Name = "Fill",

			Size = function()
				if value() then
					return UDim2.fromScale(1, 1)
				end

				return UDim2.fromScale(0, 1)
			end,

			BackgroundColor3 = function()
				return read(props.fillColor3, Color3.fromRGB(0, 255, 238))
			end,

			BackgroundTransparency = function()
				return read(props.fillTransparency, 0.68)
			end,

			BorderSizePixel = 0,
			ZIndex = function()
				return read(props.zIndex, 1) + 1
			end,

			create("UICorner")({
				CornerRadius = function()
					return read(props.cornerRadius, UDim.new(0.5, 0))
				end,
			}),
		}),

		create("Frame")({
			Name = "Knob",

			Size = function()
				return read(props.knobSize, UDim2.fromScale(0.15, 0.76))
			end,

			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = function()
				if value() then
					return read(props.onKnobColor3, Color3.fromRGB(255, 83, 151))
				end

				return read(props.knobColor3, Color3.fromRGB(37, 46, 56))
			end,

			BorderSizePixel = 0,
			ZIndex = function()
				return read(props.zIndex, 1) + 2
			end,

			Effects.TweenGuiObjectLayout({
				isOpen = function()
					return value()
				end,

				targetPosition = function()
					if value() then
						return read(props.knobOnPosition, UDim2.fromScale(0.73, 0.5))
					end

					return read(props.knobOffPosition, UDim2.fromScale(0.27, 0.5))
				end,

				duration = props.tweenDuration or 0.14,
				easingStyle = Enum.EasingStyle.Quad,
				easingDirection = Enum.EasingDirection.Out,
			}),

			create("UICorner")({
				CornerRadius = UDim.new(0.5, 0),
			}),
		}),
	})
end

return ToggleSwitch
