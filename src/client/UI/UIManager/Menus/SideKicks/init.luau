--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Components)

local MockSideKicks = require(script.MockSideKicks)
local SideKickCard = require(script.SideKickCard)
local SideKickInfo = require(script.SideKickInfo)
local Effects = require(script.Parent.Parent.Effects)
local SideKickButtons = require(script.SideKickButtons)

Vide.strict = true

local create = Vide.create
local source = Vide.source

local dividerColor = source(Color3.fromRGB(0, 229, 255))

local CARD_FULL_CELL_SIZE = UDim2.fromScale(0.1625, 0.34)
local CARD_DETAIL_CELL_SIZE = UDim2.fromScale(0.1625, 0.28)

local REPEAT_COUNT = 50
local pulsePhase = source(0)

type MockSideKick = MockSideKicks.MockSideKick

local SCROLL_FULL_SIZE = UDim2.fromScale(0.75, 0.6)
local SCROLL_FULL_POSITION = UDim2.fromScale(0.493, 0.52)

local SCROLL_DETAIL_SIZE = UDim2.fromScale(0.5, 0.521)
local SCROLL_DETAIL_POSITION = UDim2.fromScale(0.38, 0.48)

local SCROLL_ANCHOR_POINT = Vector2.new(0.5, 0.5)

-- COMPONENTS
local Panel = Components.Panel
local ScrollArea = Components.ScrollArea

local function SideKickMenu(props: Types.SideKickMenuProps)
	local selectedSideKickId = source(nil :: string?)
	local selectedSideKick = source(nil :: MockSideKick?)

	local cards: { Instance } = {}

	for repeatIndex = 1, REPEAT_COUNT do
		for sideKickIndex, sideKick in ipairs(MockSideKicks) do
			local instanceId = `{sideKick.SideKickId}_{repeatIndex}`
			local layoutOrder = ((repeatIndex - 1) * #MockSideKicks) + sideKickIndex

			table.insert(
				cards,
				SideKickCard({
					sideKick = sideKick,
					layoutOrder = layoutOrder,

					selected = function()
						return selectedSideKickId() == instanceId
					end,

					equipped = function()
						return instanceId == ""
					end,

					locked = function()
						return sideKick.SideKickId == ""
					end,

					onClick = function()
						if selectedSideKickId() == instanceId then
							selectedSideKickId(nil)
							selectedSideKick(nil)
							return
						end

						selectedSideKickId(instanceId)
						selectedSideKick(sideKick)
					end,
				})
			)
		end
	end

	return Panel({
		name = "SideKickMenu",
		store = props.store,
		menuId = "SideKicks",
		title = "SIDEKICKS",

		content = create("Frame")({
			Name = "SideKicksContent",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			create("Frame")({
				Name = "PulseDriverHost",

				Size = UDim2.fromScale(0, 0),
				BackgroundTransparency = 1,
				Visible = false,

				Effects.PulseDriver({
					phase = pulsePhase,
					duration = 3.6,
					easingStyle = Enum.EasingStyle.Sine,
					easingDirection = Enum.EasingDirection.InOut,
				}),
			}),

			ScrollArea({
				name = "SideKickScrollArea",
				anchorPoint = SCROLL_ANCHOR_POINT,
				position = SCROLL_FULL_POSITION,
				size = SCROLL_FULL_SIZE,

				layoutTween = {
					isOpen = function()
						return selectedSideKick() ~= nil
					end,

					targetSize = function()
						if selectedSideKick() ~= nil then
							return SCROLL_DETAIL_SIZE
						end

						return SCROLL_FULL_SIZE
					end,

					targetPosition = function()
						if selectedSideKick() ~= nil then
							return SCROLL_DETAIL_POSITION
						end

						return SCROLL_FULL_POSITION
					end,

					duration = 0.38,

					easingStyle = Enum.EasingStyle.Quint,
					easingDirection = Enum.EasingDirection.Out,

					bounce = {
						overshoot = 0.09,

						firstDuration = 0.22,
						settleDuration = 0.16,

						firstEasingStyle = Enum.EasingStyle.Quint,
						firstEasingDirection = Enum.EasingDirection.Out,

						settleEasingStyle = Enum.EasingStyle.Quint,
						settleEasingDirection = Enum.EasingDirection.Out,
					},
				},

				zIndex = 11,

				backgroundColor3 = Color3.fromRGB(255, 255, 255),
				backgroundTransparency = 1,

				layoutKind = "Grid",

				padding = {
					top = UDim.new(0.035, 0),
					bottom = UDim.new(0.02, 0),
					left = UDim.new(0.02, 0),
					right = UDim.new(0.02, 0),
				},

				grid = {
					cellSize = function()
						if selectedSideKick() ~= nil then
							return CARD_DETAIL_CELL_SIZE
						end

						return CARD_FULL_CELL_SIZE
					end,
					cellPadding = UDim2.fromScale(0.03, 0.05),

					fillDirection = Enum.FillDirection.Horizontal,
					horizontalAlignment = Enum.HorizontalAlignment.Left,
					verticalAlignment = Enum.VerticalAlignment.Top,
					sortOrder = Enum.SortOrder.LayoutOrder,
					startCorner = Enum.StartCorner.TopLeft,
				},

				scrollBarThickness = 6,
				scrollBarImageColor3 = Color3.fromRGB(0, 0, 0),
				scrollBarImageTransparency = 0,

				automaticCanvasSize = Enum.AutomaticSize.None,
				canvasSize = UDim2.fromOffset(0, 0),
				syncGridCanvas = true,
				canvasBottomSafetyScale = 0.08,
				scrollingDirection = Enum.ScrollingDirection.Y,

				children = cards,
			}),

			create("Frame")({
				Name = "SideKickDivider",

				Size = UDim2.fromScale(0.0015, 0.5),
				Position = UDim2.fromScale(0.639, 0.49),
				AnchorPoint = Vector2.new(0.5, 0.5),

				Visible = false,
				BackgroundTransparency = 1,

				BackgroundColor3 = Color3.fromRGB(255, 255, 255),
				BorderSizePixel = 0,
				ZIndex = 16,

				Effects.FadeGuiObject({
					open = function()
						return selectedSideKick() ~= nil
					end,

					openTransparency = 0,
					closedTransparency = 1,

					openDuration = 3,
					closeDuration = 0.08,

					easingStyle = Enum.EasingStyle.Quad,
					easingDirection = Enum.EasingDirection.Out,

					hideWhenClosed = true,
				}),

				create("UIGradient")({
					Rotation = 90,

					Color = ColorSequence.new({
						ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 255, 255)),
						ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0, 229, 255)),
						ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 255, 255)),
					}),

					Transparency = NumberSequence.new({
						NumberSequenceKeypoint.new(0, 1),
						NumberSequenceKeypoint.new(0.5, 0),
						NumberSequenceKeypoint.new(1, 1),
					}),

					Effects.SweepGradientKeypoint({
						phase = pulsePhase,
						edgeColor = Color3.fromRGB(255, 255, 255),

						middleColors = {
							Color3.fromRGB(0, 229, 255), -- cyan
							Color3.fromRGB(255, 0, 255), -- magenta
							Color3.fromRGB(255, 0, 60), -- redish
						},

						edgeTransparency = 1,
						middleTransparency = 0,

						loopsPerColor = 3,

						segmentDuration = 1.2,
						easingStyle = Enum.EasingStyle.Sine,
						easingDirection = Enum.EasingDirection.InOut,

						colorTweenDuration = 0.45,
						colorEasingStyle = Enum.EasingStyle.Sine,
						colorEasingDirection = Enum.EasingDirection.InOut,

						onColorChanged = function(color: Color3)
							dividerColor(color)
						end,
					}),
				}),
			}),

			SideKickInfo({
				selectedSideKick = selectedSideKick,
				accentColor = dividerColor,
				pulsePhase = pulsePhase,

				onLockClicked = function()
					print("Lock clicked")
				end,

				onRenameClicked = function()
					print("Rename clicked")
				end,

				onNameSubmitted = function(newName: string)
					print("Rename submitted:", newName)
				end,
			}),

			SideKickButtons({
				selectedSideKick = selectedSideKick,

				onEquip = function()
					print("Equip clicked")
				end,

				onUnequipAll = function()
					print("Unequip all clicked")
				end,

				onUpgrade = function()
					print("Upgrade clicked")
				end,

				onSelectDelete = function()
					print("Select delete clicked")
				end,

				onDeleteAll = function()
					print("Delete all clicked")
				end,

				onEquipBest = function()
					print("Equip best clicked")
				end,

				onDelete = function()
					print("Delete clicked")
				end,
			}),
		}),
	})
end

return SideKickMenu
