#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apply Settings menu shared-style migration.

Run from the Arcadia-Vide repo root:

    python apply_settings_shared_style_v1.py

This updates:
- UIManager/Style/Pages.lua
- UIManager/Style/Controls.lua
- UIManager/Style/Decorators.lua
- UIManager/Style/init.lua
- UIManager/Menus/Settings/init.lua
- UIManager/Menus/Settings/SettingsPage.lua
- UIManager/Menus/Settings/SettingsRow.lua
- UIManager/Menus/Settings/VolumeSettingRow.lua
- UIManager/Menus/Settings/ToggleSettingRow.lua
- UIManager/Menus/Settings/NumberInput.lua
- UIManager/Menus/Settings/UserSettingsPage.lua
- UIManager/Menus/Settings/GameSettingsPage.lua
- UIManager/Menus/Settings/VolumeSettingsPage.lua

It does NOT delete old Settings/Style.lua, Settings/TabButton.lua, or Settings/TabStrip.lua.
Delete those after typecheck confirms no module requires them.
"""

from pathlib import Path
import shutil

ROOT = Path.cwd()
BASE = ROOT / "src" / "client" / "UI" / "UIManager"
BACKUP = ROOT / "_local_backups" / "settings_shared_style_v1"

FILES = {
BASE / "Style" / "Pages.lua": r'''--!strict

local Tokens = require(script.Parent.Tokens)
local Gradients = require(script.Parent.Gradients)

local Pages = {}

Pages.Layouts = {
	WideLower = {
		size = UDim2.fromScale(0.76, 0.43),
		position = UDim2.fromScale(0.5, 0.58),
		anchorPoint = Vector2.new(0.5, 0.5),
	},

	SettingsMain = {
		size = UDim2.fromScale(0.76, 0.58),
		position = UDim2.fromScale(0.5, 0.575),
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

	SettingsSoft = {
		duration = 0.42,
		fadeDuration = 0.42,
		closeFadeDuration = 0.34,

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
''',

BASE / "Style" / "Controls.lua": r'''--!strict

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
''',

BASE / "Style" / "Decorators.lua": r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Controls = require(script.Parent.Controls)

Vide.strict = true

local create = Vide.create

local Decorators = {}

local SETTINGS_COLORS = Controls.Settings.Colors

function Decorators.NeonStroke(thickness: number?, transparency: number?)
	return create("UIStroke")({
		Thickness = thickness or 2,
		Transparency = transparency or 0.08,
		Color = SETTINGS_COLORS.White,
		ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

		create("UIGradient")({
			Rotation = 0,

			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, SETTINGS_COLORS.Cyan),
				ColorSequenceKeypoint.new(0.55, Color3.fromRGB(95, 82, 255)),
				ColorSequenceKeypoint.new(1, SETTINGS_COLORS.Magenta),
			}),
		}),
	})
end

function Decorators.RowGradient()
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

return Decorators
''',

BASE / "Style" / "init.lua": r'''--!strict

local Style = {}

Style.Merge = require(script.Merge)
Style.Tokens = require(script.Tokens)
Style.Gradients = require(script.Gradients)

Style.Tabs = require(script.Tabs)
Style.Pages = require(script.Pages)
Style.Rows = require(script.Rows)
Style.Controls = require(script.Controls)
Style.Decorators = require(script.Decorators)

return Style
''',
}

# Add long Settings files after the short shared style files.
FILES.update({
BASE / "Menus" / "Settings" / "SettingsPage.lua": r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)

local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local create = Vide.create

local ScrollArea = Components.ScrollArea

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type SettingsPageProps = {
	tab: SettingsTab,
	selectedTab: Source<SettingsTab>,
	layoutOrder: number,
	zIndex: number,
	children: { Instance },
}

local PAGE_LAYOUT = Style.Pages.Layouts.SettingsMain
local PAGE_TRANSITION = Style.Pages.Transitions.SettingsSoft
local SETTINGS_COLORS = Style.Controls.Settings.Colors

local function SettingsPage(props: SettingsPageProps)
	return create("CanvasGroup")({
		Name = `{props.tab}Page`,

		Size = PAGE_LAYOUT.size,
		Position = PAGE_LAYOUT.position,
		AnchorPoint = PAGE_LAYOUT.anchorPoint,

		LayoutOrder = props.layoutOrder,

		Visible = false,
		GroupTransparency = 1,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = function()
			if props.selectedTab() == props.tab then
				return props.zIndex + 1
			end

			return props.zIndex
		end,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return props.selectedTab() == props.tab
			end,

			openPosition = PAGE_LAYOUT.position,
			closedPosition = PAGE_LAYOUT.position,

			openTransparency = 0,
			closedTransparency = 1,

			duration = PAGE_TRANSITION.duration,
			fadeDuration = PAGE_TRANSITION.fadeDuration,
			closeFadeDuration = PAGE_TRANSITION.closeFadeDuration,

			easingStyle = PAGE_TRANSITION.easingStyle,
			easingDirection = PAGE_TRANSITION.easingDirection,

			fadeEasingStyle = PAGE_TRANSITION.fadeEasingStyle,
			fadeEasingDirection = PAGE_TRANSITION.fadeEasingDirection,

			hideWhenClosed = true,
		}),

		ScrollArea({
			name = `{props.tab}ScrollArea`,

			size = UDim2.fromScale(1, 1),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			zIndex = props.zIndex + 1,

			backgroundTransparency = 1,
			backgroundColor3 = Color3.fromRGB(0, 0, 0),

			layoutKind = "List",

			padding = {
				top = UDim.new(0.035, 0),
				bottom = UDim.new(0.05, 0),
				left = UDim.new(0.02, 0),
				right = UDim.new(0.02, 0),
			},

			list = {
				padding = UDim.new(0.035, 0),
				fillDirection = Enum.FillDirection.Vertical,
				horizontalAlignment = Enum.HorizontalAlignment.Center,
				verticalAlignment = Enum.VerticalAlignment.Top,
				sortOrder = Enum.SortOrder.LayoutOrder,
			},

			scrollBarThickness = 6,
			scrollBarImageColor3 = SETTINGS_COLORS.Cyan,
			scrollBarImageTransparency = 0.15,

			automaticCanvasSize = Enum.AutomaticSize.Y,
			canvasSize = UDim2.fromScale(0, 0),
			scrollingDirection = Enum.ScrollingDirection.Y,

			children = props.children,
		}),
	})
end

return SettingsPage
''',

BASE / "Menus" / "Settings" / "SettingsRow.lua": r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local create = Vide.create

export type SettingsRowProps = {
	name: string,
	layoutOrder: number,
	size: UDim2,
	zIndex: number,
	dimmed: (() -> boolean)?,
	children: { Instance },
}

local SETTINGS = Style.Controls.Settings
local COLORS = SETTINGS.Colors
local ROW = SETTINGS.Row

local function SettingsRow(props: SettingsRowProps)
	return create("Frame")({
		Name = props.name,

		Size = props.size,
		LayoutOrder = props.layoutOrder,

		BackgroundColor3 = function()
			if props.dimmed ~= nil and props.dimmed() then
				return COLORS.DimmedRow
			end

			return COLORS.DarkAlt
		end,

		BackgroundTransparency = function()
			if props.dimmed ~= nil and props.dimmed() then
				return ROW.dimmedBackgroundTransparency
			end

			return ROW.backgroundTransparency
		end,

		BorderSizePixel = 0,
		ZIndex = props.zIndex,

		create("UICorner")({
			CornerRadius = ROW.cornerRadius,
		}),

		Style.Decorators.RowGradient(),
		Style.Decorators.NeonStroke(ROW.strokeThickness, ROW.strokeTransparency),

		props.children,
	})
end

return SettingsRow
''',

BASE / "Menus" / "Settings" / "VolumeSettingRow.lua": r'''--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)

local Components = require(script.Parent.Parent.Parent.Components)
local Style = require(script.Parent.Parent.Parent.Style)

local NumberInput = require(script.Parent.NumberInput)
local SettingsRow = require(script.Parent.SettingsRow)

local Text = Components.Text
local Slider = Components.Slider
local ToggleButton = Components.ToggleButton

type Source<T> = SharedTypes.Source<T>

export type VolumeSettingRowProps = {
	name: string,
	label: string,
	description: string,
	value: Source<number>,
	muted: Source<boolean>,
	layoutOrder: number,
	zIndex: number,
}

local SETTINGS = Style.Controls.Settings
local COLORS = SETTINGS.Colors
local FONTS = SETTINGS.Fonts
local LAYOUT = SETTINGS.Layouts.VolumeRow

local function VolumeSettingRow(props: VolumeSettingRowProps)
	return SettingsRow({
		name = props.name,
		layoutOrder = props.layoutOrder,
		size = LAYOUT.rowSize,
		zIndex = props.zIndex,
		dimmed = props.muted,

		children = {
			Text({
				name = "Label",
				text = props.label,

				size = LAYOUT.labelSize,
				position = LAYOUT.labelPosition,
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = FONTS.BoldItalic,
				textScaled = true,
				minTextSize = 8,
				maxTextSize = 22,

				textColor3 = COLORS.Cyan,
				textXAlignment = Enum.TextXAlignment.Left,
				textYAlignment = Enum.TextYAlignment.Center,

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.35,
				},

				zIndex = props.zIndex + 1,
			}),

			Text({
				name = "Description",
				text = props.description,

				size = LAYOUT.descriptionSize,
				position = LAYOUT.descriptionPosition,
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = FONTS.BoldItalic,
				textScaled = true,
				minTextSize = 7,
				maxTextSize = 16,

				textColor3 = COLORS.Pink,
				textXAlignment = Enum.TextXAlignment.Left,
				textYAlignment = Enum.TextYAlignment.Center,

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.45,
				},

				zIndex = props.zIndex + 1,
			}),

			ToggleButton({
				name = "MuteToggle",
				value = props.muted,

				size = LAYOUT.toggleButtonSize,
				position = LAYOUT.toggleButtonPosition,
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = props.zIndex + 1,

				textOn = "OFF",
				textOff = "ON",

				fontFace = FONTS.Bold,
				textColor3 = COLORS.ToggleText,
				onTextColor3 = COLORS.ToggleOnText,

				strokeColor3 = COLORS.Cyan,
				onStrokeColor3 = COLORS.Pink,
				strokeThickness = 2,
				strokeTransparency = 0.02,

				cornerRadius = UDim.new(0.16, 0),

				minTextSize = 7,
				maxTextSize = 13,
			}),

			Slider({
				name = "VolumeSlider",

				value = props.value,
				min = 0,
				max = 100,
				step = 1,
				dimmed = props.muted,

				size = LAYOUT.sliderSize,
				position = LAYOUT.sliderPosition,
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = props.zIndex + 1,

				backgroundColor3 = COLORS.Dark,

				fillColor3 = function()
					if props.muted() then
						return COLORS.DimmedSliderFill
					end

					return COLORS.White
				end,

				fillGradient = function()
					if props.muted() then
						return ColorSequence.new(COLORS.DimmedSliderFill)
					end

					return ColorSequence.new({
						ColorSequenceKeypoint.new(0, COLORS.Cyan),
						ColorSequenceKeypoint.new(1, COLORS.Magenta),
					})
				end,

				fillGradientEffect = {
					enabled = function()
						return not props.muted()
					end,

					duration = 4.2,
					primaryColor = COLORS.Cyan,
					secondaryColor = COLORS.Magenta,
					disabledColor = COLORS.DimmedSliderFill,
				},

				knobColor3 = COLORS.White,
				dimmedKnobColor3 = COLORS.DimmedKnob,

				strokeColor3 = function()
					if props.muted() then
						return COLORS.DimmedSliderFill
					end

					return COLORS.Cyan
				end,

				strokeThickness = 1,
				strokeTransparency = 0.12,
				dimmedFillTransparency = 0.08,
			}),

			NumberInput({
				name = "PercentInput",

				value = props.value,
				muted = props.muted,

				size = LAYOUT.inputSize,
				position = LAYOUT.inputPosition,

				zIndex = props.zIndex + 1,
			}),
		},
	})
end

return VolumeSettingRow
''',
})

# Add the rest from embedded smaller external files to keep this script readable.
FILES[BASE / "Menus" / "Settings" / "ToggleSettingRow.lua"] = r'''--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)

local Components = require(script.Parent.Parent.Parent.Components)
local Style = require(script.Parent.Parent.Parent.Style)

local SettingsRow = require(script.Parent.SettingsRow)

local Text = Components.Text
local ToggleButton = Components.ToggleButton

type Source<T> = SharedTypes.Source<T>

export type ToggleSettingRowLayout = {
	rowSize: UDim2,
	labelSize: UDim2,
	labelPosition: UDim2,
	descriptionSize: UDim2,
	descriptionPosition: UDim2,
	toggleButtonSize: UDim2,
	toggleButtonPosition: UDim2,
}

export type ToggleSettingRowProps = {
	name: string,
	label: string,
	description: string,
	value: Source<boolean>,
	layoutOrder: number,
	zIndex: number,
	layout: ToggleSettingRowLayout?,
}

local SETTINGS = Style.Controls.Settings
local COLORS = SETTINGS.Colors
local FONTS = SETTINGS.Fonts

local function ToggleSettingRow(props: ToggleSettingRowProps)
	local layout = props.layout or SETTINGS.Layouts.ToggleRow

	return SettingsRow({
		name = props.name,
		layoutOrder = props.layoutOrder,
		size = layout.rowSize,
		zIndex = props.zIndex,

		children = {
			Text({
				name = "Label",
				text = props.label,
				size = layout.labelSize,
				position = layout.labelPosition,
				anchorPoint = Vector2.new(0.5, 0.5),
				fontFace = FONTS.BoldItalic,
				textScaled = true,
				minTextSize = 8,
				maxTextSize = 20,
				textColor3 = COLORS.Cyan,
				textXAlignment = Enum.TextXAlignment.Left,
				textYAlignment = Enum.TextYAlignment.Center,
				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.35,
				},
				zIndex = props.zIndex + 1,
			}),

			Text({
				name = "Description",
				text = props.description,
				size = layout.descriptionSize,
				position = layout.descriptionPosition,
				anchorPoint = Vector2.new(0.5, 0.5),
				fontFace = FONTS.BoldItalic,
				textScaled = true,
				minTextSize = 7,
				maxTextSize = 15,
				textColor3 = COLORS.Pink,
				textXAlignment = Enum.TextXAlignment.Left,
				textYAlignment = Enum.TextYAlignment.Center,
				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.45,
				},
				zIndex = props.zIndex + 1,
			}),

			ToggleButton({
				name = "Toggle",
				value = props.value,
				size = layout.toggleButtonSize,
				position = layout.toggleButtonPosition,
				anchorPoint = Vector2.new(0.5, 0.5),
				zIndex = props.zIndex + 1,
				textOn = "OFF",
				textOff = "ON",
				fontFace = FONTS.Bold,
				textColor3 = COLORS.ToggleText,
				onTextColor3 = COLORS.ToggleOnText,
				strokeColor3 = COLORS.Cyan,
				onStrokeColor3 = COLORS.Pink,
				strokeThickness = 2,
				strokeTransparency = 0.02,
				cornerRadius = UDim.new(0.16, 0),
				minTextSize = 7,
				maxTextSize = 13,
			}),
		},
	})
end

return ToggleSettingRow
'''

FILES[BASE / "Menus" / "Settings" / "NumberInput.lua"] = r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local create = Vide.create
local effect = Vide.effect
local source = Vide.source

local Text = Components.Text

type Source<T> = SharedTypes.Source<T>

export type NumberInputProps = {
	name: string,
	value: Source<number>,
	muted: Source<boolean>,
	size: UDim2,
	position: UDim2,
	anchorPoint: Vector2?,
	zIndex: number,
}

local SETTINGS = Style.Controls.Settings
local COLORS = SETTINGS.Colors
local FONTS = SETTINGS.Fonts
local INPUT = SETTINGS.NumberInput

local function clampPercent(value: number): number
	return math.clamp(math.round(value), 0, 100)
end

local function formatPercent(value: number): string
	return tostring(clampPercent(value))
end

local function NumberInput(props: NumberInputProps)
	local textBox: TextBox? = nil
	local focused = source(false)
	local draftText = source("")

	local function commitText()
		if textBox == nil then
			return
		end

		local cleanedText = string.gsub(textBox.Text, "%%", "")
		cleanedText = string.gsub(cleanedText, "%s", "")

		local parsed = tonumber(cleanedText)

		if parsed == nil then
			textBox.Text = formatPercent(props.value())
			return
		end

		local nextValue = clampPercent(parsed)

		props.value(nextValue)
		textBox.Text = formatPercent(nextValue)
	end

	return create("Frame")({
		Name = props.name,
		Size = props.size,
		Position = props.position,
		AnchorPoint = props.anchorPoint or Vector2.new(0.5, 0.5),
		BackgroundColor3 = COLORS.Dark,
		BackgroundTransparency = function()
			if props.muted() then
				return 0.28
			end
			return 0.03
		end,
		BorderSizePixel = 0,
		ZIndex = props.zIndex,

		create("UICorner")({ CornerRadius = INPUT.cornerRadius }),
		Style.Decorators.NeonStroke(1, 0.12),

		create("TextBox")({
			Name = "Input",
			Size = INPUT.textBoxSize,
			Position = INPUT.textBoxPosition,
			AnchorPoint = Vector2.new(0.5, 0.5),
			Text = function()
				if focused() then
					return ""
				end
				return formatPercent(props.value())
			end,
			PlaceholderText = "",
			PlaceholderColor3 = Color3.fromRGB(150, 160, 170),
			ClearTextOnFocus = false,
			TextEditable = true,
			MultiLine = false,
			FontFace = FONTS.Bold,
			TextScaled = true,
			TextTransparency = function()
				if focused() then
					return 1
				end
				return 0
			end,
			TextColor3 = function()
				if props.muted() then
					return COLORS.MutedText
				end
				return COLORS.White
			end,
			TextStrokeTransparency = 0.55,
			TextXAlignment = Enum.TextXAlignment.Right,
			TextYAlignment = Enum.TextYAlignment.Center,
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = props.zIndex + 1,
			Focused = function()
				focused(true)
				draftText("")
				if textBox ~= nil then
					textBox.Text = ""
				end
			end,
			FocusLost = function(_enterPressed: boolean)
				commitText()
				focused(false)
			end,
			action(function(instance: Instance)
				if not instance:IsA("TextBox") then
					return
				end
				textBox = instance
				local textChanged = instance:GetPropertyChangedSignal("Text"):Connect(function()
					draftText(instance.Text)
				end)
				cleanup(function()
					textChanged:Disconnect()
					if textBox == instance then
						textBox = nil
					end
				end)
			end),
			create("UITextSizeConstraint")({ MinTextSize = 7, MaxTextSize = 16 }),
		}),

		Text({
			name = "DraftText",
			text = function() return draftText() end,
			size = INPUT.textBoxSize,
			position = INPUT.textBoxPosition,
			anchorPoint = Vector2.new(0.5, 0.5),
			visible = function() return focused() end,
			fontFace = FONTS.Bold,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,
			textColor3 = function()
				if props.muted() then
					return COLORS.MutedText
				end
				return COLORS.White
			end,
			textXAlignment = Enum.TextXAlignment.Right,
			textYAlignment = Enum.TextYAlignment.Center,
			zIndex = props.zIndex + 2,
		}),

		create("Frame")({
			Name = "InputCaretPulse",
			Size = INPUT.caretSize,
			Position = INPUT.caretPosition,
			AnchorPoint = Vector2.new(0.5, 0.5),
			Visible = function() return focused() end,
			BackgroundColor3 = function()
				if props.muted() then
					return COLORS.MutedText
				end
				return COLORS.Cyan
			end,
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = props.zIndex + 3,
			action(function(instance: Instance)
				if not instance:IsA("Frame") then
					return
				end
				local caret = instance :: Frame
				local activeTween: Tween? = nil
				local function stopTween()
					if activeTween ~= nil then
						activeTween:Cancel()
						activeTween = nil
					end
				end
				effect(function()
					stopTween()
					if not focused() then
						caret.BackgroundTransparency = 1
						return
					end
					caret.BackgroundTransparency = 0.05
					local tween = TweenService:Create(
						caret,
						TweenInfo.new(0.46, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut, -1, true),
						{ BackgroundTransparency = 0.85 }
					)
					activeTween = tween
					tween:Play()
				end)
				cleanup(function() stopTween() end)
			end),
			create("UICorner")({ CornerRadius = UDim.new(0.5, 0) }),
		}),

		Text({
			name = "Percent",
			text = "%",
			size = INPUT.percentSize,
			position = INPUT.percentPosition,
			anchorPoint = Vector2.new(0.5, 0.5),
			fontFace = FONTS.Bold,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 14,
			textColor3 = function()
				if props.muted() then
					return COLORS.MutedText
				end
				return COLORS.Cyan
			end,
			textXAlignment = Enum.TextXAlignment.Left,
			textYAlignment = Enum.TextYAlignment.Center,
			zIndex = props.zIndex + 1,
		}),
	})
end

return NumberInput
'''

FILES[BASE / "Menus" / "Settings" / "UserSettingsPage.lua"] = r'''--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Style = require(script.Parent.Parent.Parent.Style)
local SettingsPage = require(script.Parent.SettingsPage)
local ToggleSettingRow = require(script.Parent.ToggleSettingRow)

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type UserSettingsPageProps = {
	selectedTab: Source<SettingsTab>,
	hideYourRank: Source<boolean>,
	hideOthersRank: Source<boolean>,
	hideYourNameplate: Source<boolean>,
	hideOthersNameplate: Source<boolean>,
}

local USER_TOGGLE_LAYOUT = Style.Controls.Settings.Layouts.UserToggleRow

local function UserSettingsPage(props: UserSettingsPageProps)
	return SettingsPage({
		tab = "User",
		selectedTab = props.selectedTab,
		layoutOrder = 2,
		zIndex = 20,
		children = {
			ToggleSettingRow({ name = "HideYourRankRow", label = "Hide Your Rank", description = "Other players will not see your rank.", value = props.hideYourRank, layoutOrder = 1, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "HideOthersRankRow", label = "Hide Others Rank", description = "You will not see other player ranks.", value = props.hideOthersRank, layoutOrder = 2, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "HideYourNameplateRow", label = "Hide Your Nameplate", description = "Your nameplate is hidden from view.", value = props.hideYourNameplate, layoutOrder = 3, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "HideOthersNameplateRow", label = "Hide Others Nameplate", description = "You will not see other players nameplate.", value = props.hideOthersNameplate, layoutOrder = 4, zIndex = 24, layout = USER_TOGGLE_LAYOUT }),
		},
	})
end

return UserSettingsPage
'''

FILES[BASE / "Menus" / "Settings" / "GameSettingsPage.lua"] = r'''--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Style = require(script.Parent.Parent.Parent.Style)
local SettingsPage = require(script.Parent.SettingsPage)
local ToggleSettingRow = require(script.Parent.ToggleSettingRow)

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type GameSettingsPageProps = {
	selectedTab: Source<SettingsTab>,
	hidePopups: Source<boolean>,
	disableVFX: Source<boolean>,
	disableCameraShake: Source<boolean>,
}

local GAME_TOGGLE_LAYOUT = Style.Controls.Settings.Layouts.GameToggleRow

local function GameSettingsPage(props: GameSettingsPageProps)
	return SettingsPage({
		tab = "Game",
		selectedTab = props.selectedTab,
		layoutOrder = 3,
		zIndex = 20,
		children = {
			ToggleSettingRow({ name = "HidePopupsRow", label = "Hide Popups", description = "Reduce non-critical popup messages.", value = props.hidePopups, layoutOrder = 1, zIndex = 24, layout = GAME_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "DisableVFXRow", label = "Disable VFX", description = "Reduce visual effects intensity.", value = props.disableVFX, layoutOrder = 2, zIndex = 24, layout = GAME_TOGGLE_LAYOUT }),
			ToggleSettingRow({ name = "DisableCameraShakeRow", label = "Disable Camera Shake", description = "Turn off camera shake effects.", value = props.disableCameraShake, layoutOrder = 3, zIndex = 24, layout = GAME_TOGGLE_LAYOUT }),
		},
	})
end

return GameSettingsPage
'''

FILES[BASE / "Menus" / "Settings" / "VolumeSettingsPage.lua"] = r'''--!strict

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local SettingsPage = require(script.Parent.SettingsPage)
local VolumeSettingRow = require(script.Parent.VolumeSettingRow)

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab

export type VolumeSettingsPageProps = {
	selectedTab: Source<SettingsTab>,
	masterVolume: Source<number>,
	sfxVolume: Source<number>,
	musicVolume: Source<number>,
	masterMuted: Source<boolean>,
	sfxMuted: Source<boolean>,
	musicMuted: Source<boolean>,
}

local function VolumeSettingsPage(props: VolumeSettingsPageProps)
	return SettingsPage({
		tab = "Volume",
		selectedTab = props.selectedTab,
		layoutOrder = 1,
		zIndex = 20,
		children = {
			VolumeSettingRow({ name = "MasterVolumeRow", label = "Master Volume", description = "Controls every sound in the game.", value = props.masterVolume, muted = props.masterMuted, layoutOrder = 1, zIndex = 24 }),
			VolumeSettingRow({ name = "SFXVolumeRow", label = "SFX Volume", description = "Controls interface and gameplay sounds.", value = props.sfxVolume, muted = props.sfxMuted, layoutOrder = 2, zIndex = 24 }),
			VolumeSettingRow({ name = "MusicVolumeRow", label = "Music Volume", description = "Controls background music.", value = props.musicVolume, muted = props.musicMuted, layoutOrder = 3, zIndex = 24 }),
		},
	})
end

return VolumeSettingsPage
'''

FILES[BASE / "Menus" / "Settings" / "init.lua"] = r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local SharedTypes = require(script.Parent.Parent.UITypes.SharedTypes)
local ComponentTypes = require(script.Parent.Parent.UITypes.ComponentTypes)
local Components = require(script.Parent.Parent.Components)
local Tabs = require(script.Parent.Parent.Components.Tabs)
local Style = require(script.Parent.Parent.Style)
local GameSettingsPage = require(script.GameSettingsPage)
local UserSettingsPage = require(script.UserSettingsPage)
local VolumeSettingsPage = require(script.VolumeSettingsPage)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local Panel = Components.Panel

type Source<T> = SharedTypes.Source<T>
type SettingsTab = Types.SettingsTab
type TabDefinition<T> = ComponentTypes.TabDefinition<T>

local SETTINGS_TABS: { TabDefinition<SettingsTab> } = {
	{ id = "Volume", label = "VOLUME", layoutOrder = 1, disabled = false, hasAlert = false },
	{ id = "User", label = "USER", layoutOrder = 2, disabled = false, hasAlert = false },
	{ id = "Game", label = "GAME", layoutOrder = 3, disabled = false, hasAlert = false },
}

local TAB_LAYOUT = Style.Tabs.Layouts.SettingsThree
local TAB_STYLE = Style.Tabs.Presets.SettingsPink

local function SettingsMenu(props: Types.SettingsMenuProps)
	local selectedTab: Source<SettingsTab> = source("Volume" :: SettingsTab)
	local masterVolume: Source<number> = source(75)
	local sfxVolume: Source<number> = source(80)
	local musicVolume: Source<number> = source(65)
	local masterMuted: Source<boolean> = source(false)
	local sfxMuted: Source<boolean> = source(false)
	local musicMuted: Source<boolean> = source(false)
	local hideYourRank: Source<boolean> = source(false)
	local hideOthersRank: Source<boolean> = source(false)
	local hideYourNameplate: Source<boolean> = source(false)
	local hideOthersNameplate: Source<boolean> = source(false)
	local hidePopups: Source<boolean> = source(false)
	local disableVFX: Source<boolean> = source(false)
	local disableCameraShake: Source<boolean> = source(false)

	return Panel({
		name = "SettingsMenu",
		store = props.store,
		menuId = "Settings",
		title = "SETTINGS",
		content = create("Frame")({
			Name = "SettingsContent",
			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			Tabs.TabStrip({
				name = "SettingsTabStrip",
				tabs = SETTINGS_TABS,
				selectedTab = selectedTab,
				size = TAB_LAYOUT.size,
				position = TAB_LAYOUT.position,
				anchorPoint = TAB_LAYOUT.anchorPoint,
				cellSize = TAB_LAYOUT.cellSize,
				cellPadding = TAB_LAYOUT.cellPadding,
				fillDirectionMaxCells = TAB_LAYOUT.fillDirectionMaxCells,
				style = TAB_STYLE,
				zIndex = 21,
			}),

			VolumeSettingsPage({ selectedTab = selectedTab, masterVolume = masterVolume, sfxVolume = sfxVolume, musicVolume = musicVolume, masterMuted = masterMuted, sfxMuted = sfxMuted, musicMuted = musicMuted }),
			UserSettingsPage({ selectedTab = selectedTab, hideYourRank = hideYourRank, hideOthersRank = hideOthersRank, hideYourNameplate = hideYourNameplate, hideOthersNameplate = hideOthersNameplate }),
			GameSettingsPage({ selectedTab = selectedTab, hidePopups = hidePopups, disableVFX = disableVFX, disableCameraShake = disableCameraShake }),
		}),
	})
end

return SettingsMenu
'''

def backup_file(path: Path) -> None:
    if not path.exists():
        return
    rel = path.relative_to(ROOT)
    target = BACKUP / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_file(path)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    if not BASE.exists():
        raise SystemExit(f"Could not find UIManager folder: {BASE}")

    for path, text in FILES.items():
        write_file(path, text)
        print(f"wrote {path.relative_to(ROOT)}")

    print()
    print(f"Backups saved under: {BACKUP}")
    print("Next:")
    print("1) Run Roblox Studio / VSCode typecheck.")
    print("2) Search for: require(script.Parent.Style)")
    print("3) If no results remain, delete Menus/Settings/Style.lua, TabButton.lua, TabStrip.lua.")


if __name__ == "__main__":
    main()
