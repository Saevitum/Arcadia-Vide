--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Reactive = SharedTypes.Reactive

export type ScrollAreaLayoutKind = "Grid" | "List" | "None"

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

	backgroundTransparency: Reactive?,
	backgroundColor3: Reactive?,
	clipsDescendants: boolean?,

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

	layoutTween: any?,
	syncGridCanvas: boolean?,
	canvasBottomSafetyScale: Reactive?,

	children: any?,
}

return {}
