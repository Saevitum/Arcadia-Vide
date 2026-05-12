--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local MockSideKicks = require(script.Parent.MockSideKicks)

Vide.strict = true

local create = Vide.create

local ActionButton = Components.ActionButton

type MockSideKick = MockSideKicks.MockSideKick

export type SideKickButtonsProps = {
	selectedSideKick: () -> MockSideKick?,

	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	zIndex: number?,

	onEquip: (() -> ())?,
	onEquipBest: (() -> ())?,
	onUnequipAll: (() -> ())?,
	onUpgrade: (() -> ())?,
	onDelete: (() -> ())?,
	onSelectDelete: (() -> ())?,
	onDeleteAll: (() -> ())?,
}

local function SideKickButtons(props: SideKickButtonsProps)
	local size = props.size or UDim2.fromScale(0.75, 0.05)
	local position = props.position or UDim2.fromScale(0.494, 0.8)
	local anchorPoint = props.anchorPoint or Vector2.new(0.5, 0.5)
	local zIndex = props.zIndex or 22

	return create("CanvasGroup")({
		Name = "SideKickButtons",

		Size = size,
		Position = position,
		AnchorPoint = anchorPoint,

		Visible = false,
		GroupTransparency = 1,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = zIndex,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return props.selectedSideKick() ~= nil
			end,

			openPosition = position,
			closedPosition = UDim2.fromScale(position.X.Scale, 1.08),

			openTransparency = 0,
			closedTransparency = 1,

			duration = 0.34,
			fadeDuration = 0.16,
			closeFadeDuration = 0.08,

			openEasingStyle = Enum.EasingStyle.Back,
			openEasingDirection = Enum.EasingDirection.Out,

			closeEasingStyle = Enum.EasingStyle.Quad,
			closeEasingDirection = Enum.EasingDirection.Out,

			fadeEasingStyle = Enum.EasingStyle.Quad,
			fadeEasingDirection = Enum.EasingDirection.Out,

			hideWhenClosed = true,
		}),

		create("UIListLayout")({
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			VerticalAlignment = Enum.VerticalAlignment.Center,
			SortOrder = Enum.SortOrder.LayoutOrder,
			Padding = UDim.new(0.015, 0),
		}),

		ActionButton({
			name = "EquipButton",
			text = "EQUIP",
			iconText = "🔥",

			variant = "Green",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 1,
			zIndex = zIndex + 1,

			onClick = props.onEquip,
		}),

		ActionButton({
			name = "EquipBestButton",
			text = "BEST",
			iconText = "💪",

			variant = "OrangeYellow",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 2,
			zIndex = zIndex + 1,

			onClick = props.onEquipBest,
		}),

		ActionButton({
			name = "UnequipAllButton",
			text = "UNEQUIP",
			iconText = "",

			variant = "Blue",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 3,
			zIndex = zIndex + 1,

			onClick = props.onUnequipAll,
		}),

		ActionButton({
			name = "UpgradeButton",
			text = "2/3",
			iconText = "🧬",

			variant = "Dark",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 4,
			zIndex = zIndex + 1,

			onClick = props.onUpgrade,
		}),

		ActionButton({
			name = "DeleteButton",
			text = "DELETE",
			iconText = "",

			variant = "Red",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 5,
			zIndex = zIndex + 1,

			onClick = props.onDelete,
		}),

		ActionButton({
			name = "SelectDeleteButton",
			text = "SELECT",
			iconText = "👆",

			variant = "Red2",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 6,
			zIndex = zIndex + 1,

			onClick = props.onSelectDelete,
		}),

		ActionButton({
			name = "DeleteAllButton",
			text = "DELETE  ALL",
			iconText = "",

			variant = "Red3",

			size = UDim2.fromScale(0.125, 0.6),
			layoutOrder = 7,
			zIndex = zIndex + 1,

			onClick = props.onDeleteAll,
		}),
	})
end

return SideKickButtons
