--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.ComponentTypes)
local Text = require(script.Parent.Text)

Vide.strict = true

local create = Vide.create

local function Header(props: Types.HeaderProps?)
	local resolvedProps: Types.HeaderProps = props or {}

	return create("Frame")({
		Name = "Header",
		AnchorPoint = Vector2.new(0.5, 0.5),
		Position = UDim2.fromScale(0.496, 0.072),
		Size = UDim2.fromScale(0.592, 0.062),
		BackgroundTransparency = 1,

		Text({
			name = "Title",

			anchorPoint = Vector2.new(0.5, 0.5),
			position = UDim2.fromScale(0.5, 0.5),
			size = UDim2.fromScale(1, 1),

			text = resolvedProps.text or "HEADER",

			fontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),

			textScaled = true,
			minTextSize = 16,
			maxTextSize = 36,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			gradient = {
				color = ColorSequence.new({
					ColorSequenceKeypoint.new(0.0, Color3.fromRGB(0, 255, 238)),
					ColorSequenceKeypoint.new(0.7, Color3.fromRGB(255, 255, 255)),
					ColorSequenceKeypoint.new(1.0, Color3.fromRGB(255, 255, 255)),
				}),
				rotation = -85,
			},

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(255, 0, 255),

				pulse = {
					colorA = Color3.fromRGB(255, 0, 255),
					colorB = Color3.fromRGB(120, 1, 255),
					duration = 0.8,
				},
			},
		}),
	})
end

return Header
