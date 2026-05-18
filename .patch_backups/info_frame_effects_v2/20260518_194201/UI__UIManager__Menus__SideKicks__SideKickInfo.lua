--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Components = require(script.Parent.Parent.Parent.Components)
local MockSideKicks = require(script.Parent.MockSideKicks)
local Effects = require(script.Parent.Parent.Parent.Effects)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

local Text = Components.Text
local Image = Components.Image

type MockSideKick = MockSideKicks.MockSideKick

export type SideKickInfoProps = {
	selectedSideKick: () -> MockSideKick?,
	accentColor: () -> Color3,

	pulsePhase: (() -> number)?,
	onLockClicked: (() -> ())?,
	onRenameClicked: (() -> ())?,
	onNameSubmitted: ((newName: string) -> ())?,
}

local LOCK_IMAGE = "rbxassetid://13414458532"
local RENAME_IMAGE = "rbxassetid://13414468097"
local EXISTS_IMAGE = "rbxassetid://13415034457"

local function getSelected(props: SideKickInfoProps): MockSideKick?
	return props.selectedSideKick()
end

local function getSelectedText(props: SideKickInfoProps, selector: (MockSideKick) -> string, fallback: string): string
	local selected = getSelected(props)

	if selected == nil then
		return fallback
	end

	return selector(selected)
end

local function getSkillText(sideKick: MockSideKick?): string
	if sideKick == nil then
		return "--"
	end

	if sideKick.Skill == nil or sideKick.Skill == "" then
		return "Has no Skill!"
	end

	return sideKick.Skill
end

local function IconButton(props: {
	name: string,
	image: string,
	size: UDim2,
	position: UDim2,
	anchorPoint: Vector2,
	zIndex: number,
	onClick: (() -> ())?,
})
	return create("ImageButton")({
		Name = props.name,

		Image = props.image,
		ImageColor3 = Color3.fromRGB(255, 255, 255),
		ImageTransparency = 0,
		ScaleType = Enum.ScaleType.Fit,

		AutoButtonColor = false,

		Size = props.size,
		Position = props.position,
		AnchorPoint = props.anchorPoint,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = props.zIndex,

		Activated = function()
			if props.onClick ~= nil then
				props.onClick()
			end
		end,

		create("UICorner")({
			CornerRadius = UDim.new(0.15, 0),
		}),
	})
end

local function InfoRow(props: {
	name: string,
	size: UDim2,
	position: UDim2,
	children: { Instance },
})
	return create("Frame")({
		Name = props.name,

		Size = props.size,
		Position = props.position,
		AnchorPoint = Vector2.new(0, 0),

		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = 18,

		create("UIListLayout")({
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Left,
			VerticalAlignment = Enum.VerticalAlignment.Center,
			SortOrder = Enum.SortOrder.LayoutOrder,
			Padding = UDim.new(0.035, 0),
		}),

		props.children,
	})
end

local function SideKickInfo(props: SideKickInfoProps)
	local renameActive = source(false)
	local nameTextBox: TextBox? = nil
	local lastSelectedSideKickId: string? = nil

	effect(function()
		local selected = getSelected(props)
		local selectedId = if selected ~= nil then selected.SideKickId else nil

		if selectedId ~= lastSelectedSideKickId then
			lastSelectedSideKickId = selectedId
			renameActive(false)
		end
	end)

	return create("CanvasGroup")({
		Name = "SideKickInfo",

		Size = UDim2.fromScale(0.159, 0.518),
		Position = UDim2.fromScale(0.75, 0.49),
		AnchorPoint = Vector2.new(0.5, 0.5),

		Visible = false,
		GroupTransparency = 1,

		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = 17,

		Effects.SlideFadeCanvasGroup({
			open = function()
				return getSelected(props) ~= nil
			end,

			openPosition = UDim2.fromScale(0.75, 0.49),
			closedPosition = UDim2.fromScale(1.05, 0.49),

			openTransparency = 0,
			closedTransparency = 1,

			duration = 0.34,
			fadeDuration = 0.16,
			closeFadeDuration = 0.08,

			openEasingStyle = Enum.EasingStyle.Back,
			openEasingDirection = Enum.EasingDirection.Out,

			closeEasingStyle = Enum.EasingStyle.Quad,
			closeEasingDirection = Enum.EasingDirection.Out,

			fadeEasingStyle = Enum.EasingStyle.Quad,
			fadeEasingDirection = Enum.EasingDirection.Out,

			hideWhenClosed = true,
		}),

		create("UIStroke")({
			Color = Color3.fromRGB(255, 255, 255),
			Thickness = 2,
			Transparency = 0,

			create("UIGradient")({
				Color = function()
					local color = props.accentColor()

					return ColorSequence.new({
						ColorSequenceKeypoint.new(0, color),
						ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 255, 255)),
					})
				end,

				Rotation = 90,

				Transparency = NumberSequence.new({
					NumberSequenceKeypoint.new(0, 0),
					NumberSequenceKeypoint.new(0.602, 0.828),
					NumberSequenceKeypoint.new(1, 1),
				}),
				Effects.PulseGradientOffset({
					phase = props.pulsePhase,
					phaseMultiplier = 3,

					minOffset = Vector2.new(0, -0.35),
					maxOffset = Vector2.new(0, 0),
				}),
			}),
		}),

		create("Frame")({
			Name = "SideKickImage",

			Size = UDim2.fromScale(1, 0.5),
			Position = UDim2.fromScale(0.5, 0.25),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 18,

			Image({
				name = "SelectedSideKickImage",

				image = function()
					local selected = getSelected(props)

					if selected == nil then
						return ""
					end

					return selected.ImageId
				end,

				size = UDim2.fromScale(1, 1),
				position = UDim2.fromScale(0.5, 0.5),
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = 18,

				gradient = {
					rotation = 90,

					transparency = NumberSequence.new({
						NumberSequenceKeypoint.new(0, 0),
						NumberSequenceKeypoint.new(0.8, 0.755),
						NumberSequenceKeypoint.new(1, 1),
					}),
				},
			}),

			IconButton({
				name = "Lock",
				image = LOCK_IMAGE,

				size = UDim2.fromScale(0.185, 0.193),
				position = UDim2.fromScale(0.149, 0.13),
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = 20,
				onClick = props.onLockClicked,
			}),

			IconButton({
				name = "Rename",
				image = RENAME_IMAGE,

				size = UDim2.fromScale(0.185, 0.193),
				position = UDim2.fromScale(0.877, 0.124),
				anchorPoint = Vector2.new(0.5, 0.5),

				zIndex = 20,
				onClick = function()
					renameActive(true)

					if props.onRenameClicked ~= nil then
						props.onRenameClicked()
					end

					task.defer(function()
						if nameTextBox ~= nil then
							nameTextBox:CaptureFocus()
						end
					end)
				end,
			}),
		}),

		Text({
			name = "Title",

			text = function()
				return getSelectedText(props, function(sideKick)
					return sideKick.Name
				end, "")
			end,

			size = UDim2.fromScale(0.926, 0.08),
			position = UDim2.fromScale(0.5, 0.55),
			anchorPoint = Vector2.new(0.5, 0.5),

			visible = function()
				return not renameActive()
			end,

			fontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal),

			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.35,
			},

			zIndex = 21,
		}),

		create("TextBox")({
			Name = "RenameTextBox",

			Size = UDim2.fromScale(0.926, 0.08),
			Position = UDim2.fromScale(0.5, 0.55),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Visible = function()
				return renameActive()
			end,

			Text = function()
				if renameActive() then
					return ""
				end

				return getSelectedText(props, function(sideKick)
					return sideKick.Name
				end, "")
			end,

			PlaceholderText = "Type a name..",
			PlaceholderColor3 = Color3.fromRGB(180, 180, 190),

			ClearTextOnFocus = false,
			TextEditable = true,
			MultiLine = false,

			FontFace = Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Normal),

			TextScaled = true,
			TextColor3 = Color3.fromRGB(255, 255, 255),
			TextStrokeTransparency = 0.35,
			TextXAlignment = Enum.TextXAlignment.Center,
			TextYAlignment = Enum.TextYAlignment.Center,

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 22,

			FocusLost = function(enterPressed: boolean)
				local typedName = ""

				if nameTextBox ~= nil then
					typedName = nameTextBox.Text
				end

				renameActive(false)

				if not enterPressed then
					return
				end

				if typedName == "" then
					return
				end

				if props.onNameSubmitted == nil then
					return
				end

				props.onNameSubmitted(typedName)
			end,

			action(function(instance: Instance)
				if not instance:IsA("TextBox") then
					return
				end

				nameTextBox = instance

				cleanup(function()
					if nameTextBox == instance then
						nameTextBox = nil
					end
				end)
			end),

			create("UIStroke")({
				Color = Color3.fromRGB(0, 0, 0),
				Thickness = 3,
				Transparency = 0,
			}),

			create("UITextSizeConstraint")({
				MinTextSize = 7,
				MaxTextSize = 16,
			}),
		}),

		Text({
			name = "Rarity",

			text = function()
				return getSelectedText(props, function(sideKick)
					return sideKick.Rarity
				end, "--")
			end,

			size = UDim2.fromScale(0.395, 0.05),
			position = UDim2.fromScale(0.5, 0.62),
			anchorPoint = Vector2.new(0.5, 0.5),

			textScaled = true,
			minTextSize = 6,
			maxTextSize = 14,

			textColor3 = Color3.fromRGB(255, 255, 255),
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,

			stroke = {
				thickness = 1,
				color = Color3.fromRGB(0, 0, 0),
				transparency = 0.2,
			},

			zIndex = 21,
		}),

		create("Frame")({
			Name = "SelectedSideKickInfo",

			Size = UDim2.fromScale(1, 0.5),
			Position = UDim2.fromScale(0.5, 0.75),
			AnchorPoint = Vector2.new(0.5, 0.5),

			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 18,

			InfoRow({
				name = "Role",
				size = UDim2.fromScale(0.681, 0.17),
				position = UDim2.fromScale(0.054, 0.363),

				children = {
					Text({
						name = "Type",

						text = function()
							return getSelectedText(props, function(sideKick)
								return sideKick.Type
							end, "--")
						end,

						size = UDim2.fromScale(0.839, 0.651),

						textScaled = true,
						minTextSize = 6,
						maxTextSize = 13,

						textColor3 = Color3.fromRGB(255, 255, 255),
						textXAlignment = Enum.TextXAlignment.Left,
						textYAlignment = Enum.TextYAlignment.Center,

						zIndex = 19,
					}),
				},
			}),

			InfoRow({
				name = "Power",
				size = UDim2.fromScale(0.681, 0.17),
				position = UDim2.fromScale(0.054, 0.513),

				children = {
					Text({
						name = "Amount",

						text = function()
							local selected = getSelected(props)

							if selected == nil then
								return "--"
							end

							return `x{selected.BasePower}`
						end,

						size = UDim2.fromScale(0.839, 0.651),

						textScaled = true,
						minTextSize = 6,
						maxTextSize = 13,

						textColor3 = Color3.fromRGB(255, 255, 255),
						textXAlignment = Enum.TextXAlignment.Left,
						textYAlignment = Enum.TextYAlignment.Center,

						zIndex = 19,
					}),
				},
			}),

			InfoRow({
				name = "Exists",
				size = UDim2.fromScale(0.681, 0.17),
				position = UDim2.fromScale(0.054, 0.655),

				children = {
					Image({
						name = "ExistingImage",
						image = EXISTS_IMAGE,

						size = UDim2.fromScale(0.099, 0.553),

						zIndex = 19,
					}),

					Text({
						name = "ExistingAmount",
						text = "?",

						size = UDim2.fromScale(0.839, 0.651),

						textScaled = true,
						minTextSize = 6,
						maxTextSize = 13,

						textColor3 = Color3.fromRGB(255, 255, 255),
						textXAlignment = Enum.TextXAlignment.Left,
						textYAlignment = Enum.TextYAlignment.Center,

						zIndex = 19,
					}),
				},
			}),

			create("Frame")({
				Name = "Skill",

				Size = UDim2.fromScale(0.595, 0.148),
				Position = UDim2.fromScale(0.5, 0.882),
				AnchorPoint = Vector2.new(0.5, 0.5),

				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				ZIndex = 19,

				create("TextButton")({
					Name = "SkillButton",

					Size = UDim2.fromScale(1, 1),
					Position = UDim2.fromScale(0.5, 0.5),
					AnchorPoint = Vector2.new(0.5, 0.5),

					Text = "",
					AutoButtonColor = false,

					BackgroundColor3 = Color3.fromRGB(12, 13, 20),
					BackgroundTransparency = 0,
					BorderSizePixel = 0,
					ZIndex = 19,

					create("UICorner")({
						CornerRadius = UDim.new(0.1, 0),
					}),

					create("UIStroke")({
						Color = Color3.fromRGB(0, 0, 0),
						Thickness = 1,
						Transparency = 0.5,
					}),

					Text({
						name = "HasSkill",

						text = function()
							return getSkillText(getSelected(props))
						end,

						size = UDim2.fromScale(1, 1),
						position = UDim2.fromScale(0.5, 0.5),
						anchorPoint = Vector2.new(0.5, 0.5),

						textScaled = true,
						minTextSize = 5,
						maxTextSize = 12,

						textColor3 = Color3.fromRGB(255, 255, 255),
						textXAlignment = Enum.TextXAlignment.Center,
						textYAlignment = Enum.TextYAlignment.Center,

						zIndex = 20,
					}),
				}),
			}),
		}),
	})
end

return SideKickInfo
