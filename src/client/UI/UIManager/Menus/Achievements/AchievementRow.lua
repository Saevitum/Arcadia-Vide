--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local MockAchievements = require(script.Parent.MockAchievements)
local Style = require(script.Parent.Style)

Vide.strict = true

local create = Vide.create

local Text = Components.Text

type MockAchievement = MockAchievements.MockAchievement

export type AchievementRowProps = {
	achievement: MockAchievement,
	layoutOrder: number?,
	zIndex: number?,
	onCollect: ((achievement: MockAchievement) -> ())?,
}

local function getStateText(state: MockAchievements.AchievementState): string
	if state == "Available" then
		return "Collect"
	end

	if state == "Claimed" then
		return "Claimed"
	end

	return "Not Ready"
end

local function getStatusColor(state: MockAchievements.AchievementState): Color3
	if state == "Available" then
		return Color3.fromRGB(82, 230, 35)
	end

	if state == "Claimed" then
		return Color3.fromRGB(70, 86, 94)
	end

	return Color3.fromRGB(35, 42, 54)
end

local function Segment(props: {
	name: string,
	size: UDim2,
	position: UDim2,
	anchorPoint: Vector2,
	zIndex: number,
})
	return create("Frame")({
		Name = props.name,

		Size = props.size,
		Position = props.position,
		AnchorPoint = props.anchorPoint,

		BackgroundColor3 = Color3.fromRGB(25, 34, 45),
		BackgroundTransparency = 0.12,
		BorderSizePixel = 0,
		ZIndex = props.zIndex,

		create("UICorner")({
			CornerRadius = UDim.new(0.16, 0),
		}),

		create("UIGradient")({
			Rotation = 0,
			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, Color3.fromRGB(30, 42, 55)),
				ColorSequenceKeypoint.new(1, Color3.fromRGB(11, 15, 23)),
			}),
			Transparency = NumberSequence.new({
				NumberSequenceKeypoint.new(0, 0.12),
				NumberSequenceKeypoint.new(1, 0.3),
			}),
		}),
	})
end

local function AchievementRow(props: AchievementRowProps)
	local achievement = props.achievement
	local zIndex = props.zIndex or 24
	local isAvailable = achievement.State == "Available"

	return create("Frame")({
		Name = `AchievementRow_{achievement.Id}`,

		Size = Style.ROW_SIZE,
		BackgroundColor3 = Color3.fromRGB(15, 21, 30),
		BackgroundTransparency = 0.12,
		BorderSizePixel = 0,

		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		create("UICorner")({
			CornerRadius = UDim.new(0.2, 0),
		}),

		create("UIGradient")({
			Rotation = 0,
			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, Color3.fromRGB(24, 33, 43)),
				ColorSequenceKeypoint.new(0.55, Color3.fromRGB(12, 17, 25)),
				ColorSequenceKeypoint.new(1, Color3.fromRGB(24, 33, 43)),
			}),
			Transparency = NumberSequence.new({
				NumberSequenceKeypoint.new(0, 0.18),
				NumberSequenceKeypoint.new(0.5, 0.03),
				NumberSequenceKeypoint.new(1, 0.18),
			}),
		}),

		Segment({
			name = "NameSegment",
			size = UDim2.fromScale(0.2, 0.64),
			position = UDim2.fromScale(0.12, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),
			zIndex = zIndex + 1,
		}),

		Segment({
			name = "TaskSegment",
			size = UDim2.fromScale(0.28, 0.64),
			position = UDim2.fromScale(0.39, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),
			zIndex = zIndex + 1,
		}),

		Segment({
			name = "ProgressSegment",
			size = UDim2.fromScale(0.25, 0.64),
			position = UDim2.fromScale(0.66, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),
			zIndex = zIndex + 1,
		}),

		Text({
			name = "Title",
			text = achievement.Title,

			size = UDim2.fromScale(0.19, 0.7),
			position = UDim2.fromScale(0.12, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Style.FONT_BOLD_ITALIC,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 16,

			textColor3 = Style.CYAN,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.12,
			},

			zIndex = zIndex + 2,
		}),

		Text({
			name = "Task",
			text = `Task: {achievement.TaskText}`,

			size = UDim2.fromScale(0.27, 0.7),
			position = UDim2.fromScale(0.39, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Style.FONT_BOLD_ITALIC,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 15,

			textColor3 = Color3.fromRGB(235, 240, 245),

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.16,
			},

			zIndex = zIndex + 2,
		}),

		Text({
			name = "Progress",
			text = `Progress: {achievement.ProgressText}`,

			size = UDim2.fromScale(0.24, 0.7),
			position = UDim2.fromScale(0.66, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Style.FONT_BOLD_ITALIC,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 15,

			textColor3 = Color3.fromRGB(235, 240, 245),

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.16,
			},

			zIndex = zIndex + 2,
		}),

		if isAvailable
			then create("TextButton")({
				Name = "CollectButton",

				Size = UDim2.fromScale(0.125, 0.62),
				Position = UDim2.fromScale(0.9, 0.5),
				AnchorPoint = Vector2.new(0.5, 0.5),

				AutoButtonColor = false,
				Text = "",

				BackgroundColor3 = getStatusColor(achievement.State),
				BackgroundTransparency = 0,
				BorderSizePixel = 0,
				ZIndex = zIndex + 3,

				Activated = function()
					if props.onCollect ~= nil then
						props.onCollect(achievement)
					end
				end,

				create("UICorner")({
					CornerRadius = UDim.new(0.45, 0),
				}),

				create("UIStroke")({
					Thickness = 1.25,
					Color = Color3.fromRGB(190, 255, 170),
					Transparency = 0.08,
					ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
				}),

				create("UIGradient")({
					Rotation = 90,
					Color = ColorSequence.new({
						ColorSequenceKeypoint.new(0, Color3.fromRGB(160, 255, 100)),
						ColorSequenceKeypoint.new(1, Color3.fromRGB(48, 175, 28)),
					}),
				}),

				Text({
					name = "CollectText",
					text = "Collect",

					size = UDim2.fromScale(0.92, 0.82),
					position = UDim2.fromScale(0.5, 0.5),
					anchorPoint = Vector2.new(0.5, 0.5),

					fontFace = Style.FONT_BOLD_ITALIC,
					textScaled = true,
					minTextSize = 6,
					maxTextSize = 18,

					textColor3 = Style.WHITE,

					stroke = {
						thickness = 1,
						color = Color3.fromRGB(0, 0, 0),
						transparency = 0.1,
					},

					zIndex = zIndex + 4,
				}),

				Effects.HoverUIScale({
					idleScale = 1,
					hoverScale = 1.08,
					scaleTextConstraints = true,
					duration = 0.12,
				}),
			})
			else create("Frame")({
				Name = "StatusFrame",

				Size = UDim2.fromScale(0.125, 0.62),
				Position = UDim2.fromScale(0.9, 0.5),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundColor3 = getStatusColor(achievement.State),
				BackgroundTransparency = 0.18,
				BorderSizePixel = 0,
				ZIndex = zIndex + 3,

				create("UICorner")({
					CornerRadius = UDim.new(0.45, 0),
				}),

				Text({
					name = "StatusText",
					text = getStateText(achievement.State),

					size = UDim2.fromScale(0.92, 0.82),
					position = UDim2.fromScale(0.5, 0.5),
					anchorPoint = Vector2.new(0.5, 0.5),

					fontFace = Style.FONT_BOLD_ITALIC,
					textScaled = true,
					minTextSize = 6,
					maxTextSize = 16,

					textColor3 = Color3.fromRGB(235, 240, 245),

					stroke = {
						thickness = 1,
						color = Color3.fromRGB(0, 0, 0),
						transparency = 0.12,
					},

					zIndex = zIndex + 4,
				}),
			}),
	})
end

return AchievementRow
