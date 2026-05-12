--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create

local Panel = Components.Panel
local Text = Components.Text

type ActivityRowData = {
	label: string,
	value: string,
}

local FONT_ROW = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)

local LABEL_COLOR = Color3.fromRGB(0, 255, 238)
local VALUE_COLOR = Color3.fromRGB(255, 70, 130)

local DIVIDER_COLORS = {
	Color3.fromRGB(0, 229, 255),
	Color3.fromRGB(255, 0, 255),
	Color3.fromRGB(255, 0, 60),
}

local ACTIVITY_SECTIONS: { { ActivityRowData } } = {
	{
		{
			label = "First Login:",
			value = "04:01, Apr 23, 2026",
		},
		{
			label = "First Login Today:",
			value = "03:06, Apr 30, 2026",
		},
		{
			label = "Last Login:",
			value = "03:06, Apr 30, 2026",
		},
	},

	{
		{
			label = "Total Login:",
			value = "161",
		},
		{
			label = "Total Playtime:",
			value = "58h 54m 50s",
		},
		{
			label = "Total Playtime Today:",
			value = "5h 8m 33s",
		},
	},

	{
		{
			label = "Longest Daily Login Streak:",
			value = "5",
		},
		{
			label = "Current Login Streak:",
			value = "2",
		},
	},
}

local function ActivityRow(row: ActivityRowData, layoutOrder: number, zIndex: number)
	return create("Frame")({
		Name = `ActivityRow_{layoutOrder}`,

		Size = UDim2.fromScale(1, 0.105),
		BackgroundColor3 = Color3.fromRGB(16, 22, 30),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		LayoutOrder = layoutOrder,
		ZIndex = zIndex,

		create("UICorner")({
			CornerRadius = UDim.new(0.22, 0),
		}),

		create("UIGradient")({
			Rotation = 0,
			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, Color3.fromRGB(19, 28, 38)),
				ColorSequenceKeypoint.new(0.5, Color3.fromRGB(10, 14, 21)),
				ColorSequenceKeypoint.new(1, Color3.fromRGB(19, 28, 38)),
			}),
			Transparency = NumberSequence.new({
				NumberSequenceKeypoint.new(0, 0.28),
				NumberSequenceKeypoint.new(0.5, 0.08),
				NumberSequenceKeypoint.new(1, 0.28),
			}),
		}),

		Text({
			name = "Label",
			text = row.label,

			size = UDim2.fromScale(0.56, 0.82),
			position = UDim2.fromScale(0.025, 0.5),
			anchorPoint = Vector2.new(0, 0.5),

			fontFace = FONT_ROW,
			textScaled = true,
			minTextSize = 8,
			maxTextSize = 25,

			textColor3 = LABEL_COLOR,
			textXAlignment = Enum.TextXAlignment.Left,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.16,
			},

			zIndex = zIndex + 1,
		}),

		Text({
			name = "Value",
			text = row.value,

			size = UDim2.fromScale(0.42, 0.82),
			position = UDim2.fromScale(0.975, 0.5),
			anchorPoint = Vector2.new(1, 0.5),

			fontFace = FONT_ROW,
			textScaled = true,
			minTextSize = 8,
			maxTextSize = 25,

			textColor3 = VALUE_COLOR,
			textXAlignment = Enum.TextXAlignment.Right,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.16,
			},

			zIndex = zIndex + 1,
		}),
	})
end

local function ActivityDivider(layoutOrder: number, zIndex: number)
	return create("Frame")({
		Name = `ActivityDivider_{layoutOrder}`,

		Size = UDim2.fromScale(1, 0.035),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		LayoutOrder = layoutOrder,
		ZIndex = zIndex,

		create("Frame")({
			Name = "NeonLine",

			Size = UDim2.fromScale(1, 0.12),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = Color3.fromRGB(255, 255, 255),
			BackgroundTransparency = 0,
			BorderSizePixel = 0,

			ZIndex = zIndex + 1,

			create("UICorner")({
				CornerRadius = UDim.new(1, 0),
			}),

			create("UIGradient")({
				Rotation = 0,
				Color = ColorSequence.new({
					ColorSequenceKeypoint.new(0, DIVIDER_COLORS[1]),
					ColorSequenceKeypoint.new(0.5, DIVIDER_COLORS[2]),
					ColorSequenceKeypoint.new(1, DIVIDER_COLORS[3]),
				}),
				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 1),
					NumberSequenceKeypoint.new(0.12, 0.4),
					NumberSequenceKeypoint.new(0.5, 0),
					NumberSequenceKeypoint.new(0.88, 0.4),
					NumberSequenceKeypoint.new(1, 1),
				}),

				Effects.SweepGradientKeypoint({
					middleColors = DIVIDER_COLORS,
					loopsPerColor = 1,
					colorTweenDuration = 0.35,

					edgeColor = Color3.fromRGB(255, 255, 255),
					edgeTransparency = 1,
					middleTransparency = 0,

					duration = 2.8,
				}),
			}),
		}),
	})
end

local function buildActivityChildren(zIndex: number): { Instance }
	local children: { Instance } = {}
	local layoutOrder = 0

	for sectionIndex, section in ACTIVITY_SECTIONS do
		if sectionIndex > 1 then
			layoutOrder += 1
			table.insert(children, ActivityDivider(layoutOrder, zIndex))
		end

		for _, row in section do
			layoutOrder += 1
			table.insert(children, ActivityRow(row, layoutOrder, zIndex))
		end
	end

	return children
end

local function ActivityMenu(props: Types.ActivityMenuProps)
	local rows = buildActivityChildren(13)

	return Panel({
		name = "ActivityMenu",
		store = props.store,
		menuId = "Activity",
		title = "ACTIVITY",

		content = create("Frame")({
			Name = "ActivityContent",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			create("Frame")({
				Name = "ActivityRows",

				Size = UDim2.fromScale(0.7, 0.5),
				Position = UDim2.fromScale(0.49, 0.5),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				ZIndex = 12,

				create("UIListLayout")({
					FillDirection = Enum.FillDirection.Vertical,
					HorizontalAlignment = Enum.HorizontalAlignment.Center,
					VerticalAlignment = Enum.VerticalAlignment.Center,
					SortOrder = Enum.SortOrder.LayoutOrder,
					Padding = UDim.new(0.018, 0),
				}),

				table.unpack(rows),
			}),
		}),
	})
end

return ActivityMenu
