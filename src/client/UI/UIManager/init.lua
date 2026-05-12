--!strict

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Store = require(script.Store)
local Menus = require(script.Menus)
local Buttons = require(script.Buttons)

local ButtonBar = Buttons.ButtonBar
local SideKickMenu = Menus.SideKickMenu
local BoostersMenu = Menus.BoostersMenu
local ActivityMenu = Menus.ActivityMenu
local StatsMenu = Menus.StatsMenu
local QuestsMenu = Menus.QuestsMenu
local InventoryMenu = Menus.InventoryMenu
local AchievementsMenu = Menus.AchievementsMenu
local RewardsMenu = Menus.RewardsMenu
local SettingsMenu = Menus.SettingsMenu
local ShopMenu = Menus.ShopMenu

Vide.strict = true

local UI = {}

local destroyRoot: (() -> ())? = nil

function UI.Start()
	if destroyRoot ~= nil then
		return
	end

	local player = Players.LocalPlayer
	local playerGui = player:WaitForChild("PlayerGui")

	destroyRoot = Vide.root(function()
		local screenGui = Vide.create("ScreenGui")({
			Name = "ArcadiaUI",
			ResetOnSpawn = false,
			IgnoreGuiInset = true,
			ZIndexBehavior = Enum.ZIndexBehavior.Sibling,

			-- BUTTON BAR (bottom UI)
			ButtonBar({
				store = Store,
			}),

			-- MENUS
			SideKickMenu({
				store = Store,
			}),
			BoostersMenu({
				store = Store,
			}),
			ActivityMenu({
				store = Store,
			}),
			StatsMenu({
				store = Store,
			}),
			QuestsMenu({
				store = Store,
			}),
			InventoryMenu({
				store = Store,
			}),
			AchievementsMenu({
				store = Store,
			}),
			RewardsMenu({
				store = Store,
			}),
			SettingsMenu({
				store = Store,
			}),
			ShopMenu({
				store = Store,
			}),
		})

		screenGui.Parent = playerGui
	end)
end

function UI.Stop()
	if destroyRoot ~= nil then
		destroyRoot()
		destroyRoot = nil
	end
end

return UI
