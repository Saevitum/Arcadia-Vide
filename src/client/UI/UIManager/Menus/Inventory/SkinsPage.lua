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
	selectedSkinId: Source<string?>,
	equippedSkinId: Source<string?>,
	searchQuery: Source<string>,

	onSelectSkin: (skin: SkinItem) -> (),
}

local Tokens = Style.Tokens

local PAGE_SIZE = UDim2.fromScale(0.5, 0.56)
local PAGE_POSITION = UDim2.fromScale(0.36, 0.565)
local PAGE_ANCHOR = Vector2.new(0.5, 0.5)

local function trim(value: string): string
	return string.gsub(value, "^%s*(.-)%s*$", "%1")
end

local function matchesSearch(skin: SkinItem, query: string): boolean
	local cleanQuery = string.lower(trim(query))

	if cleanQuery == "" then
		return true
	end

	local name = string.lower(skin.Name)
	local rarity = string.lower(skin.Rarity)
	local description = string.lower(skin.Description)

	return string.find(name, cleanQuery, 1, true) ~= nil
		or string.find(rarity, cleanQuery, 1, true) ~= nil
		or string.find(description, cleanQuery, 1, true) ~= nil
end

local function buildSkinCards(props: SkinsPageProps): { Instance }
	local children: { Instance } = {}
	local order = 0
	local query = props.searchQuery()

	for _, skin in ipairs(MockInventory.SKINS) do
		if matchesSearch(skin, query) then
			order += 1

			table.insert(
				children,
				SkinCard({
					skin = skin,
					selectedSkinId = props.selectedSkinId,
					equippedSkinId = props.equippedSkinId,
					layoutOrder = order,
					zIndex = 24,
					onSelected = props.onSelectSkin,
				})
			)
		end
	end

	return children
end

local function SkinsPage(props: SkinsPageProps)
	return create("CanvasGroup")({
		Name = "SkinsInventoryPage",

		Size = PAGE_SIZE,
		Position = PAGE_POSITION,
		AnchorPoint = PAGE_ANCHOR,

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

		ScrollArea({
			name = "SkinsScrollArea",

			size = UDim2.fromScale(1, 1),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

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
				cellSize = UDim2.fromScale(0.205, 0.34),
				cellPadding = UDim2.fromScale(0.03, 0.045),
				fillDirection = Enum.FillDirection.Horizontal,
				fillDirectionMaxCells = 4,
				horizontalAlignment = Enum.HorizontalAlignment.Left,
				verticalAlignment = Enum.VerticalAlignment.Top,
				sortOrder = Enum.SortOrder.LayoutOrder,
			},

			scrollBarThickness = 5,
			scrollBarImageColor3 = Tokens.Colors.CyanBright,
			scrollBarImageTransparency = 0.2,

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
