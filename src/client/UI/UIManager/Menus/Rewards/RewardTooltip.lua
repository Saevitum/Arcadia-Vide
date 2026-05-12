--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local MockRewards = require(script.Parent.MockRewards)

Vide.strict = true

local create = Vide.create

local Text = Components.Text
local Image = Components.Image

type RewardView = MockRewards.RewardView

export type RewardTooltipProps = {
	reward: () -> RewardView?,
	visible: () -> boolean,
	position: (() -> UDim2)?,
	zIndex: number?,
}

local FONT_TITLE = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)

local FONT_BODY = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal)

local THEME_CYAN = Color3.fromRGB(0, 255, 238)
local THEME_MAGENTA = Color3.fromRGB(255, 0, 255)

local function getRewardValueText(reward: RewardView): string
	if reward.Money ~= nil then
		return `+{reward.Money} Money`
	end

	if reward.SideKick ~= nil then
		return `SideKick: {reward.SideKick}`
	end

	return "Unknown Reward"
end

local function getRewardDescription(reward: RewardView): string
	return reward.Description
end

local function getStateText(reward: RewardView): string
	if reward.State == "Claimed" then
		return "Already claimed in this cycle."
	end

	if reward.State == "Available" then
		return "Ready to collect now."
	end

	return `Unlocks in {reward.TimeRemaining or "soon"}.`
end

local function RewardTooltip(props: RewardTooltipProps)
	local function getReward(): RewardView?
		return props.reward()
	end
	local zIndex = props.zIndex or 80

	return create("Frame")({
		Name = "RewardTooltip",

		Visible = props.visible,

		Size = UDim2.fromScale(0.32, 0.32),
		Position = function()
			if props.position ~= nil then
				return props.position()
			end

			return UDim2.fromOffset(0, 0)
		end,

		AnchorPoint = Vector2.new(0, 0),

		BackgroundColor3 = Color3.fromRGB(4, 6, 11),
		BackgroundTransparency = 0,
		BorderSizePixel = 0,
		ZIndex = zIndex,

		create("UIAspectRatioConstraint")({
			AspectRatio = 1,
			DominantAxis = Enum.DominantAxis.Width,
		}),

		create("UISizeConstraint")({
			MinSize = Vector2.new(240, 240),
			MaxSize = Vector2.new(460, 460),
		}),

		create("UICorner")({
			CornerRadius = UDim.new(0.06, 0),
		}),

		create("UIStroke")({
			Thickness = 1.75,
			Color = Color3.fromRGB(255, 255, 255),
			Transparency = 0.04,
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

			create("UIGradient")({
				Rotation = 0,
				Color = ColorSequence.new({
					ColorSequenceKeypoint.new(0, THEME_CYAN),
					ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 255, 255)),
					ColorSequenceKeypoint.new(1, THEME_MAGENTA),
				}),
			}),
		}),

		create("UIGradient")({
			Rotation = 90,
			Color = ColorSequence.new({
				ColorSequenceKeypoint.new(0, Color3.fromRGB(24, 29, 40)),
				ColorSequenceKeypoint.new(0.48, Color3.fromRGB(7, 9, 15)),
				ColorSequenceKeypoint.new(1, Color3.fromRGB(2, 3, 6)),
			}),
		}),

		create("Frame")({
			Name = "TopSheen",

			Size = UDim2.fromScale(1, 0.34),
			Position = UDim2.fromScale(0.5, 0),
			AnchorPoint = Vector2.new(0.5, 0),

			BackgroundColor3 = Color3.fromRGB(255, 255, 255),
			BackgroundTransparency = 0.91,
			BorderSizePixel = 0,
			ZIndex = zIndex + 1,

			create("UICorner")({
				CornerRadius = UDim.new(0.06, 0),
			}),

			create("UIGradient")({
				Rotation = 90,
				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 0.52),
					NumberSequenceKeypoint.new(0.72, 0.96),
					NumberSequenceKeypoint.new(1, 1),
				}),
			}),
		}),

		Text({
			name = "TooltipName",
			text = function()
				local reward = getReward()
				return if reward ~= nil then reward.Title else ""
			end,

			size = UDim2.fromScale(0.86, 0.14),
			position = UDim2.fromScale(0.5, 0.08),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_TITLE,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 18,

			textColor3 = Color3.fromRGB(255, 255, 255),

			stroke = {
				thickness = 1.25,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.12,
			},

			zIndex = zIndex + 3,
		}),

		create("Frame")({
			Name = "ImageGlow",

			Size = UDim2.fromScale(0.52, 0.38),
			Position = UDim2.fromScale(0.5, 0.355),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = THEME_CYAN,
			BackgroundTransparency = 0.84,
			BorderSizePixel = 0,
			ZIndex = zIndex + 1,

			create("UICorner")({
				CornerRadius = UDim.new(0.2, 0),
			}),

			create("UIGradient")({
				Rotation = 0,
				Color = ColorSequence.new({
					ColorSequenceKeypoint.new(0, THEME_CYAN),
					ColorSequenceKeypoint.new(1, THEME_MAGENTA),
				}),
				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 1),
					NumberSequenceKeypoint.new(0.5, 0.22),
					NumberSequenceKeypoint.new(1, 1),
				}),
			}),
		}),

		Image({
			name = "TooltipImage",
			image = function()
				local reward = getReward()
				return if reward ~= nil then reward.ImageId else ""
			end,

			size = UDim2.fromScale(0.52, 0.52),
			position = UDim2.fromScale(0.5, 0.36),
			anchorPoint = Vector2.new(0.5, 0.5),

			backgroundTransparency = 1,
			zIndex = zIndex + 3,

			aspectRatio = 1,
		}),

		Text({
			name = "TooltipValue",
			text = function()
				local reward = getReward()
				return if reward ~= nil then getRewardValueText(reward) else ""
			end,

			size = UDim2.fromScale(0.84, 0.13),
			position = UDim2.fromScale(0.5, 0.625),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_TITLE,
			textScaled = true,
			minTextSize = 12,
			maxTextSize = 22,

			textColor3 = function()
				local reward = getReward()
				return if reward ~= nil and reward.State == "Available"
					then THEME_CYAN
					else Color3.fromRGB(225, 235, 240)
			end,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.18,
			},

			zIndex = zIndex + 3,
		}),

		Text({
			name = "TooltipDescription",
			text = function()
				local reward = getReward()
				return if reward ~= nil then getRewardDescription(reward) else ""
			end,

			size = UDim2.fromScale(0.82, 0.18),
			position = UDim2.fromScale(0.5, 0.765),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_BODY,
			textScaled = true,
			minTextSize = 12,
			maxTextSize = 22,

			textColor3 = Color3.fromRGB(185, 205, 215),

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.3,
			},

			zIndex = zIndex + 3,
		}),

		Text({
			name = "TooltipState",
			text = function()
				local reward = getReward()
				return if reward ~= nil then getStateText(reward) else ""
			end,

			size = UDim2.fromScale(0.82, 0.1),
			position = UDim2.fromScale(0.5, 0.91),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = FONT_BODY,
			textScaled = true,
			minTextSize = 12,
			maxTextSize = 22,

			textColor3 = function()
				local reward = getReward()
				return if reward ~= nil and reward.State == "Available"
					then THEME_CYAN
					else Color3.fromRGB(145, 160, 170)
			end,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.35,
			},

			zIndex = zIndex + 3,
		}),
	})
end

return RewardTooltip
