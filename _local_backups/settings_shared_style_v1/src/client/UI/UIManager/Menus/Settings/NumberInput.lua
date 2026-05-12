--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Style = require(script.Parent.Style)

Vide.strict = true

local action = Vide.action
local cleanup = Vide.cleanup
local create = Vide.create
local effect = Vide.effect
local source = Vide.source

local Text = Components.Text

type Source<T> = Types.Source<T>

export type NumberInputProps = {
	name: string,
	value: Source<number>,
	muted: Source<boolean>,
	size: UDim2,
	position: UDim2,
	anchorPoint: Vector2?,
	zIndex: number,
}

local function clampPercent(value: number): number
	return math.clamp(math.round(value), 0, 100)
end

local function formatPercent(value: number): string
	return tostring(clampPercent(value))
end

local function NumberInput(props: NumberInputProps)
	local textBox: TextBox? = nil
	local focused = source(false)
	local draftText = source("")

	local function commitText()
		if textBox == nil then
			return
		end

		local cleanedText = string.gsub(textBox.Text, "%%", "")
		cleanedText = string.gsub(cleanedText, "%s", "")

		local parsed = tonumber(cleanedText)
		if parsed == nil then
			textBox.Text = formatPercent(props.value())
			return
		end

		local nextValue = clampPercent(parsed)
		props.value(nextValue)
		textBox.Text = formatPercent(nextValue)
	end

	return create("Frame")({
		Name = props.name,

		Size = props.size,
		Position = props.position,
		AnchorPoint = props.anchorPoint or Vector2.new(0.5, 0.5),

		BackgroundColor3 = Style.DARK,
		BackgroundTransparency = function()
			if props.muted() then
				return 0.28
			end

			return 0.03
		end,

		BorderSizePixel = 0,
		ZIndex = props.zIndex,

		create("UICorner")({
			CornerRadius = UDim.new(0.22, 0),
		}),

		Style.NeonStroke(1, 0.12),

		create("TextBox")({
			Name = "Input",

			Size = UDim2.fromScale(0.64, 0.82),
			Position = UDim2.fromScale(0.38, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Text = function()
				if focused() then
					return ""
				end

				return formatPercent(props.value())
			end,

			PlaceholderText = "",
			PlaceholderColor3 = Color3.fromRGB(150, 160, 170),

			ClearTextOnFocus = false,
			TextEditable = true,
			MultiLine = false,

			FontFace = Style.FONT_BOLD,
			TextScaled = true,
			TextTransparency = function()
				if focused() then
					return 1
				end

				return 0
			end,
			TextColor3 = function()
				if props.muted() then
					return Color3.fromRGB(145, 152, 165)
				end

				return Style.WHITE
			end,
			TextStrokeTransparency = 0.55,
			TextXAlignment = Enum.TextXAlignment.Right,
			TextYAlignment = Enum.TextYAlignment.Center,

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = props.zIndex + 1,

			Focused = function()
				focused(true)
				draftText("")

				if textBox ~= nil then
					textBox.Text = ""
				end
			end,

			FocusLost = function(_enterPressed: boolean)
				commitText()
				focused(false)
			end,

			action(function(instance: Instance)
				if not instance:IsA("TextBox") then
					return
				end

				textBox = instance
				local textChanged = instance:GetPropertyChangedSignal("Text"):Connect(function()
					draftText(instance.Text)
				end)

				cleanup(function()
					textChanged:Disconnect()

					if textBox == instance then
						textBox = nil
					end
				end)
			end),

			create("UITextSizeConstraint")({
				MinTextSize = 7,
				MaxTextSize = 16,
			}),
		}),

		Text({
			name = "DraftText",
			text = function()
				return draftText()
			end,

			size = UDim2.fromScale(0.64, 0.82),
			position = UDim2.fromScale(0.38, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			visible = function()
				return focused()
			end,

			fontFace = Style.FONT_BOLD,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,

			textColor3 = function()
				if props.muted() then
					return Color3.fromRGB(145, 152, 165)
				end

				return Style.WHITE
			end,

			textXAlignment = Enum.TextXAlignment.Right,
			textYAlignment = Enum.TextYAlignment.Center,
			zIndex = props.zIndex + 2,
		}),

		create("Frame")({
			Name = "InputCaretPulse",

			Size = UDim2.fromScale(0.018, 0.55),
			Position = UDim2.fromScale(0.66, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Visible = function()
				return focused()
			end,

			BackgroundColor3 = function()
				if props.muted() then
					return Color3.fromRGB(145, 152, 165)
				end

				return Style.CYAN
			end,
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = props.zIndex + 3,

			action(function(instance: Instance)
				if not instance:IsA("Frame") then
					return
				end

				local caret = instance :: Frame
				local activeTween: Tween? = nil

				local function stopTween()
					if activeTween ~= nil then
						activeTween:Cancel()
						activeTween = nil
					end
				end

				effect(function()
					stopTween()

					if not focused() then
						caret.BackgroundTransparency = 1
						return
					end

					caret.BackgroundTransparency = 0.05
					local tween = TweenService:Create(
						caret,
						TweenInfo.new(0.46, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut, -1, true),
						{
							BackgroundTransparency = 0.85,
						}
					)
					activeTween = tween
					tween:Play()
				end)

				cleanup(function()
					stopTween()
				end)
			end),

			create("UICorner")({
				CornerRadius = UDim.new(0.5, 0),
			}),
		}),

		Text({
			name = "Percent",
			text = "%",

			size = UDim2.fromScale(0.24, 0.78),
			position = UDim2.fromScale(0.85, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),

			fontFace = Style.FONT_BOLD,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 14,

			textColor3 = function()
				if props.muted() then
					return Color3.fromRGB(145, 152, 165)
				end

				return Style.CYAN
			end,

			textXAlignment = Enum.TextXAlignment.Left,
			textYAlignment = Enum.TextYAlignment.Center,
			zIndex = props.zIndex + 1,
		}),
	})
end

return NumberInput
