--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

local MockInventory = require(script.Parent.MockInventory)
local SkinCard = require(script.Parent.SkinCard)

Vide.strict = true

local create = Vide.create

local ScrollArea = Components.ScrollArea

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = MenuTypes.InventoryTabId
type SkinItem = MenuTypes.SkinItem

export type SkinsPageProps = {
	selectedTab: Source<InventoryTabId>,
	selectedSkin: Source<SkinItem?>,
	selectedSkinId: Source<string?>,
	equippedSkinId: Source<string?>,

	onSelectSkin: (skin: SkinItem) -> (),
}

local Tokens = Style.Tokens

local PAGE_FULL_SIZE = UDim2.fromScale(0.75, 0.53)
local PAGE_FULL_POSITION = UDim2.fromScale(0.5, 0.55)

local PAGE_DETAIL_SIZE = UDim2.fromScale(0.5, 0.53)
local PAGE_DETAIL_POSITION = UDim2.fromScale(0.38, 0.55)

local PAGE_ANCHOR = Vector2.new(0.5, 0.5)

local GRID_FULL_CELL_SIZE = UDim2.fromScale(0.1625, 0.385)
local GRID_DETAIL_CELL_SIZE = UDim2.fromScale(0.1625, 0.265)
local GRID_CELL_PADDING = UDim2.fromScale(0.03, 0.045)

local function hasSelectedSkin(props: SkinsPageProps): boolean
	return props.selectedSkin() ~= nil
end

local function buildSkinCards(props: SkinsPageProps): { Instance }
	local children: { Instance } = {}

	for index, skin in ipairs(MockInventory.SKINS) do
		table.insert(children, SkinCard({
			skin = skin,

			selectedSkinId = props.selectedSkinId,
			equippedSkinId = props.equippedSkinId,

			layoutOrder = index,
			zIndex = 24,

			onSelected = props.onSelectSkin,
		}))
	end

	return children
end

local function SkinsPage(props: SkinsPageProps)
	return create("CanvasGroup")({
		Name = "SkinInventoryPage",

		Size = UDim2.fromScale(1, 1),
		Position = UDim2.fromScale(0, 0),
		AnchorPoint = Vector2.new(0, 0),

		Visible = false,
		GroupTransparency = 1,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = function()
			if props.selectedTab() == "Skins" then
				return 21
			end

			return 20
		end,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return props.selectedTab() == "Skins"
			end,

			openPosition = UDim2.fromScale(0, 0),
			closedPosition = UDim2.fromScale(0, 0),

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

		ScrollArea({
			name = "SkinsScrollArea",

			verticalScrollBarPosition = Enum.VerticalScrollBarPosition.Left, size = PAGE_FULL_SIZE,
			position = PAGE_FULL_POSITION,
			anchorPoint = PAGE_ANCHOR,

			zIndex = 22,

			backgroundTransparency = 1,
			backgroundColor3 = Tokens.Colors.Black,

			layoutKind = "Grid",

			padding = {
				top = UDim.new(0.025, 0),
				bottom = UDim.new(0.06, 0),
				left = UDim.new(0.025, 0),
				right = UDim.new(0.025, 0),
			},

			grid = {
				cellSize = function()
					if hasSelectedSkin(props) then
						return GRID_DETAIL_CELL_SIZE
					end

					return GRID_FULL_CELL_SIZE
				end,

				cellPadding = GRID_CELL_PADDING,

				fillDirection = Enum.FillDirection.Horizontal,
				fillDirectionMaxCells = 0,

				horizontalAlignment = Enum.HorizontalAlignment.Left,
				verticalAlignment = Enum.VerticalAlignment.Top,

				sortOrder = Enum.SortOrder.LayoutOrder,
			},

			layoutTween = { isOpen = function() return hasSelectedSkin(props) end, targetSize = function() if hasSelectedSkin(props) then return PAGE_DETAIL_SIZE end return PAGE_FULL_SIZE end, targetPosition = function() if hasSelectedSkin(props) then return PAGE_DETAIL_POSITION end return PAGE_FULL_POSITION end, duration = 0.38, easingStyle = Enum.EasingStyle.Quint, easingDirection = Enum.EasingDirection.Out, bounce = { overshoot = 0.09, firstDuration = 0.22, settleDuration = 0.16, firstEasingStyle = Enum.EasingStyle.Quint, firstEasingDirection = Enum.EasingDirection.Out, settleEasingStyle = Enum.EasingStyle.Quint, settleEasingDirection = Enum.EasingDirection.Out, }, },

			scrollBarThickness = 5,
			scrollBarImageColor3 = Color3.fromRGB(0, 0, 0),
			scrollBarImageTransparency = 0,

			automaticCanvasSize = Enum.AutomaticSize.None,
			canvasSize = UDim2.fromOffset(0, 0),
			syncGridCanvas = true,
			canvasBottomSafetyScale = 0.08,

			scrollingDirection = Enum.ScrollingDirection.Y,

			children = buildSkinCards(props),
		}),
	})
end

return SkinsPage
