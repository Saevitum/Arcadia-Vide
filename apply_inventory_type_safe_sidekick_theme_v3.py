#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inventory sidekick-theme patch v3.

Writes these files:
- src/client/UI/UIManager/Menus/Inventory/init.lua
- src/client/UI/UIManager/Menus/Inventory/SkinsPage.lua
- src/client/UI/UIManager/Menus/Inventory/SkinCard.lua
- src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua

Main fixes:
- Uses generic SharedTypes.Source<T> everywhere.
- Applies requested layout values:
    InventoryTabStrip position 0.5, 0.23 size 0.42, 0.06
    SkinInventoryPage position 0.35, 0.55 size 0.45, 0.53
    SelectedSkinInfo position 0.735, 0.55 size 0.22, 0.52
- Makes SkinCard visually mirror SideKickCard:
    ImageButton root
    rarity border
    equipped ImageLabel
    locked ImageLabel
    name only
    no rarity text
    no equipped text
- Makes SelectedSkinInfo visually mirror SideKickInfo:
    CanvasGroup transparent shell
    SlideFadeCanvasGroup
    same animated UIStroke + PulseGradientOffset pattern
    same image gradient/fade style
- Keeps Inventory-specific equip ActionButton.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / "src" / "client" / "UI" / "UIManager" / "Menus" / "Inventory"
BACKUP = ROOT / "_local_backups" / "inventory_type_safe_sidekick_theme_v3"

FILES: dict[str, str] = {}

FILES["init.lua"] = """--!strict

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

local TAB_STYLE = Style.Tabs.Presets.CyberThreeTabs

local TAB_STRIP_SIZE = UDim2.fromScale(0.42, 0.06)
local TAB_STRIP_POSITION = UDim2.fromScale(0.5, 0.23)

local SEARCH_SIZE = UDim2.fromScale(0.25, 0.045)
local SEARCH_POSITION = UDim2.fromScale(0.735, 0.23)

local DIVIDER_SIZE = UDim2.fromScale(0.004, 0.5)
local DIVIDER_POSITION = UDim2.fromScale(0.605, 0.55)

local function InventoryMenu(props: Types.InventoryMenuProps)
	local selectedTab: Source<InventoryTabId> = source("Skins" :: InventoryTabId)

	local defaultSkin: SkinItem? = MockInventory.getDefaultSkin()
	local selectedSkin: Source<SkinItem?> = source(defaultSkin)
	local selectedSkinId: Source<string?> = source(if defaultSkin ~= nil then defaultSkin.SkinId else nil)
	local equippedSkinId: Source<string?> = source(MockInventory.getDefaultEquippedSkinId())
	local searchQuery: Source<string> = source("")

	local pulsePhase: Source<number> = source(0)
	local accentColor: Source<Color3> = source(Style.Tokens.Colors.CyanBright)

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

			Tabs.TabStrip({
				name = "InventoryTabStrip",

				tabs = MockInventory.TABS :: any,
				selectedTab = selectedTab,

				size = TAB_STRIP_SIZE,
				position = TAB_STRIP_POSITION,
				anchorPoint = Vector2.new(0.5, 0.5),

				cellSize = UDim2.fromScale(0.3, 0.7),
				cellPadding = UDim2.fromScale(0.035, 0),
				fillDirectionMaxCells = 3,

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

				Size = DIVIDER_SIZE,
				Position = DIVIDER_POSITION,
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
						phase = pulsePhase,
						edgeColor = Style.Tokens.Colors.White,
						middleColors = {
							Style.Tokens.Colors.CyanBright,
							Style.Tokens.Colors.Magenta,
							Style.Tokens.Colors.Red,
						},
						loopsPerColor = 1,
						edgeTransparency = 1,
						middleTransparency = 0,
						colorTweenDuration = 0.22,

						onColorChanged = function(color: Color3)
							accentColor(color)
						end,
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
				accentColor = accentColor,
				pulsePhase = pulsePhase,
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
"""

FILES["SkinsPage.lua"] = """--!strict

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

local PAGE_SIZE = UDim2.fromScale(0.45, 0.53)
local PAGE_POSITION = UDim2.fromScale(0.35, 0.55)
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
		Name = "SkinInventoryPage",

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
				cellSize = UDim2.fromScale(0.215, 0.305),
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
"""

FILES["SkinCard.lua"] = """--!strict

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
"""

FILES["SelectedSkinInfo.lua"] = """--!strict

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
local ActionButton = Components.ActionButton

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = MenuTypes.InventoryTabId
type SkinItem = MenuTypes.SkinItem

export type SelectedSkinInfoProps = {
	selectedTab: Source<InventoryTabId>,
	selectedSkin: Source<SkinItem?>,
	equippedSkinId: Source<string?>,
	accentColor: Source<Color3>,
	pulsePhase: Source<number>,
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

			fontFace = Font.new(
				"rbxasset://fonts/families/Michroma.json",
				Enum.FontWeight.Bold,
				Enum.FontStyle.Normal
			),

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

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
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

				fontFace = Font.new(
					"rbxasset://fonts/families/Michroma.json",
					Enum.FontWeight.Bold,
					Enum.FontStyle.Normal
				),

				textScaled = true,
				minTextSize = 6,
				maxTextSize = 12,

				textColor3 = Color3.fromRGB(0, 255, 238),
				textXAlignment = Enum.TextXAlignment.Center,
				textYAlignment = Enum.TextYAlignment.Center,

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
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

				fontFace = Font.new(
					"rbxasset://fonts/families/Michroma.json",
					Enum.FontWeight.Regular,
					Enum.FontStyle.Normal
				),

				textScaled = true,
				textWrapped = true,
				minTextSize = 6,
				maxTextSize = 12,

				textColor3 = Color3.fromRGB(220, 230, 235),
				textXAlignment = Enum.TextXAlignment.Center,
				textYAlignment = Enum.TextYAlignment.Center,

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
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

					return skin == nil
						or skin.Locked
						or not skin.Owned
						or props.equippedSkinId() == skin.SkinId
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
		}),
	})
end

return SelectedSkinInfo
"""


def backup_file(path: Path) -> None:
    if not path.exists():
        return

    rel = path.relative_to(ROOT)
    dst = BACKUP / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)


def write_file(name: str, content: str) -> None:
    path = BASE / name
    backup_file(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


def main() -> None:
    if not BASE.exists():
        raise SystemExit(f"Inventory folder not found: {BASE}")

    BACKUP.mkdir(parents=True, exist_ok=True)

    for name, content in FILES.items():
        write_file(name, content)

    print()
    print("Done.")
    print(f"Backups: {BACKUP.relative_to(ROOT)}")
    print()
    print("Next:")
    print("  1. Open Roblox Studio / Rojo sync.")
    print("  2. Check Luau type errors.")
    print("  3. If clean, run: git diff")
    print("  4. Commit when verified.")


if __name__ == "__main__":
    main()
