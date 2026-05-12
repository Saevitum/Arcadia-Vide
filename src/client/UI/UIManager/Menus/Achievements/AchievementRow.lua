--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

local MockAchievements = require(script.Parent.MockAchievements)

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

local Tokens = Style.Tokens
local ROW_LAYOUT = Style.Rows.Layouts.WideList
local ROW_STYLE = Style.Rows.Presets.SegmentedCyber

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
		return ROW_STYLE.collectColor
	end

	if state == "Claimed" then
		return ROW_STYLE.claimedColor
	end

	return ROW_STYLE.lockedColor
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

		BackgroundColor3 = ROW_STYLE.segmentBackgroundColor,
		BackgroundTransparency = ROW_STYLE.segmentBackgroundTransparency,
		BorderSizePixel = 0,

		ZIndex = props.zIndex,

		create("UICorner")({
			CornerRadius = ROW_STYLE.segmentCornerRadius,
		}),

		create("UIGradient")({
			Rotation = 0,
			Color = ROW_STYLE.segmentGradient,
			Transparency = ROW_STYLE.segmentTransparency,
		}),
	})
end

local function AchievementRow(props: AchievementRowProps)
	local achievement = props.achievement
	local zIndex = props.zIndex or 24
	local isAvailable = achievement.State == "Available"

	return create("Frame")({
		Name = `AchievementRow_{achievement.Id}`,

		Size = ROW_LAYOUT.rowSize,

		BackgroundColor3 = ROW_STYLE.rowBackgroundColor,
		BackgroundTransparency = ROW_STYLE.rowBackgroundTransparency,
		BorderSizePixel = 0,

		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		create("UICorner")({
			CornerRadius = ROW_STYLE.rowCornerRadius,
		}),

		create("UIGradient")({
			Rotation = 0,
			Color = ROW_STYLE.rowGradient,
			Transparency = ROW_STYLE.rowTransparency,
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

			fontFace = ROW_STYLE.fontFace,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 16,

			textColor3 = ROW_STYLE.titleColor,

			stroke = {
				thickness = ROW_STYLE.textStrokeThickness,
				color = ROW_STYLE.textStrokeColor,
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

			fontFace = ROW_STYLE.fontFace,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 15,

			textColor3 = ROW_STYLE.textColor,

			stroke = {
				thickness = ROW_STYLE.textStrokeThickness,
				color = ROW_STYLE.textStrokeColor,
				transparency = ROW_STYLE.textStrokeTransparency,
			},

			zIndex = zIndex + 2,
		}),

		Text({
			name = "Progress",
			text = `Progress: {achievement.ProgressText}`,

			size = UDim2.fromScale(0.24, 0.7),
			position = UDim2.fromScale(0.66, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = ROW_STYLE.fontFace,
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 15,

			textColor3 = ROW_STYLE.textColor,

			stroke = {
				thickness = ROW_STYLE.textStrokeThickness,
				color = ROW_STYLE.textStrokeColor,
				transparency = ROW_STYLE.textStrokeTransparency,
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
					Thickness = Tokens.Strokes.Thin,
					Color = ROW_STYLE.collectStrokeColor,
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

					fontFace = ROW_STYLE.fontFace,
					textScaled = true,
					minTextSize = 6,
					maxTextSize = 18,

					textColor3 = Tokens.Colors.White,

					stroke = {
						thickness = 1,
						color = Tokens.Colors.Black,
						transparency = 0.1,
					},

					zIndex = zIndex + 4,
				}),

				Effects.HoverUIScale({
					idleScale = 1,
					hoverScale = 1.08,
					scaleTextConstraints = true,
					duration = Tokens.Timing.Hover,
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

					fontFace = ROW_STYLE.fontFace,
					textScaled = true,
					minTextSize = 6,
					maxTextSize = 16,

					textColor3 = ROW_STYLE.textColor,

					stroke = {
						thickness = ROW_STYLE.textStrokeThickness,
						color = ROW_STYLE.textStrokeColor,
						transparency = 0.12,
					},

					zIndex = zIndex + 4,
				}),
			}),
	})
end

return AchievementRow
