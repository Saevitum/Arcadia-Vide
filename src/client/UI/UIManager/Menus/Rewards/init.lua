--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Components)

local MockRewards = require(script.MockRewards)
local RewardCard = require(script.RewardCard)
local RewardTooltip = require(script.RewardTooltip)
local RewardsInfoButton = require(script.RewardsInfoButton)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action

local Panel = Components.Panel

local GRID_SIZE = UDim2.fromScale(0.66, 0.62)
local GRID_POSITION = UDim2.fromScale(0.49, 0.525)

local CARD_CELL_SIZE = UDim2.fromScale(0.215, 0.272)
local CARD_CELL_PADDING = UDim2.fromScale(0.027, 0.04)

local function RewardsMenu(props: Types.RewardsMenuProps)
	local hoveredReward = source(nil :: MockRewards.RewardView?)
	local tooltipVisible = source(false)
	local tooltipPosition = source(UDim2.fromOffset(0, 0))

	local contentFrame: Frame? = nil

	local TOOLTIP_GAP_X = 45
	local TOOLTIP_GAP_Y = -250

	local function updateTooltipPosition()
		if contentFrame == nil then
			return
		end

		local mousePosition = UserInputService:GetMouseLocation()

		local localX = mousePosition.X - contentFrame.AbsolutePosition.X
		local localY = mousePosition.Y - contentFrame.AbsolutePosition.Y

		tooltipPosition(UDim2.fromOffset(localX + TOOLTIP_GAP_X, localY + TOOLTIP_GAP_Y))
	end

	local rewardCards = {}

	for index, reward in MockRewards do
		table.insert(
			rewardCards,
			RewardCard({
				reward = reward,
				layoutOrder = index,
				zIndex = 13,

				onCollect = function()
					print(`Collect reward clicked: tier={reward.Tier}, title={reward.Title}`)
				end,

				onHoverStart = function(hovered: MockRewards.RewardView, _x: number, _y: number)
					hoveredReward(hovered)
					tooltipVisible(true)
					updateTooltipPosition()
				end,

				onHoverMove = function(_x: number, _y: number)
					updateTooltipPosition()
				end,

				onHoverEnd = function()
					tooltipVisible(false)
					hoveredReward(nil)
				end,
			})
		)
	end

	return Panel({
		name = "RewardsMenu",
		store = props.store,
		menuId = "Rewards",
		title = "REWARDS",

		content = create("Frame")({
			Name = "RewardsContent",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			action(function(instance: Instance)
				if not instance:IsA("Frame") then
					return
				end

				contentFrame = instance

				return function()
					if contentFrame == instance then
						contentFrame = nil
					end
				end
			end),

			RewardsInfoButton({
				zIndex = 900,
			}),

			create("Frame")({
				Name = "RewardsGrid",

				Size = GRID_SIZE,
				Position = GRID_POSITION,
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				ZIndex = 12,

				create("UIGridLayout")({
					CellSize = CARD_CELL_SIZE,
					CellPadding = CARD_CELL_PADDING,

					FillDirection = Enum.FillDirection.Horizontal,
					FillDirectionMaxCells = 4,

					HorizontalAlignment = Enum.HorizontalAlignment.Center,
					VerticalAlignment = Enum.VerticalAlignment.Center,

					SortOrder = Enum.SortOrder.LayoutOrder,
				}),

				table.unpack(rewardCards),
			}),

			RewardTooltip({
				reward = function()
					return hoveredReward()
				end,

				visible = function()
					return tooltipVisible() and hoveredReward() ~= nil
				end,

				position = function()
					return tooltipPosition()
				end,

				zIndex = 999,
			}),
		}),
	})
end

return RewardsMenu
