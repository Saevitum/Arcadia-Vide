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

local Tokens = Style.Tokens
local Gradients = Style.Gradients

type Source = SharedTypes.Source
type InventoryTabId = MenuTypes.InventoryTabId
type SkinItem = MenuTypes.SkinItem

export type SelectedSkinInfoProps = {
	selectedTab: Source,
	selectedSkin: Source,
	equippedSkinId: Source,
	accentColor: Source,
	pulsePhase: Source,
	onEquip: ((skin: SkinItem) -> ())?,
}

local INFO_SIZE = UDim2.fromScale(0.22, 0.52)
local INFO_OPEN_POSITION = UDim2.fromScale(0.735, 0.55)
local INFO_CLOSED_POSITION = UDim2.fromScale(1.05, 0.55)

local function getSelected(props: SelectedSkinInfoProps): SkinItem?
	return props.selectedSkin()
end

local function getSelectedText(
	props: SelectedSkinInfoProps,
	selector: (SkinItem) -> string,
	fallback: string
): string
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

	if equippedSkinId == skin.SkinId then
		return "EQUIPPED"
	end

	return "EQUIP"
end

local function getStatusText(skin: SkinItem?, equippedSkinId: string?): string
	if skin == nil then
		return "Select a skin from the list."
	end

	if equippedSkinId == skin.SkinId then
		return "Currently equipped"
	end

	return "Ready to equip"
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
			Color = Tokens.Colors.White,
			Thickness = 2,
			Transparency = 0,

			create("UIGradient")({
				Color = function()
					local color = props.accentColor()
					return ColorSequence.new({
						ColorSequenceKeypoint.new(0, color),
						ColorSequenceKeypoint.new(0.5, Tokens.Colors.White),
						ColorSequenceKeypoint.new(1, color),
					})
				end,
				Rotation = 90,
				Transparency = Gradients.strokePulseTransparency(),

				Effects.PulseGradientOffset({
					phase = props.pulsePhase,
					phaseMultiplier = 3,
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
			fontFace = Tokens.Fonts.MichromaBold,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,
			textColor3 = Tokens.Colors.White,
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,
			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.35,
			},
			zIndex = 25,
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
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 14,
			textColor3 = Tokens.Colors.White,
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,
			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.2,
			},
			zIndex = 25,
		}),

		create("Frame")({
			Name = "SelectedSkinDetails",
			Size = UDim2.fromScale(1, 0.5),
			Position = UDim2.fromScale(0.5, 0.75),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 24,

			Text({
				name = "Status",
				text = function()
					return getStatusText(props.selectedSkin(), props.equippedSkinId())
				end,
				size = UDim2.fromScale(0.84, 0.12),
				position = UDim2.fromScale(0.5, 0.2),
				anchorPoint = Vector2.new(0.5, 0.5),
				fontFace = Tokens.Fonts.MichromaBold,
				textScaled = true,
				minTextSize = 6,
				maxTextSize = 12,
				textColor3 = Tokens.Colors.CyanBright,
				textXAlignment = Enum.TextXAlignment.Center,
				textYAlignment = Enum.TextYAlignment.Center,
				stroke = {
					thickness = 1,
					color = Tokens.Colors.Black,
					transparency = 0.3,
				},
				zIndex = 25,
			}),

			Text({
				name = "Description",
				text = function()
					return getSelectedText(props, function(skin)
						return skin.Description
					end, "")
				end,
				size = UDim2.fromScale(0.84, 0.26),
				position = UDim2.fromScale(0.5, 0.43),
				anchorPoint = Vector2.new(0.5, 0.5),
				fontFace = Tokens.Fonts.MichromaRegular,
				textScaled = true,
				textWrapped = true,
				minTextSize = 6,
				maxTextSize = 12,
				textColor3 = Color3.fromRGB(220, 230, 235),
				textXAlignment = Enum.TextXAlignment.Center,
				textYAlignment = Enum.TextYAlignment.Center,
				stroke = {
					thickness = 1,
					color = Tokens.Colors.Black,
					transparency = 0.35,
				},
				zIndex = 25,
			}),

			ActionButton({
				name = "EquipButton",
				text = function()
					return getButtonText(props.selectedSkin(), props.equippedSkinId())
				end,
				size = UDim2.fromScale(0.72, 0.13),
				position = UDim2.fromScale(0.5, 0.82),
				anchorPoint = Vector2.new(0.5, 0.5),
				variant = function()
					local skin = props.selectedSkin()
					if skin == nil then
						return "Disabled"
					end

					if props.equippedSkinId() == skin.SkinId then
						return "Blue"
					end

					return "Green"
				end,
				disabled = function()
					local skin = props.selectedSkin()
					return skin == nil or props.equippedSkinId() == skin.SkinId
				end,
				strokeThickness = 1.5,
				hoverScale = 1.08,
				scaleTextConstraints = true,
				zIndex = 25,
				onClick = function()
					local skin = props.selectedSkin()
					if skin == nil then
						return
					end

					if props.onEquip ~= nil then
						props.onEquip(skin)
					end
				end,
			}),
		}),
	})
end

return SelectedSkinInfo
