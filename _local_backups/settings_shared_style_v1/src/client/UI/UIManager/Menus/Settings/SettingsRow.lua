--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Style = require(script.Parent.Style)

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

local function SettingsRow(props: SettingsRowProps)
	return create("Frame")({
		Name = props.name,
		Size = props.size,
		LayoutOrder = props.layoutOrder,

		BackgroundColor3 = function()
			if props.dimmed ~= nil and props.dimmed() then
				return Color3.fromRGB(13, 17, 25)
			end

			return Style.DARK_ALT
		end,

		BackgroundTransparency = function()
			if props.dimmed ~= nil and props.dimmed() then
				return 0.2
			end

			return 0.08
		end,

		BorderSizePixel = 0,
		ZIndex = props.zIndex,

		create("UICorner")({
			CornerRadius = UDim.new(0.18, 0),
		}),

		Style.RowGradient(),
		Style.NeonStroke(2, 0.05),

		props.children,
	})
end

return SettingsRow
