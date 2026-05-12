--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes)

Vide.strict = true

local create = Vide.create

type ImageProps = Types.ImageProps
type ImageStrokeProps = Types.ImageStrokeProps
type ImageGradientProps = Types.ImageGradientProps
type Reactive<T> = Types.Reactive<T>

local function read<T>(value: Reactive<T>?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function createCorner(cornerRadius: Reactive<UDim>?)
	if cornerRadius == nil then
		return nil
	end

	return create("UICorner")({
		CornerRadius = function()
			return read(cornerRadius, UDim.new(0, 0))
		end,
	})
end

local function createStroke(stroke: ImageStrokeProps?)
	if stroke == nil then
		return nil
	end

	return create("UIStroke")({
		Thickness = function()
			return read(stroke.thickness, 1)
		end,

		Color = function()
			return read(stroke.color, Color3.fromRGB(255, 255, 255))
		end,

		Transparency = function()
			return read(stroke.transparency, 0)
		end,

		ApplyStrokeMode = stroke.applyStrokeMode or Enum.ApplyStrokeMode.Border,
	})
end

local function createGradient(gradient: ImageGradientProps?)
	if gradient == nil then
		return nil
	end

	return create("UIGradient")({
		Color = gradient.color or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		Transparency = gradient.transparency or NumberSequence.new(0),
		Rotation = gradient.rotation or 0,
		Offset = gradient.offset or Vector2.new(0, 0),
	})
end

local function Image(props: ImageProps?)
	local resolvedProps: ImageProps = props or {}

	return create("ImageLabel")({
		Name = resolvedProps.name or "Image",

		Image = function()
			return read(resolvedProps.image, "")
		end,

		AnchorPoint = function()
			return read(resolvedProps.anchorPoint, Vector2.new(0, 0))
		end,

		Position = function()
			return read(resolvedProps.position, UDim2.fromScale(0, 0))
		end,

		Size = function()
			return read(resolvedProps.size, UDim2.fromScale(1, 1))
		end,

		Rotation = function()
			return read(resolvedProps.rotation, 0)
		end,

		Visible = function()
			return read(resolvedProps.visible, true)
		end,

		ZIndex = function()
			return read(resolvedProps.zIndex, 1)
		end,

		LayoutOrder = function()
			return read(resolvedProps.layoutOrder, 0)
		end,

		BackgroundTransparency = function()
			return read(resolvedProps.backgroundTransparency, 1)
		end,

		BackgroundColor3 = function()
			return read(resolvedProps.backgroundColor3, Color3.fromRGB(255, 255, 255))
		end,

		BorderSizePixel = 0,

		ImageColor3 = function()
			return read(resolvedProps.imageColor3, Color3.fromRGB(255, 255, 255))
		end,

		ImageTransparency = function()
			return read(resolvedProps.imageTransparency, 0)
		end,

		ScaleType = resolvedProps.scaleType or Enum.ScaleType.Fit,
		SliceCenter = resolvedProps.sliceCenter or Rect.new(0, 0, 0, 0),
		SliceScale = resolvedProps.sliceScale or 1,

		createCorner(resolvedProps.cornerRadius),
		createStroke(resolvedProps.stroke),
		createGradient(resolvedProps.gradient),
	})
end

return Image
