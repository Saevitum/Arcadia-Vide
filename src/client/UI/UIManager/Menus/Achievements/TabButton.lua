--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local MockAchievements = require(script.Parent.MockAchievements)
local Style = require(script.Parent.Style)

Vide.strict = true

local create = Vide.create

local ActionButton = Components.ActionButton
local Text = Components.Text

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory
type AchievementTabDefinition = MockAchievements.AchievementTabDefinition

local function TabButton(tab: AchievementTabDefinition, selectedTab: Source<AchievementCategory>)
	local tabId: AchievementCategory = tab.id

	return create("Frame")({
		Name = `{tabId}TabHost`,

		Size = Style.TAB_BUTTON_SIZE,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		LayoutOrder = tab.layoutOrder,
		ZIndex = 22,

		ActionButton({
			name = `{tabId}TabButton`,
			text = tab.label,

			variant = function()
				if selectedTab() == tabId then
					return "Orange"
				end

				return "Dark"
			end,

			gradient = {
				keypoints = function()
					if selectedTab() == tabId then
						return Style.TAB_ACTIVE_GRADIENT_KEYPOINTS
					end

					return Style.TAB_INACTIVE_GRADIENT_KEYPOINTS
				end,
				rotation = 0,
			},

			strokeGradient = {
				keypoints = function()
					if selectedTab() == tabId then
						return Style.TAB_STROKE_ACTIVE_KEYPOINTS
					end

					return Style.TAB_STROKE_INACTIVE_KEYPOINTS
				end,
				rotation = 0,
			},

			size = UDim2.fromScale(1, 1),
			zIndex = 23,

			hoverScale = 1.05,
			hoverDuration = 0.12,
			scaleTextConstraints = false,

			cornerRadius = Style.TAB_BUTTON_CORNER_RADIUS,
			strokeThickness = function()
				if selectedTab() == tabId then
					return 2
				end

				return 1.5
			end,

			strokeColor = Style.WHITE,
			strokeTransparency = function()
				if selectedTab() == tabId then
					return 0
				end

				return 0.18
			end,

			textColor3 = function()
				if selectedTab() == tabId then
					return Style.WHITE
				end

				return Color3.fromRGB(205, 215, 225)
			end,

			onClick = function()
				selectedTab(tabId)
			end,
		}),

		if tab.hasAlert == true
			then create("Frame")({
				Name = "AlertBadge",

				Size = UDim2.fromScale(0.18, 0.38),
				Position = UDim2.fromScale(0.95, -0.08),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundColor3 = Color3.fromRGB(255, 42, 80),
				BackgroundTransparency = 0,
				BorderSizePixel = 0,
				ZIndex = 30,

				create("UIAspectRatioConstraint")({
					AspectRatio = 1,
				}),

				create("UICorner")({
					CornerRadius = UDim.new(1, 0),
				}),

				create("UIStroke")({
					Thickness = 1.25,
					Color = Color3.fromRGB(45, 20, 10),
					Transparency = 0.05,
					ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
				}),

				Text({
					name = "AlertText",
					text = "!",

					size = UDim2.fromScale(0.85, 0.85),
					position = UDim2.fromScale(0.5, 0.45),
					anchorPoint = Vector2.new(0.5, 0.5),

					fontFace = Style.FONT_BOLD_ITALIC,
					textScaled = true,
					minTextSize = 7,
					maxTextSize = 16,

					textColor3 = Color3.fromRGB(20, 20, 20),

					stroke = {
						thickness = 0,
						color = Color3.fromRGB(0, 0, 0),
						transparency = 1,
					},

					zIndex = 31,
				}),
			})
			else nil,
	})
end

return TabButton
