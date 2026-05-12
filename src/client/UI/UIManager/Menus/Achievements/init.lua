--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Components)
local MockAchievements = require(script.MockAchievements)

local TabStrip = require(script.TabStrip)

local MoneyPage = require(script.MoneyPage)
local GemsPage = require(script.GemsPage)
local PointsPage = require(script.PointsPage)
local WinsPage = require(script.WinsPage)
local LevelPage = require(script.LevelPage)
local PlaytimePage = require(script.PlaytimePage)
local LoginPage = require(script.LoginPage)
local QuestsPage = require(script.QuestsPage)
local SideKicksPage = require(script.SideKicksPage)
local PlaceholderPage = require(script.PlaceholderPage)

Vide.strict = true

local create = Vide.create
local source = Vide.source

local Panel = Components.Panel

type AchievementCategory = MockAchievements.AchievementCategory

local function AchievementsMenu(props: Types.AchievementsMenuProps)
	local selectedTab = source("Money" :: AchievementCategory)

	return Panel({
		name = "AchievementsMenu",
		store = props.store,
		menuId = "Achievements",
		title = "ACHIEVEMENTS",

		content = create("Frame")({
			Name = "AchievementsContent",

			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0, 0),
			AnchorPoint = Vector2.new(0, 0),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 11,

			TabStrip({
				selectedTab = selectedTab,
				zIndex = 21,
			}),

			MoneyPage({
				selectedTab = selectedTab,
			}),

			GemsPage({
				selectedTab = selectedTab,
			}),

			PointsPage({
				selectedTab = selectedTab,
			}),

			WinsPage({
				selectedTab = selectedTab,
			}),

			LevelPage({
				selectedTab = selectedTab,
			}),

			PlaytimePage({
				selectedTab = selectedTab,
			}),

			LoginPage({
				selectedTab = selectedTab,
			}),

			QuestsPage({
				selectedTab = selectedTab,
			}),

			SideKicksPage({
				selectedTab = selectedTab,
			}),

			PlaceholderPage({
				selectedTab = selectedTab,
			}),
		}),
	})
end

return AchievementsMenu
