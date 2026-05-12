--!strict

local Merge = require(script.Parent.Merge)
local Tokens = require(script.Parent.Tokens)
local Gradients = require(script.Parent.Gradients)

local Types = require(script.Parent.Parent.UITypes.ComponentTypes)

type TabStripStyle = Types.TabStripStyle

local Tabs = {}

Tabs.Presets = {}
Tabs.Layouts = {}

function Tabs.merge<T>(base: T, override: any?): T
	return Merge.deep(base, override)
end

Tabs.Presets.CyberDefault = {
	backgroundColor = Tokens.Colors.Black,
	backgroundTransparency = 1,

	cellSize = UDim2.fromScale(0.18, 0.42),
	cellPadding = UDim2.fromScale(0.025, 0.12),
	fillDirectionMaxCells = 5,

	horizontalAlignment = Enum.HorizontalAlignment.Center,
	verticalAlignment = Enum.VerticalAlignment.Center,

	padding = {
		top = UDim.new(0, 0),
		bottom = UDim.new(0, 0),
		left = UDim.new(0, 0),
		right = UDim.new(0, 0),
	},

	button = {
		cornerRadius = Tokens.Corners.Large,

		fontFace = Tokens.Fonts.MichromaBoldItalic,
		minTextSize = 7,
		maxTextSize = 17,

		hoverScale = 1,
		hoverDuration = Tokens.Timing.Hover,

		textStrokeColor = Tokens.Colors.Black,
		textStrokeTransparency = 0.55,
		textStrokeThickness = 1,

		default = {
			backgroundColor = Tokens.Colors.DarkGlass,
			backgroundTransparency = 0.08,

			gradient = Gradients.darkGlass(),
			gradientRotation = 90,

			strokeColor = Tokens.Colors.Cyan,
			strokeTransparency = 0.18,
			strokeThickness = 2,
			strokeGradient = Gradients.cyberCyanMagenta(),
			strokeGradientRotation = 0,

			textColor = Tokens.Colors.SoftWhite,
			textTransparency = 0,

			glossColor = Tokens.Colors.White,
			glossTransparency = Gradients.glossTransparency(),
		},

		hover = {
			backgroundColor = Tokens.Colors.Graphite,
			backgroundTransparency = 0.02,

			gradient = Gradients.cyberCyanMagenta(),
			gradientRotation = 0,

			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0.04,
			strokeThickness = 2,
			strokeGradient = Gradients.cyberPrimary(),
			strokeGradientRotation = 0,

			textColor = Tokens.Colors.White,
			textTransparency = 0,

			glossColor = Tokens.Colors.White,
			glossTransparency = Gradients.glossTransparency(),
		},

		selected = {
			backgroundColor = Tokens.Colors.Cyan,
			backgroundTransparency = 0,

			gradient = Gradients.cyberPrimary(),
			gradientRotation = 0,

			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0,
			strokeThickness = 2.5,
			strokeGradient = Gradients.cyberPrimary(),
			strokeGradientRotation = 0,

			textColor = Tokens.Colors.White,
			textTransparency = 0,

			glossColor = Tokens.Colors.White,
			glossTransparency = Gradients.glossTransparency(),
		},

		disabled = {
			backgroundColor = Tokens.Colors.Gray800,
			backgroundTransparency = 0.25,

			gradient = Gradients.claimedGray(),
			gradientRotation = 90,

			strokeColor = Tokens.Colors.Gray500,
			strokeTransparency = 0.35,
			strokeThickness = 1.5,

			textColor = Tokens.Colors.Gray300,
			textTransparency = 0.15,

			glossColor = Tokens.Colors.White,
			glossTransparency = Gradients.glossTransparency(),
		},
	},
} :: TabStripStyle

Tabs.Presets.CyberCompact = Tabs.merge(Tabs.Presets.CyberDefault, {
	cellSize = UDim2.fromScale(0.18, 0.36),
	cellPadding = UDim2.fromScale(0.02, 0.08),

	button = {
		cornerRadius = Tokens.Corners.Medium,
		minTextSize = 7,
		maxTextSize = 15,
	},
}) :: TabStripStyle

Tabs.Presets.CyberThreeTabs = Tabs.merge(Tabs.Presets.CyberDefault, {
	cellSize = UDim2.fromScale(0.3, 0.7),
	cellPadding = UDim2.fromScale(0.035, 0),
	fillDirectionMaxCells = 3,
}) :: TabStripStyle

Tabs.Layouts.ThreeTop = {
	size = UDim2.fromScale(0.42, 0.08),
	position = UDim2.fromScale(0.5, 0.275),
	anchorPoint = Vector2.new(0.5, 0.5),
	cellSize = UDim2.fromScale(0.3, 0.7),
	cellPadding = UDim2.fromScale(0.035, 0),
	fillDirectionMaxCells = 3,
}

Tabs.Layouts.FiveByTwo = {
	size = UDim2.fromScale(0.74, 0.17),
	position = UDim2.fromScale(0.5, 0.305),
	anchorPoint = Vector2.new(0.5, 0.5),
	cellSize = UDim2.fromScale(0.16, 0.25),
	cellPadding = UDim2.fromScale(0.035, 0.12),
	fillDirectionMaxCells = 5,
}

return Tabs
