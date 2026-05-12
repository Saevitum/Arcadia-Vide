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
