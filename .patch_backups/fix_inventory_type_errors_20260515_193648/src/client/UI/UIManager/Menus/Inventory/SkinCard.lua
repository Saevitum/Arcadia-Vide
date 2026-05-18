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

local Tokens = Style.Tokens

type Source = SharedTypes.Source
type SkinItem = MenuTypes.SkinItem

export type SkinCardProps = {
	skin: SkinItem,
	selectedSkinId: Source,
	equippedSkinId: Source,
	layoutOrder: number?,
	zIndex: number?,
	onSelected: (skin: SkinItem) -> (),
}

local EQUIPPED_IMAGE = "rbxassetid://13415241367"
local SELECTED_IMAGE = "rbxassetid://13415286900"

local function getRarityColor(rarity: string): Color3
	return (Tokens.RarityColors :: { [string]: Color3 })[rarity] or Tokens.Colors.White
end

local function isSelected(props: SkinCardProps): boolean
	return props.selectedSkinId() == props.skin.SkinId
end

local function isEquipped(props: SkinCardProps): boolean
	return props.equippedSkinId() == props.skin.SkinId
end

local function SkinCard(props: SkinCardProps)
	local skin = props.skin
	local rarityColor = getRarityColor(skin.Rarity)
	local zIndex = props.zIndex or 24

	return create("ImageButton")({
		Name = `SkinCard_{skin.SkinId}`,
		Image = skin.ImageId,
		ImageTransparency = 0,
		ImageColor3 = Tokens.Colors.White,
		ScaleType = Enum.ScaleType.Stretch,
		AutoButtonColor = false,
		Size = UDim2.fromScale(1, 1),
		BackgroundTransparency = 1,
		BackgroundColor3 = Tokens.Colors.DarkGlass,
		BorderSizePixel = 0,
		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		Activated = function()
			props.onSelected(skin)
		end,

		create("UICorner")({
			CornerRadius = Tokens.Corners.Small,
		}),

		create("UIStroke")({
			Thickness = 2,
			Color = function()
				if isSelected(props) then
					return Tokens.Colors.Magenta
				end

				return rarityColor
			end,
			Transparency = function()
				if isSelected(props) then
					return 0
				end

				return 0.15
			end,
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
		}),

		-- Kept hidden for future deletion/select-delete mode.
		Image({
			name = "Selected",
			image = SELECTED_IMAGE,
			size = UDim2.fromScale(0.8, 0.8),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),
			visible = false,
			zIndex = zIndex + 1,
		}),

		Image({
			name = "Equipped",
			image = EQUIPPED_IMAGE,
			size = UDim2.fromScale(0.339, 0.289),
			position = UDim2.fromScale(0, 0),
			anchorPoint = Vector2.new(0, 0),
			visible = function()
				return isEquipped(props)
			end,
			zIndex = zIndex + 4,
		}),

		Text({
			name = "Title",
			text = skin.Name,
			size = UDim2.fromScale(0.843, 0.173),
			position = UDim2.fromScale(0.5, 0.9),
			anchorPoint = Vector2.new(0.5, 0.5),
			fontFace = Tokens.Fonts.MichromaBoldItalic,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,
			textColor3 = Tokens.Colors.White,
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,
			stroke = {
				thickness = 2,
				color = Tokens.Colors.Black,
				transparency = 0.1,
			},
			zIndex = zIndex + 5,
		}),

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = 1.06,
			duration = 0.12,
		}),
	})
end

return SkinCard
