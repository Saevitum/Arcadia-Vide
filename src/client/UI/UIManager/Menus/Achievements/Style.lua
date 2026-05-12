--!strict

local Style = {}

Style.CYAN = Color3.fromRGB(0, 255, 238)
Style.MAGENTA = Color3.fromRGB(255, 0, 255)
Style.PINK = Color3.fromRGB(255, 83, 151)
Style.WHITE = Color3.fromRGB(255, 255, 255)

Style.DARK = Color3.fromRGB(5, 7, 13)
Style.DARK_ALT = Color3.fromRGB(16, 22, 30)

Style.FONT_BOLD_ITALIC =
	Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)

Style.CONTENT_SIZE = UDim2.fromScale(1, 1)

Style.TAB_STRIP_SIZE = UDim2.fromScale(0.74, 0.17)
Style.TAB_STRIP_POSITION = UDim2.fromScale(0.5, 0.28)
Style.TAB_STRIP_ANCHOR_POINT = Vector2.new(0.5, 0.5)

Style.TAB_BUTTON_SIZE = UDim2.fromScale(0.16, 0.25)
Style.TAB_BUTTON_CORNER_RADIUS = UDim.new(0.18, 0)

Style.TAB_ACTIVE_GRADIENT_KEYPOINTS = {
	{ time = 0, color = Color3.fromRGB(255, 128, 28) },
	{ time = 0.48, color = Color3.fromRGB(255, 67, 95) },
	{ time = 1, color = Color3.fromRGB(255, 0, 180) },
}

Style.TAB_INACTIVE_GRADIENT_KEYPOINTS = {
	{ time = 0, color = Color3.fromRGB(68, 74, 84) },
	{ time = 0.5, color = Color3.fromRGB(35, 41, 52) },
	{ time = 1, color = Color3.fromRGB(12, 16, 24) },
}

Style.TAB_STROKE_ACTIVE_KEYPOINTS = {
	{ time = 0, color = Style.CYAN },
	{ time = 1, color = Style.MAGENTA },
}

Style.TAB_STROKE_INACTIVE_KEYPOINTS = {
	{ time = 0, color = Color3.fromRGB(0, 125, 140) },
	{ time = 1, color = Color3.fromRGB(70, 35, 90) },
}

Style.PAGE_POSITION = UDim2.fromScale(0.5, 0.58)
Style.PAGE_SIZE = UDim2.fromScale(0.76, 0.43)
Style.PAGE_TRANSITION_DURATION = 0.28
Style.PAGE_FADE_DURATION = 0.2
Style.PAGE_CLOSE_FADE_DURATION = 0.12

Style.ROW_SIZE = UDim2.fromScale(0.96, 0.12)
Style.ROW_PADDING = UDim.new(0.04, 0)

Style.EMPTY_TEXT_COLOR = Color3.fromRGB(180, 205, 220)

return Style
