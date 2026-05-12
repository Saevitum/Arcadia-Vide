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

local Tokens = Style.Tokens
local Gradients = Style.Gradients

local function rarityColor(rarity: string): Color3
	return Tokens.RarityColors[rarity] or Tokens.Colors.CyanBright
end

local function isSelected(props: SkinCardProps): boolean
	return props.selectedSkinId() == props.skin.SkinId
end

local function isEquipped(props: SkinCardProps): boolean
	return props.equippedSkinId() == props.skin.SkinId
end

local function SkinCard(props: SkinCardProps)
	local skin = props.skin
	local zIndex = props.zIndex or 24

	local function selected(): boolean
		return isSelected(props)
	end

	local function equipped(): boolean
		return isEquipped(props)
	end

	local function locked(): boolean
		return skin.Locked or not skin.Owned
	end

	return create("ImageButton")({
		Name = `SkinCard_{skin.SkinId}`,

		Image = skin.ImageId,
		ScaleType = Enum.ScaleType.Crop,
		AutoButtonColor = false,

		BackgroundColor3 = Tokens.Colors.DarkGlass,
		BackgroundTransparency = function()
			if locked() then
				return 0.28
			end

			return 0.04
		end,

		BorderSizePixel = 0,

		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		Activated = function()
			if props.onSelected ~= nil then
				props.onSelected(skin)
			end
		end,

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = 1.05,
			scaleTextConstraints = true,
			duration = Tokens.Timing.Hover,
		}),

		create("UICorner")({
			CornerRadius = Tokens.Corners.Medium,
		}),

		create("UIStroke")({
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

			Color = function()
				if selected() then
					return Tokens.Colors.White
				end

				return rarityColor(skin.Rarity)
			end,

			Thickness = function()
				if selected() then
					return 3
				end

				return 2
			end,

			Transparency = function()
				if locked() then
					return 0.45
				end

				if selected() then
					return 0
				end

				return 0.12
			end,

			create("UIGradient")({
				Rotation = 0,

				Color = function()
					if selected() then
						return Gradients.cyberPrimary()
					end

					return Gradients.rarity(skin.Rarity)
				end,
			}),
		}),

		create("UIGradient")({
			Rotation = 90,
			Transparency = NumberSequence.new({
				NumberSequenceKeypoint.new(0, 0.05),
				NumberSequenceKeypoint.new(0.62, 0.24),
				NumberSequenceKeypoint.new(1, 0.58),
			}),
		}),

		create("Frame")({
			Name = "BottomShade",

			Size = UDim2.fromScale(1, 0.36),
			Position = UDim2.fromScale(0.5, 1),
			AnchorPoint = Vector2.new(0.5, 1),

			BackgroundColor3 = Tokens.Colors.Black,
			BackgroundTransparency = 0.18,
			BorderSizePixel = 0,

			ZIndex = zIndex + 1,

			create("UICorner")({
				CornerRadius = Tokens.Corners.Medium,
			}),

			create("UIGradient")({
				Rotation = 90,
				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 1),
					NumberSequenceKeypoint.new(0.45, 0.35),
					NumberSequenceKeypoint.new(1, 0),
				}),
			}),
		}),

		Text({
			name = "SkinName",
			text = skin.Name,

			size = UDim2.fromScale(0.88, 0.18),
			position = UDim2.fromScale(0.5, 0.82),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Tokens.Fonts.MichromaBoldItalic,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 15,

			textColor3 = Tokens.Colors.White,

			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.12,
			},

			zIndex = zIndex + 2,
		}),

		Text({
			name = "Rarity",
			text = skin.Rarity:upper(),

			size = UDim2.fromScale(0.78, 0.13),
			position = UDim2.fromScale(0.5, 0.94),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Tokens.Fonts.MichromaBold,
			textScaled = true,
			minTextSize = 5,
			maxTextSize = 11,

			textColor3 = rarityColor(skin.Rarity),

			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.2,
			},

			zIndex = zIndex + 2,
		}),

		create("Frame")({
			Name = "EquippedBadge",

			Size = UDim2.fromScale(0.42, 0.16),
			Position = UDim2.fromScale(0.5, 0.08),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Visible = equipped,

			BackgroundColor3 = Tokens.Colors.Green,
			BackgroundTransparency = 0.02,
			BorderSizePixel = 0,

			ZIndex = zIndex + 3,

			create("UICorner")({
				CornerRadius = Tokens.Corners.Round,
			}),

			create("UIStroke")({
				ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
				Color = Tokens.Colors.White,
				Transparency = 0.15,
				Thickness = 1,
			}),

			Text({
				name = "EquippedText",
				text = "EQUIPPED",

				size = UDim2.fromScale(0.9, 0.8),
				position = UDim2.fromScale(0.5, 0.5),
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = Tokens.Fonts.MichromaBold,
				textScaled = true,
				minTextSize = 5,
				maxTextSize = 10,

				textColor3 = Tokens.Colors.White,

				stroke = {
					thickness = 1,
					color = Tokens.Colors.Black,
					transparency = 0.2,
				},

				zIndex = zIndex + 4,
			}),
		}),

		create("Frame")({
			Name = "LockedOverlay",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Visible = locked,

			BackgroundColor3 = Tokens.Colors.Black,
			BackgroundTransparency = 0.48,
			BorderSizePixel = 0,

			ZIndex = zIndex + 5,

			create("UICorner")({
				CornerRadius = Tokens.Corners.Medium,
			}),

			Text({
				name = "LockedText",
				text = "LOCKED",

				size = UDim2.fromScale(0.7, 0.16),
				position = UDim2.fromScale(0.5, 0.45),
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = Tokens.Fonts.MichromaBoldItalic,
				textScaled = true,
				minTextSize = 8,
				maxTextSize = 18,

				textColor3 = Tokens.Colors.MutedWhite,

				stroke = {
					thickness = 1,
					color = Tokens.Colors.Black,
					transparency = 0.1,
				},

				zIndex = zIndex + 6,
			}),
		}),
	})
end

return SkinCard
