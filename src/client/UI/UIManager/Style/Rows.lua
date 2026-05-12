--!strict

local Tokens = require(script.Parent.Tokens)
local Gradients = require(script.Parent.Gradients)

local Rows = {}

Rows.Layouts = {
	WideList = {
		rowSize = UDim2.fromScale(0.96, 0.12),
		rowPadding = UDim.new(0.04, 0),
	},
}

Rows.Presets = {
	SegmentedCyber = {
		fontFace = Tokens.Fonts.MichromaBoldItalic,

		rowBackgroundColor = Color3.fromRGB(15, 21, 30),
		rowBackgroundTransparency = 0.12,
		rowCornerRadius = UDim.new(0.2, 0),

		rowGradient = Gradients.colorSequence({
			{
				time = 0,
				color = Color3.fromRGB(24, 33, 43),
			},
			{
				time = 0.55,
				color = Color3.fromRGB(12, 17, 25),
			},
			{
				time = 1,
				color = Color3.fromRGB(24, 33, 43),
			},
		}),

		rowTransparency = Gradients.transparencySequence({
			{
				time = 0,
				transparency = 0.18,
			},
			{
				time = 0.5,
				transparency = 0.03,
			},
			{
				time = 1,
				transparency = 0.18,
			},
		}),

		segmentBackgroundColor = Color3.fromRGB(25, 34, 45),
		segmentBackgroundTransparency = 0.12,
		segmentCornerRadius = UDim.new(0.16, 0),

		segmentGradient = Gradients.colorSequence({
			{
				time = 0,
				color = Color3.fromRGB(30, 42, 55),
			},
			{
				time = 1,
				color = Color3.fromRGB(11, 15, 23),
			},
		}),

		segmentTransparency = Gradients.transparencySequence({
			{
				time = 0,
				transparency = 0.12,
			},
			{
				time = 1,
				transparency = 0.3,
			},
		}),

		titleColor = Tokens.Colors.CyanBright,
		textColor = Color3.fromRGB(235, 240, 245),

		textStrokeColor = Tokens.Colors.Black,
		textStrokeTransparency = 0.16,
		textStrokeThickness = 1,

		collectColor = Tokens.Colors.Green,
		collectStrokeColor = Color3.fromRGB(190, 255, 170),

		claimedColor = Color3.fromRGB(70, 86, 94),
		lockedColor = Color3.fromRGB(35, 42, 54),
	},
}

return Rows
