--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Controls = require(script.Parent.Controls)

Vide.strict = true

local create = Vide.create

local Decorators = {}

local SETTINGS_COLORS = Controls.Settings.Colors

function Decorators.NeonStroke(thickness: number?, transparency: number?)
	return create("UIStroke")({
		Thickness = thickness or 2,
		Transparency = transparency or 0.08,
		Color = SETTINGS_COLORS.White,
		ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

		create("UIGradient")({
			Rotation = 0,

			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, SETTINGS_COLORS.Cyan),
				ColorSequenceKeypoint.new(0.55, Color3.fromRGB(95, 82, 255)),
				ColorSequenceKeypoint.new(1, SETTINGS_COLORS.Magenta),
			}),
		}),
	})
end

function Decorators.RowGradient()
	return create("UIGradient")({
		Rotation = 0,

		Color = ColorSequence.new({
			ColorSequenceKeypoint.new(0, Color3.fromRGB(18, 27, 38)),
			ColorSequenceKeypoint.new(0.52, Color3.fromRGB(24, 31, 43)),
			ColorSequenceKeypoint.new(1, Color3.fromRGB(15, 18, 27)),
		}),

		Transparency = NumberSequence.new({
			NumberSequenceKeypoint.new(0, 0.03),
			NumberSequenceKeypoint.new(0.72, 0.1),
			NumberSequenceKeypoint.new(1, 0.18),
		}),
	})
end

return Decorators
