--!strict

local UserInputService = game:GetService("UserInputService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Vide = require(ReplicatedStorage.Packages.vide)
local Assets = require(script.StatsTreeAssets)
local Data = require(script.StatsTreeData)

Vide.strict = true
local create = Vide.create
local source = Vide.source
local action = Vide.action
local cleanup = Vide.cleanup

type Source<T> = (() -> T) & ((T) -> ())
type NodeDefinition = typeof(Data.nodes[1])

export type StatsTreeMenuProps = { store: any?, visible: (() -> boolean)? }

local CANVAS_SIZE = Vector2.new(2800, 1800)
local CANVAS_CENTER = CANVAS_SIZE / 2
local NODE_SIZE = UDim2.fromOffset(142, 142)
local MIN_ZOOM = 0.55
local MAX_ZOOM = 1.8
local INITIAL_POINTS = 10

local function getLevel(levels: { [string]: number }, nodeId: string): number
	return levels[nodeId] or 0
end

local function findNode(nodeId: string): NodeDefinition?
	for _, node in ipairs(Data.nodes) do
		if node.id == nodeId then return node end
	end
	return nil
end

local function requirementsMet(requirements: { any }?, levels: { [string]: number }): boolean
	if requirements == nil then return true end
	for _, req in ipairs(requirements) do
		if getLevel(levels, req.nodeId) < req.minLevel then return false end
	end
	return true
end

local function isVisible(node: NodeDefinition, opened: { [string]: boolean }, levels: { [string]: number }): boolean
	if node.kind == "Group" then return true end
	if node.visibleWhenGroupOpen ~= nil and opened[node.visibleWhenGroupOpen] ~= true then return false end
	return requirementsMet(node.visibleWhen, levels)
end

local function imageFor(node: NodeDefinition, selected: boolean, levels: { [string]: number }, points: number): string
	if node.kind == "Group" then return Assets.YellowHex end
	if node.kind == "Mystery" then return Assets.GrayQuestionHex end
	if getLevel(levels, node.id) >= (node.maxLevel or 10) then return Assets.YellowHex end
	if selected and points <= 0 then return Assets.RedHex end
	return Assets.BlueHex
end

local function label(text: string | (() -> string), pos: UDim2, size: UDim2, z: number, visible: boolean | (() -> boolean)?)
	return create("TextLabel")({
		Size = size, Position = pos, AnchorPoint = Vector2.new(0.5, 0.5), BackgroundTransparency = 1,
		Text = text, Visible = visible == nil and true or visible, TextScaled = true, TextWrapped = false,
		FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy), TextColor3 = Color3.fromRGB(255, 255, 255), ZIndex = z,
		create("UITextSizeConstraint")({ MinTextSize = 8, MaxTextSize = 18 }),
		create("UIStroke")({ ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual, Color = Color3.fromRGB(0, 0, 0), Transparency = 0.05, Thickness = 3 }),
	})
end

local function nodeView(node: NodeDefinition, levels: Source<{ [string]: number }>, selectedId: Source<string?>, points: Source<number>, onClick: (NodeDefinition) -> (), z: number)
	local hovered = source(false)
	return create("ImageButton")({
		Name = "StatsTreeNode_" .. node.id,
		Size = NODE_SIZE,
		Position = UDim2.fromOffset(CANVAS_CENTER.X + node.position.X, CANVAS_CENTER.Y + node.position.Y),
		AnchorPoint = Vector2.new(0.5, 0.5), BackgroundTransparency = 1, BorderSizePixel = 0,
		Image = function() return imageFor(node, selectedId() == node.id, levels(), points()) end,
		ScaleType = Enum.ScaleType.Fit, AutoButtonColor = false, ZIndex = z,
		Activated = function() onClick(node) end,
		MouseEnter = function() hovered(true) end,
		MouseLeave = function() hovered(false) end,
		create("UIScale")({ Scale = function() if selectedId() == node.id then return 1.09 elseif hovered() then return 1.045 else return 1 end end }),
		label("?", UDim2.fromScale(0.5, 0.47), UDim2.fromScale(0.68, 0.68), z + 3, function() return node.kind == "Mystery" end),
		label(node.title, UDim2.fromScale(0.5, 0.61), UDim2.fromScale(0.86, 0.22), z + 3, function() return node.kind ~= "Mystery" end),
		label(node.subtitle or "", UDim2.fromScale(0.5, 0.77), UDim2.fromScale(0.86, 0.18), z + 3, function() return node.kind ~= "Mystery" and node.subtitle ~= nil end),
		label(function() return tostring(getLevel(levels(), node.id)) .. "/" .. tostring(node.maxLevel or 10) end, UDim2.fromScale(0.78, 0.22), UDim2.fromScale(0.38, 0.2), z + 4, function() return node.kind == "Stat" end),
	})
end

local function connectionView(fromNode: NodeDefinition, toNode: NodeDefinition, opened: Source<{ [string]: boolean }>, levels: Source<{ [string]: number }>, z: number)
	local delta = toNode.position - fromNode.position
	local dist = delta.Magnitude
	local mid = (fromNode.position + toNode.position) / 2
	return create("Frame")({
		Name = "Connection_" .. fromNode.id .. "_" .. toNode.id,
		Size = UDim2.fromOffset(dist, 6), Position = UDim2.fromOffset(CANVAS_CENTER.X + mid.X, CANVAS_CENTER.Y + mid.Y), AnchorPoint = Vector2.new(0.5, 0.5),
		Rotation = math.deg(math.atan2(delta.Y, delta.X)), BorderSizePixel = 0, ZIndex = z,
		Visible = function() return isVisible(fromNode, opened(), levels()) and isVisible(toNode, opened(), levels()) end,
		BackgroundColor3 = function() if fromNode.kind == "Group" or getLevel(levels(), fromNode.id) > 0 then return Color3.fromRGB(0, 229, 255) end return Color3.fromRGB(42, 49, 70) end,
		BackgroundTransparency = function() if fromNode.kind == "Group" or getLevel(levels(), fromNode.id) > 0 then return 0.08 end return 0.28 end,
		create("UICorner")({ CornerRadius = UDim.new(1, 0) }),
		create("UIStroke")({ Color = Color3.fromRGB(0, 0, 0), Transparency = 0.25, Thickness = 2 }),
	})
end

local function detailsView(selectedId: Source<string?>, levels: Source<{ [string]: number }>, points: Source<number>, onUpgrade: (NodeDefinition) -> (), z: number)
	local function selected(): NodeDefinition? local id = selectedId(); if id == nil then return nil end; return findNode(id) end
	local function canUpgrade(node: NodeDefinition): boolean return node.kind == "Stat" and points() > 0 and getLevel(levels(), node.id) < (node.maxLevel or 10) end
	return create("Frame")({
		Name = "StatsTreeDetails", Size = UDim2.fromScale(0.24, 0.34), Position = UDim2.fromScale(0.985, 0.5), AnchorPoint = Vector2.new(1, 0.5),
		BackgroundColor3 = Color3.fromRGB(6, 9, 15), BackgroundTransparency = 0.14, BorderSizePixel = 0, Visible = function() return selected() ~= nil end, ZIndex = z,
		create("UICorner")({ CornerRadius = UDim.new(0.055, 0) }),
		create("UIStroke")({ Color = Color3.fromRGB(0, 229, 255), Transparency = 0.2, Thickness = 2 }),
		label(function() local n = selected(); if n == nil then return "" end; if n.kind == "Mystery" then return "UNKNOWN" end; return n.title .. (n.subtitle and (" " .. n.subtitle) or "") end, UDim2.fromScale(0.5, 0.1), UDim2.fromScale(0.9, 0.16), z + 1, nil),
		label(function() local n = selected(); if n == nil or n.kind ~= "Stat" then return "" end; return "Level: " .. getLevel(levels(), n.id) .. "/" .. (n.maxLevel or 10) end, UDim2.fromScale(0.5, 0.25), UDim2.fromScale(0.9, 0.11), z + 1, nil),
		label(function() local n = selected(); return n and (n.description or "") or "" end, UDim2.fromScale(0.5, 0.43), UDim2.fromScale(0.86, 0.23), z + 1, nil),
		label(function() local n = selected(); return n and n.effectText and ("Effect: " .. n.effectText) or "" end, UDim2.fromScale(0.5, 0.62), UDim2.fromScale(0.86, 0.14), z + 1, nil),
		create("TextButton")({
			Name = "AddPoint", Size = UDim2.fromScale(0.62, 0.16), Position = UDim2.fromScale(0.5, 0.84), AnchorPoint = Vector2.new(0.5, 0.5), BorderSizePixel = 0,
			BackgroundColor3 = function() local n = selected(); if n ~= nil and canUpgrade(n) then return Color3.fromRGB(0, 180, 65) end; return Color3.fromRGB(60, 60, 70) end,
			Text = "ADD POINT", TextScaled = true, FontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold), TextColor3 = Color3.fromRGB(255, 255, 255), AutoButtonColor = false,
			Visible = function() local n = selected(); return n ~= nil and n.kind == "Stat" end, ZIndex = z + 2,
			Activated = function() local n = selected(); if n ~= nil and canUpgrade(n) then onUpgrade(n) end end,
			create("UICorner")({ CornerRadius = UDim.new(0.5, 0) }), create("UIStroke")({ Color = Color3.fromRGB(180, 255, 255), Transparency = 0.08, Thickness = 2 }),
		}),
	})
end

local function StatsTreeMenu(props: StatsTreeMenuProps?)
	props = props or {}
	local opened: Source<{ [string]: boolean }> = source({})
	local levels: Source<{ [string]: number }> = source({})
	local selectedId: Source<string?> = source(nil :: string?)
	local points: Source<number> = source(INITIAL_POINTS)
	local pan: Source<Vector2> = source(Vector2.new(0, 0))
	local zoom: Source<number> = source(1)

	local function menuVisible(): boolean
		if props.visible ~= nil then return props.visible() end
		if props.store ~= nil and props.store.currentMenu ~= nil then return props.store.currentMenu() == "StatsTree" end
		return true
	end

	local function clickNode(node: NodeDefinition)
		selectedId(node.id)
		if node.kind == "Group" and node.groupId ~= nil then local next = table.clone(opened()); next[node.groupId] = next[node.groupId] ~= true; opened(next) end
	end

	local function upgrade(node: NodeDefinition)
		if node.kind ~= "Stat" or points() <= 0 then return end
		local next = table.clone(levels())
		local maxLevel = node.maxLevel or 10
		if getLevel(next, node.id) >= maxLevel then return end
		next[node.id] = getLevel(next, node.id) + 1
		levels(next)
		points(math.max(0, points() - 1))
	end

	local canvasChildren: { any } = {}
	for _, c in ipairs(Data.connections) do
		local a = findNode(c.from); local b = findNode(c.to)
		if a ~= nil and b ~= nil then table.insert(canvasChildren, connectionView(a, b, opened, levels, 101)) end
	end
	for _, n in ipairs(Data.nodes) do
		table.insert(canvasChildren, nodeView(n, levels, selectedId, points, clickNode, 110))
	end

	return create("Frame")({
		Name = "StatsTreeMenu", Size = UDim2.fromScale(1, 1), Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5), Visible = menuVisible,
		BackgroundColor3 = Color3.fromRGB(0, 0, 0), BackgroundTransparency = 0.34, BorderSizePixel = 0, ClipsDescendants = true, ZIndex = 100,
		action(function(inst: Instance)
			if not inst:IsA("GuiObject") then return end
			local gui = inst :: GuiObject
			local dragging = false
			local last: Vector2? = nil
			local began = gui.InputBegan:Connect(function(input) if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then dragging = true; last = Vector2.new(input.Position.X, input.Position.Y) end end)
			local changed = gui.InputChanged:Connect(function(input) if input.UserInputType == Enum.UserInputType.MouseWheel then local z = zoom(); if input.Position.Z > 0 then z *= 1.1 else z /= 1.1 end; zoom(math.clamp(z, MIN_ZOOM, MAX_ZOOM)) end end)
			local globalChanged = UserInputService.InputChanged:Connect(function(input)
				if not dragging or (input.UserInputType ~= Enum.UserInputType.MouseMovement and input.UserInputType ~= Enum.UserInputType.Touch) then return end
				local now = Vector2.new(input.Position.X, input.Position.Y); if last == nil then last = now; return end
				pan(pan() + (now - last)); last = now
			end)
			local ended = UserInputService.InputEnded:Connect(function(input) if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then dragging = false; last = nil end end)
			cleanup(function() began:Disconnect(); changed:Disconnect(); globalChanged:Disconnect(); ended:Disconnect() end)
		end),
		create("Frame")({
			Name = "Canvas", Size = UDim2.fromOffset(CANVAS_SIZE.X, CANVAS_SIZE.Y), Position = function() local p = pan(); return UDim2.new(0.5, p.X, 0.5, p.Y) end, AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1, BorderSizePixel = 0, ZIndex = 100, create("UIScale")({ Scale = zoom }), table.unpack(canvasChildren),
		}),
		create("Frame")({
			Name = "TopBar", Size = UDim2.fromScale(0.42, 0.095), Position = UDim2.fromScale(0.5, 0.045), AnchorPoint = Vector2.new(0.5, 0), BackgroundColor3 = Color3.fromRGB(0, 0, 0), BackgroundTransparency = 0.42, BorderSizePixel = 0, ZIndex = 210,
			create("UICorner")({ CornerRadius = UDim.new(0.2, 0) }), create("UIStroke")({ Color = Color3.fromRGB(0, 229, 255), Transparency = 0.25, Thickness = 2 }),
			label("STATS TREE", UDim2.fromScale(0.5, 0.28), UDim2.fromScale(1, 0.5), 211, nil),
			label(function() return "Available Points: " .. points() end, UDim2.fromScale(0.5, 0.74), UDim2.fromScale(1, 0.35), 211, nil),
		}),
		detailsView(selectedId, levels, points, upgrade, 220),
		label("DRAG TO MOVE  |  MOUSE WHEEL TO ZOOM", UDim2.fromScale(0.5, 0.935), UDim2.fromScale(0.34, 0.045), 230, nil),
		create("TextButton")({
			Name = "CloseButton", Size = UDim2.fromScale(0.16, 0.075), Position = UDim2.fromScale(0.5, 0.975), AnchorPoint = Vector2.new(0.5, 1), BackgroundColor3 = Color3.fromRGB(255, 30, 30), BorderSizePixel = 0,
			Text = "CLOSE", TextScaled = true, FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy), TextColor3 = Color3.fromRGB(255, 255, 255), AutoButtonColor = true, ZIndex = 230,
			Activated = function() if props.store ~= nil and props.store.currentMenu ~= nil then props.store.currentMenu(nil) end end,
			create("UICorner")({ CornerRadius = UDim.new(0.14, 0) }), create("UIStroke")({ Color = Color3.fromRGB(0, 0, 0), Transparency = 0, Thickness = 4 }),
		}),
	})
end

return StatsTreeMenu
