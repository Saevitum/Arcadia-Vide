--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Components)

Vide.strict = true

local Panel = Components.Panel

local function QuestsMenu(props: Types.QuestsMenuProps)
	return Panel({
		name = "QuestsMenu",
		store = props.store,
		menuId = "Quests",
		title = "QUESTS",
	})
end

return QuestsMenu
