--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Components)

Vide.strict = true

local Panel = Components.Panel

local function InventoryMenu(props: Types.InventoryMenuProps)
	return Panel({
		name = "InventoryMenu",
		store = props.store,
		menuId = "Inventory",
		title = "INVENTORY",
	})
end

return InventoryMenu
