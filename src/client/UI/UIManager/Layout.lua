--!strict

local Device = require(script.Parent.Device)
local Types = require(script.Parent.UITypes)

local Layout = {}

-- Menu size
function Layout.GetMenuSize(): UDim2
	local device = Device.GetKind()

	if device == "Mobile" then
		return UDim2.fromScale(0.537, 0.618)
	end

	if device == "Tablet" then
		return UDim2.fromScale(0.537, 0.618)
	end

	-- Desktop (default)
	return UDim2.fromScale(0.537, 0.618)
end

-- Exit button size
function Layout.GetExitButtonSize(): UDim2
	local device = Device.GetKind()

	if device == "Mobile" then
		return UDim2.fromScale(0.144, 0.239)
	end

	if device == "Tablet" then
		return UDim2.fromScale(0.144, 0.239)
	end

	-- Desktop (default)
	return UDim2.fromScale(0.144, 0.239)
end

function Layout.GetGridCellSize(options: Types.GridCellSizeOptions): UDim2
	local columns = math.max(1, math.floor(options.columns))
	local rowsVisible = math.max(1, options.rowsVisible or 2)

	local gap = options.gap or 0

	local widthFill = options.widthFill or 1
	local heightFill = options.heightFill or 1

	local totalHorizontalGap = gap * math.max(columns - 1, 0)
	local totalVerticalGap = gap * math.max(rowsVisible - 1, 0)

	local cellWidth = (widthFill - totalHorizontalGap) / columns
	local cellHeight = (heightFill - totalVerticalGap) / rowsVisible

	return UDim2.fromScale(cellWidth, cellHeight)
end

return Layout
