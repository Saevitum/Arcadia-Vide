--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)
local Components = require(script.Parent.Parent.Components)

Vide.strict = true

local Panel = Components.Panel

local function ShopMenu(props: Types.ShopMenuProps)
	return Panel({
		name = "ShopMenu",
		store = props.store,
		menuId = "Shop",
		title = "SHOP",
	})
end

return ShopMenu
