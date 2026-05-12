--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action

local Text = Components.Text

export type RewardsInfoButtonProps = {
	zIndex: number?,
}

local FONT_TITLE = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic)
local FONT_INFO = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal)

local FONT_BODY = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Medium, Enum.FontStyle.Italic)

local THEME_CYAN = Color3.fromRGB(0, 255, 238)
local THEME_MAGENTA = Color3.fromRGB(255, 0, 255)

local function RewardsInfoButton(props: RewardsInfoButtonProps)
	local zIndex = props.zIndex or 100

	local isHovering = source(false)
	local tooltipPosition = source(UDim2.fromOffset(0, 0))

	local rootFrame: Frame? = nil

	local function updateTooltipPosition()
		if rootFrame == nil then
			return
		end

		local mousePosition = UserInputService:GetMouseLocation()

		local localX = mousePosition.X - rootFrame.AbsolutePosition.X + 45
		local localY = mousePosition.Y - rootFrame.AbsolutePosition.Y - 250

		tooltipPosition(UDim2.fromOffset(localX, localY))
	end

	return create("Frame")({
		Name = "RewardsInfoButtonHost",

		Size = UDim2.fromScale(1, 1),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = zIndex,

		action(function(instance: Instance)
			if not instance:IsA("Frame") then
				return
			end

			rootFrame = instance

			return function()
				if rootFrame == instance then
					rootFrame = nil
				end
			end
		end),

		create("TextButton")({
			Name = "InfoButton",

			AutoButtonColor = false,
			Text = "",

			Size = UDim2.fromScale(0.045, 0.072),
			Position = UDim2.fromScale(0.135, 0.25),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = Color3.fromRGB(4, 8, 14),
			BackgroundTransparency = 0.08,
			BorderSizePixel = 0,

			ZIndex = zIndex + 1,

			MouseEnter = function()
				isHovering(true)
				updateTooltipPosition()
			end,

			MouseMoved = function()
				updateTooltipPosition()
			end,

			MouseLeave = function()
				isHovering(false)
			end,

			create("UICorner")({
				CornerRadius = UDim.new(1, 0),
			}),

			create("UIStroke")({
				Thickness = 1.5,
				Color = Color3.fromRGB(255, 255, 255),
				Transparency = 0.08,
				ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

				create("UIGradient")({
					Rotation = 0,
					Color = ColorSequence.new({
						ColorSequenceKeypoint.new(0, THEME_CYAN),
						ColorSequenceKeypoint.new(1, THEME_MAGENTA),
					}),
				}),
			}),

			create("UIGradient")({
				Rotation = 90,
				Color = ColorSequence.new({
					ColorSequenceKeypoint.new(0, Color3.fromRGB(22, 27, 38)),
					ColorSequenceKeypoint.new(1, Color3.fromRGB(3, 5, 10)),
				}),
			}),

			Text({
				name = "InfoText",
				text = "Info",

				size = UDim2.fromScale(0.8, 0.8),
				position = UDim2.fromScale(0.5, 0.45),
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = FONT_INFO,
				textScaled = true,
				minTextSize = 8,
				maxTextSize = 24,

				textColor3 = Color3.fromRGB(255, 255, 255),

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.15,
				},

				zIndex = zIndex + 2,
			}),

			Effects.HoverUIScale({
				idleScale = 1,
				hoverScale = 1.08,
				duration = 0.12,
				scaleTextConstraints = true,
			}),
		}),

		create("Frame")({
			Name = "RewardsInfoTooltip",

			Visible = function()
				return isHovering()
			end,

			Size = UDim2.fromScale(0.36, 0.3),
			Position = function()
				return tooltipPosition()
			end,
			AnchorPoint = Vector2.new(0, 0),

			BackgroundColor3 = Color3.fromRGB(4, 6, 11),
			BackgroundTransparency = 0.035,
			BorderSizePixel = 0,

			ZIndex = zIndex + 20,

			create("UISizeConstraint")({
				MinSize = Vector2.new(300, 230),
				MaxSize = Vector2.new(520, 400),
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
					ColorSequenceKeypoint.new(0.5, Color3.fromRGB(7, 9, 15)),
					ColorSequenceKeypoint.new(1, Color3.fromRGB(2, 3, 6)),
				}),
			}),

			Text({
				name = "InfoTitle",
				text = "REWARD CYCLES",

				size = UDim2.fromScale(0.86, 0.16),
				position = UDim2.fromScale(0.5, 0.1),
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = FONT_TITLE,
				textScaled = true,
				minTextSize = 12,
				maxTextSize = 22,

				textColor3 = Color3.fromRGB(255, 255, 255),

				stroke = {
					thickness = 1.25,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.12,
				},

				zIndex = zIndex + 22,
			}),

			Text({
				name = "InfoBody",
				text = "Stay in game to unlock rewards over time. Claim all 12 rewards to complete a cycle. Each completed cycle upgrades future rewards. There are 6 cycles total.",

				size = UDim2.fromScale(0.82, 0.58),
				position = UDim2.fromScale(0.5, 0.47),
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = FONT_BODY,
				textScaled = true,
				textWrapped = true,
				minTextSize = 12,
				maxTextSize = 22,

				textColor3 = Color3.fromRGB(195, 215, 225),

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.35,
				},

				zIndex = zIndex + 22,
			}),

			Text({
				name = "InfoFooter",
				text = "Finish a cycle to unlock stronger rewards.",

				size = UDim2.fromScale(0.82, 0.12),
				position = UDim2.fromScale(0.5, 0.87),
				anchorPoint = Vector2.new(0.5, 0.5),

				fontFace = FONT_BODY,
				textScaled = true,
				minTextSize = 12,
				maxTextSize = 22,

				textColor3 = THEME_CYAN,

				stroke = {
					thickness = 1,
					color = Color3.fromRGB(0, 0, 0),
					transparency = 0.3,
				},

				zIndex = zIndex + 22,
			}),
		}),
	})
end

return RewardsInfoButton
