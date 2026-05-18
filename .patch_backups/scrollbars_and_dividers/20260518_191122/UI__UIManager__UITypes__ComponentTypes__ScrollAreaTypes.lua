--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)
local EffectTypes = require(script.Parent.Parent.EffectTypes)

export type Reactive<T> = SharedTypes.Reactive<T>
export type TweenGuiObjectLayoutOptions = EffectTypes.TweenGuiObjectLayoutOptions

export type ScrollAreaLayoutKind = "Grid" | "List" | "None"
export type ScrollAreaChildren = Instance | { Instance } | (() -> Instance?) | (() -> { Instance })

export type ScrollAreaPaddingProps = {
	top: Reactive<UDim>?,
	bottom: Reactive<UDim>?,
	left: Reactive<UDim>?,
	right: Reactive<UDim>?,
}

export type ScrollAreaGridProps = {
	cellSize: Reactive<UDim2>?,
	cellPadding: Reactive<UDim2>?,
	fillDirection: Enum.FillDirection?,
	fillDirectionMaxCells: number?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
	startCorner: Enum.StartCorner?,
}

export type ScrollAreaListProps = {
	padding: Reactive<UDim>?,
	fillDirection: Enum.FillDirection?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	sortOrder: Enum.SortOrder?,
}

export type GridCellSizeOptions = {
	columns: number,
	rowsVisible: number?,
	gap: number?,
	widthFill: number?,
	heightFill: number?,
}

export type ScrollAreaProps = {
	name: string?,
	size: Reactive<UDim2>?,
	position: Reactive<UDim2>?,
	anchorPoint: Reactive<Vector2>?,
	visible: Reactive<boolean>?,
	zIndex: Reactive<number>?,
	layoutOrder: Reactive<number>?,
	layoutTween: TweenGuiObjectLayoutOptions?,
	backgroundTransparency: Reactive<number>?,
	backgroundColor3: Reactive<Color3>?,
	clipsDescendants: boolean?,
	syncGridCanvas: boolean?,
	canvasBottomSafetyScale: Reactive<number>?,
	canvasHeightScale: Reactive<number>?,
	canvasSize: Reactive<UDim2>?,
	automaticCanvasSize: Enum.AutomaticSize?,
	scrollingDirection: Enum.ScrollingDirection?,
	scrollingEnabled: Reactive<boolean>?,
	scrollBarThickness: Reactive<number>?,
	scrollBarImageColor3: Reactive<Color3>?,
	scrollBarImageTransparency: Reactive<number>?,
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
