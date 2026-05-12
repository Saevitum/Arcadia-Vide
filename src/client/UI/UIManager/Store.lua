--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.UITypes.StoreTypes)

Vide.strict = true

local Store: Types.UIStore = {
	currentMenu = Vide.source(nil),
}

return Store
