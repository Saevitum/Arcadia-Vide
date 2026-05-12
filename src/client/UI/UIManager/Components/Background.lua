--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true
local create = Vide.create

type BackgroundProps = Types.BackgroundProps

local function Background(props: BackgroundProps?)
	local resolvedProps: BackgroundProps = props or {}

	return create("ImageLabel")({
		Name = "Background",

		Size = resolvedProps.size or UDim2.fromScale(1, 1),
		Position = resolvedProps.position or UDim2.fromScale(0, 0),
		AnchorPoint = resolvedProps.anchorPoint or Vector2.new(0, 0),

		BackgroundTransparency = 1,
		Image = "rbxassetid://132010738056728",
		ScaleType = Enum.ScaleType.Fit,
	})
end

return Background
