--!strict

local StoreTypes = require(script.Parent.Parent.StoreTypes)

export type ActivityMenuProps = {
	store: StoreTypes.UIStore,
}

export type ActivityRow = {
	label: string,
	value: string,
}

return {}
