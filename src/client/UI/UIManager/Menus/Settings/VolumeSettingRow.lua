--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Parent.Components)
local NumberInput = require(script.Parent.NumberInput)
local SettingsRow = require(script.Parent.SettingsRow)
local Style = require(script.Parent.Style)

local Text = Components.Text
local Slider = Components.Slider
local ToggleButton = Components.ToggleButton

type Source<T> = Types.Source<T>

export type VolumeSettingRowProps = {
	name: string,
	label: string,
	description: string,
	value: Source<number>,
	muted: Source<boolean>,
	layoutOrder: number,
	zIndex: number,
}

local function VolumeSettingRow(props: VolumeSettingRowProps)
	return SettingsRow({
		name = props.name,
		layoutOrder = props.layoutOrder,
		size = Style.VOLUME_SETTING_ROW_SIZE,
		zIndex = props.zIndex,
		dimmed = props.muted,

		children = {
			Text({
				name = "Label",
				text = props.label,

				size = Style.VOLUME_LABEL_SIZE,
				position = Style.VOLUME_LABEL_POSITION,
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = Style.FONT_BOLD_ITALIC,
				textScaled = true,
				minTextSize = 8,
				maxTextSize = 22,

				textColor3 = Style.CYAN,
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

				size = Style.VOLUME_DESCRIPTION_SIZE,
				position = Style.VOLUME_DESCRIPTION_POSITION,
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = Style.FONT_BOLD_ITALIC,
				textScaled = true,
				minTextSize = 7,
				maxTextSize = 16,

				textColor3 = Style.PINK,
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
				size = Style.VOLUME_TOGGLE_SIZE,
				position = Style.VOLUME_TOGGLE_POSITION,
				anchorPoint = Vector2.new(0.5, 0.5),
				zIndex = props.zIndex + 1,
				textOn = "OFF",
				textOff = "ON",
				fontFace = Style.FONT_BOLD,
				textColor3 = Color3.fromRGB(5, 22, 25),
				onTextColor3 = Color3.fromRGB(35, 8, 22),
				strokeColor3 = Style.CYAN,
				onStrokeColor3 = Style.PINK,
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
				size = Style.VOLUME_SLIDER_SIZE,
				position = Style.VOLUME_SLIDER_POSITION,
				anchorPoint = Vector2.new(0.5, 0.5),
				zIndex = props.zIndex + 1,
				backgroundColor3 = Style.DARK,
				fillColor3 = function()
					if props.muted() then
						return Style.DIMMED_SLIDER_FILL
					end

					return Style.WHITE
				end,
				fillGradient = function()
					if props.muted() then
						return ColorSequence.new(Style.DIMMED_SLIDER_FILL)
					end

					return ColorSequence.new({
						ColorSequenceKeypoint.new(0, Style.CYAN),
						ColorSequenceKeypoint.new(1, Style.MAGENTA),
					})
				end,
				fillGradientEffect = {
					enabled = function()
						return not props.muted()
					end,
					duration = 4.2,
					primaryColor = Style.CYAN,
					secondaryColor = Style.MAGENTA,
					disabledColor = Style.DIMMED_SLIDER_FILL,
				},
				knobColor3 = Style.WHITE,
				dimmedKnobColor3 = Style.DIMMED_KNOB,
				strokeColor3 = function()
					if props.muted() then
						return Style.DIMMED_SLIDER_FILL
					end

					return Style.CYAN
				end,
				strokeThickness = 1,
				strokeTransparency = 0.12,
				dimmedFillTransparency = 0.08,
			}),

			NumberInput({
				name = "PercentInput",
				value = props.value,
				muted = props.muted,
				size = Style.VOLUME_INPUT_SIZE,
				position = Style.VOLUME_INPUT_POSITION,
				zIndex = props.zIndex + 1,
			}),
		},
	})
end

return VolumeSettingRow
