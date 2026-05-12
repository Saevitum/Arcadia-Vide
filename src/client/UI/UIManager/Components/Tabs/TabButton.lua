--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)
local Types = require(script.Parent.Parent.Parent.UITypes.ComponentTypes)

Vide.strict = true

local create = Vide.create
local source = Vide.source

type TabButtonProps<T> = Types.TabButtonProps<T>
type TabButtonStyle = Types.TabButtonStyle
type TabVisualStateStyle = Types.TabVisualStateStyle
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

local DEFAULT_BUTTON_STYLE: TabButtonStyle = Style.Tabs.Presets.CyberDefault.button :: TabButtonStyle

local function mergeButtonStyle(style: TabButtonStyle?): TabButtonStyle
	return Style.Tabs.merge(DEFAULT_BUTTON_STYLE, style or {}) :: TabButtonStyle
end

local function isSelected<T>(props: TabButtonProps<T>): boolean
	return (props.selectedTab() :: any) == (props.tab.id :: any)
end

local function isDisabled<T>(props: TabButtonProps<T>): boolean
	return props.tab.disabled == true
end

local function getStateStyle<T>(
	props: TabButtonProps<T>,
	buttonStyle: TabButtonStyle,
	hovered: Types.Source<boolean>
): TabVisualStateStyle
	if isDisabled(props) then
		return buttonStyle.disabled or buttonStyle.default or {}
	end

	if isSelected(props) then
		return buttonStyle.selected or buttonStyle.default or {}
	end

	if hovered() then
		return buttonStyle.hover or buttonStyle.default or {}
	end

	return buttonStyle.default or {}
end

local function TabButton<T>(props: TabButtonProps<T>)
	local hovered = source(false)
	local buttonStyle = mergeButtonStyle(props.style)

	local function currentStyle(): TabVisualStateStyle
		return getStateStyle(props, buttonStyle, hovered)
	end

	local function activate()
		if isDisabled(props) then
			return
		end

		if props.onTabSelected ~= nil then
			props.onTabSelected(props.tab.id)
			return
		end

		props.selectedTab(props.tab.id)
	end

	return create("TextButton")({
		Name = "Tab_" .. props.tab.label,

		Size = function()
			return read(props.size, UDim2.fromScale(1, 1))
		end,

		Position = function()
			return read(props.position, UDim2.fromScale(0, 0))
		end,

		AnchorPoint = function()
			return read(props.anchorPoint, Vector2.new(0, 0))
		end,

		Visible = function()
			return read(props.visible, true)
		end,

		LayoutOrder = props.tab.layoutOrder or 0,

		ZIndex = function()
			return read(props.zIndex, 1)
		end,

		Text = "",
		AutoButtonColor = false,
		ClipsDescendants = true,
		BorderSizePixel = 0,

		BackgroundColor3 = function()
			return currentStyle().backgroundColor or Color3.fromRGB(10, 17, 24)
		end,

		BackgroundTransparency = function()
			return currentStyle().glossBackgroundTransparency or 0
		end,

		Activated = activate,

		MouseEnter = function()
			hovered(true)
		end,

		MouseLeave = function()
			hovered(false)
		end,

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = buttonStyle.hoverScale or 1,
			duration = buttonStyle.hoverDuration or 0.12,
			scaleTextConstraints = true,
		}),

		create("UICorner")({
			CornerRadius = buttonStyle.cornerRadius or UDim.new(0.16, 0),
		}),

		create("UIGradient")({
			Color = function()
				return currentStyle().gradient or ColorSequence.new(Color3.fromRGB(10, 17, 24))
			end,

			Rotation = function()
				return currentStyle().gradientRotation or 0
			end,
		}),

		create("UIStroke")({
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,

			Color = function()
				return currentStyle().strokeColor or Color3.fromRGB(0, 229, 255)
			end,

			Transparency = function()
				return currentStyle().strokeTransparency or 0.15
			end,

			Thickness = function()
				return currentStyle().strokeThickness or 2
			end,

			create("UIGradient")({
				Color = function()
					return currentStyle().strokeGradient or ColorSequence.new(Color3.fromRGB(255, 255, 255))
				end,

				Rotation = function()
					return currentStyle().strokeGradientRotation or 0
				end,
			}),
		}),

		create("Frame")({
			Name = "Gloss",
			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundColor3 = function()
				return currentStyle().glossColor or Color3.fromRGB(255, 255, 255)
			end,

			BackgroundTransparency = function()
				return currentStyle().glossBackgroundTransparency or 0
			end,

			BorderSizePixel = 0,

			ZIndex = function()
				return read(props.zIndex, 1) + 1
			end,

			create("UICorner")({
				CornerRadius = buttonStyle.cornerRadius or UDim.new(0.16, 0),
			}),

			create("UIGradient")({
				Rotation = 90,

				Transparency = function()
					return currentStyle().glossTransparency
						or NumberSequence.new({
							NumberSequenceKeypoint.new(0, 1),
							NumberSequenceKeypoint.new(0.5, 0.75),
							NumberSequenceKeypoint.new(1, 0),
						})
				end,
			}),
		}),

		create("TextLabel")({
			Name = "Label",
			Size = UDim2.fromScale(0.9, 0.68),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,

			Text = props.tab.label,
			TextScaled = true,
			TextWrapped = false,
			TextXAlignment = Enum.TextXAlignment.Center,
			TextYAlignment = Enum.TextYAlignment.Center,

			FontFace = buttonStyle.fontFace
				or Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),

			TextColor3 = function()
				return currentStyle().textColor or Color3.fromRGB(255, 255, 255)
			end,

			TextTransparency = function()
				return currentStyle().textTransparency or 0
			end,

			ZIndex = function()
				return read(props.zIndex, 1) + 2
			end,

			create("UITextSizeConstraint")({
				MinTextSize = buttonStyle.minTextSize or 7,
				MaxTextSize = buttonStyle.maxTextSize or 17,
			}),

			create("UIStroke")({
				ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual,
				Color = buttonStyle.textStrokeColor or Color3.fromRGB(0, 0, 0),
				Transparency = buttonStyle.textStrokeTransparency or 0.55,
				Thickness = buttonStyle.textStrokeThickness or 1,
			}),
		}),
	})
end

return TabButton
