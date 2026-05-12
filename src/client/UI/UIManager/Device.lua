--!strict

local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")

local Types = require(script.Parent.UITypes.DeviceTypes)

local Device = {}

local function getViewport(): Vector2
	local camera = Workspace.CurrentCamera
	if camera == nil then
		return Vector2.new(1920, 1080)
	end

	return camera.ViewportSize
end

function Device.GetKind(): Types.DeviceKind
	local viewport = getViewport()

	local width = viewport.X
	local height = viewport.Y

	local shortestSide = math.min(width, height)
	local longestSide = math.max(width, height)
	local diagonal = math.sqrt((width * width) + (height * height))
	local aspectRatio = longestSide / shortestSide

	local hasTouch = UserInputService.TouchEnabled
	local hasKeyboard = UserInputService.KeyboardEnabled
	local hasMouse = UserInputService.MouseEnabled
	local hasGamepad = UserInputService.GamepadEnabled

	-- Console / controller-focused
	if hasGamepad and not hasKeyboard and not hasMouse then
		return "Console"
	end

	-- Desktop / laptop
	if hasKeyboard and hasMouse and not hasTouch then
		return "Desktop"
	end

	-- Hybrid devices, for example touchscreen laptop
	if hasKeyboard and hasMouse and hasTouch then
		return "Desktop"
	end

	-- Touch devices
	if hasTouch then
		-- Very small touch screen = phone
		if shortestSide <= 650 then
			return "Mobile"
		end

		-- Very tall/narrow touch screen = phone-like
		if aspectRatio >= 1.9 and shortestSide <= 760 then
			return "Mobile"
		end

		-- Larger touch screen = tablet
		if shortestSide >= 700 or diagonal >= 1300 then
			return "Tablet"
		end

		return "Mobile"
	end

	return "Desktop"
end

function Device.DebugPrint()
	local viewport = getViewport()

	print("[Device] Kind:", Device.GetKind())
	print("[Device] Viewport:", viewport)
	print("[Device] Touch:", UserInputService.TouchEnabled)
	print("[Device] Keyboard:", UserInputService.KeyboardEnabled)
	print("[Device] Mouse:", UserInputService.MouseEnabled)
	print("[Device] Gamepad:", UserInputService.GamepadEnabled)
end

return Device
