--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.ComponentTypes)
local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local create = Vide.create

type Reactive<T> = Types.Reactive<T>
type SliderProps = Types.SliderProps

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function getRange(props: SliderProps): (number, number)
	local min = props.min or 0
	local max = props.max or 100

	if max < min then
		return max, min
	end

	if max == min then
		return min, min + 1
	end

	return min, max
end

local function clampToStep(value: number, min: number, max: number, step: number?): number
	local clamped = math.clamp(value, min, max)

	if step == nil or step <= 0 then
		return clamped
	end

	local stepped = min + (math.round((clamped - min) / step) * step)
	return math.clamp(stepped, min, max)
end

local function getAlpha(value: number, min: number, max: number): number
	return math.clamp((value - min) / (max - min), 0, 1)
end

local function createFillGradient(props: SliderProps): Instance?
	if
		props.fillGradient == nil
		and props.fillGradientTransparency == nil
		and props.fillGradientEffect == nil
		and props.fillGradientOffset == nil
		and props.fillGradientRotation == nil
	then
		return nil
	end

	return create("UIGradient")({
		Color = function()
			return read(
				props.fillGradient,
				ColorSequence.new({
					ColorSequenceKeypoint.new(0, Color3.fromRGB(0, 255, 238)),
					ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 0, 255)),
					ColorSequenceKeypoint.new(1, Color3.fromRGB(0, 255, 238)),
				})
			)
		end,

		Transparency = function()
			return read(props.fillGradientTransparency, NumberSequence.new(0))
		end,

		Rotation = function()
			return read(props.fillGradientRotation, 0)
		end,

		Offset = function()
			return read(props.fillGradientOffset, Vector2.new(0, 0))
		end,

		if props.fillGradientEffect ~= nil then Effects.LiquidGradient(props.fillGradientEffect) else nil,
	})
end

local function Slider(props: SliderProps)
	local value = props.value

	return create("TextButton")({
		Name = props.name or "Slider",

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
			return read(props.backgroundColor3, Color3.fromRGB(9, 13, 22))
		end,

		BackgroundTransparency = function()
			if read(props.dimmed, false) then
				return math.max(read(props.backgroundTransparency, 0), 0.28)
			end

			return read(props.backgroundTransparency, 0)
		end,

		BorderSizePixel = 0,

		action(function(instance: Instance)
			if not instance:IsA("GuiObject") then
				return
			end

			local gui = instance :: GuiObject
			local dragging = false

			local function setFromScreenX(screenX: number)
				if read(props.disabled, false) then
					return
				end

				local width = gui.AbsoluteSize.X
				if width <= 0 then
					return
				end

				local min, max = getRange(props)
				local alpha = math.clamp((screenX - gui.AbsolutePosition.X) / width, 0, 1)
				local nextValue = clampToStep(min + ((max - min) * alpha), min, max, props.step)

				value(nextValue)

				if props.onChanged ~= nil then
					props.onChanged(nextValue)
				end
			end

			local inputBegan = gui.InputBegan:Connect(function(input: InputObject)
				if
					input.UserInputType ~= Enum.UserInputType.MouseButton1
					and input.UserInputType ~= Enum.UserInputType.Touch
				then
					return
				end

				dragging = true
				setFromScreenX(input.Position.X)
			end)

			local inputChanged = UserInputService.InputChanged:Connect(function(input: InputObject)
				if not dragging then
					return
				end

				if
					input.UserInputType ~= Enum.UserInputType.MouseMovement
					and input.UserInputType ~= Enum.UserInputType.Touch
				then
					return
				end

				setFromScreenX(input.Position.X)
			end)

			local inputEnded = UserInputService.InputEnded:Connect(function(input: InputObject)
				if
					input.UserInputType == Enum.UserInputType.MouseButton1
					or input.UserInputType == Enum.UserInputType.Touch
				then
					dragging = false
				end
			end)

			cleanup(function()
				inputBegan:Disconnect()
				inputChanged:Disconnect()
				inputEnded:Disconnect()
			end)
		end),

		create("UICorner")({
			CornerRadius = function()
				return read(props.cornerRadius, UDim.new(0.5, 0))
			end,
		}),

		create("UIStroke")({
			Thickness = function()
				return read(props.strokeThickness, 1)
			end,

			Color = function()
				return read(props.strokeColor3, Color3.fromRGB(0, 255, 238))
			end,

			Transparency = function()
				return read(props.strokeTransparency, 0.12)
			end,
		}),

		create("Frame")({
			Name = "Fill",

			Size = function()
				local min, max = getRange(props)
				return UDim2.fromScale(getAlpha(value(), min, max), 1)
			end,

			BackgroundColor3 = function()
				return read(props.fillColor3, Color3.fromRGB(0, 255, 238))
			end,

			BackgroundTransparency = function()
				if read(props.dimmed, false) then
					return read(props.dimmedFillTransparency, 0.55)
				end

				return read(props.fillTransparency, 0.08)
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

			createFillGradient(props),
		}),

		create("Frame")({
			Name = "Knob",

			Size = function()
				return read(props.knobSize, UDim2.fromScale(0.07, 1.65))
			end,

			Position = function()
				local min, max = getRange(props)
				return UDim2.fromScale(getAlpha(value(), min, max), 0.5)
			end,

			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = function()
				if read(props.dimmed, false) then
					return read(props.dimmedKnobColor3, Color3.fromRGB(82, 91, 105))
				end

				return read(props.knobColor3, Color3.fromRGB(255, 255, 255))
			end,

			BorderSizePixel = 0,
			ZIndex = function()
				return read(props.zIndex, 1) + 2
			end,

			create("UICorner")({
				CornerRadius = UDim.new(0.5, 0),
			}),

			create("UIStroke")({
				Thickness = 1,
				Color = function()
					return read(props.strokeColor3, Color3.fromRGB(0, 255, 238))
				end,
				Transparency = 0.2,
			}),
		}),
	})
end

return Slider
