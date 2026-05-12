--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Components)

Vide.strict = true

local Panel = Components.Panel

local function BoostersMenu(props: Types.BoostersMenuProps)
	return Panel({
		name = "BoostersMenu",
		store = props.store,
		menuId = "Boosters",
		title = "BOOSTERS",
	})
end

return BoostersMenu
