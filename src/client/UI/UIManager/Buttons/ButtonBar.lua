--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local create = Vide.create

local SideKickButton = require(script.Parent.SideKickButton)
local BoostersButton = require(script.Parent.BoostersButton)
local ActivityButton = require(script.Parent.ActivityButton)
local StatsButton = require(script.Parent.StatsButton)
local QuestsButton = require(script.Parent.QuestsButton)
local InventoryButton = require(script.Parent.InventoryButton)
local AchievementsButton = require(script.Parent.AchievementsButton)
local RewardsButton = require(script.Parent.RewardsButton)
local SettingsButton = require(script.Parent.SettingsButton)
local ShopButton = require(script.Parent.ShopButton)

Vide.strict = true

local function ButtonBar(props)
	return create("Frame")({
		Name = "ButtonBar",

		AnchorPoint = Vector2.new(0.5, 1),
		Position = UDim2.fromScale(0.5, 0.97),

		Size = UDim2.fromScale(0.8, 0.16),

		BackgroundTransparency = 1,

		create("UIListLayout")({
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			VerticalAlignment = Enum.VerticalAlignment.Center,
			Padding = UDim.new(0.02, 0),
			SortOrder = Enum.SortOrder.LayoutOrder,
		}),

		SideKickButton({
			store = props.store,
			layoutOrder = 1,
		}),

		BoostersButton({
			store = props.store,
			layoutOrder = 2,
		}),

		StatsButton({
			store = props.store,
			layoutOrder = 3,
		}),

		QuestsButton({
			store = props.store,
			layoutOrder = 4,
		}),

		InventoryButton({
			store = props.store,
			layoutOrder = 5,
		}),

		AchievementsButton({
			store = props.store,
			layoutOrder = 6,
		}),

		ActivityButton({
			store = props.store,
			layoutOrder = 7,
		}),

		RewardsButton({
			store = props.store,
			layoutOrder = 8,
		}),

		SettingsButton({
			store = props.store,
			layoutOrder = 9,
		}),

		ShopButton({
			store = props.store,
			layoutOrder = 10,
		}),
	})
end

return ButtonBar
