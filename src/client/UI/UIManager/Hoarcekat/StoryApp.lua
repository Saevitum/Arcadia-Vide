--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

local Buttons = require(script.Parent.Parent.Buttons)
local Menus = require(script.Parent.Parent.Menus)

Vide.strict = true

local create = Vide.create

type UIStore = Types.UIStore

export type StoryAppProps = {
	store: UIStore,
}

local function StoryApp(props: StoryAppProps)
	local store = props.store

	return create("Frame")({
		Name = "HoarcekatStoryApp",

		Size = UDim2.fromScale(1, 1),
		Position = UDim2.fromScale(0, 0),
		AnchorPoint = Vector2.new(0, 0),

		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		ClipsDescendants = false,
		ZIndex = 1,

		-- Full interactive button bar.
		Buttons.ButtonBar({
			store = store,
		}),

		-- All menus mounted at once.
		-- Visibility/opening is controlled by store.currentMenu.
		Menus.SideKickMenu({
			store = store,
		}),

		Menus.BoostersMenu({
			store = store,
		}),

		Menus.ActivityMenu({
			store = store,
		}),

		Menus.StatsMenu({
			store = store,
		}),

		Menus.QuestsMenu({
			store = store,
		}),

		Menus.InventoryMenu({
			store = store,
		}),

		Menus.AchievementsMenu({
			store = store,
		}),

		Menus.RewardsMenu({
			store = store,
		}),

		Menus.SettingsMenu({
			store = store,
		}),

		Menus.ShopMenu({
			store = store,
		}),
	})
end

return StoryApp
