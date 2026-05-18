--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.ComponentTypes)
local Effects = require(script.Parent.Parent.Effects)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect
local create = Vide.create

type Reactive<T> = Types.Reactive<T>
type ScrollAreaProps = Types.ScrollAreaProps
type ScrollAreaPaddingProps = Types.ScrollAreaPaddingProps
type ScrollAreaGridProps = Types.ScrollAreaGridProps
type ScrollAreaListProps = Types.ScrollAreaListProps
type ScrollAreaLayoutKind = Types.ScrollAreaLayoutKind

local DEFAULT_PADDING = UDim.new(0.03, 0)

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function createPadding(padding: ScrollAreaPaddingProps?)
	return create("UIPadding")({
		PaddingTop = function()
			return read(if padding ~= nil then padding.top else nil, DEFAULT_PADDING)
		end,

		PaddingBottom = function()
			return read(if padding ~= nil then padding.bottom else nil, DEFAULT_PADDING)
		end,

		PaddingLeft = function()
			return read(if padding ~= nil then padding.left else nil, DEFAULT_PADDING)
		end,

		PaddingRight = function()
			return read(if padding ~= nil then padding.right else nil, DEFAULT_PADDING)
		end,
	})
end

local function createGridLayout(grid: ScrollAreaGridProps?)
	return create("UIGridLayout")({
		CellSize = function()
			return read(if grid ~= nil then grid.cellSize else nil, UDim2.fromScale(0.22, 0.28))
		end,

		CellPadding = function()
			return read(if grid ~= nil then grid.cellPadding else nil, UDim2.fromScale(0.025, 0.025))
		end,

		FillDirection = if grid ~= nil and grid.fillDirection ~= nil
			then grid.fillDirection
			else Enum.FillDirection.Horizontal,

		FillDirectionMaxCells = if grid ~= nil and grid.fillDirectionMaxCells ~= nil
			then grid.fillDirectionMaxCells
			else 0,

		HorizontalAlignment = if grid ~= nil and grid.horizontalAlignment ~= nil
			then grid.horizontalAlignment
			else Enum.HorizontalAlignment.Left,

		VerticalAlignment = if grid ~= nil and grid.verticalAlignment ~= nil
			then grid.verticalAlignment
			else Enum.VerticalAlignment.Top,

		SortOrder = if grid ~= nil and grid.sortOrder ~= nil then grid.sortOrder else Enum.SortOrder.LayoutOrder,

		StartCorner = if grid ~= nil and grid.startCorner ~= nil then grid.startCorner else Enum.StartCorner.TopLeft,
	})
end

local function createListLayout(list: ScrollAreaListProps?)
	return create("UIListLayout")({
		Padding = function()
			return read(if list ~= nil then list.padding else nil, UDim.new(0.02, 0))
		end,

		FillDirection = if list ~= nil and list.fillDirection ~= nil
			then list.fillDirection
			else Enum.FillDirection.Vertical,

		HorizontalAlignment = if list ~= nil and list.horizontalAlignment ~= nil
			then list.horizontalAlignment
			else Enum.HorizontalAlignment.Center,

		VerticalAlignment = if list ~= nil and list.verticalAlignment ~= nil
			then list.verticalAlignment
			else Enum.VerticalAlignment.Top,

		SortOrder = if list ~= nil and list.sortOrder ~= nil then list.sortOrder else Enum.SortOrder.LayoutOrder,
	})
end

local function createLayout(layoutKind: ScrollAreaLayoutKind?, grid: ScrollAreaGridProps?, list: ScrollAreaListProps?)
	local resolvedLayoutKind = layoutKind or "Grid"

	if resolvedLayoutKind == "Grid" then
		return createGridLayout(grid)
	end

	if resolvedLayoutKind == "List" then
		return createListLayout(list)
	end

	return nil
end

local function toViewportOffsetUDim(value: UDim, viewportPixels: number): UDim
	return UDim.new(0, math.round((value.Scale * viewportPixels) + value.Offset))
end

local function toViewportOffsetUDim2(value: UDim2, viewportSize: Vector2): UDim2
	return UDim2.fromOffset(
		math.round((value.X.Scale * viewportSize.X) + value.X.Offset),
		math.round((value.Y.Scale * viewportSize.Y) + value.Y.Offset)
	)
end

local function syncGridCanvas(
	enabled: boolean?,
	paddingProps: ScrollAreaPaddingProps?,
	gridProps: ScrollAreaGridProps?,
	canvasBottomSafetyScale: Reactive<number>?
)
	if enabled ~= true then
		return nil
	end

	return action(function(instance: Instance)
		if not instance:IsA("ScrollingFrame") then
			return
		end

		local scrollingFrame = instance :: ScrollingFrame
		local alive = true

		local function update()
			if not alive then
				return
			end

			local viewportSize = scrollingFrame.AbsoluteSize
			if viewportSize.X <= 0 or viewportSize.Y <= 0 then
				return
			end

			local grid = scrollingFrame:FindFirstChildOfClass("UIGridLayout")
			if grid == nil then
				return
			end

			local padding = scrollingFrame:FindFirstChildOfClass("UIPadding")

			local rawCellSize = if gridProps ~= nil
				then read(gridProps.cellSize, UDim2.fromScale(0.17, 0.34))
				else UDim2.fromScale(0.17, 0.34)

			local rawCellPadding = if gridProps ~= nil
				then read(gridProps.cellPadding, UDim2.fromScale(0.03, 0.05))
				else UDim2.fromScale(0.03, 0.05)

			grid.CellSize = toViewportOffsetUDim2(rawCellSize, viewportSize)
			grid.CellPadding = toViewportOffsetUDim2(rawCellPadding, viewportSize)

			local paddingTopPixels = 0
			local paddingBottomPixels = 0

			if padding ~= nil then
				local top = if paddingProps ~= nil then read(paddingProps.top, UDim.new(0, 0)) else UDim.new(0, 0)
				local bottom = if paddingProps ~= nil then read(paddingProps.bottom, UDim.new(0, 0)) else UDim.new(0, 0)
				local left = if paddingProps ~= nil then read(paddingProps.left, UDim.new(0, 0)) else UDim.new(0, 0)
				local right = if paddingProps ~= nil then read(paddingProps.right, UDim.new(0, 0)) else UDim.new(0, 0)

				local topOffset = toViewportOffsetUDim(top, viewportSize.Y)
				local bottomOffset = toViewportOffsetUDim(bottom, viewportSize.Y)
				local leftOffset = toViewportOffsetUDim(left, viewportSize.X)
				local rightOffset = toViewportOffsetUDim(right, viewportSize.X)

				padding.PaddingTop = topOffset
				padding.PaddingBottom = bottomOffset
				padding.PaddingLeft = leftOffset
				padding.PaddingRight = rightOffset

				paddingTopPixels = topOffset.Offset
				paddingBottomPixels = bottomOffset.Offset
			end

			task.defer(function()
				if not alive then
					return
				end

				local safetyScale = read(canvasBottomSafetyScale, 0.08)
				local safetyPixels = math.round(viewportSize.Y * safetyScale)

				local contentHeight = grid.AbsoluteContentSize.Y
				local canvasHeight = contentHeight + paddingTopPixels + paddingBottomPixels + safetyPixels

				scrollingFrame.CanvasSize = UDim2.fromOffset(0, math.max(viewportSize.Y, canvasHeight))
			end)
		end

		local absoluteSizeConnection = scrollingFrame:GetPropertyChangedSignal("AbsoluteSize"):Connect(update)

		local childAddedConnection = scrollingFrame.ChildAdded:Connect(function()
			task.defer(update)
		end)

		local childRemovedConnection = scrollingFrame.ChildRemoved:Connect(function()
			task.defer(update)
		end)

		local grid = scrollingFrame:FindFirstChildOfClass("UIGridLayout")
		local absoluteContentConnection: RBXScriptConnection? = nil

		if grid ~= nil then
			absoluteContentConnection = grid:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(update)
		end

		effect(update)
		task.defer(update)

		cleanup(function()
			alive = false

			absoluteSizeConnection:Disconnect()
			childAddedConnection:Disconnect()
			childRemovedConnection:Disconnect()

			if absoluteContentConnection ~= nil then
				absoluteContentConnection:Disconnect()
			end
		end)
	end)
end

local function ScrollArea(props: ScrollAreaProps?)
	local resolvedProps: ScrollAreaProps = props or {}

	local layout = createLayout(resolvedProps.layoutKind, resolvedProps.grid, resolvedProps.list)

	return create("ScrollingFrame")({
		Name = resolvedProps.name or "ScrollArea",

		AnchorPoint = function()
			return read(resolvedProps.anchorPoint, Vector2.new(0.5, 0.5))
		end,

		Position = function()
			return read(resolvedProps.position, UDim2.fromScale(0.5, 0.5))
		end,

		Size = function()
			return read(resolvedProps.size, UDim2.fromScale(1, 1))
		end,

		Visible = function()
			return read(resolvedProps.visible, true)
		end,

		ZIndex = function()
			return read(resolvedProps.zIndex, 1)
		end,

		LayoutOrder = function()
			return read(resolvedProps.layoutOrder, 0)
		end,

		BackgroundTransparency = function()
			return read(resolvedProps.backgroundTransparency, 1)
		end,

		BackgroundColor3 = function()
			return read(resolvedProps.backgroundColor3, Color3.fromRGB(0, 0, 0))
		end,

		BorderSizePixel = 0,
		ClipsDescendants = if resolvedProps.clipsDescendants == nil then true else resolvedProps.clipsDescendants,
		Active = true,

		CanvasSize = function()
			return read(resolvedProps.canvasSize, UDim2.fromScale(0, 0))
		end,

		AutomaticCanvasSize = resolvedProps.automaticCanvasSize or Enum.AutomaticSize.Y,
		ScrollingDirection = resolvedProps.scrollingDirection or Enum.ScrollingDirection.Y,

		ScrollingEnabled = function()
			return read(resolvedProps.scrollingEnabled, true)
		end,

		ScrollBarThickness = function()
			return read(resolvedProps.scrollBarThickness, 6)
		end,

		ScrollBarImageColor3 = function()
			return read(resolvedProps.scrollBarImageColor3, Color3.fromRGB(0, 255, 238))
		end,

		ScrollBarImageTransparency = function()
			return read(resolvedProps.scrollBarImageTransparency, 0.15)
		end,

		ElasticBehavior = resolvedProps.elasticBehavior or Enum.ElasticBehavior.WhenScrollable,
		VerticalScrollBarInset = resolvedProps.verticalScrollBarInset or Enum.ScrollBarInset.None,
		HorizontalScrollBarInset = resolvedProps.horizontalScrollBarInset or Enum.ScrollBarInset.None,

		createPadding(resolvedProps.padding),

		layout,

		syncGridCanvas(
			resolvedProps.syncGridCanvas,
			resolvedProps.padding,
			resolvedProps.grid,
			resolvedProps.canvasBottomSafetyScale
		),

		if resolvedProps.layoutTween ~= nil then Effects.TweenGuiObjectLayout(resolvedProps.layoutTween) else nil,

		resolvedProps.children,
	})
end

return ScrollArea
