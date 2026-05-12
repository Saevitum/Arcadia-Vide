--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local StoryStore = require(script.Parent.StoryStore)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local root = Vide.root

type UIStore = Types.UIStore

export type MountOptions = {
	initialMenu: string?,
	render: (store: UIStore) -> Instance,

	backgroundColor3: Color3?,
	backgroundTransparency: number?,
}

local StoryRoot = {}

function StoryRoot.mount(target: Instance, options: MountOptions): () -> ()
	assert(target:IsA("GuiObject"), "Hoarcekat story target must be a GuiObject.")

	target:ClearAllChildren()

	local host = Instance.new("Frame")
	host.Name = "VideStoryHost"
	host.Size = UDim2.fromScale(1, 1)
	host.Position = UDim2.fromScale(0, 0)
	host.AnchorPoint = Vector2.new(0, 0)
	host.BackgroundColor3 = options.backgroundColor3 or Color3.fromRGB(8, 10, 16)
	host.BackgroundTransparency = if options.backgroundTransparency ~= nil then options.backgroundTransparency else 1
	host.BorderSizePixel = 0
	host.ClipsDescendants = false
	host.Parent = target

	local destroyVide = root(function()
		local store = StoryStore.create(options.initialMenu)
		local mounted = options.render(store)

		mounted.Parent = host
	end)

	return function()
		destroyVide()

		if host.Parent ~= nil then
			host:Destroy()
		end
	end
end

return StoryRoot
