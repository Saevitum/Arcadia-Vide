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

local Panel = Components.Panel

type Source<T> = SharedTypes.Source<T>
type InventoryTabId = Types.InventoryTabId
type SkinItem = Types.SkinItem

local TAB_STYLE = Style.Tabs.Presets.CyberThreeTabs
local TAB_STRIP_SIZE = UDim2.fromScale(0.42, 0.06)
local TAB_STRIP_POSITION = UDim2.fromScale(0.5, 0.23)

local DIVIDER_SIZE = UDim2.fromScale(0.004, 0.5)
local DIVIDER_POSITION = UDim2.fromScale(0.605, 0.55)

local function InventoryMenu(props: Types.InventoryMenuProps)
	local selectedTab: Source<InventoryTabId> = source("Skins" :: InventoryTabId)

	local selectedSkin: Source<SkinItem?> = source(nil :: SkinItem?)
	local selectedSkinId: Source<string?> = source(nil :: string?)

	local equippedSkinId: Source<string?> = source(MockInventory.getDefaultEquippedSkinId())

	local pulsePhase: Source<number> = source(0)
	local accentColor: Source<Color3> = source(Style.Tokens.Colors.CyanBright)

	local function hasSelectedSkin(): boolean
		return selectedTab() == "Skins" and selectedSkin() ~= nil
	end

	local function selectSkin(skin: SkinItem)
		if selectedSkinId() == skin.SkinId then
			selectedSkin(nil)
			selectedSkinId(nil)
			return
		end

		selectedSkin(skin)
		selectedSkinId(skin.SkinId)
	end

	local function equipSkin(skin: SkinItem) equippedSkinId(skin.SkinId) end

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
					open = hasSelectedSkin,
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
				selectedSkin = selectedSkin,
				selectedSkinId = selectedSkinId,
				equippedSkinId = equippedSkinId,
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
