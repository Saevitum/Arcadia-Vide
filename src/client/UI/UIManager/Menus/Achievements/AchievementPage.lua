--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local MockAchievements = require(script.Parent.MockAchievements)
local Style = require(script.Parent.Style)

Vide.strict = true

local create = Vide.create
local ScrollArea = Components.ScrollArea

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type AchievementPageProps = {
	tab: AchievementCategory,
	selectedTab: Source<AchievementCategory>,
	layoutOrder: number,
	zIndex: number,
	children: { Instance },
}

local function AchievementPage(props: AchievementPageProps)
	return create("CanvasGroup")({
		Name = `{props.tab}AchievementsPage`,

		Size = Style.PAGE_SIZE,
		Position = Style.PAGE_POSITION,
		AnchorPoint = Vector2.new(0.5, 0.5),

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

			openPosition = Style.PAGE_POSITION,
			closedPosition = Style.PAGE_POSITION,

			openTransparency = 0,
			closedTransparency = 1,

			duration = Style.PAGE_TRANSITION_DURATION,
			fadeDuration = Style.PAGE_FADE_DURATION,
			closeFadeDuration = Style.PAGE_CLOSE_FADE_DURATION,

			easingStyle = Enum.EasingStyle.Sine,
			easingDirection = Enum.EasingDirection.InOut,
			fadeEasingStyle = Enum.EasingStyle.Sine,
			fadeEasingDirection = Enum.EasingDirection.InOut,

			hideWhenClosed = true,
		}),

		ScrollArea({
			name = `{props.tab}AchievementsScrollArea`,

			size = UDim2.fromScale(1, 1),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			zIndex = props.zIndex + 1,

			backgroundTransparency = 1,
			backgroundColor3 = Color3.fromRGB(0, 0, 0),

			layoutKind = "List",

			padding = {
				top = UDim.new(0.02, 0),
				bottom = UDim.new(0.04, 0),
				left = UDim.new(0.02, 0),
				right = UDim.new(0.02, 0),
			},

			list = {
				padding = Style.ROW_PADDING,
				fillDirection = Enum.FillDirection.Vertical,
				horizontalAlignment = Enum.HorizontalAlignment.Center,
				verticalAlignment = Enum.VerticalAlignment.Top,
				sortOrder = Enum.SortOrder.LayoutOrder,
			},

			scrollBarThickness = 5,
			scrollBarImageColor3 = Style.CYAN,
			scrollBarImageTransparency = 0.2,

			automaticCanvasSize = Enum.AutomaticSize.Y,
			canvasSize = UDim2.fromScale(0, 0),
			scrollingDirection = Enum.ScrollingDirection.Y,

			children = props.children,
		}),
	})
end

return AchievementPage
