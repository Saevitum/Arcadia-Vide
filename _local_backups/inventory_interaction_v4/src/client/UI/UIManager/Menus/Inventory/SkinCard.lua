--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)

local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create

local Text = Components.Text
local Image = Components.Image

type Source<T> = SharedTypes.Source<T>
type SkinItem = MenuTypes.SkinItem

export type SkinCardProps = {
	skin: SkinItem,
	selectedSkinId: Source<string?>,
	equippedSkinId: Source<string?>,
	layoutOrder: number?,
	zIndex: number?,
	onSelected: ((skin: SkinItem) -> ())?,
}

local EQUIPPED_IMAGE = "rbxassetid://13415241367"
local LOCKED_IMAGE = "rbxassetid://14608383463"
local SELECTED_IMAGE = "rbxassetid://13415286900"

local function getRarityColor(rarity: string): Color3
	if rarity == "Common" then
		return Color3.fromRGB(175, 180, 190)
	end

	if rarity == "Uncommon" then
		return Color3.fromRGB(90, 255, 120)
	end

	if rarity == "Rare" then
		return Color3.fromRGB(0, 255, 238)
	end

	if rarity == "Epic" then
		return Color3.fromRGB(142, 5, 255)
	end

	if rarity == "Legendary" then
		return Color3.fromRGB(255, 170, 0)
	end

	if rarity == "Mythic" then
		return Color3.fromRGB(255, 0, 170)
	end

	return Color3.fromRGB(255, 255, 255)
end

local function SkinCard(props: SkinCardProps)
	local skin = props.skin
	local rarityColor = getRarityColor(skin.Rarity)
	local zIndex = props.zIndex or 24

	local function selected(): boolean
		return props.selectedSkinId() == skin.SkinId
	end

	local function equipped(): boolean
		return props.equippedSkinId() == skin.SkinId
	end

	local function locked(): boolean
		return skin.Locked or not skin.Owned
	end

	return create("ImageButton")({
		Name = `SkinCard_{skin.SkinId}`,

		Image = skin.ImageId,
		ImageTransparency = function()
			if locked() then
				return 0.28
			end

			return 0
		end,
		ImageColor3 = Color3.fromRGB(255, 255, 255),
		ScaleType = Enum.ScaleType.Stretch,

		AutoButtonColor = false,
		Size = UDim2.fromScale(1, 1),

		BackgroundTransparency = 1,
		BackgroundColor3 = Color3.fromRGB(10, 11, 18),
		BorderSizePixel = 0,

		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		Activated = function()
			if props.onSelected ~= nil then
				props.onSelected(skin)
			end
		end,

		create("UICorner")({
			CornerRadius = UDim.new(0.08, 0),
		}),

		create("UIStroke")({
			Thickness = 2,

			Color = function()
				if selected() then
					return Color3.fromRGB(255, 0, 255)
				end

				return rarityColor
			end,

			Transparency = function()
				if selected() then
					return 0
				end

				if locked() then
					return 0.35
				end

				return 0.15
			end,

			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
		}),

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

			visible = equipped,
			zIndex = zIndex + 4,
		}),

		Image({
			name = "Locked",
			image = LOCKED_IMAGE,

			size = UDim2.fromScale(0.396, 0.472),
			position = UDim2.fromScale(0.82, 0.6),
			anchorPoint = Vector2.new(0.5, 0.5),

			visible = locked,
			zIndex = zIndex + 4,
		}),

		Text({
			name = "Title",
			text = skin.Name,

			size = UDim2.fromScale(0.843, 0.173),
			position = UDim2.fromScale(0.5, 0.9),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Font.new(
				"rbxasset://fonts/families/Michroma.json",
				Enum.FontWeight.Bold,
				Enum.FontStyle.Italic
			),

			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 2,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.1,
			},

			zIndex = zIndex + 5,
		}),

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = 1.06,
			duration = 0.12,
			scaleTextConstraints = true,
		}),
	})
end

return SkinCard
