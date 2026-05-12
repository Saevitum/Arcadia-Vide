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
