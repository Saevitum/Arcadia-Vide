--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local MockSideKicks = require(script.Parent.MockSideKicks)
local Effects = require(script.Parent.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create

local Text = Components.Text
local Image = Components.Image

type MockSideKick = MockSideKicks.MockSideKick

export type SideKickCardProps = {
	sideKick: MockSideKick,

	layoutOrder: number?,

	selected: (() -> boolean)?,
	equipped: (() -> boolean)?,
	locked: (() -> boolean)?,

	onClick: (() -> ())?,
}

local EQUIPPED_IMAGE = "rbxassetid://13415241367"
local LOCKED_IMAGE = "rbxassetid://14608383463"
local SELECTED_IMAGE = "rbxassetid://13415286900"

local function readBool(reader: (() -> boolean)?): boolean
	if reader == nil then
		return false
	end

	return reader()
end

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

local function SideKickCard(props: SideKickCardProps)
	local sideKick = props.sideKick
	local rarityColor = getRarityColor(sideKick.Rarity)

	return create("ImageButton")({
		Name = `SideKickCard_{sideKick.SideKickId}`,

		Image = sideKick.ImageId,
		ImageTransparency = 0,
		ImageColor3 = Color3.fromRGB(255, 255, 255),
		ScaleType = Enum.ScaleType.Stretch,

		AutoButtonColor = false,

		Size = UDim2.fromScale(1, 1),
		BackgroundTransparency = 1,
		BackgroundColor3 = Color3.fromRGB(10, 11, 18),
		BorderSizePixel = 0,

		LayoutOrder = props.layoutOrder or 0,
		ZIndex = 12,

		Activated = function()
			if props.onClick ~= nil then
				props.onClick()
			end
		end,

		create("UICorner")({
			CornerRadius = UDim.new(0.08, 0),
		}),

		create("UIStroke")({
			Thickness = function()
				if readBool(props.selected) then
					return 2
				end

				return 2
			end,

			Color = function()
				if readBool(props.selected) then
					return Color3.fromRGB(255, 0, 255)
				end

				return rarityColor
			end,

			Transparency = function()
				if readBool(props.selected) then
					return 0
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

			zIndex = 13,
		}),

		Image({
			name = "Equipped",
			image = EQUIPPED_IMAGE,

			size = UDim2.fromScale(0.339, 0.289),
			position = UDim2.fromScale(0, 0),
			anchorPoint = Vector2.new(0, 0),

			visible = function()
				return readBool(props.equipped)
			end,

			zIndex = 16,
		}),

		Image({
			name = "Locked",
			image = LOCKED_IMAGE,

			size = UDim2.fromScale(0.396, 0.472),
			position = UDim2.fromScale(0.82, 0.6),
			anchorPoint = Vector2.new(0.5, 0.5),

			visible = function()
				return readBool(props.locked)
			end,

			zIndex = 16,
		}),

		Text({
			name = "Power",
			text = `x{sideKick.BasePower}`,

			size = UDim2.fromScale(0.35, 0.2),
			position = UDim2.fromScale(0.78, 0.1),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),

			textScaled = true,
			minTextSize = 8,
			maxTextSize = 18,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Right,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.15,
			},

			zIndex = 17,
		}),

		Text({
			name = "Title",
			text = sideKick.Name,

			size = UDim2.fromScale(0.843, 0.173),
			position = UDim2.fromScale(0.5, 0.9),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),

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

			zIndex = 17,
		}),

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = 1.06,
			duration = 0.12,
		}),
	})
end

return SideKickCard
