--!strict

local Types = require(script.Parent.Parent.UITypes.MenuTypes)
local StatsTree = require(script.Parent.StatsTree)

local function StatsMenu(props: Types.StatsMenuProps)
	local store = props.store

	return StatsTree({
		store = store,
		visible = function()
			if store == nil then
				return true
			end

			local currentMenu = store.currentMenu

			if currentMenu == nil then
				return true
			end

			return currentMenu() == "Stats"
		end,
	})
end

return StatsMenu
