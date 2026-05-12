--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Style = require(script.Parent.Style)
local TabButton = require(script.Parent.TabButton)

Vide.strict = true

local create = Vide.create

type Source<T> = Types.Source<T>
type SettingsTab = Types.SettingsTab

export type TabStripProps = {
	selectedTab: Source<SettingsTab>,

	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	zIndex: number?,
}

local function TabStrip(props: TabStripProps)
	local zIndex = props.zIndex or 21

	return create("Frame")({
		Name = "TabStrip",

		Size = props.size or Style.TAB_STRIP_SIZE,
		Position = props.position or Style.TAB_STRIP_POSITION,
		AnchorPoint = props.anchorPoint or Style.TAB_STRIP_ANCHOR_POINT,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = zIndex,

		create("UIListLayout")({
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			VerticalAlignment = Enum.VerticalAlignment.Center,
			Padding = UDim.new(0.035, 0),
			SortOrder = Enum.SortOrder.LayoutOrder,
		}),

		TabButton("Volume", props.selectedTab, 1),
		TabButton("User", props.selectedTab, 2),
		TabButton("Game", props.selectedTab, 3),
	})
end

return TabStrip
