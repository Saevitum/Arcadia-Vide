--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)
local EffectTypes = require(script.Parent.Parent.EffectTypes)

export type Reactive = SharedTypes.Reactive
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions

export type ScrollAreaLayoutKind = "Grid" | "List" | "None"
export type ScrollAreaChildren = Instance | { Instance } | (() -> Instance?) | (() -> { Instance })

export type ScrollAreaPaddingProps = {
	top: Reactive?,
	bottom: Reactive?,
	left: Reactive?,
	right: Reactive?,
}

export type ScrollAreaGridProps = {
	cellSize: Reactive?,
	cellPadding: Reactive?,
	fillDirection: Enum.FillDirection?,
	fillDirectionMaxCells: number?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
	startCorner: Enum.StartCorner?,
}

export type ScrollAreaListProps = {
	padding: Reactive?,
	fillDirection: Enum.FillDirection?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
}

export type ScrollAreaProps = {
	name: string?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	layoutOrder: Reactive?,
	layoutTween: TweenGuiObjectLayoutOptions?,
	backgroundTransparency: Reactive?,
	backgroundColor3: Reactive?,
	clipsDescendants: boolean?,
	syncGridCanvas: boolean?,
	canvasBottomSafetyScale: Reactive?,
	canvasHeightScale: Reactive?,
	canvasSize: Reactive?,
	automaticCanvasSize: Enum.AutomaticSize?,
	scrollingDirection: Enum.ScrollingDirection?,
	scrollingEnabled: Reactive?,
	scrollBarThickness: Reactive?,
	scrollBarImageColor3: Reactive?,
	scrollBarImageTransparency: Reactive?,
	elasticBehavior: Enum.ElasticBehavior?,
	verticalScrollBarInset: Enum.ScrollBarInset?,
	horizontalScrollBarInset: Enum.ScrollBarInset?,
	padding: ScrollAreaPaddingProps?,
	layoutKind: ScrollAreaLayoutKind?,
	grid: ScrollAreaGridProps?,
	list: ScrollAreaListProps?,
	children: ScrollAreaChildren?,
}

return {}
