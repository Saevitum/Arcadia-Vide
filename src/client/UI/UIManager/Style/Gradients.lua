--!strict

local Tokens = require(script.Parent.Tokens)

export type ColorPoint = {
	time: number,
	color: Color3,
}

export type TransparencyPoint = {
	time: number,
	transparency: number,
}

local Gradients = {}

local function clamp01(value: number): number
	return math.clamp(value, 0, 1)
end

function Gradients.colorSequence(points: { ColorPoint }): ColorSequence
	local keypoints: { ColorSequenceKeypoint } = {}

	for _, point in ipairs(points) do
		table.insert(keypoints, ColorSequenceKeypoint.new(clamp01(point.time), point.color))
	end

	table.sort(keypoints, function(a, b)
		return a.Time < b.Time
	end)

	return ColorSequence.new(keypoints)
end

function Gradients.transparencySequence(points: { TransparencyPoint }): NumberSequence
	local keypoints: { NumberSequenceKeypoint } = {}

	for _, point in ipairs(points) do
		table.insert(keypoints, NumberSequenceKeypoint.new(clamp01(point.time), clamp01(point.transparency)))
	end

	table.sort(keypoints, function(a, b)
		return a.Time < b.Time
	end)

	return NumberSequence.new(keypoints)
end

function Gradients.fromColors(colors: { Color3 }): ColorSequence
	local count = #colors

	if count <= 0 then
		return ColorSequence.new(Tokens.Colors.White)
	end

	if count == 1 then
		return ColorSequence.new(colors[1])
	end

	local points: { ColorPoint } = {}

	for index, color in ipairs(colors) do
		table.insert(points, {
			time = (index - 1) / (count - 1),
			color = color,
		})
	end

	return Gradients.colorSequence(points)
end

function Gradients.solid(color: Color3): ColorSequence
	return ColorSequence.new(color)
end

function Gradients.cyberPrimary(): ColorSequence
	return Gradients.colorSequence({
		{
			time = 0,
			color = Tokens.Colors.Cyan,
		},
		{
			time = 0.5,
			color = Tokens.Colors.White,
		},
		{
			time = 1,
			color = Tokens.Colors.Magenta,
		},
	})
end

function Gradients.cyberCyanMagenta(): ColorSequence
	return Gradients.colorSequence({
		{
			time = 0,
			color = Tokens.Colors.Cyan,
		},
		{
			time = 1,
			color = Tokens.Colors.Magenta,
		},
	})
end

function Gradients.cyberCyanWhite(): ColorSequence
	return Gradients.colorSequence({
		{
			time = 0,
			color = Tokens.Colors.Cyan,
		},
		{
			time = 1,
			color = Tokens.Colors.White,
		},
	})
end

function Gradients.cyberMagentaWhite(): ColorSequence
	return Gradients.colorSequence({
		{
			time = 0,
			color = Tokens.Colors.Magenta,
		},
		{
			time = 1,
			color = Tokens.Colors.White,
		},
	})
end

function Gradients.darkGlass(): ColorSequence
	return Gradients.colorSequence({
		{
			time = 0,
			color = Tokens.Colors.NearBlack,
		},
		{
			time = 0.5,
			color = Tokens.Colors.DarkGlass,
		},
		{
			time = 1,
			color = Tokens.Colors.Graphite,
		},
	})
end

function Gradients.claimedGray(): ColorSequence
	return Gradients.colorSequence({
		{
			time = 0,
			color = Tokens.Colors.Gray900,
		},
		{
			time = 0.5,
			color = Tokens.Colors.Gray700,
		},
		{
			time = 1,
			color = Tokens.Colors.Gray500,
		},
	})
end

function Gradients.rarity(rarity: string): ColorSequence
	local rarityColor = Tokens.RarityColors[rarity] or Tokens.Colors.Cyan

	return Gradients.colorSequence({
		{
			time = 0,
			color = rarityColor,
		},
		{
			time = 0.5,
			color = Tokens.Colors.White,
		},
		{
			time = 1,
			color = rarityColor,
		},
	})
end

function Gradients.glossTransparency(): NumberSequence
	return Gradients.transparencySequence({
		{
			time = 0,
			transparency = 1,
		},
		{
			time = 0.5,
			transparency = 0.75,
		},
		{
			time = 1,
			transparency = 0,
		},
	})
end

function Gradients.edgeFadeTransparency(): NumberSequence
	return Gradients.transparencySequence({
		{
			time = 0,
			transparency = 1,
		},
		{
			time = 0.5,
			transparency = 0,
		},
		{
			time = 1,
			transparency = 1,
		},
	})
end

function Gradients.topFadeTransparency(): NumberSequence
	return Gradients.transparencySequence({
		{
			time = 0,
			transparency = 0,
		},
		{
			time = 0.65,
			transparency = 0.45,
		},
		{
			time = 1,
			transparency = 1,
		},
	})
end

function Gradients.strokePulseTransparency(): NumberSequence
	return Gradients.transparencySequence({
		{
			time = 0,
			transparency = 0,
		},
		{
			time = 0.6,
			transparency = 0.82,
		},
		{
			time = 1,
			transparency = 1,
		},
	})
end

return Gradients
