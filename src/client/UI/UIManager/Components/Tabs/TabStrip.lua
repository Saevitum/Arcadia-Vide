--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Style = require(script.Parent.Parent.Parent.Style)
local Types = require(script.Parent.Parent.Parent.UITypes.ComponentTypes.TabsTypes)
local TabButton = require(script.Parent.TabButton)

Vide.strict = true

local create = Vide.create

type Reactive<T> = Types.Reactive<T>
type TabButtonProps<T> = Types.TabButtonProps<T>
type TabStripProps<T> = Types.TabStripProps<T>
type TabStripStyle = Types.TabStripStyle
type TabPadding = Types.TabPadding

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function mergeStripStyle(style: TabStripStyle?): TabStripStyle
	return Style.Tabs.merge(Style.Tabs.Presets.CyberDefault, style or {}) :: TabStripStyle
end

local function getPadding(padding: TabPadding?, key: string): UDim
	if padding == nil then
		return UDim.new(0, 0)
	end

	local value = padding[key]

	if value == nil then
		return UDim.new(0, 0)
	end

	return value
end

local function TabStrip<T>(props: TabStripProps<T>)
	local stripStyle = mergeStripStyle(props.style)

	local children: { any } = {
		create("UIPadding")({
			PaddingTop = getPadding(stripStyle.padding, "top"),
			PaddingBottom = getPadding(stripStyle.padding, "bottom"),
			PaddingLeft = getPadding(stripStyle.padding, "left"),
			PaddingRight = getPadding(stripStyle.padding, "right"),
		}),

		create("UIGridLayout")({
			FillDirection = Enum.FillDirection.Horizontal,
			SortOrder = Enum.SortOrder.LayoutOrder,
			HorizontalAlignment = stripStyle.horizontalAlignment or Enum.HorizontalAlignment.Center,
			VerticalAlignment = stripStyle.verticalAlignment or Enum.VerticalAlignment.Center,
			CellSize = function()
				return read(props.cellSize, stripStyle.cellSize or UDim2.fromScale(0.18, 0.42))
			end,
			CellPadding = function()
				return read(props.cellPadding, stripStyle.cellPadding or UDim2.fromScale(0.025, 0.12))
			end,
			FillDirectionMaxCells = function()
				return read(props.fillDirectionMaxCells, stripStyle.fillDirectionMaxCells or 5)
			end,
		}),
	}

	for _, tab in ipairs(props.tabs) do
		local tabButtonProps: TabButtonProps<T> = {
			tab = tab,
			selectedTab = props.selectedTab,
			style = stripStyle.button,
			zIndex = function()
				return read(props.zIndex, 1) + 1
			end,
			onTabSelected = props.onTabSelected,
		}

		table.insert(children, TabButton(tabButtonProps))
	end

	local frameProps: { [any]: any } = {
		Name = props.name or "TabStrip",
		Size = function()
			return read(props.size, UDim2.fromScale(1, 1))
		end,
		Position = function()
			return read(props.position, UDim2.fromScale(0, 0))
		end,
		AnchorPoint = function()
			return read(props.anchorPoint, Vector2.new(0, 0))
		end,
		Visible = function()
			return read(props.visible, true)
		end,
		ZIndex = function()
			return read(props.zIndex, 1)
		end,
		BackgroundColor3 = stripStyle.backgroundColor or Color3.fromRGB(0, 0, 0),
		BackgroundTransparency = stripStyle.backgroundTransparency or 1,
		BorderSizePixel = 0,
	}

	for _, child in ipairs(children) do
		table.insert(frameProps, child)
	end

	return create("Frame")(frameProps)
end

return TabStrip
