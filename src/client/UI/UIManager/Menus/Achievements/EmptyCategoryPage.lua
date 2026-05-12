--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)

local MockAchievements = require(script.Parent.MockAchievements)
local AchievementPage = require(script.Parent.AchievementPage)
local Style = require(script.Parent.Style)

Vide.strict = true

local create = Vide.create
local Text = Components.Text

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

local function EmptyCategoryPage(
	tab: AchievementCategory,
	selectedTab: Source<AchievementCategory>,
	layoutOrder: number,
	label: string
)
	return AchievementPage({
		tab = tab,
		selectedTab = selectedTab,
		layoutOrder = layoutOrder,
		zIndex = 20,

		children = {
			create("Frame")({
				Name = `{tab}EmptyState`,

				Size = UDim2.fromScale(0.96, 0.35),
				BackgroundColor3 = Color3.fromRGB(8, 12, 20),
				BackgroundTransparency = 0.35,
				BorderSizePixel = 0,

				LayoutOrder = 1,
				ZIndex = 24,

				create("UICorner")({
					CornerRadius = UDim.new(0.08, 0),
				}),

				create("UIStroke")({
					Thickness = 1.25,
					Color = Style.WHITE,
					Transparency = 0.35,
					ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

					create("UIGradient")({
						Rotation = 0,
						Color = ColorSequence.new({
							ColorSequenceKeypoint.new(0, Style.CYAN),
							ColorSequenceKeypoint.new(1, Style.MAGENTA),
						}),
					}),
				}),

				Text({
					name = "EmptyText",
					text = `{label} achievements are not added yet.`,

					size = UDim2.fromScale(0.82, 0.45),
					position = UDim2.fromScale(0.5, 0.5),
					anchorPoint = Vector2.new(0.5, 0.5),

					fontFace = Style.FONT_BOLD_ITALIC,
					textScaled = true,
					minTextSize = 8,
					maxTextSize = 22,

					textColor3 = Style.EMPTY_TEXT_COLOR,

					stroke = {
						thickness = 1,
						color = Color3.fromRGB(0, 0, 0),
						transparency = 0.2,
					},

					zIndex = 25,
				}),
			}),
		},
	})
end

return EmptyCategoryPage
