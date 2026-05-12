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
local ActionButton = Components.ActionButton

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = MenuTypes.InventoryTabId
type SkinItem = MenuTypes.SkinItem

export type SelectedSkinInfoProps = {
	selectedTab: Source<InventoryTabId>,
	selectedSkin: Source<SkinItem?>,
	equippedSkinId: Source<string?>,

	onEquip: ((skin: SkinItem) -> ())?,
}

local Tokens = Style.Tokens
local Gradients = Style.Gradients

local INFO_SIZE = UDim2.fromScale(0.22, 0.56)
local INFO_OPEN_POSITION = UDim2.fromScale(0.735, 0.565)
local INFO_CLOSED_POSITION = UDim2.fromScale(1.05, 0.565)

local function rarityColor(rarity: string): Color3
	return Tokens.RarityColors[rarity] or Tokens.Colors.CyanBright
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

local function SelectedSkinInfo(props: SelectedSkinInfoProps)
	local function open(): boolean
		return props.selectedTab() == "Skins" and props.selectedSkin() ~= nil
	end

	return create("CanvasGroup")({
		Name = "SelectedSkinInfo",

		Size = INFO_SIZE,
		Position = INFO_OPEN_POSITION,
		AnchorPoint = Vector2.new(0.5, 0.5),

		Visible = false,
		GroupTransparency = 1,

		BackgroundColor3 = Tokens.Colors.DarkGlass,
		BackgroundTransparency = 0.08,
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

			easingStyle = Enum.EasingStyle.Back,
			easingDirection = Enum.EasingDirection.Out,

			fadeEasingStyle = Enum.EasingStyle.Sine,
			fadeEasingDirection = Enum.EasingDirection.InOut,

			hideWhenClosed = true,
		}),

		create("UICorner")({
			CornerRadius = Tokens.Corners.Medium,
		}),

		create("UIStroke")({
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
			Color = Tokens.Colors.White,
			Transparency = 0.08,
			Thickness = 2,

			create("UIGradient")({
				Color = function()
					local skin = props.selectedSkin()

					if skin == nil then
						return Gradients.cyberCyanMagenta()
					end

					return Gradients.rarity(skin.Rarity)
				end,

				Rotation = 90,
				Transparency = Gradients.strokePulseTransparency(),
			}),
		}),

		create("ImageLabel")({
			Name = "PreviewImage",

			Size = UDim2.fromScale(0.82, 0.42),
			Position = UDim2.fromScale(0.5, 0.25),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Image = function()
				local skin = props.selectedSkin()
				return if skin ~= nil then skin.ImageId else ""
			end,

			ScaleType = Enum.ScaleType.Fit,

			BackgroundTransparency = 1,
			BorderSizePixel = 0,

			ZIndex = 24,
		}),

		Text({
			name = "SkinName",

			text = function()
				local skin = props.selectedSkin()
				return if skin ~= nil then skin.Name else "SELECT SKIN"
			end,

			size = UDim2.fromScale(0.9, 0.08),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Tokens.Fonts.MichromaBoldItalic,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 18,

			textColor3 = Tokens.Colors.White,

			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.08,
			},

			zIndex = 25,
		}),

		Text({
			name = "Rarity",

			text = function()
				local skin = props.selectedSkin()
				return if skin ~= nil then skin.Rarity:upper() else ""
			end,

			size = UDim2.fromScale(0.86, 0.055),
			position = UDim2.fromScale(0.5, 0.57),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Tokens.Fonts.MichromaBold,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 13,

			textColor3 = function()
				local skin = props.selectedSkin()
				return if skin ~= nil then rarityColor(skin.Rarity) else Tokens.Colors.CyanBright
			end,

			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.2,
			},

			zIndex = 25,
		}),

		Text({
			name = "Description",

			text = function()
				local skin = props.selectedSkin()
				return if skin ~= nil then skin.Description else ""
			end,

			size = UDim2.fromScale(0.82, 0.16),
			position = UDim2.fromScale(0.5, 0.69),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Tokens.Fonts.MichromaRegular,
			textScaled = true,
			textWrapped = true,
			minTextSize = 6,
			maxTextSize = 12,

			textColor3 = Tokens.Colors.MutedWhite,

			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.35,
			},

			zIndex = 25,
		}),

		Text({
			name = "Status",

			text = function()
				return getStatusText(props.selectedSkin(), props.equippedSkinId())
			end,

			size = UDim2.fromScale(0.82, 0.055),
			position = UDim2.fromScale(0.5, 0.81),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Tokens.Fonts.MichromaBold,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 12,

			textColor3 = Tokens.Colors.CyanBright,

			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.3,
			},

			zIndex = 25,
		}),

		ActionButton({
			name = "EquipButton",

			text = function()
				return getButtonText(props.selectedSkin(), props.equippedSkinId())
			end,

			size = UDim2.fromScale(0.72, 0.07),
			position = UDim2.fromScale(0.5, 0.91),
			anchorPoint = Vector2.new(0.5, 0.5),

			variant = function()
				local skin = props.selectedSkin()

				if skin == nil or skin.Locked or not skin.Owned then
					return "Disabled"
				end

				if props.equippedSkinId() == skin.SkinId then
					return "Blue"
				end

				return "Green"
			end,

			disabled = function()
				local skin = props.selectedSkin()
				return skin == nil or skin.Locked or not skin.Owned or props.equippedSkinId() == skin.SkinId
			end,

			strokeThickness = 1.5,
			hoverScale = 1.08,
			scaleTextConstraints = true,

			zIndex = 25,

			onClick = function()
				local skin = props.selectedSkin()

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
