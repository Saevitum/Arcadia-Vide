--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local MockRewards = require(script.Parent.MockRewards)

Vide.strict = true

local create = Vide.create

local Text = Components.Text
local Image = Components.Image

type RewardView = MockRewards.RewardView
type RewardState = MockRewards.RewardState

export type RewardCardProps = {
	reward: RewardView,
	layoutOrder: number?,
	zIndex: number?,

	onCollect: (() -> ())?,

	onHoverStart: ((reward: RewardView, x: number, y: number) -> ())?,
	onHoverMove: ((x: number, y: number) -> ())?,
	onHoverEnd: (() -> ())?,
}

local FONT_TITLE = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)

local FONT_STATUS = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)

local THEME_CYAN = Color3.fromRGB(0, 255, 238)
local THEME_MAGENTA = Color3.fromRGB(255, 0, 255)
local THEME_PURPLE = Color3.fromRGB(142, 5, 255)

local CLAIMED_STROKE_A = Color3.fromRGB(56, 66, 72)
local CLAIMED_STROKE_B = Color3.fromRGB(18, 22, 26)

local function getAccentColor(state: RewardState): Color3
	if state == "Claimed" then
		return CLAIMED_STROKE_A
	end

	return THEME_CYAN
end

local function getStrokeGradient(state: RewardState): ColorSequence
	if state == "Claimed" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, CLAIMED_STROKE_A),
			ColorSequenceKeypoint.new(0.5, Color3.fromRGB(105, 116, 124)),
			ColorSequenceKeypoint.new(1, CLAIMED_STROKE_B),
		})
	end

	if state == "Available" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, THEME_CYAN),
			ColorSequenceKeypoint.new(0.52, Color3.fromRGB(255, 255, 255)),
			ColorSequenceKeypoint.new(1, THEME_MAGENTA),
		})
	end

	return ColorSequence.new({
		ColorSequenceKeypoint.new(0, Color3.fromRGB(0, 135, 145)),
		ColorSequenceKeypoint.new(0.5, THEME_PURPLE),
		ColorSequenceKeypoint.new(1, Color3.fromRGB(150, 0, 165)),
	})
end

local function getStrokeTransparency(state: RewardState): number
	if state == "Available" then
		return 0
	end

	if state == "Locked" then
		return 0.28
	end

	return 0.42
end

local function getStatusBaseColor(state: RewardState): Color3
	if state == "Available" then
		return Color3.fromRGB(0, 205, 170)
	end

	if state == "Locked" then
		return Color3.fromRGB(20, 8, 30)
	end

	return Color3.fromRGB(18, 22, 26)
end

local function getStatusGradient(state: RewardState): ColorSequence
	if state == "Claimed" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, Color3.fromRGB(62, 68, 72)),
			ColorSequenceKeypoint.new(0.5, Color3.fromRGB(26, 30, 34)),
			ColorSequenceKeypoint.new(1, Color3.fromRGB(9, 12, 15)),
		})
	end

	if state == "Available" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, Color3.fromRGB(115, 255, 235)),
			ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0, 220, 170)),
			ColorSequenceKeypoint.new(1, Color3.fromRGB(170, 0, 255)),
		})
	end

	return ColorSequence.new({
		ColorSequenceKeypoint.new(0, Color3.fromRGB(0, 95, 105)),
		ColorSequenceKeypoint.new(0.5, Color3.fromRGB(42, 16, 72)),
		ColorSequenceKeypoint.new(1, Color3.fromRGB(115, 0, 125)),
	})
end

local function getCardGradient(state: RewardState): ColorSequence
	if state == "Claimed" then
		return ColorSequence.new({
			ColorSequenceKeypoint.new(0, Color3.fromRGB(24, 27, 31)),
			ColorSequenceKeypoint.new(0.52, Color3.fromRGB(8, 10, 13)),
			ColorSequenceKeypoint.new(1, Color3.fromRGB(2, 3, 5)),
		})
	end

	return ColorSequence.new({
		ColorSequenceKeypoint.new(0, Color3.fromRGB(22, 27, 38)),
		ColorSequenceKeypoint.new(0.52, Color3.fromRGB(7, 9, 15)),
		ColorSequenceKeypoint.new(1, Color3.fromRGB(2, 3, 6)),
	})
end

local function getAmountText(reward: RewardView): string
	if reward.Money ~= nil then
		return `+{reward.Money} Money`
	end

	if reward.SideKick ~= nil then
		return `SideKick: {reward.SideKick}`
	end

	return "Reward"
end

local function getFooterText(reward: RewardView): string
	if reward.State == "Claimed" then
		return "CLAIMED"
	end

	if reward.State == "Available" then
		return "COLLECT"
	end

	return reward.TimeRemaining or "LOCKED"
end

local function getImageTransparency(state: RewardState): number
	if state == "Claimed" then
		return 0.18
	end

	if state == "Locked" then
		return 0.28
	end

	return 0
end

local function getCardBackgroundTransparency(state: RewardState): number
	if state == "Available" then
		return 0.08
	end

	return 0.16
end

local function RewardCard(props: RewardCardProps)
	local reward = props.reward
	local zIndex = props.zIndex or 12

	local accentColor = getAccentColor(reward.State)
	local isAvailable = reward.State == "Available"
	local isLocked = reward.State == "Locked"

	return create("Frame")({
		Name = `RewardCard_{reward.Tier}_{reward.Title}`,

		Size = UDim2.fromScale(1, 1),
		BackgroundColor3 = Color3.fromRGB(5, 7, 13),
		BackgroundTransparency = getCardBackgroundTransparency(reward.State),
		BorderSizePixel = 0,

		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		create("UICorner")({
			CornerRadius = UDim.new(0.055, 0),
		}),

		create("UIStroke")({
			Thickness = if isAvailable then 2 else 1.25,
			Color = Color3.fromRGB(255, 255, 255),
			Transparency = getStrokeTransparency(reward.State),
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

			create("UIGradient")({
				Rotation = 0,
				Color = getStrokeGradient(reward.State),
			}),
		}),

		create("UIGradient")({
			Rotation = 90,
			Color = getCardGradient(reward.State),
			Transparency = NumberSequence.new({
				NumberSequenceKeypoint.new(0, if reward.State == "Claimed" then 0.08 else 0.02),
				NumberSequenceKeypoint.new(0.55, if reward.State == "Claimed" then 0.14 else 0.08),
				NumberSequenceKeypoint.new(1, if reward.State == "Claimed" then 0.22 else 0.16),
			}),
		}),

		-- Soft top glass reflection.
		create("Frame")({
			Name = "GlassSheen",

			Size = UDim2.fromScale(1, 0.42),
			Position = UDim2.fromScale(0.5, 0),
			AnchorPoint = Vector2.new(0.5, 0),

			BackgroundColor3 = Color3.fromRGB(255, 255, 255),
			BackgroundTransparency = 0.9,
			BorderSizePixel = 0,
			ZIndex = zIndex + 1,

			create("UICorner")({
				CornerRadius = UDim.new(0.055, 0),
			}),

			create("UIGradient")({
				Rotation = 90,
				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 0.58),
					NumberSequenceKeypoint.new(0.68, 0.96),
					NumberSequenceKeypoint.new(1, 1),
				}),
			}),
		}),

		-- Very subtle state glow behind the image.
		create("Frame")({
			Name = "ImageGlow",

			Size = UDim2.fromScale(0.62, 0.38),
			Position = UDim2.fromScale(0.5, 0.445),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = if reward.State == "Claimed" then Color3.fromRGB(70, 78, 84) else accentColor,
			BackgroundTransparency = if isAvailable then 0.78 elseif reward.State == "Claimed" then 0.94 else 0.88,
			BorderSizePixel = 0,
			ZIndex = zIndex + 1,

			create("UICorner")({
				CornerRadius = UDim.new(0.22, 0),
			}),

			create("UIGradient")({
				Rotation = 0,
				Color = if reward.State == "Claimed"
					then ColorSequence.new({
						ColorSequenceKeypoint.new(0, Color3.fromRGB(46, 52, 58)),
						ColorSequenceKeypoint.new(1, Color3.fromRGB(12, 14, 18)),
					})
					else ColorSequence.new({
						ColorSequenceKeypoint.new(0, THEME_CYAN),
						ColorSequenceKeypoint.new(1, THEME_MAGENTA),
					}),
				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 1),
					NumberSequenceKeypoint.new(0.5, 0.25),
					NumberSequenceKeypoint.new(1, 1),
				}),
			}),
		}),

		Text({
			name = "Title",
			text = reward.Title,

			size = UDim2.fromScale(0.88, 0.16),
			position = UDim2.fromScale(0.5, 0.07),
			anchorPoint = Vector2.new(0.5, 0),

			fontFace = FONT_TITLE,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 18,

			textColor3 = Color3.fromRGB(245, 248, 255),
			textTransparency = if isLocked then 0.08 else 0,

			stroke = {
				thickness = 1.25,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.18,
			},

			zIndex = zIndex + 5,
		}),

		create("ImageButton")({
			Name = "RewardImage",

			AutoButtonColor = false,
			Image = reward.ImageId,

			Size = UDim2.fromScale(0.62, 0.56),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,

			ImageTransparency = getImageTransparency(reward.State),

			ZIndex = zIndex + 100,

			MouseEnter = function(x: number, y: number)
				if props.onHoverStart ~= nil then
					props.onHoverStart(reward, x, y)
				end
			end,

			MouseMoved = function(x: number, y: number)
				if props.onHoverMove ~= nil then
					props.onHoverMove(x, y)
				end
			end,

			MouseLeave = function()
				if props.onHoverEnd ~= nil then
					props.onHoverEnd()
				end
			end,

			create("UIAspectRatioConstraint")({
				AspectRatio = 1,
				DominantAxis = Enum.DominantAxis.Height,
			}),

			Effects.HoverUIScale({
				idleScale = 1,
				hoverScale = if reward.State == "Locked" then 1.5 else 1.5,
				duration = 0.12,
			}),
		}),

		if isAvailable
			then create("TextButton")({
				Name = "CollectButton",

				AutoButtonColor = false,
				Text = "",
				Size = UDim2.fromScale(0.82, 0.17),
				Position = UDim2.fromScale(0.5, 0.855),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundColor3 = getStatusBaseColor(reward.State),
				BackgroundTransparency = 0.04,
				BorderSizePixel = 0,

				ZIndex = zIndex + 8,

				Activated = function()
					if props.onCollect ~= nil then
						props.onCollect()
					end
				end,

				create("UICorner")({
					CornerRadius = UDim.new(0.22, 0),
				}),

				create("UIStroke")({
					Thickness = 1.5,
					Color = Color3.fromRGB(255, 255, 255),
					Transparency = 0.04,
					ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

					create("UIGradient")({
						Rotation = 0,
						Color = getStrokeGradient(reward.State),
					}),
				}),

				create("UIGradient")({
					Rotation = 90,
					Color = getStatusGradient(reward.State),
				}),

				Text({
					name = "CollectText",
					text = "COLLECT",

					size = UDim2.fromScale(0.92, 0.84),
					position = UDim2.fromScale(0.5, 0.5),
					anchorPoint = Vector2.new(0.5, 0.5),

					fontFace = FONT_STATUS,
					textScaled = true,
					minTextSize = 8,
					maxTextSize = 17,

					textColor3 = Color3.fromRGB(255, 255, 255),

					stroke = {
						thickness = 1.5,
						color = Color3.fromRGB(0, 0, 0),
						transparency = 0.08,
					},

					zIndex = zIndex + 9,
				}),

				Effects.HoverUIScale({
					idleScale = 1,
					hoverScale = 1.06,
					duration = 0.1,
					scaleTextConstraints = true,
				}),
			})
			else create("Frame")({
				Name = "StatusStrip",

				Size = UDim2.fromScale(0.82, 0.17),
				Position = UDim2.fromScale(0.5, 0.855),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundColor3 = getStatusBaseColor(reward.State),
				BackgroundTransparency = if reward.State == "Claimed" then 0.36 else 0.28,
				BorderSizePixel = 0,

				ZIndex = zIndex + 6,

				create("UICorner")({
					CornerRadius = UDim.new(0.22, 0),
				}),

				create("UIGradient")({
					Rotation = 90,
					Color = getStatusGradient(reward.State),
					Transparency = NumberSequence.new({
						NumberSequenceKeypoint.new(0, if reward.State == "Claimed" then 0.72 else 0.62),
						NumberSequenceKeypoint.new(1, if reward.State == "Claimed" then 0.12 else 0.04),
					}),
				}),

				Text({
					name = "StatusText",
					text = getFooterText(reward),

					size = UDim2.fromScale(0.92, 0.82),
					position = UDim2.fromScale(0.5, 0.5),
					anchorPoint = Vector2.new(0.5, 0.5),

					fontFace = FONT_STATUS,
					textScaled = true,
					minTextSize = 7,
					maxTextSize = 16,

					textColor3 = Color3.fromRGB(245, 248, 255),
					textTransparency = if reward.State == "Claimed" then 0.08 else 0,

					stroke = {
						thickness = 1.35,
						color = Color3.fromRGB(0, 0, 0),
						transparency = 0.12,
					},

					zIndex = zIndex + 7,
				}),
			}),
		if isAvailable
			then Effects.PulseUIScale({
				idleScale = 1,
				pulseScale = 1.06,
				period = 2.2,
			})
			else nil,
	})
end

return RewardCard
