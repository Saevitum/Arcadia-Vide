--!strict

local StoryRoot = require(script.Parent.StoryRoot)
local StoryApp = require(script.Parent.StoryApp)

local function AppStory(target: Instance): () -> ()
	return StoryRoot.mount(target, {
		initialMenu = nil,

		backgroundTransparency = 1,

		render = function(store)
			return StoryApp({
				store = store,
			})
		end,
	})
end

return AppStory
