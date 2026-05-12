--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Components)

Vide.strict = true

local Panel = Components.Panel

local function StatsMenu(props: Types.StatsMenuProps)
	return Panel({
		name = "StatsMenu",
		store = props.store,
		menuId = "Stats",
		title = "STATS",
	})
end

return StatsMenu
