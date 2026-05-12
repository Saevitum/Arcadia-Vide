--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

local MockAchievements = require(script.Parent.MockAchievements)

Vide.strict = true

local create = Vide.create

local ScrollArea = Components.ScrollArea

type Source<T> = SharedTypes.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type AchievementPageProps = {
	tab: AchievementCategory,
	selectedTab: Source<AchievementCategory>,
	layoutOrder: number,
	zIndex: number,
	children: { Instance },
}

local PAGE_LAYOUT = Style.Pages.Layouts.WideLower
local PAGE_TRANSITION = Style.Pages.Transitions.SoftFade
local ROW_LAYOUT = Style.Rows.Layouts.WideList

local function AchievementPage(props: AchievementPageProps)
	return create("CanvasGroup")({
		Name = `{props.tab}AchievementsPage`,

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
				padding = ROW_LAYOUT.rowPadding,
				fillDirection = Enum.FillDirection.Vertical,
				horizontalAlignment = Enum.HorizontalAlignment.Center,
				verticalAlignment = Enum.VerticalAlignment.Top,
				sortOrder = Enum.SortOrder.LayoutOrder,
			},

			scrollBarThickness = 5,
			scrollBarImageColor3 = Style.Tokens.Colors.CyanBright,
			scrollBarImageTransparency = 0.2,

			automaticCanvasSize = Enum.AutomaticSize.Y,
			canvasSize = UDim2.fromScale(0, 0),
			scrollingDirection = Enum.ScrollingDirection.Y,

			children = props.children,
		}),
	})
end

return AchievementPage
