--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)
local StoreTypes = require(script.Parent.Parent.StoreTypes)
local MenuIdTypes = require(script.Parent.Parent.MenuTypes.MenuIdTypes)

export type Reactive<T> = SharedTypes.Reactive<T>
export type UIStore = StoreTypes.UIStore
export type MenuId = MenuIdTypes.MenuId

export type BackgroundProps = {
	size: UDim2?,
	position: UDim2?,
	anchorPoint: Vector2?,
}

export type ExitButtonProps = {
	onClick: (() -> ())?,
	position: UDim2?,
	size: UDim2?,
	anchorPoint: Vector2?,
}

export type HeaderProps = {
	text: string | (() -> string)?,
}

export type PanelProps = {
	store: UIStore,
	menuId: MenuId,
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
