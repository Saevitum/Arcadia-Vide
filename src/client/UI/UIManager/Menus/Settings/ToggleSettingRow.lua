--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Parent.Components)
local SettingsRow = require(script.Parent.SettingsRow)
local Style = require(script.Parent.Style)

local Text = Components.Text
local ToggleButton = Components.ToggleButton

type Source<T> = Types.Source<T>

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

local function ToggleSettingRow(props: ToggleSettingRowProps)
	local layout = props.layout or Style.TOGGLE_SETTING_ROW_LAYOUT

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

				fontFace = Style.FONT_BOLD_ITALIC,
				textScaled = true,
				minTextSize = 8,
				maxTextSize = 20,

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

				size = layout.descriptionSize,
				position = layout.descriptionPosition,
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = Style.FONT_BOLD_ITALIC,
				textScaled = true,
				minTextSize = 7,
				maxTextSize = 15,

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
				name = "Toggle",
				value = props.value,
				size = layout.toggleButtonSize,
				position = layout.toggleButtonPosition,
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
		},
	})
end

return ToggleSettingRow
