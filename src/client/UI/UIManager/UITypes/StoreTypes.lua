--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type SourceOf<T> = SharedTypes.SourceOf<T>
export type MenuId = MenuIdTypes.MenuId

export type UIStore = {
	currentMenu: SourceOf<MenuId?>,
}

return {}
