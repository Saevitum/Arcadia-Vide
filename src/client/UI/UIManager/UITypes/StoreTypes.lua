--!strict

local SharedTypes = require(script.Parent.SharedTypes)
local MenuIdTypes = require(script.Parent.MenuTypes.MenuIdTypes)

export type Source<T> = SharedTypes.Source<T>
export type MenuId = MenuIdTypes.MenuId

export type UIStore = {
	currentMenu: Source<MenuId?>,
}

return {}
