--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.Parent.UITypes)
local MockAchievements = require(script.Parent.MockAchievements)
local Style = require(script.Parent.Style)
local TabButton = require(script.Parent.TabButton)

Vide.strict = true

local create = Vide.create

type Source<T> = Types.Source<T>
type AchievementCategory = MockAchievements.AchievementCategory

export type TabStripProps = {
	selectedTab: Source<AchievementCategory>,
	zIndex: number?,
}

local function TabStrip(props: TabStripProps)
	local zIndex = props.zIndex or 21
	local tabs: { Instance } = {}

	for _, tab in ipairs(MockAchievements.TABS) do
		table.insert(tabs, TabButton(tab, props.selectedTab))
	end

	return create("Frame")({
		Name = "AchievementsTabStrip",

		Size = Style.TAB_STRIP_SIZE,
		Position = Style.TAB_STRIP_POSITION,
		AnchorPoint = Style.TAB_STRIP_ANCHOR_POINT,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = zIndex,

		create("UIGridLayout")({
			CellSize = Style.TAB_BUTTON_SIZE,
			CellPadding = UDim2.fromScale(0.02, 0.16),

			FillDirection = Enum.FillDirection.Horizontal,
			FillDirectionMaxCells = 5,

			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			VerticalAlignment = Enum.VerticalAlignment.Center,

			SortOrder = Enum.SortOrder.LayoutOrder,
		}),

		table.unpack(tabs),
	})
end

return TabStrip
