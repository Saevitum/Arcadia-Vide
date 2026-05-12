--!strict

local Tokens = require(script.Parent.Tokens)
local Gradients = require(script.Parent.Gradients)

local Pages = {}

Pages.Layouts = {
	WideLower = {
		size = UDim2.fromScale(0.76, 0.43),
		position = UDim2.fromScale(0.5, 0.58),
		anchorPoint = Vector2.new(0.5, 0.5),
	},
}

Pages.Transitions = {
	SoftFade = {
		duration = 0.28,
		fadeDuration = 0.2,
		closeFadeDuration = 0.12,

		easingStyle = Enum.EasingStyle.Sine,
		easingDirection = Enum.EasingDirection.InOut,

		fadeEasingStyle = Enum.EasingStyle.Sine,
		fadeEasingDirection = Enum.EasingDirection.InOut,
	},
}

Pages.EmptyStates = {
	CyberPanel = {
		size = UDim2.fromScale(0.96, 0.35),

		backgroundColor = Tokens.Colors.Dark,
		backgroundTransparency = 0.35,

		cornerRadius = Tokens.Corners.Small,

		strokeThickness = Tokens.Strokes.Thin,
		strokeColor = Tokens.Colors.White,
		strokeTransparency = 0.35,
		strokeGradient = Gradients.cyberCyanMagenta(),
		strokeGradientRotation = 0,

		textColor = Tokens.Colors.MutedWhite,
		fontFace = Tokens.Fonts.MichromaBoldItalic,

		textSize = UDim2.fromScale(0.82, 0.45),
		textPosition = UDim2.fromScale(0.5, 0.5),
		textAnchorPoint = Vector2.new(0.5, 0.5),

		minTextSize = 8,
		maxTextSize = 22,

		textStrokeColor = Tokens.Colors.Black,
		textStrokeTransparency = 0.2,
		textStrokeThickness = 1,
	},
}

return Pages
