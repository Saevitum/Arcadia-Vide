--!strict

local Types = require(script.Parent.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Style = require(script.Parent.Style)

local ActionButton = Components.ActionButton

type Source<T> = Types.Source<T>
type SettingsTab = Types.SettingsTab

local function TabButton(tab: SettingsTab, selectedTab: Source<SettingsTab>, layoutOrder: number)
	return ActionButton({
		name = `{tab}TabButton`,
		text = string.upper(tab),

		variant = function()
			if selectedTab() == tab then
				return "Blue"
			end

			return "Dark"
		end,
		gradient = {
			keypoints = function()
				if selectedTab() == tab then
					return Style.TAB_ACTIVE_GRADIENT_KEYPOINTS
				end

				return Style.TAB_INACTIVE_GRADIENT_KEYPOINTS
			end,
			rotation = 0,
		},

		size = Style.TAB_BUTTON_SIZE,
		layoutOrder = layoutOrder,
		zIndex = 22,

		cornerRadius = Style.TAB_BUTTON_CORNER_RADIUS,
		strokeThickness = function()
			if selectedTab() == tab then
				return 2
			end

			return 1
		end,
		strokeColor = Style.WHITE,
		strokeGradient = {
			keypoints = function()
				if selectedTab() == tab then
					return Style.TAB_STROKE_GRADIENT.keypoints
				end

				return Style.TAB_INACTIVE_STROKE_GRADIENT_KEYPOINTS
			end,
			rotation = Style.TAB_STROKE_GRADIENT.rotation,
		},
		strokeTransparency = function()
			if selectedTab() == tab then
				return 0
			end

			return 0.18
		end,
		textColor3 = function()
			if selectedTab() == tab then
				return Style.WHITE
			end

			return Color3.fromRGB(190, 205, 220)
		end,

		onClick = function()
			selectedTab(tab)
		end,
	})
end

return TabButton
