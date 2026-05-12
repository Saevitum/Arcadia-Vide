#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apply Inventory menu v1 for Arcadia-Vide.

Run from repo root:
    python apply_inventory_menu_v1.py

What it does:
- Replaces UIManager/Menus/init.lua Inventory export to require script.Inventory
- Writes folder-based Inventory modules:
    Menus/Inventory/init.lua
    Menus/Inventory/MockInventory.lua
    Menus/Inventory/SkinCard.lua
    Menus/Inventory/SkinsPage.lua
    Menus/Inventory/RanksPage.lua
    Menus/Inventory/QuestsPage.lua
    Menus/Inventory/SelectedSkinInfo.lua
- Removes Menus/Inventory/Style.lua if present, because Inventory uses shared UIManager/Style
- Creates backups under _local_backups/inventory_menu_v1/
"""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path.cwd()
UI_MANAGER = REPO_ROOT / "src" / "client" / "UI" / "UIManager"
MENUS_DIR = UI_MANAGER / "Menus"
INVENTORY_DIR = MENUS_DIR / "Inventory"
BACKUP_ROOT = REPO_ROOT / "_local_backups" / "inventory_menu_v1"


def backup(path: Path) -> None:
    if not path.exists():
        return
    rel = path.relative_to(REPO_ROOT)
    target = BACKUP_ROOT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def write_file(path: Path, content: str) -> None:
    backup(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8", newline="\n")


def remove_file(path: Path) -> None:
    if path.exists():
        backup(path)
        path.unlink()


MOCK_INVENTORY = r'''
--!strict

local ComponentTypes = require(script.Parent.Parent.Parent.UITypes.ComponentTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)

export type InventoryTabId = MenuTypes.InventoryTabId
export type SkinItem = MenuTypes.SkinItem
export type SkinRarity = MenuTypes.SkinRarity
export type InventoryTabDefinition = ComponentTypes.TabDefinition<InventoryTabId>

local MockInventory = {}

local TABS: { InventoryTabDefinition } = {
	{
		id = "Skins",
		label = "SKINS",
		layoutOrder = 1,
		disabled = false,
		hasAlert = false,
	},

	{
		id = "Ranks",
		label = "RANKS",
		layoutOrder = 2,
		disabled = false,
		hasAlert = false,
	},

	{
		id = "Quests",
		label = "QUESTS",
		layoutOrder = 3,
		disabled = false,
		hasAlert = false,
	},
}

MockInventory.TABS = TABS

local SKINS: { SkinItem } = {
	{
		SkinId = "skin_cyber_runner",
		Name = "Cyber Runner",
		ImageId = "rbxassetid://13415286900",
		Rarity = "Common",
		Description = "A lightweight runner suit built for speed, agility, and clean neon movement trails.",
		Owned = true,
		Equipped = true,
		Locked = false,
	},

	{
		SkinId = "skin_neon_hacker",
		Name = "Neon Hacker",
		ImageId = "rbxassetid://13415241367",
		Rarity = "Uncommon",
		Description = "A neon-coded street outfit with reactive cyan panels and encrypted visor glow.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_void_agent",
		Name = "Void Agent",
		ImageId = "rbxassetid://14608383463",
		Rarity = "Rare",
		Description = "A dark tactical avatar prototype designed for stealth movement through Arcadia sectors.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_pulse_knight",
		Name = "Pulse Knight",
		ImageId = "rbxassetid://13414458532",
		Rarity = "Epic",
		Description = "A premium armored skin with magenta pulse lines and reinforced cyber plating.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_arc_light",
		Name = "Arc Light",
		ImageId = "rbxassetid://13414468097",
		Rarity = "Legendary",
		Description = "A radiant Arcadia champion skin powered by a high-density cyber core.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_singularity",
		Name = "Singularity",
		ImageId = "rbxassetid://13415034457",
		Rarity = "Mythic",
		Description = "A forbidden prototype that bends light around its frame and leaves unstable energy scars.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_grid_nomad",
		Name = "Grid Nomad",
		ImageId = "rbxassetid://13415286900",
		Rarity = "Common",
		Description = "A clean utility skin for new runners entering the grid for the first time.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_metro_jumper",
		Name = "Metro Jumper",
		ImageId = "rbxassetid://13415241367",
		Rarity = "Uncommon",
		Description = "A streetwear-inspired skin used by platform racers in the lower Arcadia routes.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_redline",
		Name = "Redline",
		ImageId = "rbxassetid://14608383463",
		Rarity = "Rare",
		Description = "A high-risk racing skin with red warning trims and aggressive combat-sport styling.",
		Owned = true,
		Equipped = false,
		Locked = false,
	},

	{
		SkinId = "skin_starforged",
		Name = "Starforged",
		ImageId = "rbxassetid://13414458532",
		Rarity = "Epic",
		Description = "A refined space-tech skin forged for elite dashers and late-cycle progression.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_overseer",
		Name = "Overseer",
		ImageId = "rbxassetid://13414468097",
		Rarity = "Legendary",
		Description = "A commanding premium skin with heavy black plating and controlled neon emission.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},

	{
		SkinId = "skin_eclipse",
		Name = "Eclipse",
		ImageId = "rbxassetid://13415034457",
		Rarity = "Mythic",
		Description = "A rare eclipse-class avatar silhouette made for special events and high prestige.",
		Owned = false,
		Equipped = false,
		Locked = true,
	},
}

MockInventory.SKINS = SKINS

function MockInventory.getDefaultSkin(): SkinItem?
	return SKINS[1]
end

function MockInventory.getDefaultEquippedSkinId(): string?
	for _, skin in ipairs(SKINS) do
		if skin.Equipped then
			return skin.SkinId
		end
	end

	return nil
end

function MockInventory.findSkinById(skinId: string): SkinItem?
	for _, skin in ipairs(SKINS) do
		if skin.SkinId == skinId then
			return skin
		end
	end

	return nil
end

return MockInventory
'''

SKIN_CARD = r'''
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
'''

SKINS_PAGE = r'''
--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

local MockInventory = require(script.Parent.MockInventory)
local SkinCard = require(script.Parent.SkinCard)

Vide.strict = true

local create = Vide.create

local ScrollArea = Components.ScrollArea

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = MenuTypes.InventoryTabId
type SkinItem = MenuTypes.SkinItem

export type SkinsPageProps = {
	selectedTab: Source<InventoryTabId>,
	selectedSkinId: Source<string?>,
	equippedSkinId: Source<string?>,
	searchQuery: Source<string>,

	onSelectSkin: (skin: SkinItem) -> (),
}

local Tokens = Style.Tokens

local PAGE_SIZE = UDim2.fromScale(0.5, 0.56)
local PAGE_POSITION = UDim2.fromScale(0.36, 0.565)
local PAGE_ANCHOR = Vector2.new(0.5, 0.5)

local function trim(value: string): string
	return string.gsub(value, "^%s*(.-)%s*$", "%1")
end

local function matchesSearch(skin: SkinItem, query: string): boolean
	local cleanQuery = string.lower(trim(query))

	if cleanQuery == "" then
		return true
	end

	local name = string.lower(skin.Name)
	local rarity = string.lower(skin.Rarity)
	local description = string.lower(skin.Description)

	return string.find(name, cleanQuery, 1, true) ~= nil
		or string.find(rarity, cleanQuery, 1, true) ~= nil
		or string.find(description, cleanQuery, 1, true) ~= nil
end

local function buildSkinCards(props: SkinsPageProps): { Instance }
	local children: { Instance } = {}
	local order = 0
	local query = props.searchQuery()

	for _, skin in ipairs(MockInventory.SKINS) do
		if matchesSearch(skin, query) then
			order += 1

			table.insert(
				children,
				SkinCard({
					skin = skin,
					selectedSkinId = props.selectedSkinId,
					equippedSkinId = props.equippedSkinId,
					layoutOrder = order,
					zIndex = 24,
					onSelected = props.onSelectSkin,
				})
			)
		end
	end

	return children
end

local function SkinsPage(props: SkinsPageProps)
	return create("CanvasGroup")({
		Name = "SkinsInventoryPage",

		Size = PAGE_SIZE,
		Position = PAGE_POSITION,
		AnchorPoint = PAGE_ANCHOR,

		Visible = false,
		GroupTransparency = 1,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = function()
			if props.selectedTab() == "Skins" then
				return 21
			end

			return 20
		end,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return props.selectedTab() == "Skins"
			end,

			openPosition = PAGE_POSITION,
			closedPosition = PAGE_POSITION,

			openTransparency = 0,
			closedTransparency = 1,

			duration = 0.28,
			fadeDuration = 0.2,
			closeFadeDuration = 0.12,

			easingStyle = Enum.EasingStyle.Sine,
			easingDirection = Enum.EasingDirection.InOut,

			fadeEasingStyle = Enum.EasingStyle.Sine,
			fadeEasingDirection = Enum.EasingDirection.InOut,

			hideWhenClosed = true,
		}),

		ScrollArea({
			name = "SkinsScrollArea",

			size = UDim2.fromScale(1, 1),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			zIndex = 22,

			backgroundTransparency = 1,
			backgroundColor3 = Tokens.Colors.Black,

			layoutKind = "Grid",

			padding = {
				top = UDim.new(0.025, 0),
				bottom = UDim.new(0.06, 0),
				left = UDim.new(0.025, 0),
				right = UDim.new(0.025, 0),
			},

			grid = {
				cellSize = UDim2.fromScale(0.205, 0.34),
				cellPadding = UDim2.fromScale(0.03, 0.045),
				fillDirection = Enum.FillDirection.Horizontal,
				fillDirectionMaxCells = 4,
				horizontalAlignment = Enum.HorizontalAlignment.Left,
				verticalAlignment = Enum.VerticalAlignment.Top,
				sortOrder = Enum.SortOrder.LayoutOrder,
			},

			scrollBarThickness = 5,
			scrollBarImageColor3 = Tokens.Colors.CyanBright,
			scrollBarImageTransparency = 0.2,

			automaticCanvasSize = Enum.AutomaticSize.None,
			canvasSize = UDim2.fromOffset(0, 0),
			syncGridCanvas = true,
			canvasBottomSafetyScale = 0.08,
			scrollingDirection = Enum.ScrollingDirection.Y,

			children = buildSkinCards(props),
		}),
	})
end

return SkinsPage
'''

SELECTED_SKIN_INFO = r'''
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
'''

EMPTY_PAGE_TEMPLATE = r'''
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
type InventoryTabId = MenuTypes.InventoryTabId

export type __PAGE_NAME__Props = {
	selectedTab: Source<InventoryTabId>,
}

local EMPTY_STYLE = Style.Pages.EmptyStates.CyberPanel
local PAGE_POSITION = UDim2.fromScale(0.5, 0.58)

local function __PAGE_NAME__(props: __PAGE_NAME__Props)
	return create("CanvasGroup")({
		Name = "__TAB__InventoryPage",

		Size = UDim2.fromScale(0.76, 0.43),
		Position = PAGE_POSITION,
		AnchorPoint = Vector2.new(0.5, 0.5),

		Visible = false,
		GroupTransparency = 1,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ZIndex = 21,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return props.selectedTab() == "__TAB__"
			end,

			openPosition = PAGE_POSITION,
			closedPosition = PAGE_POSITION,

			openTransparency = 0,
			closedTransparency = 1,

			duration = 0.28,
			fadeDuration = 0.2,
			closeFadeDuration = 0.12,

			easingStyle = Enum.EasingStyle.Sine,
			easingDirection = Enum.EasingDirection.InOut,

			fadeEasingStyle = Enum.EasingStyle.Sine,
			fadeEasingDirection = Enum.EasingDirection.InOut,

			hideWhenClosed = true,
		}),

		create("Frame")({
			Name = "__TAB__EmptyState",

			Size = EMPTY_STYLE.size,
			Position = UDim2.fromScale(0.5, 0.42),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = EMPTY_STYLE.backgroundColor,
			BackgroundTransparency = EMPTY_STYLE.backgroundTransparency,
			BorderSizePixel = 0,

			ZIndex = 22,

			create("UICorner")({
				CornerRadius = EMPTY_STYLE.cornerRadius,
			}),

			create("UIStroke")({
				Thickness = EMPTY_STYLE.strokeThickness,
				Color = EMPTY_STYLE.strokeColor,
				Transparency = EMPTY_STYLE.strokeTransparency,
				ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

				create("UIGradient")({
					Rotation = EMPTY_STYLE.strokeGradientRotation,
					Color = EMPTY_STYLE.strokeGradient,
				}),
			}),

			Text({
				name = "EmptyText",
				text = "__EMPTY_TEXT__",

				size = EMPTY_STYLE.textSize,
				position = EMPTY_STYLE.textPosition,
				anchorPoint = EMPTY_STYLE.textAnchorPoint,

				fontFace = EMPTY_STYLE.fontFace,
				textScaled = true,
				minTextSize = EMPTY_STYLE.minTextSize,
				maxTextSize = EMPTY_STYLE.maxTextSize,

				textColor3 = EMPTY_STYLE.textColor,

				stroke = {
					thickness = EMPTY_STYLE.textStrokeThickness,
					color = EMPTY_STYLE.textStrokeColor,
					transparency = EMPTY_STYLE.textStrokeTransparency,
				},

				zIndex = 23,
			}),
		}),
	})
end

return __PAGE_NAME__
'''

RANKS_PAGE = EMPTY_PAGE_TEMPLATE.replace("__PAGE_NAME__", "RanksPage").replace("__TAB__", "Ranks").replace("__EMPTY_TEXT__", "Rank inventory is not added yet.")
QUESTS_PAGE = EMPTY_PAGE_TEMPLATE.replace("__PAGE_NAME__", "QuestsPage").replace("__TAB__", "Quests").replace("__EMPTY_TEXT__", "Quest inventory is not added yet.")

INVENTORY_INIT = r'''
--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local SharedTypes = require(script.Parent.Parent.UITypes.SharedTypes)

local Components = require(script.Parent.Parent.Components)
local Tabs = require(script.Parent.Parent.Components.Tabs)
local Effects = require(script.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Style)

local MockInventory = require(script.MockInventory)
local SkinsPage = require(script.SkinsPage)
local RanksPage = require(script.RanksPage)
local QuestsPage = require(script.QuestsPage)
local SelectedSkinInfo = require(script.SelectedSkinInfo)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action
local cleanup = Vide.cleanup

local Panel = Components.Panel

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = Types.InventoryTabId
type SkinItem = Types.SkinItem

local TAB_LAYOUT = Style.Tabs.Layouts.ThreeTop
local TAB_STYLE = Style.Tabs.Presets.CyberThreeTabs

local SEARCH_SIZE = UDim2.fromScale(0.25, 0.055)
local SEARCH_POSITION = UDim2.fromScale(0.73, 0.275)

local function InventoryMenu(props: Types.InventoryMenuProps)
	local selectedTab: Source<InventoryTabId> = source("Skins" :: InventoryTabId)

	local defaultSkin = MockInventory.getDefaultSkin()
	local selectedSkin: Source<SkinItem?> = source(defaultSkin)
	local selectedSkinId: Source<string?> = source(if defaultSkin ~= nil then defaultSkin.SkinId else nil)
	local equippedSkinId: Source<string?> = source(MockInventory.getDefaultEquippedSkinId())
	local searchQuery: Source<string> = source("")

	local function selectSkin(skin: SkinItem)
		selectedSkin(skin)
		selectedSkinId(skin.SkinId)
	end

	local function equipSkin(skin: SkinItem)
		if skin.Locked or not skin.Owned then
			return
		end

		equippedSkinId(skin.SkinId)
	end

	return Panel({
		name = "InventoryMenu",
		store = props.store,
		menuId = "Inventory",
		title = "INVENTORY",

		content = create("Frame")({
			Name = "InventoryContent",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			Tabs.TabStrip({
				name = "InventoryTabStrip",

				tabs = MockInventory.TABS,
				selectedTab = selectedTab,

				size = TAB_LAYOUT.size,
				position = TAB_LAYOUT.position,
				anchorPoint = TAB_LAYOUT.anchorPoint,

				cellSize = TAB_LAYOUT.cellSize,
				cellPadding = TAB_LAYOUT.cellPadding,
				fillDirectionMaxCells = TAB_LAYOUT.fillDirectionMaxCells,

				style = TAB_STYLE,
				zIndex = 21,
			}),

			create("TextBox")({
				Name = "InventorySearchBox",

				Size = SEARCH_SIZE,
				Position = SEARCH_POSITION,
				AnchorPoint = Vector2.new(0.5, 0.5),

				Visible = function()
					return selectedTab() == "Skins"
				end,

				Text = "",
				PlaceholderText = "Search here...",
				ClearTextOnFocus = false,

				FontFace = Style.Tokens.Fonts.MichromaBold,
				TextScaled = true,
				TextColor3 = Style.Tokens.Colors.White,
				PlaceholderColor3 = Style.Tokens.Colors.Gray300,
				TextXAlignment = Enum.TextXAlignment.Left,
				TextYAlignment = Enum.TextYAlignment.Center,

				BackgroundColor3 = Style.Tokens.Colors.DarkGlass,
				BackgroundTransparency = 0.08,
				BorderSizePixel = 0,

				ZIndex = 23,

				action(function(instance: Instance)
					if not instance:IsA("TextBox") then
						return
					end

					local textBox = instance :: TextBox

					local connection = textBox:GetPropertyChangedSignal("Text"):Connect(function()
						searchQuery(textBox.Text)
					end)

					cleanup(function()
						connection:Disconnect()
					end)
				end),

				create("UICorner")({
					CornerRadius = Style.Tokens.Corners.Round,
				}),

				create("UIStroke")({
					ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
					Color = Style.Tokens.Colors.CyanBright,
					Transparency = 0.2,
					Thickness = 1.5,

					create("UIGradient")({
						Color = Style.Gradients.cyberCyanMagenta(),
						Rotation = 0,
					}),
				}),

				create("UIPadding")({
					PaddingLeft = UDim.new(0.07, 0),
					PaddingRight = UDim.new(0.07, 0),
				}),

				create("UITextSizeConstraint")({
					MinTextSize = 6,
					MaxTextSize = 14,
				}),
			}),

			create("Frame")({
				Name = "InventoryDivider",

				Size = UDim2.fromScale(0.003, 0.52),
				Position = UDim2.fromScale(0.59, 0.565),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundColor3 = Style.Tokens.Colors.White,
				BackgroundTransparency = 1,
				BorderSizePixel = 0,

				ZIndex = 22,

				Effects.FadeGuiObject({
					open = function()
						return selectedTab() == "Skins"
					end,

					openTransparency = 0,
					closedTransparency = 1,
					duration = 0.18,
					hideWhenClosed = true,
				}),

				create("UIGradient")({
					Rotation = 90,
					Color = ColorSequence.new(Style.Tokens.Colors.White),
					Transparency = Style.Gradients.edgeFadeTransparency(),

					Effects.SweepGradientKeypoint({
						edgeColor = Style.Tokens.Colors.White,
						middleColors = {
							Style.Tokens.Colors.CyanBright,
							Style.Tokens.Colors.Magenta,
							Style.Tokens.Colors.Red,
						},
						edgeTransparency = 1,
						middleTransparency = 0,
						duration = 1.2,
						colorTweenDuration = 0.22,
					}),
				}),
			}),

			SkinsPage({
				selectedTab = selectedTab,
				selectedSkinId = selectedSkinId,
				equippedSkinId = equippedSkinId,
				searchQuery = searchQuery,
				onSelectSkin = selectSkin,
			}),

			SelectedSkinInfo({
				selectedTab = selectedTab,
				selectedSkin = selectedSkin,
				equippedSkinId = equippedSkinId,
				onEquip = equipSkin,
			}),

			RanksPage({
				selectedTab = selectedTab,
			}),

			QuestsPage({
				selectedTab = selectedTab,
			}),
		}),
	})
end

return InventoryMenu
'''


def update_menus_init() -> None:
    path = MENUS_DIR / "init.lua"
    backup(path)
    text = path.read_text(encoding="utf-8")
    old = "InventoryMenu = require(script.InventoryMenu)"
    new = "InventoryMenu = require(script.Inventory)"
    if old not in text:
        print(f"[WARN] Did not find old InventoryMenu require in {path}")
    else:
        text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"[UPDATED] {path.relative_to(REPO_ROOT)}")


def main() -> None:
    if not UI_MANAGER.exists():
        raise SystemExit(f"UIManager not found: {UI_MANAGER}")

    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    INVENTORY_DIR.mkdir(parents=True, exist_ok=True)

    update_menus_init()

    write_file(INVENTORY_DIR / "MockInventory.lua", MOCK_INVENTORY)
    write_file(INVENTORY_DIR / "SkinCard.lua", SKIN_CARD)
    write_file(INVENTORY_DIR / "SkinsPage.lua", SKINS_PAGE)
    write_file(INVENTORY_DIR / "SelectedSkinInfo.lua", SELECTED_SKIN_INFO)
    write_file(INVENTORY_DIR / "RanksPage.lua", RANKS_PAGE)
    write_file(INVENTORY_DIR / "QuestsPage.lua", QUESTS_PAGE)
    write_file(INVENTORY_DIR / "init.lua", INVENTORY_INIT)

    remove_file(INVENTORY_DIR / "Style.lua")

    print()
    print("Inventory menu v1 applied.")
    print(f"Backups are in: {BACKUP_ROOT}")
    print()
    print("Next:")
    print("  1. Run Rojo/Studio typecheck.")
    print("  2. Test Inventory in Hoarcekat.")
    print("  3. If stable, delete old Menus/InventoryMenu.lua manually after verifying no requires remain.")


if __name__ == "__main__":
    main()
