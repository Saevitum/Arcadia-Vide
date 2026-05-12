--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local create = Vide.create

local Text = Components.Text
local Image = Components.Image
local ActionButton = Components.ActionButton

type Source = SharedTypes.Source
type SkinItem = MenuTypes.SkinItem

export type SelectedSkinInfoProps = {
	selectedTab: Source,
	selectedSkin: Source,
	equippedSkinId: Source,
	accentColor: () -> Color3,
	pulsePhase: (() -> number)?,
	onEquip: ((skin: SkinItem) -> ())?,
}

local LOCK_IMAGE = "rbxassetid://13414458532"
local RENAME_IMAGE = "rbxassetid://13414468097"

local FONT_BOLD = Font.new(
	"rbxasset://fonts/families/Michroma.json",
	Enum.FontWeight.Bold,
	Enum.FontStyle.Normal
)

local FONT_BOLD_ITALIC = Font.new(
	"rbxasset://fonts/families/Michroma.json",
	Enum.FontWeight.Bold,
	Enum.FontStyle.Italic
)

local INFO_SIZE = UDim2.fromScale(0.22, 0.52)
local INFO_OPEN_POSITION = UDim2.fromScale(0.735, 0.55)
local INFO_CLOSED_POSITION = UDim2.fromScale(1.05, 0.55)

local function getSelected(props: SelectedSkinInfoProps): SkinItem?
	return props.selectedSkin()
end

local function getSelectedText(props: SelectedSkinInfoProps, selector: (SkinItem) -> string, fallback: string): string
	local selected = getSelected(props)

	if selected == nil then
		return fallback
	end

	return selector(selected)
end

local function getButtonText(skin: SkinItem?, equippedSkinId: string?): string
	if skin == nil then
		return "SELECT"
	end

	if skin.Locked or not skin.Owned then
		return "LOCKED"
	end

	if equippedSkinId == skin.SkinId then
		return "EQUIPPED"
	end

	return "EQUIP"
end

local function getStatusText(skin: SkinItem?, equippedSkinId: string?): string
	if skin == nil then
		return "Select a skin from the list."
	end

	if skin.Locked or not skin.Owned then
		return "Locked"
	end

	if equippedSkinId == skin.SkinId then
		return "Currently equipped"
	end

	return "Owned"
end

local function IconButton(props: {
	name: string,
	image: string,
	size: UDim2,
	position: UDim2,
	anchorPoint: Vector2,
	zIndex: number,
	onClick: (() -> ())?,
})
	return create("ImageButton")({
		Name = props.name,
		Image = props.image,
		ImageColor3 = Color3.fromRGB(255, 255, 255),
		ImageTransparency = 0,
		ScaleType = Enum.ScaleType.Fit,
		AutoButtonColor = false,

		Size = props.size,
		Position = props.position,
		AnchorPoint = props.anchorPoint,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = props.zIndex,

		Activated = function()
			if props.onClick ~= nil then
				props.onClick()
			end
		end,

		create("UICorner")({
			CornerRadius = UDim.new(0.15, 0),
		}),
	})
end

local function SelectedSkinInfo(props: SelectedSkinInfoProps)
	local function open(): boolean
		return props.selectedTab() == "Skins" and getSelected(props) ~= nil
	end

	return create("CanvasGroup")({
		Name = "SelectedSkinInfo",

		Size = INFO_SIZE,
		Position = INFO_OPEN_POSITION,
		AnchorPoint = Vector2.new(0.5, 0.5),

		Visible = false,
		GroupTransparency = 1,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = 23,

		Effects.SlideFadeCanvasGroup({
			open = open,

			openPosition = INFO_OPEN_POSITION,
			closedPosition = INFO_CLOSED_POSITION,

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

		create("UIStroke")({
			Color = Color3.fromRGB(255, 255, 255),
			Thickness = 2,
			Transparency = 0,

			create("UIGradient")({
				Color = function()
					local color = props.accentColor()

					return ColorSequence.new({
						ColorSequenceKeypoint.new(0, color),
						ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 255, 255)),
					})
				end,

				Rotation = 90,

				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 0),
					NumberSequenceKeypoint.new(0.602, 0.828),
					NumberSequenceKeypoint.new(1, 1),
				}),

				Effects.PulseGradientOffset({
					phase = props.pulsePhase,
					phaseMultiplier = 1,
					minOffset = Vector2.new(0, -0.35),
					maxOffset = Vector2.new(0, 0),
				}),
			}),
		}),

		create("Frame")({
			Name = "SkinImage",

			Size = UDim2.fromScale(1, 0.5),
			Position = UDim2.fromScale(0.5, 0.25),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,

			ZIndex = 24,

			Image({
				name = "SelectedSkinImage",

				image = function()
					local selected = getSelected(props)

					if selected == nil then
						return ""
					end

					return selected.ImageId
				end,

				size = UDim2.fromScale(1, 1),
				position = UDim2.fromScale(0.5, 0.5),
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = 24,

				gradient = {
					rotation = 90,

					transparency = NumberSequence.new({
						NumberSequenceKeypoint.new(0, 0),
						NumberSequenceKeypoint.new(0.8, 0.755),
						NumberSequenceKeypoint.new(1, 1),
					}),
				},
			}),

			IconButton({
				name = "Lock",
				image = LOCK_IMAGE,

				size = UDim2.fromScale(0.185, 0.193),
				position = UDim2.fromScale(0.149, 0.13),
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = 26,
			}),

			IconButton({
				name = "Rename",
				image = RENAME_IMAGE,

				size = UDim2.fromScale(0.185, 0.193),
				position = UDim2.fromScale(0.877, 0.124),
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = 26,
			}),
		}),

		Text({
			name = "Title",

			text = function()
				return getSelectedText(props, function(skin)
					return skin.Name
				end, "")
			end,

			size = UDim2.fromScale(0.926, 0.08),
			position = UDim2.fromScale(0.5, 0.55),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_BOLD,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.35,
			},

			zIndex = 27,
		}),

		Text({
			name = "Rarity",

			text = function()
				return getSelectedText(props, function(skin)
					return skin.Rarity
				end, "--")
			end,

			size = UDim2.fromScale(0.395, 0.05),
			position = UDim2.fromScale(0.5, 0.62),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_BOLD_ITALIC,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 14,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.2,
			},

			zIndex = 27,
		}),

		Text({
			name = "Description",

			text = function()
				return getSelectedText(props, function(skin)
					return skin.Description
				end, "")
			end,

			size = UDim2.fromScale(0.82, 0.16),
			position = UDim2.fromScale(0.5, 0.73),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Font.new(
				"rbxasset://fonts/families/Michroma.json",
				Enum.FontWeight.Regular,
				Enum.FontStyle.Normal
			),

			textScaled = true,
			textWrapped = true,
			minTextSize = 6,
			maxTextSize = 12,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.35,
			},

			zIndex = 27,
		}),

		Text({
			name = "Status",

			text = function()
				return getStatusText(getSelected(props), props.equippedSkinId())
			end,

			size = UDim2.fromScale(0.82, 0.055),
			position = UDim2.fromScale(0.5, 0.84),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_BOLD,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 12,

			textColor3 = Color3.fromRGB(0, 255, 238),

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.3,
			},

			zIndex = 27,
		}),

		ActionButton({
			name = "EquipButton",

			text = function()
				return getButtonText(getSelected(props), props.equippedSkinId())
			end,

			size = UDim2.fromScale(0.72, 0.07),
			position = UDim2.fromScale(0.5, 0.925),
			anchorPoint = Vector2.new(0.5, 0.5),

			variant = function()
				local skin = getSelected(props)

				if skin == nil or skin.Locked or not skin.Owned then
					return "Disabled"
				end

				if props.equippedSkinId() == skin.SkinId then
					return "Blue"
				end

				return "Green"
			end,

			disabled = function()
				local skin = getSelected(props)

				return skin == nil or skin.Locked or not skin.Owned or props.equippedSkinId() == skin.SkinId
			end,

			strokeThickness = 1.5,
			hoverScale = 1.08,
			scaleTextConstraints = true,

			zIndex = 27,

			onClick = function()
				local skin = getSelected(props)

				if skin == nil or skin.Locked or not skin.Owned then
					return
				end

				if props.onEquip ~= nil then
					props.onEquip(skin)
				end
			end,
		}),
	})
end

return SelectedSkinInfo
