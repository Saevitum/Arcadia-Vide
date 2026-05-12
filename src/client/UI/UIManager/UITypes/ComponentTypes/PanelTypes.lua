--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.Parent.MenuTypes.MenuIdTypes)

export type PanelProps = {
	store: StoreTypes.UIStore,
	menuId: MenuIdTypes.MenuId,
	name: string?,
	title: string | (() -> string)?,
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	zIndex: number?,
	aspectRatio: number?,
	exitButtonSize: UDim2?,
	exitButtonPosition: UDim2?,
	exitButtonAnchorPoint: Vector2?,
	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	slideDuration: number?,
	content: Instance?,
}

return {}
