--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.Parent.MenuTypes.MenuIdTypes)

export type UIStore = StoreTypes.UIStore
export type MenuId = MenuIdTypes.MenuId

export type PanelProps = {
	name: string?,
	store: UIStore,
	menuId: MenuId,
	title: string?,

	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
	zIndex: number?,
	aspectRatio: number?,

	content: Instance?,

	openPosition: UDim2?,
	enterPosition: UDim2?,
	exitPosition: UDim2?,
	slideDuration: number?,

	exitButtonSize: UDim2?,
	exitButtonPosition: UDim2?,
	exitButtonAnchorPoint: Vector2?,
}

return {}
