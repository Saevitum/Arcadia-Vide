--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

Vide.strict = true

local create = Vide.create

local Style = {}

Style.CYAN = Color3.fromRGB(0, 255, 238)
Style.MAGENTA = Color3.fromRGB(255, 0, 255)
Style.PINK = Color3.fromRGB(255, 83, 151)
Style.WHITE = Color3.fromRGB(255, 255, 255)
Style.DARK = Color3.fromRGB(9, 13, 22)
Style.DARK_ALT = Color3.fromRGB(19, 27, 38)
Style.DIMMED_KNOB = Color3.fromRGB(82, 91, 105)
Style.DIMMED_SLIDER_FILL = Color3.fromRGB(55, 60, 70)

Style.FONT_BOLD_ITALIC =
	Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)
Style.FONT_BOLD = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal)

Style.TAB_STRIP_SIZE = UDim2.fromScale(0.62, 0.06)
Style.TAB_STRIP_POSITION = UDim2.fromScale(0.5, 0.25)
Style.TAB_STRIP_ANCHOR_POINT = Vector2.new(0.5, 0.5)
Style.TAB_BUTTON_SIZE = UDim2.fromScale(0.26, 0.76)
Style.TAB_BUTTON_CORNER_RADIUS = UDim.new(0.22, 0)
Style.TAB_ACTIVE_GRADIENT_KEYPOINTS = {
	{ time = 0, color = Color3.fromRGB(255, 0, 123) },
	{ time = 0.71, color = Color3.fromRGB(220, 0, 106) },
	{ time = 1, color = Color3.fromRGB(134, 0, 65) },
}
Style.TAB_INACTIVE_GRADIENT_KEYPOINTS = {
	{ time = 0, color = Color3.fromRGB(98, 98, 98) },
	{ time = 0.71, color = Color3.fromRGB(66, 66, 57) },
	{ time = 1, color = Color3.fromRGB(25, 25, 25) },
}
Style.TAB_STROKE_GRADIENT = {
	keypoints = {
		{ time = 0, color = Color3.fromRGB(255, 0, 123) },
		{ time = 1, color = Color3.fromRGB(238, 0, 255) },
	},
	rotation = 0,
}
Style.TAB_INACTIVE_STROKE_GRADIENT_KEYPOINTS = {
	{ time = 0, color = Color3.fromRGB(74, 168, 255) },
	{ time = 1, color = Color3.fromRGB(30, 30, 30) },
}

Style.PAGE_POSITION = UDim2.fromScale(0.5, 0.575)
Style.PAGE_SIZE = UDim2.fromScale(0.76, 0.58)
Style.PAGE_TRANSITION_DURATION = 0.42
Style.PAGE_FADE_DURATION = 0.42
Style.PAGE_CLOSE_FADE_DURATION = 0.34

Style.VOLUME_SETTING_ROW_SIZE = UDim2.fromScale(0.94, 0.2)
Style.TOGGLE_SETTING_ROW_SIZE = UDim2.fromScale(0.94, 0.18)

Style.VOLUME_LABEL_SIZE = UDim2.fromScale(0.3, 0.26)
Style.VOLUME_LABEL_POSITION = UDim2.fromScale(0.18, 0.28)
Style.VOLUME_DESCRIPTION_SIZE = UDim2.fromScale(0.38, 0.28)
Style.VOLUME_DESCRIPTION_POSITION = UDim2.fromScale(0.53, 0.28)
Style.VOLUME_TOGGLE_SIZE = UDim2.fromScale(0.1, 0.5)
Style.VOLUME_TOGGLE_POSITION = UDim2.fromScale(0.95, 0.5)
Style.VOLUME_SLIDER_SIZE = UDim2.fromScale(0.53, 0.17)
Style.VOLUME_SLIDER_POSITION = UDim2.fromScale(0.4, 0.72)
Style.VOLUME_INPUT_SIZE = UDim2.fromScale(0.15, 0.34)
Style.VOLUME_INPUT_POSITION = UDim2.fromScale(0.77, 0.72)

Style.TOGGLE_LABEL_SIZE = UDim2.fromScale(0.31, 0.42)
Style.TOGGLE_LABEL_POSITION = UDim2.fromScale(0.18, 0.5)
Style.TOGGLE_DESCRIPTION_SIZE = UDim2.fromScale(0.39, 0.5)
Style.TOGGLE_DESCRIPTION_POSITION = UDim2.fromScale(0.53, 0.5)
Style.TOGGLE_BUTTON_SIZE = UDim2.fromScale(0.1, 0.5)
Style.TOGGLE_BUTTON_POSITION = UDim2.fromScale(0.95, 0.5)
Style.TOGGLE_SWITCH_SIZE = UDim2.fromScale(0.1, 0.5)
Style.TOGGLE_SWITCH_POSITION = UDim2.fromScale(0.95, 0.5)

Style.USER_SETTING_ROW_SIZE = UDim2.fromScale(0.94, 0.2)
Style.USER_LABEL_SIZE = UDim2.fromScale(0.31, 0.42)
Style.USER_LABEL_POSITION = UDim2.fromScale(0.18, 0.5)
Style.USER_DESCRIPTION_SIZE = UDim2.fromScale(0.55, 0.5)
Style.USER_DESCRIPTION_POSITION = UDim2.fromScale(0.626, 0.5)
Style.USER_TOGGLE_BUTTON_SIZE = UDim2.fromScale(0.1, 0.5)
Style.USER_TOGGLE_BUTTON_POSITION = UDim2.fromScale(0.95, 0.5)

Style.GAME_SETTING_ROW_SIZE = UDim2.fromScale(0.94, 0.2)
Style.GAME_LABEL_SIZE = UDim2.fromScale(0.31, 0.42)
Style.GAME_LABEL_POSITION = UDim2.fromScale(0.18, 0.5)
Style.GAME_DESCRIPTION_SIZE = UDim2.fromScale(0.55, 0.5)
Style.GAME_DESCRIPTION_POSITION = UDim2.fromScale(0.626, 0.5)
Style.GAME_TOGGLE_BUTTON_SIZE = UDim2.fromScale(0.1, 0.5)
Style.GAME_TOGGLE_BUTTON_POSITION = UDim2.fromScale(0.95, 0.5)

Style.TOGGLE_SETTING_ROW_LAYOUT = {
	rowSize = Style.TOGGLE_SETTING_ROW_SIZE,
	labelSize = Style.TOGGLE_LABEL_SIZE,
	labelPosition = Style.TOGGLE_LABEL_POSITION,
	descriptionSize = Style.TOGGLE_DESCRIPTION_SIZE,
	descriptionPosition = Style.TOGGLE_DESCRIPTION_POSITION,
	toggleButtonSize = Style.TOGGLE_BUTTON_SIZE,
	toggleButtonPosition = Style.TOGGLE_BUTTON_POSITION,
}

Style.USER_SETTING_ROW_LAYOUT = {
	rowSize = Style.USER_SETTING_ROW_SIZE,
	labelSize = Style.USER_LABEL_SIZE,
	labelPosition = Style.USER_LABEL_POSITION,
	descriptionSize = Style.USER_DESCRIPTION_SIZE,
	descriptionPosition = Style.USER_DESCRIPTION_POSITION,
	toggleButtonSize = Style.USER_TOGGLE_BUTTON_SIZE,
	toggleButtonPosition = Style.USER_TOGGLE_BUTTON_POSITION,
}

Style.GAME_SETTING_ROW_LAYOUT = {
	rowSize = Style.GAME_SETTING_ROW_SIZE,
	labelSize = Style.GAME_LABEL_SIZE,
	labelPosition = Style.GAME_LABEL_POSITION,
	descriptionSize = Style.GAME_DESCRIPTION_SIZE,
	descriptionPosition = Style.GAME_DESCRIPTION_POSITION,
	toggleButtonSize = Style.GAME_TOGGLE_BUTTON_SIZE,
	toggleButtonPosition = Style.GAME_TOGGLE_BUTTON_POSITION,
}

function Style.NeonStroke(thickness: number?, transparency: number?)
	return create("UIStroke")({
		Thickness = thickness or 2,
		Transparency = transparency or 0.08,
		Color = Style.WHITE,
		ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

		create("UIGradient")({
			Rotation = 0,
			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, Style.CYAN),
				ColorSequenceKeypoint.new(0.55, Color3.fromRGB(95, 82, 255)),
				ColorSequenceKeypoint.new(1, Style.MAGENTA),
			}),
		}),
	})
end

function Style.RowGradient()
	return create("UIGradient")({
		Rotation = 0,
		Color = ColorSequence.new({
			ColorSequenceKeypoint.new(0, Color3.fromRGB(18, 27, 38)),
			ColorSequenceKeypoint.new(0.52, Color3.fromRGB(24, 31, 43)),
			ColorSequenceKeypoint.new(1, Color3.fromRGB(15, 18, 27)),
		}),
		Transparency = NumberSequence.new({
			NumberSequenceKeypoint.new(0, 0.03),
			NumberSequenceKeypoint.new(0.72, 0.1),
			NumberSequenceKeypoint.new(1, 0.18),
		}),
	})
end

return Style
