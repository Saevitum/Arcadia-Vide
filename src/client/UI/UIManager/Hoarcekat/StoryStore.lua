--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.StoreTypes)

Vide.strict = true

local source = Vide.source

type UIStore = Types.UIStore

local StoryStore = {}

function StoryStore.create(initialMenu: string?): UIStore
	local store = {
		currentMenu = source(initialMenu),
	}

	return (store :: any) :: UIStore
end

return StoryStore
