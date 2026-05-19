--!strict

local ContextActionService = game:GetService("ContextActionService")
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

type Requirement = {
	nodeId: string,
	minLevel: number,
}

type NodeKind = "Group" | "Stat"

type NodeDefinition = {
	id: string,
	kind: NodeKind,
	groupId: string,

	title: string,
	subtitle: string?,
	effectShort: string?,
	description: string?,

	maxLevel: number?,
	position: Vector2,
	requires: { Requirement }?,
}

export type StatsTreeMenuProps = {
	store: any?,
	visible: (() -> boolean)?,
}

local NODES: { NodeDefinition } = Data.nodes :: { NodeDefinition }

local CANVAS_SIZE = Vector2.new(2400, 1600)
local CANVAS_CENTER = CANVAS_SIZE / 2
local NODE_SIZE = UDim2.fromOffset(148, 148)
local MIN_ZOOM = 0.55
local MAX_ZOOM = 1.8
local INITIAL_POINTS = 10
local WHEEL_ACTION_NAME = "ArcadiaStatsTreeSinkMouseWheel"

local function getLevel(levels: { [string]: number }, nodeId: string): number
	return levels[nodeId] or 0
end

local function requirementsMet(requirements: { Requirement }?, levels: { [string]: number }): boolean
	if requirements == nil then
		return true
	end

	for _, requirement in ipairs(requirements) do
		if getLevel(levels, requirement.nodeId) < requirement.minLevel then
			return false
		end
	end

	return true
end

local function isKnown(node: NodeDefinition, levels: { [string]: number }): boolean
	return requirementsMet(node.requires, levels)
end

local function isNodeVisible(node: NodeDefinition, activeGroup: string?): boolean
	if node.kind == "Group" then
		return activeGroup == nil or activeGroup == node.groupId
	end

	return activeGroup == node.groupId
end

local function getNodeImage(
	node: NodeDefinition,
	activeGroup: string?,
	levels: { [string]: number }
): string
	if node.kind == "Group" then
		if activeGroup == node.groupId then
			return Assets.RedHex
		end

		return Assets.YellowHex
	end

	if not isKnown(node, levels) then
		return Assets.GrayQuestionHex
	end

	local level = getLevel(levels, node.id)
	local maxLevel = node.maxLevel or 10

	if level >= maxLevel then
		return Assets.YellowHex
	end

	if level > 0 then
		return Assets.BlueHex
	end

	return Assets.GrayHex
end

local function makeText(
	name: string,
	text: string | (() -> string),
	position: UDim2,
	size: UDim2,
	zIndex: number,
	visible: boolean | (() -> boolean)?,
	maxTextSize: number,
	color: Color3?
)
	return create("TextLabel")({
		Name = name,
		Size = size,
		Position = position,
		AnchorPoint = Vector2.new(0.5, 0.5),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		Text = text,
		Visible = if visible == nil then true else visible,
		TextScaled = true,
		TextWrapped = false,
		TextXAlignment = Enum.TextXAlignment.Center,
		TextYAlignment = Enum.TextYAlignment.Center,
		FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy),
		TextColor3 = color or Color3.fromRGB(255, 255, 255),
		ZIndex = zIndex,

		create("UITextSizeConstraint")({
			MinTextSize = 7,
			MaxTextSize = maxTextSize,
		}),

		create("UIStroke")({
			ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual,
			Color = Color3.fromRGB(0, 0, 0),
			Transparency = 0.04,
			Thickness = 3,
		}),
	})
end

local function nodeView(
	node: NodeDefinition,
	activeGroup: Source<string?>,
	levels: Source<{ [string]: number }>,
	points: Source<number>,
	onClick: (NodeDefinition) -> (),
	zIndex: number
)
	local hovered: Source<boolean> = source(false)

	local function known(): boolean
		return node.kind == "Group" or isKnown(node, levels())
	end

	return create("ImageButton")({
		Name = "StatsTreeNode_" .. node.id,
		Size = NODE_SIZE,
		Position = UDim2.fromOffset(
			CANVAS_CENTER.X + node.position.X,
			CANVAS_CENTER.Y + node.position.Y
		),
		AnchorPoint = Vector2.new(0.5, 0.5),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		Image = function()
			return getNodeImage(node, activeGroup(), levels())
		end,
		ScaleType = Enum.ScaleType.Fit,
		AutoButtonColor = false,
		Visible = function()
			return isNodeVisible(node, activeGroup())
		end,
		ZIndex = zIndex,

		Activated = function()
			onClick(node)
		end,

		MouseEnter = function()
			hovered(true)
		end,

		MouseLeave = function()
			hovered(false)
		end,

		create("UIScale")({
			Scale = function()
				if hovered() then
					return 1.045
				end

				return 1
			end,
		}),

		makeText(
			"QuestionMark",
			"?",
			UDim2.fromScale(0.5, 0.48),
			UDim2.fromScale(0.62, 0.62),
			zIndex + 4,
			function()
				return node.kind == "Stat" and not known()
			end,
			62,
			Color3.fromRGB(238, 241, 250)
		),

		makeText(
			"Effect",
			function()
				return node.effectShort or ""
			end,
			UDim2.fromScale(0.5, 0.31),
			UDim2.fromScale(0.74, 0.2),
			zIndex + 4,
			function()
				return node.kind == "Stat" and known() and node.effectShort ~= nil
			end,
			20,
			Color3.fromRGB(255, 255, 255)
		),

		makeText(
			"Title",
			node.title,
			UDim2.fromScale(0.5, 0.57),
			UDim2.fromScale(0.86, 0.22),
			zIndex + 4,
			function()
				return known()
			end,
			18,
			Color3.fromRGB(255, 255, 255)
		),

		makeText(
			"Subtitle",
			node.subtitle or "",
			UDim2.fromScale(0.5, 0.73),
			UDim2.fromScale(0.86, 0.18),
			zIndex + 4,
			function()
				return known() and node.subtitle ~= nil
			end,
			15,
			Color3.fromRGB(255, 255, 255)
		),

		makeText(
			"Level",
			function()
				return tostring(getLevel(levels(), node.id)) .. "/" .. tostring(node.maxLevel or 10)
			end,
			UDim2.fromScale(0.78, 0.18),
			UDim2.fromScale(0.42, 0.2),
			zIndex + 5,
			function()
				return node.kind == "Stat" and known()
			end,
			18,
			Color3.fromRGB(255, 255, 255)
		),

		makeText(
			"NoPoints",
			"NO POINTS",
			UDim2.fromScale(0.5, 0.87),
			UDim2.fromScale(0.76, 0.16),
			zIndex + 5,
			function()
				return node.kind == "Stat"
					and known()
					and points() <= 0
					and getLevel(levels(), node.id) < (node.maxLevel or 10)
			end,
			13,
			Color3.fromRGB(255, 70, 70)
		),
	})
end

local function StatsTreeMenu(rawProps: StatsTreeMenuProps?)
	local props: StatsTreeMenuProps = rawProps or {}

	local activeGroup: Source<string?> = source(nil :: string?)
	local levels: Source<{ [string]: number }> = source({})
	local points: Source<number> = source(INITIAL_POINTS)
	local pan: Source<Vector2> = source(Vector2.new(0, 0))
	local zoom: Source<number> = source(1)

	local function menuVisible(): boolean
		local visible = props.visible

		if visible ~= nil then
			return visible()
		end

		local store = props.store

		if store ~= nil then
			local currentMenu = store.currentMenu

			if currentMenu ~= nil then
				return currentMenu() == "StatsTree"
			end
		end

		return true
	end

	local function spendPoint(node: NodeDefinition)
		if node.kind ~= "Stat" then
			return
		end

		if not isKnown(node, levels()) then
			return
		end

		if points() <= 0 then
			return
		end

		local maxLevel = node.maxLevel or 10
		local currentLevel = getLevel(levels(), node.id)

		if currentLevel >= maxLevel then
			return
		end

		local nextLevels: { [string]: number } = table.clone(levels()) :: { [string]: number }
		nextLevels[node.id] = currentLevel + 1

		levels(nextLevels)
		points(math.max(0, points() - 1))
	end

	local function clickNode(node: NodeDefinition)
		if node.kind == "Group" then
			if activeGroup() == node.groupId then
				activeGroup(nil)
			else
				activeGroup(node.groupId)
			end

			return
		end

		spendPoint(node)
	end

	local canvasChildren: { any } = {}

	for _, node in ipairs(NODES) do
		table.insert(canvasChildren, nodeView(node, activeGroup, levels, points, clickNode, 110))
	end

	return create("Frame")({
		Name = "StatsTreeMenu",
		Size = UDim2.fromScale(1, 1),
		Position = UDim2.fromScale(0.5, 0.5),
		AnchorPoint = Vector2.new(0.5, 0.5),
		Visible = menuVisible,
		BackgroundColor3 = Color3.fromRGB(0, 0, 0),
		BackgroundTransparency = 0.34,
		BorderSizePixel = 0,
		ClipsDescendants = true,
		Active = true,
		ZIndex = 100,

		action(function(instance: Instance)
			if not instance:IsA("GuiObject") then
				return
			end

			local gui = instance :: GuiObject
			local dragging = false
			local lastPosition: Vector2? = nil

			ContextActionService:BindActionAtPriority(
				WHEEL_ACTION_NAME,
				function(_actionName: string, inputState: Enum.UserInputState, inputObject: InputObject)
					if not menuVisible() then
						return Enum.ContextActionResult.Pass
					end

					if inputState == Enum.UserInputState.Change then
						local nextZoom = zoom()

						if inputObject.Position.Z > 0 then
							nextZoom *= 1.1
						else
							nextZoom /= 1.1
						end

						zoom(math.clamp(nextZoom, MIN_ZOOM, MAX_ZOOM))
					end

					return Enum.ContextActionResult.Sink
				end,
				false,
				3000,
				Enum.UserInputType.MouseWheel
			)

			local inputBegan = gui.InputBegan:Connect(function(input: InputObject)
				if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
					dragging = true
					lastPosition = Vector2.new(input.Position.X, input.Position.Y)
				end
			end)

			local inputChanged = UserInputService.InputChanged:Connect(function(input: InputObject)
				if not dragging then
					return
				end

				if input.UserInputType ~= Enum.UserInputType.MouseMovement and input.UserInputType ~= Enum.UserInputType.Touch then
					return
				end

				local currentPosition = Vector2.new(input.Position.X, input.Position.Y)

				if lastPosition == nil then
					lastPosition = currentPosition
					return
				end

				local delta = currentPosition - lastPosition
				lastPosition = currentPosition

				pan(pan() + delta)
			end)

			local inputEnded = UserInputService.InputEnded:Connect(function(input: InputObject)
				if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
					dragging = false
					lastPosition = nil
				end
			end)

			cleanup(function()
				ContextActionService:UnbindAction(WHEEL_ACTION_NAME)
				inputBegan:Disconnect()
				inputChanged:Disconnect()
				inputEnded:Disconnect()
			end)
		end),

		create("Frame")({
			Name = "Canvas",
			Size = UDim2.fromOffset(CANVAS_SIZE.X, CANVAS_SIZE.Y),
			Position = function()
				local value = pan()

				return UDim2.new(0.5, value.X, 0.5, value.Y)
			end,
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 101,

			create("UIScale")({
				Scale = zoom,
			}),

			table.unpack(canvasChildren),
		}),

		create("Frame")({
			Name = "TopBar",
			Size = UDim2.fromScale(0.36, 0.08),
			Position = UDim2.fromScale(0.5, 0.035),
			AnchorPoint = Vector2.new(0.5, 0),
			BackgroundColor3 = Color3.fromRGB(0, 0, 0),
			BackgroundTransparency = 0.42,
			BorderSizePixel = 0,
			ZIndex = 220,

			create("UICorner")({
				CornerRadius = UDim.new(0.2, 0),
			}),

			create("UIStroke")({
				Color = Color3.fromRGB(0, 229, 255),
				Transparency = 0.25,
				Thickness = 2,
			}),

			makeText(
				"Title",
				"STATS TREE",
				UDim2.fromScale(0.5, 0.3),
				UDim2.fromScale(0.95, 0.46),
				221,
				true,
				34,
				Color3.fromRGB(255, 255, 255)
			),

			makeText(
				"Points",
				function()
					return "Available Points: " .. tostring(points())
				end,
				UDim2.fromScale(0.5, 0.73),
				UDim2.fromScale(0.95, 0.34),
				221,
				true,
				22,
				Color3.fromRGB(0, 229, 255)
			),
		}),

		makeText(
			"Hint",
			"DRAG TO MOVE  |  MOUSE WHEEL TO ZOOM",
			UDim2.fromScale(0.5, 0.925),
			UDim2.fromScale(0.36, 0.045),
			230,
			true,
			18,
			Color3.fromRGB(255, 255, 255)
		),

		create("TextButton")({
			Name = "CloseButton",
			Size = UDim2.fromScale(0.16, 0.075),
			Position = UDim2.fromScale(0.5, 0.975),
			AnchorPoint = Vector2.new(0.5, 1),
			BackgroundColor3 = Color3.fromRGB(255, 30, 30),
			BorderSizePixel = 0,
			Text = "CLOSE",
			TextScaled = true,
			FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy),
			TextColor3 = Color3.fromRGB(255, 255, 255),
			AutoButtonColor = true,
			ZIndex = 230,

			Activated = function()
				local store = props.store

				if store == nil then
					return
				end

				local currentMenu = store.currentMenu

				if currentMenu ~= nil then
					currentMenu(nil)
				end
			end,

			create("UICorner")({
				CornerRadius = UDim.new(0.14, 0),
			}),

			create("UIStroke")({
				Color = Color3.fromRGB(0, 0, 0),
				Transparency = 0,
				Thickness = 4,
			}),
		}),
	})
end

return StatsTreeMenu
