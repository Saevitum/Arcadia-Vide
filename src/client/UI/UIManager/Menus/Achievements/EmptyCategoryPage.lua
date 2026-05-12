--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Style = require(script.Parent.Parent.Parent.Style)

local MockAchievements = require(script.Parent.MockAchievements)
local AchievementPage = require(script.Parent.AchievementPage)

Vide.strict = true

local create = Vide.create

local Text = Components.Text

type Source<T> = SharedTypes.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

local EMPTY_STYLE = Style.Pages.EmptyStates.CyberPanel

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

				Size = EMPTY_STYLE.size,

				BackgroundColor3 = EMPTY_STYLE.backgroundColor,
				BackgroundTransparency = EMPTY_STYLE.backgroundTransparency,
				BorderSizePixel = 0,

				LayoutOrder = 1,
				ZIndex = 24,

				create("UICorner")({
					CornerRadius = EMPTY_STYLE.cornerRadius,
				}),

				create("UIStroke")({
					Thickness = EMPTY_STYLE.strokeThickness,
					Color = EMPTY_STYLE.strokeColor,
					Transparency = EMPTY_STYLE.strokeTransparency,
					ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

					create("UIGradient")({
						Rotation = EMPTY_STYLE.strokeGradientRotation,
						Color = EMPTY_STYLE.strokeGradient,
					}),
				}),

				Text({
					name = "EmptyText",
					text = `{label} achievements are not added yet.`,

					size = EMPTY_STYLE.textSize,
					position = EMPTY_STYLE.textPosition,
					anchorPoint = EMPTY_STYLE.textAnchorPoint,

					fontFace = EMPTY_STYLE.fontFace,
					textScaled = true,
					minTextSize = EMPTY_STYLE.minTextSize,
					maxTextSize = EMPTY_STYLE.maxTextSize,

					textColor3 = EMPTY_STYLE.textColor,

					stroke = {
						thickness = EMPTY_STYLE.textStrokeThickness,
						color = EMPTY_STYLE.textStrokeColor,
						transparency = EMPTY_STYLE.textStrokeTransparency,
					},

					zIndex = 25,
				}),
			}),
		},
	})
end

return EmptyCategoryPage
