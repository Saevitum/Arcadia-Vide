--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Effects = require(script.Parent.Parent.Effects)
local Text = require(script.Parent.Text)

Vide.strict = true

local create = Vide.create

type ActionButtonProps = Types.ActionButtonProps
type ActionButtonVariant = Types.ActionButtonVariant
type Reactive<T> = Types.Reactive<T>

type GradientKeypoint = {
	time: number,
	color: Color3,
}

type VariantStyle = {
	gradient: { GradientKeypoint },
	rotation: number,
	stroke: Color3,
	text: Color3,
}

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function readVariant(value: Reactive<ActionButtonVariant?>?): ActionButtonVariant?
	if value == nil then
		return nil
	end

	if type(value) == "function" then
		return (value :: () -> ActionButtonVariant?)()
	end

	return value :: ActionButtonVariant
end

local function getVariantStyle(variant: ActionButtonVariant?): VariantStyle
	if variant == "Green" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(0, 188, 9) },
				{ time = 0.71, color = Color3.fromRGB(39, 147, 0) },
				{ time = 1, color = Color3.fromRGB(0, 121, 14) },
			},
			rotation = -17,
			stroke = Color3.fromRGB(170, 255, 255),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "OrangeYellow" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(255, 213, 0) },
				{ time = 0.71, color = Color3.fromRGB(255, 200, 0) },
				{ time = 1, color = Color3.fromRGB(255, 66, 69) },
			},
			rotation = -17,
			stroke = Color3.fromRGB(170, 255, 255),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Blue" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(0, 221, 255) },
				{ time = 0.71, color = Color3.fromRGB(0, 70, 183) },
				{ time = 1, color = Color3.fromRGB(0, 22, 33) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(170, 210, 255),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Purple" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(145, 45, 255) },
				{ time = 0.71, color = Color3.fromRGB(255, 255, 255) },
				{ time = 1, color = Color3.fromRGB(255, 70, 210) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(230, 170, 255),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Yellow" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(255, 235, 70) },
				{ time = 0.71, color = Color3.fromRGB(255, 255, 220) },
				{ time = 1, color = Color3.fromRGB(155, 210, 70) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(255, 255, 180),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Orange" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(255, 150, 45) },
				{ time = 0.71, color = Color3.fromRGB(255, 245, 190) },
				{ time = 1, color = Color3.fromRGB(255, 225, 95) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(255, 230, 170),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Red" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(255, 0, 4) },
				{ time = 0.71, color = Color3.fromRGB(127, 0, 8) },
				{ time = 1, color = Color3.fromRGB(18, 0, 0) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(255, 175, 195),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Red2" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(255, 0, 4) },
				{ time = 0.71, color = Color3.fromRGB(127, 0, 8) },
				{ time = 1, color = Color3.fromRGB(18, 0, 0) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(255, 175, 195),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Red3" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(255, 0, 4) },
				{ time = 0.71, color = Color3.fromRGB(127, 0, 8) },
				{ time = 1, color = Color3.fromRGB(18, 0, 0) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(255, 175, 195),
			text = Color3.fromRGB(255, 255, 255),
		}
	end

	if variant == "Disabled" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(80, 80, 90) },
				{ time = 0.71, color = Color3.fromRGB(115, 115, 125) },
				{ time = 1, color = Color3.fromRGB(45, 45, 55) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(120, 120, 130),
			text = Color3.fromRGB(180, 180, 190),
		}
	end

	if variant == "Dark" then
		return {
			gradient = {
				{ time = 0, color = Color3.fromRGB(98, 98, 98) },
				{ time = 0.71, color = Color3.fromRGB(66, 66, 57) },
				{ time = 1, color = Color3.fromRGB(25, 25, 25) },
			},
			rotation = 0,
			stroke = Color3.fromRGB(120, 120, 130),
			text = Color3.fromRGB(180, 180, 190),
		}
	end

	return {
		gradient = {
			{ time = 0, color = Color3.fromRGB(98, 98, 98) },
			{ time = 0.71, color = Color3.fromRGB(66, 66, 57) },
			{ time = 1, color = Color3.fromRGB(25, 25, 25) },
		},
		rotation = 0,
		stroke = Color3.fromRGB(110, 130, 160),
		text = Color3.fromRGB(255, 255, 255),
	}
end

local function buildColorSequence(keypoints: { GradientKeypoint }): ColorSequence
	local colorKeypoints: { ColorSequenceKeypoint } = {}

	for _, keypoint in ipairs(keypoints) do
		table.insert(colorKeypoints, ColorSequenceKeypoint.new(math.clamp(keypoint.time, 0, 1), keypoint.color))
	end

	table.sort(colorKeypoints, function(a, b)
		return a.Time < b.Time
	end)

	return ColorSequence.new(colorKeypoints)
end

local function getGradientKeypoints(props: ActionButtonProps, variantStyle: VariantStyle): { GradientKeypoint }
	if props.gradient ~= nil and props.gradient.keypoints ~= nil then
		return read(props.gradient.keypoints, variantStyle.gradient)
	end

	return variantStyle.gradient
end

local function getGradientColor(props: ActionButtonProps, variantStyle: VariantStyle): ColorSequence
	return buildColorSequence(getGradientKeypoints(props, variantStyle))
end

local function getGradientRotation(props: ActionButtonProps, variantStyle: VariantStyle): number
	if props.gradient ~= nil and props.gradient.rotation ~= nil then
		return read(props.gradient.rotation, variantStyle.rotation)
	end

	return variantStyle.rotation
end

local function getStrokeGradientKeypoints(props: ActionButtonProps): { GradientKeypoint }
	local fallback = {
		{ time = 0, color = Color3.fromRGB(255, 255, 255) },
		{ time = 1, color = Color3.fromRGB(255, 255, 255) },
	}

	if props.strokeGradient ~= nil and props.strokeGradient.keypoints ~= nil then
		return read(props.strokeGradient.keypoints, fallback)
	end

	return fallback
end

local function getStrokeGradientRotation(props: ActionButtonProps): number
	if props.strokeGradient ~= nil and props.strokeGradient.rotation ~= nil then
		return read(props.strokeGradient.rotation, 0)
	end

	return 0
end

local function createStrokeGradient(props: ActionButtonProps): Instance?
	if props.strokeGradient == nil then
		return nil
	end

	return create("UIGradient")({
		Color = function()
			return buildColorSequence(getStrokeGradientKeypoints(props))
		end,

		Rotation = function()
			return getStrokeGradientRotation(props)
		end,
	})
end

local function ActionButton(props: ActionButtonProps)
	local function getCurrentVariantStyle(): VariantStyle
		return getVariantStyle(readVariant(props.variant))
	end

	return create("TextButton")({
		Name = props.name or "ActionButton",

		Size = function()
			return read(props.size, UDim2.fromScale(1, 0.15))
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

		BackgroundColor3 = Color3.fromRGB(255, 255, 255),
		BackgroundTransparency = 0,
		BorderSizePixel = 0,

		Activated = function()
			if read(props.disabled, false) then
				return
			end

			if props.onClick ~= nil then
				props.onClick()
			end
		end,

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = read(props.hoverScale, 1.2),
			scaleTextConstraints = read(props.scaleTextConstraints, true),
			duration = read(props.hoverDuration, 0.12),
		}),

		create("UICorner")({
			CornerRadius = function()
				return read(props.cornerRadius, UDim.new(0.5, 0))
			end,
		}),

		create("UIStroke")({
			Thickness = function()
				return read(props.strokeThickness, 0)
			end,

			Color = function()
				return read(props.strokeColor, getCurrentVariantStyle().stroke)
			end,

			Transparency = function()
				return read(props.strokeTransparency, 0.15)
			end,

			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

			createStrokeGradient(props),
		}),

		create("UIGradient")({
			Color = function()
				if read(props.disabled, false) then
					local disabledStyle = getVariantStyle("Disabled")
					return getGradientColor(props, disabledStyle)
				end

				return getGradientColor(props, getCurrentVariantStyle())
			end,

			Rotation = function()
				if read(props.disabled, false) then
					local disabledStyle = getVariantStyle("Disabled")
					return getGradientRotation(props, disabledStyle)
				end

				return getGradientRotation(props, getCurrentVariantStyle())
			end,
		}),

		create("Frame")({
			Name = "Gloss",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = Color3.fromRGB(0, 0, 0),
			BackgroundTransparency = 0.5,
			BorderSizePixel = 0,

			ZIndex = function()
				return read(props.zIndex, 1) + 1
			end,

			create("UICorner")({
				CornerRadius = function()
					return read(props.cornerRadius, UDim.new(0.5, 0))
				end,
			}),

			create("UIGradient")({
				Rotation = 90,

				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 1),
					NumberSequenceKeypoint.new(0.5, 0.749),
					NumberSequenceKeypoint.new(1, 0),
				}),
			}),
		}),

		Text({
			name = "Label",

			text = props.text or "",

			size = if props.iconText == nil then UDim2.fromScale(0.88, 0.72) else UDim2.fromScale(0.74, 0.72),
			position = if props.iconText == nil then UDim2.fromScale(0.5, 0.5) else UDim2.fromScale(0.48, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),

			textScaled = true,
			minTextSize = 7,
			maxTextSize = 18,

			textColor3 = function()
				if read(props.disabled, false) then
					return getVariantStyle("Disabled").text
				end

				return read(props.textColor3, getCurrentVariantStyle().text)
			end,

			textTransparency = function()
				return read(props.textTransparency, 0)
			end,

			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.65,
			},

			zIndex = function()
				return read(props.zIndex, 1) + 2
			end,
		}),

		Text({
			name = "Icon",

			text = props.iconText or "",

			size = UDim2.fromScale(0.16, 0.72),
			position = UDim2.fromScale(0.88, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal),

			textScaled = true,
			minTextSize = 7,
			maxTextSize = 20,

			textColor3 = function()
				if read(props.disabled, false) then
					return getVariantStyle("Disabled").text
				end

				return read(props.textColor3, getCurrentVariantStyle().text)
			end,

			textTransparency = function()
				if props.iconText == nil then
					return 1
				end

				return read(props.textTransparency, 0)
			end,

			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.65,
			},

			zIndex = function()
				return read(props.zIndex, 1) + 2
			end,
		}),
	})
end

return ActionButton
