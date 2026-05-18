--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create

export type AnimatedPulseDividerProps = {
	name: string?,
	open: () -> boolean,
	phase: () -> number,

	size: UDim2,
	position: UDim2,
	anchorPoint: Vector2?,
	zIndex: number?,

	backgroundColor3: Color3?,

	edgeColor: Color3?,
	middleColors: { Color3 }?,
	onColorChanged: ((Color3) -> ())?,

	rotation: number?,

	openDuration: number?,
	closeDuration: number?,

	loopsPerColor: number?,
	segmentDuration: number?,
	colorTweenDuration: number?,

	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
	colorEasingStyle: Enum.EasingStyle?,
	colorEasingDirection: Enum.EasingDirection?,
}

local DEFAULT_EDGE_COLOR = Color3.fromRGB(255, 255, 255)
local DEFAULT_MIDDLE_COLORS = {
	Color3.fromRGB(0, 229, 255),
	Color3.fromRGB(255, 0, 255),
	Color3.fromRGB(255, 0, 60),
}

local function AnimatedPulseDivider(props: AnimatedPulseDividerProps)
	local edgeColor = props.edgeColor or DEFAULT_EDGE_COLOR
	local middleColors = props.middleColors or DEFAULT_MIDDLE_COLORS
	local easingStyle = props.easingStyle or Enum.EasingStyle.Sine
	local easingDirection = props.easingDirection or Enum.EasingDirection.InOut
	local colorEasingStyle = props.colorEasingStyle or Enum.EasingStyle.Sine
	local colorEasingDirection = props.colorEasingDirection or Enum.EasingDirection.InOut

	return create("Frame")({
		Name = props.name or "AnimatedPulseDivider",
		Size = props.size,
		Position = props.position,
		AnchorPoint = props.anchorPoint or Vector2.new(0.5, 0.5),
		Visible = false,
		BackgroundColor3 = props.backgroundColor3 or edgeColor,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = props.zIndex or 16,

		Effects.FadeGuiObject({
			open = props.open,
			openTransparency = 0,
			closedTransparency = 1,
			openDuration = props.openDuration or 3,
			closeDuration = props.closeDuration or 0.08,
			easingStyle = Enum.EasingStyle.Quad,
			easingDirection = Enum.EasingDirection.Out,
			hideWhenClosed = true,
		}),

		create("UIGradient")({
			Rotation = props.rotation or 90,
			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, edgeColor),
				ColorSequenceKeypoint.new(0.5, middleColors[1]),
				ColorSequenceKeypoint.new(1, edgeColor),
			}),
			Transparency = NumberSequence.new({
				NumberSequenceKeypoint.new(0, 1),
				NumberSequenceKeypoint.new(0.5, 0),
				NumberSequenceKeypoint.new(1, 1),
			}),

			Effects.SweepGradientKeypoint({
				phase = props.phase,
				edgeColor = edgeColor,
				middleColors = middleColors,
				edgeTransparency = 1,
				middleTransparency = 0,

				-- Reference timing from the good SideKicks divider.
				loopsPerColor = props.loopsPerColor or 3,
				segmentDuration = props.segmentDuration or 1.2,
				easingStyle = easingStyle,
				easingDirection = easingDirection,
				colorTweenDuration = props.colorTweenDuration or 0.45,
				colorEasingStyle = colorEasingStyle,
				colorEasingDirection = colorEasingDirection,

				onColorChanged = props.onColorChanged,
			}),
		}),
	})
end

return AnimatedPulseDivider
