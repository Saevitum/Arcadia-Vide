--!strict

local Tokens = {}

Tokens.Colors = {
	Cyan = Color3.fromRGB(0, 229, 255),
	CyanBright = Color3.fromRGB(0, 255, 238),
	CyanSoft = Color3.fromRGB(120, 255, 255),

	Magenta = Color3.fromRGB(255, 0, 255),
	Purple = Color3.fromRGB(142, 5, 255),
	Violet = Color3.fromRGB(120, 1, 255),

	Red = Color3.fromRGB(255, 0, 60),
	Orange = Color3.fromRGB(255, 150, 40),
	Yellow = Color3.fromRGB(255, 220, 80),
	Green = Color3.fromRGB(98, 230, 120),

	White = Color3.fromRGB(255, 255, 255),
	SoftWhite = Color3.fromRGB(225, 245, 255),
	MutedWhite = Color3.fromRGB(180, 205, 215),

	Black = Color3.fromRGB(0, 0, 0),
	NearBlack = Color3.fromRGB(3, 6, 10),
	Dark = Color3.fromRGB(8, 12, 18),
	DarkGlass = Color3.fromRGB(10, 17, 24),
	Graphite = Color3.fromRGB(18, 24, 32),
	Gunmetal = Color3.fromRGB(28, 36, 46),

	Gray900 = Color3.fromRGB(10, 10, 12),
	Gray800 = Color3.fromRGB(22, 24, 28),
	Gray700 = Color3.fromRGB(38, 42, 48),
	Gray500 = Color3.fromRGB(90, 96, 108),
	Gray300 = Color3.fromRGB(150, 158, 170),
}

Tokens.RarityColors = {
	Common = Color3.fromRGB(185, 205, 215),
	Uncommon = Color3.fromRGB(98, 230, 120),
	Rare = Color3.fromRGB(0, 229, 255),
	Epic = Color3.fromRGB(142, 5, 255),
	Legendary = Color3.fromRGB(255, 150, 40),
	Mythic = Color3.fromRGB(255, 0, 255),
}

Tokens.Fonts = {
	MichromaRegular = Font.new(
		"rbxasset://fonts/families/Michroma.json",
		Enum.FontWeight.Regular,
		Enum.FontStyle.Normal
	),

	MichromaBold = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal),

	MichromaBoldItalic = Font.new(
		"rbxasset://fonts/families/Michroma.json",
		Enum.FontWeight.Bold,
		Enum.FontStyle.Italic
	),
}

Tokens.Corners = {
	Tiny = UDim.new(0.04, 0),
	Small = UDim.new(0.08, 0),
	Medium = UDim.new(0.12, 0),
	Large = UDim.new(0.16, 0),
	Round = UDim.new(1, 0),
}

Tokens.Strokes = {
	Hairline = 1,
	Thin = 1.25,
	Default = 2,
	Strong = 2.5,
	Thick = 3,
}

Tokens.Transparency = {
	Solid = 0,
	AlmostSolid = 0.05,
	Glass = 0.18,
	SoftGlass = 0.28,
	Muted = 0.45,
	Dim = 0.65,
	Hidden = 1,
}

Tokens.Timing = {
	Instant = 0,
	Fast = 0.12,
	Default = 0.18,
	Medium = 0.28,
	Slow = 0.38,

	Hover = 0.12,
	Open = 0.34,
	Close = 0.22,
	Fade = 0.16,
	CloseFade = 0.08,
}

Tokens.Easing = {
	OpenStyle = Enum.EasingStyle.Back,
	OpenDirection = Enum.EasingDirection.Out,

	CloseStyle = Enum.EasingStyle.Quad,
	CloseDirection = Enum.EasingDirection.Out,

	HoverStyle = Enum.EasingStyle.Quad,
	HoverDirection = Enum.EasingDirection.Out,

	SweepStyle = Enum.EasingStyle.Sine,
	SweepDirection = Enum.EasingDirection.InOut,
}

Tokens.ZIndex = {
	Background = 1,
	Content = 10,
	Overlay = 50,
	Tooltip = 100,
	Modal = 200,
}

return Tokens
