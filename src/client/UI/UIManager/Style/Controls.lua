--!strict

local Tokens = require(script.Parent.Tokens)

local Controls = {}

Controls.Settings = {
	Colors = {
		Cyan = Color3.fromRGB(0, 255, 238),
		Magenta = Color3.fromRGB(255, 0, 255),
		Pink = Color3.fromRGB(255, 83, 151),

		White = Color3.fromRGB(255, 255, 255),
		Dark = Color3.fromRGB(9, 13, 22),
		DarkAlt = Color3.fromRGB(19, 27, 38),

		DimmedRow = Color3.fromRGB(13, 17, 25),
		DimmedKnob = Color3.fromRGB(82, 91, 105),
		DimmedSliderFill = Color3.fromRGB(55, 60, 70),

		MutedText = Color3.fromRGB(145, 152, 165),
		ToggleText = Color3.fromRGB(5, 22, 25),
		ToggleOnText = Color3.fromRGB(35, 8, 22),
	},

	Fonts = {
		BoldItalic = Tokens.Fonts.MichromaBoldItalic,
		Bold = Tokens.Fonts.MichromaBold,
	},

	Layouts = {
		VolumeRow = {
			rowSize = UDim2.fromScale(0.94, 0.2),

			labelSize = UDim2.fromScale(0.3, 0.26),
			labelPosition = UDim2.fromScale(0.18, 0.28),

			descriptionSize = UDim2.fromScale(0.38, 0.28),
			descriptionPosition = UDim2.fromScale(0.53, 0.28),

			toggleButtonSize = UDim2.fromScale(0.1, 0.5),
			toggleButtonPosition = UDim2.fromScale(0.95, 0.5),

			sliderSize = UDim2.fromScale(0.53, 0.17),
			sliderPosition = UDim2.fromScale(0.4, 0.72),

			inputSize = UDim2.fromScale(0.15, 0.34),
			inputPosition = UDim2.fromScale(0.77, 0.72),
		},

		ToggleRow = {
			rowSize = UDim2.fromScale(0.94, 0.18),

			labelSize = UDim2.fromScale(0.31, 0.42),
			labelPosition = UDim2.fromScale(0.18, 0.5),

			descriptionSize = UDim2.fromScale(0.39, 0.5),
			descriptionPosition = UDim2.fromScale(0.53, 0.5),

			toggleButtonSize = UDim2.fromScale(0.1, 0.5),
			toggleButtonPosition = UDim2.fromScale(0.95, 0.5),
		},

		UserToggleRow = {
			rowSize = UDim2.fromScale(0.94, 0.2),

			labelSize = UDim2.fromScale(0.31, 0.42),
			labelPosition = UDim2.fromScale(0.18, 0.5),

			descriptionSize = UDim2.fromScale(0.55, 0.5),
			descriptionPosition = UDim2.fromScale(0.626, 0.5),

			toggleButtonSize = UDim2.fromScale(0.1, 0.5),
			toggleButtonPosition = UDim2.fromScale(0.95, 0.5),
		},

		GameToggleRow = {
			rowSize = UDim2.fromScale(0.94, 0.2),

			labelSize = UDim2.fromScale(0.31, 0.42),
			labelPosition = UDim2.fromScale(0.18, 0.5),

			descriptionSize = UDim2.fromScale(0.55, 0.5),
			descriptionPosition = UDim2.fromScale(0.626, 0.5),

			toggleButtonSize = UDim2.fromScale(0.1, 0.5),
			toggleButtonPosition = UDim2.fromScale(0.95, 0.5),
		},
	},

	Row = {
		cornerRadius = UDim.new(0.18, 0),
		backgroundTransparency = 0.08,
		dimmedBackgroundTransparency = 0.2,

		strokeThickness = 2,
		strokeTransparency = 0.05,
	},

	NumberInput = {
		cornerRadius = UDim.new(0.22, 0),
		textBoxSize = UDim2.fromScale(0.64, 0.82),
		textBoxPosition = UDim2.fromScale(0.38, 0.5),

		caretSize = UDim2.fromScale(0.018, 0.55),
		caretPosition = UDim2.fromScale(0.66, 0.5),

		percentSize = UDim2.fromScale(0.24, 0.78),
		percentPosition = UDim2.fromScale(0.85, 0.5),
	},
}

return Controls
