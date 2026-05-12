--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local create = Vide.create

local Text = Components.Text

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = MenuTypes.InventoryTabId

export type QuestsPageProps = {
	selectedTab: Source<InventoryTabId>,
}

local EMPTY_STYLE = Style.Pages.EmptyStates.CyberPanel
local PAGE_POSITION = UDim2.fromScale(0.5, 0.58)

local function QuestsPage(props: QuestsPageProps)
	return create("CanvasGroup")({
		Name = "QuestsInventoryPage",

		Size = UDim2.fromScale(0.76, 0.43),
		Position = PAGE_POSITION,
		AnchorPoint = Vector2.new(0.5, 0.5),

		Visible = false,
		GroupTransparency = 1,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = 21,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return props.selectedTab() == "Quests"
			end,

			openPosition = PAGE_POSITION,
			closedPosition = PAGE_POSITION,

			openTransparency = 0,
			closedTransparency = 1,

			duration = 0.28,
			fadeDuration = 0.2,
			closeFadeDuration = 0.12,

			easingStyle = Enum.EasingStyle.Sine,
			easingDirection = Enum.EasingDirection.InOut,

			fadeEasingStyle = Enum.EasingStyle.Sine,
			fadeEasingDirection = Enum.EasingDirection.InOut,

			hideWhenClosed = true,
		}),

		create("Frame")({
			Name = "QuestsEmptyState",

			Size = EMPTY_STYLE.size,
			Position = UDim2.fromScale(0.5, 0.42),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = EMPTY_STYLE.backgroundColor,
			BackgroundTransparency = EMPTY_STYLE.backgroundTransparency,
			BorderSizePixel = 0,

			ZIndex = 22,

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
				text = "Quest inventory is not added yet.",

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

				zIndex = 23,
			}),
		}),
	})
end

return QuestsPage
