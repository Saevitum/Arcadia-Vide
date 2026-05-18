#!/usr/bin/env python3
"""
Patch Arcadia-Vide Inventory V4 UI files.

What it fixes:
  1) Inventory SkinCards no longer show lock overlays.
  2) SelectedSkinInfo no longer shows/uses Owned/Locked state; Inventory items are treated as owned.
  3) Inventory equip handler no longer blocks Locked/Owned mock fields.
  4) MockInventory is normalized so all mock skins are owned/unlocked.
  5) Info UIStroke pulse is set to 3x while the divider does 1x.
  6) Tab buttons get a tweened visual-state transition instead of snapping.
  7) Default tab style is updated to the requested white-backed orange -> magenta gradient.

Run from the repo root:
    python fix_inventory_v4_ui.py

Or pass the repo path explicitly:
    python fix_inventory_v4_ui.py --repo C:\\path\\to\\Arcadia-Vide

Use --dry-run to preview changed files without writing.
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


SKIN_CARD_LUA = r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local create = Vide.create
local Text = Components.Text
local Image = Components.Image

local Tokens = Style.Tokens

type Source = SharedTypes.Source
type SkinItem = MenuTypes.SkinItem

export type SkinCardProps = {
	skin: SkinItem,
	selectedSkinId: Source,
	equippedSkinId: Source,
	layoutOrder: number?,
	zIndex: number?,
	onSelected: (skin: SkinItem) -> (),
}

local EQUIPPED_IMAGE = "rbxassetid://13415241367"
local SELECTED_IMAGE = "rbxassetid://13415286900"

local function getRarityColor(rarity: string): Color3
	return (Tokens.RarityColors :: { [string]: Color3 })[rarity] or Tokens.Colors.White
end

local function isSelected(props: SkinCardProps): boolean
	return props.selectedSkinId() == props.skin.SkinId
end

local function isEquipped(props: SkinCardProps): boolean
	return props.equippedSkinId() == props.skin.SkinId
end

local function SkinCard(props: SkinCardProps)
	local skin = props.skin
	local rarityColor = getRarityColor(skin.Rarity)
	local zIndex = props.zIndex or 24

	return create("ImageButton")({
		Name = `SkinCard_{skin.SkinId}`,
		Image = skin.ImageId,
		ImageTransparency = 0,
		ImageColor3 = Tokens.Colors.White,
		ScaleType = Enum.ScaleType.Stretch,
		AutoButtonColor = false,
		Size = UDim2.fromScale(1, 1),
		BackgroundTransparency = 1,
		BackgroundColor3 = Tokens.Colors.DarkGlass,
		BorderSizePixel = 0,
		LayoutOrder = props.layoutOrder or 0,
		ZIndex = zIndex,

		Activated = function()
			props.onSelected(skin)
		end,

		create("UICorner")({
			CornerRadius = Tokens.Corners.Small,
		}),

		create("UIStroke")({
			Thickness = 2,
			Color = function()
				if isSelected(props) then
					return Tokens.Colors.Magenta
				end

				return rarityColor
			end,
			Transparency = function()
				if isSelected(props) then
					return 0
				end

				return 0.15
			end,
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
		}),

		-- Kept hidden for future deletion/select-delete mode.
		Image({
			name = "Selected",
			image = SELECTED_IMAGE,
			size = UDim2.fromScale(0.8, 0.8),
			position = UDim2.fromScale(0.5, 0.5),
			anchorPoint = Vector2.new(0.5, 0.5),
			visible = false,
			zIndex = zIndex + 1,
		}),

		Image({
			name = "Equipped",
			image = EQUIPPED_IMAGE,
			size = UDim2.fromScale(0.339, 0.289),
			position = UDim2.fromScale(0, 0),
			anchorPoint = Vector2.new(0, 0),
			visible = function()
				return isEquipped(props)
			end,
			zIndex = zIndex + 4,
		}),

		Text({
			name = "Title",
			text = skin.Name,
			size = UDim2.fromScale(0.843, 0.173),
			position = UDim2.fromScale(0.5, 0.9),
			anchorPoint = Vector2.new(0.5, 0.5),
			fontFace = Tokens.Fonts.MichromaBoldItalic,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,
			textColor3 = Tokens.Colors.White,
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,
			stroke = {
				thickness = 2,
				color = Tokens.Colors.Black,
				transparency = 0.1,
			},
			zIndex = zIndex + 5,
		}),

		Effects.HoverUIScale({
			idleScale = 1,
			hoverScale = 1.06,
			duration = 0.12,
		}),
	})
end

return SkinCard
'''


SELECTED_SKIN_INFO_LUA = r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local SharedTypes = require(script.Parent.Parent.Parent.UITypes.SharedTypes)
local MenuTypes = require(script.Parent.Parent.Parent.UITypes.MenuTypes)
local Components = require(script.Parent.Parent.Parent.Components)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)

Vide.strict = true

local create = Vide.create
local Text = Components.Text
local Image = Components.Image
local ActionButton = Components.ActionButton

local Tokens = Style.Tokens
local Gradients = Style.Gradients

type Source = SharedTypes.Source
type InventoryTabId = MenuTypes.InventoryTabId
type SkinItem = MenuTypes.SkinItem

export type SelectedSkinInfoProps = {
	selectedTab: Source,
	selectedSkin: Source,
	equippedSkinId: Source,
	accentColor: Source,
	pulsePhase: Source,
	onEquip: ((skin: SkinItem) -> ())?,
}

local INFO_SIZE = UDim2.fromScale(0.22, 0.52)
local INFO_OPEN_POSITION = UDim2.fromScale(0.735, 0.55)
local INFO_CLOSED_POSITION = UDim2.fromScale(1.05, 0.55)

local function getSelected(props: SelectedSkinInfoProps): SkinItem?
	return props.selectedSkin()
end

local function getSelectedText(
	props: SelectedSkinInfoProps,
	selector: (SkinItem) -> string,
	fallback: string
): string
	local selected = getSelected(props)

	if selected == nil then
		return fallback
	end

	return selector(selected)
end

local function getButtonText(skin: SkinItem?, equippedSkinId: string?): string
	if skin == nil then
		return "SELECT"
	end

	if equippedSkinId == skin.SkinId then
		return "EQUIPPED"
	end

	return "EQUIP"
end

local function getStatusText(skin: SkinItem?, equippedSkinId: string?): string
	if skin == nil then
		return "Select a skin from the list."
	end

	if equippedSkinId == skin.SkinId then
		return "Currently equipped"
	end

	return "Ready to equip"
end

local function SelectedSkinInfo(props: SelectedSkinInfoProps)
	local function open(): boolean
		return props.selectedTab() == "Skins" and props.selectedSkin() ~= nil
	end

	return create("CanvasGroup")({
		Name = "SelectedSkinInfo",
		Size = INFO_SIZE,
		Position = INFO_OPEN_POSITION,
		AnchorPoint = Vector2.new(0.5, 0.5),
		Visible = false,
		GroupTransparency = 1,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		ZIndex = 23,

		Effects.SlideFadeCanvasGroup({
			open = open,
			openPosition = INFO_OPEN_POSITION,
			closedPosition = INFO_CLOSED_POSITION,
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
			Color = Tokens.Colors.White,
			Thickness = 2,
			Transparency = 0,

			create("UIGradient")({
				Color = function()
					local color = props.accentColor()
					return ColorSequence.new({
						ColorSequenceKeypoint.new(0, color),
						ColorSequenceKeypoint.new(0.5, Tokens.Colors.White),
						ColorSequenceKeypoint.new(1, color),
					})
				end,
				Rotation = 90,
				Transparency = Gradients.strokePulseTransparency(),

				Effects.PulseGradientOffset({
					phase = props.pulsePhase,
					phaseMultiplier = 3,
					minOffset = Vector2.new(0, -0.35),
					maxOffset = Vector2.new(0, 0),
				}),
			}),
		}),

		create("Frame")({
			Name = "SkinImage",
			Size = UDim2.fromScale(1, 0.5),
			Position = UDim2.fromScale(0.5, 0.25),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 24,

			Image({
				name = "SelectedSkinImage",
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
				zIndex = 24,
				gradient = {
					rotation = 90,
					transparency = NumberSequence.new({
						NumberSequenceKeypoint.new(0, 0),
						NumberSequenceKeypoint.new(0.8, 0.755),
						NumberSequenceKeypoint.new(1, 1),
					}),
				},
			}),
		}),

		Text({
			name = "Title",
			text = function()
				return getSelectedText(props, function(skin)
					return skin.Name
				end, "")
			end,
			size = UDim2.fromScale(0.926, 0.08),
			position = UDim2.fromScale(0.5, 0.55),
			anchorPoint = Vector2.new(0.5, 0.5),
			fontFace = Tokens.Fonts.MichromaBold,
			textScaled = true,
			minTextSize = 7,
			maxTextSize = 16,
			textColor3 = Tokens.Colors.White,
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,
			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.35,
			},
			zIndex = 25,
		}),

		Text({
			name = "Rarity",
			text = function()
				return getSelectedText(props, function(skin)
					return skin.Rarity
				end, "--")
			end,
			size = UDim2.fromScale(0.395, 0.05),
			position = UDim2.fromScale(0.5, 0.62),
			anchorPoint = Vector2.new(0.5, 0.5),
			textScaled = true,
			minTextSize = 6,
			maxTextSize = 14,
			textColor3 = Tokens.Colors.White,
			textXAlignment = Enum.TextXAlignment.Center,
			textYAlignment = Enum.TextYAlignment.Center,
			stroke = {
				thickness = 1,
				color = Tokens.Colors.Black,
				transparency = 0.2,
			},
			zIndex = 25,
		}),

		create("Frame")({
			Name = "SelectedSkinDetails",
			Size = UDim2.fromScale(1, 0.5),
			Position = UDim2.fromScale(0.5, 0.75),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ZIndex = 24,

			Text({
				name = "Status",
				text = function()
					return getStatusText(props.selectedSkin(), props.equippedSkinId())
				end,
				size = UDim2.fromScale(0.84, 0.12),
				position = UDim2.fromScale(0.5, 0.2),
				anchorPoint = Vector2.new(0.5, 0.5),
				fontFace = Tokens.Fonts.MichromaBold,
				textScaled = true,
				minTextSize = 6,
				maxTextSize = 12,
				textColor3 = Tokens.Colors.CyanBright,
				textXAlignment = Enum.TextXAlignment.Center,
				textYAlignment = Enum.TextYAlignment.Center,
				stroke = {
					thickness = 1,
					color = Tokens.Colors.Black,
					transparency = 0.3,
				},
				zIndex = 25,
			}),

			Text({
				name = "Description",
				text = function()
					return getSelectedText(props, function(skin)
						return skin.Description
					end, "")
				end,
				size = UDim2.fromScale(0.84, 0.26),
				position = UDim2.fromScale(0.5, 0.43),
				anchorPoint = Vector2.new(0.5, 0.5),
				fontFace = Tokens.Fonts.MichromaRegular,
				textScaled = true,
				textWrapped = true,
				minTextSize = 6,
				maxTextSize = 12,
				textColor3 = Color3.fromRGB(220, 230, 235),
				textXAlignment = Enum.TextXAlignment.Center,
				textYAlignment = Enum.TextYAlignment.Center,
				stroke = {
					thickness = 1,
					color = Tokens.Colors.Black,
					transparency = 0.35,
				},
				zIndex = 25,
			}),

			ActionButton({
				name = "EquipButton",
				text = function()
					return getButtonText(props.selectedSkin(), props.equippedSkinId())
				end,
				size = UDim2.fromScale(0.72, 0.13),
				position = UDim2.fromScale(0.5, 0.82),
				anchorPoint = Vector2.new(0.5, 0.5),
				variant = function()
					local skin = props.selectedSkin()
					if skin == nil then
						return "Disabled"
					end

					if props.equippedSkinId() == skin.SkinId then
						return "Blue"
					end

					return "Green"
				end,
				disabled = function()
					local skin = props.selectedSkin()
					return skin == nil or props.equippedSkinId() == skin.SkinId
				end,
				strokeThickness = 1.5,
				hoverScale = 1.08,
				scaleTextConstraints = true,
				zIndex = 25,
				onClick = function()
					local skin = props.selectedSkin()
					if skin == nil then
						return
					end

					if props.onEquip ~= nil then
						props.onEquip(skin)
					end
				end,
			}),
		}),
	})
end

return SelectedSkinInfo
'''


TAB_BUTTON_LUA = r'''--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Vide = require(ReplicatedStorage.Packages.vide)
local Effects = require(script.Parent.Parent.Parent.Effects)
local Style = require(script.Parent.Parent.Parent.Style)
local Types = require(script.Parent.Parent.Parent.UITypes.ComponentTypes)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action
local cleanup = Vide.cleanup
local effect = Vide.effect

type TabButtonProps = Types.TabButtonProps
type TabButtonStyle = Types.TabButtonStyle
type TabVisualStateStyle = Types.TabVisualStateStyle
type Reactive = Types.Reactive

local DEFAULT_BUTTON_STYLE: TabButtonStyle = Style.Tabs.Presets.CyberDefault.button :: TabButtonStyle

local function readReactive<T>(value: Reactive?, fallback: T): T
	if value == nil then
		return fallback
	end

	if type(value) == "function" then
		return (value :: () -> T)()
	end

	return value :: T
end

local function mergeButtonStyle(style: TabButtonStyle?): TabButtonStyle
	return Style.Tabs.merge(DEFAULT_BUTTON_STYLE, style or {}) :: TabButtonStyle
end

local function isSelected(props: TabButtonProps): boolean
	return (props.selectedTab() :: any) == (props.tab.id :: any)
end

local function isDisabled(props: TabButtonProps): boolean
	return props.tab.disabled == true
end

local function getStateStyle(
	props: TabButtonProps,
	buttonStyle: TabButtonStyle,
	hovered: Types.Source
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

type ResolvedStyle = {
	backgroundColor: Color3,
	backgroundTransparency: number,
	gradient: ColorSequence,
	gradientRotation: number,
	strokeColor: Color3,
	strokeTransparency: number,
	strokeThickness: number,
	strokeGradient: ColorSequence,
	strokeGradientRotation: number,
	textColor: Color3,
	textTransparency: number,
	glossColor: Color3,
	glossBackgroundTransparency: number,
	glossTransparency: NumberSequence,
}

local function resolveStyle(style: TabVisualStateStyle, fallback: TabVisualStateStyle?): ResolvedStyle
	local fallbackStyle = fallback or {}
	local styleAny = style :: any
	local fallbackAny = fallbackStyle :: any

	return {
		backgroundColor = style.backgroundColor or fallbackStyle.backgroundColor or Color3.fromRGB(255, 255, 255),
		backgroundTransparency = if style.backgroundTransparency ~= nil then style.backgroundTransparency elseif fallbackStyle.backgroundTransparency ~= nil then fallbackStyle.backgroundTransparency else 0,
		gradient = style.gradient or fallbackStyle.gradient or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		gradientRotation = if style.gradientRotation ~= nil then style.gradientRotation elseif fallbackStyle.gradientRotation ~= nil then fallbackStyle.gradientRotation else 0,
		strokeColor = style.strokeColor or fallbackStyle.strokeColor or Color3.fromRGB(255, 255, 255),
		strokeTransparency = if style.strokeTransparency ~= nil then style.strokeTransparency elseif fallbackStyle.strokeTransparency ~= nil then fallbackStyle.strokeTransparency else 0,
		strokeThickness = if style.strokeThickness ~= nil then style.strokeThickness elseif fallbackStyle.strokeThickness ~= nil then fallbackStyle.strokeThickness else 1,
		strokeGradient = style.strokeGradient or fallbackStyle.strokeGradient or ColorSequence.new(Color3.fromRGB(255, 255, 255)),
		strokeGradientRotation = if style.strokeGradientRotation ~= nil then style.strokeGradientRotation elseif fallbackStyle.strokeGradientRotation ~= nil then fallbackStyle.strokeGradientRotation else 0,
		textColor = style.textColor or fallbackStyle.textColor or Color3.fromRGB(255, 255, 255),
		textTransparency = if style.textTransparency ~= nil then style.textTransparency elseif fallbackStyle.textTransparency ~= nil then fallbackStyle.textTransparency else 0,
		glossColor = style.glossColor or fallbackStyle.glossColor or Color3.fromRGB(255, 255, 255),
		glossBackgroundTransparency = if styleAny.glossBackgroundTransparency ~= nil then styleAny.glossBackgroundTransparency elseif fallbackAny.glossBackgroundTransparency ~= nil then fallbackAny.glossBackgroundTransparency else 0,
		glossTransparency = style.glossTransparency or fallbackStyle.glossTransparency or NumberSequence.new({
			NumberSequenceKeypoint.new(0, 1),
			NumberSequenceKeypoint.new(0.5, 0.75),
			NumberSequenceKeypoint.new(1, 0),
		}),
	}
end

local function colorAt(sequence: ColorSequence, time: number): Color3
	local keypoints = sequence.Keypoints

	if #keypoints == 0 then
		return Color3.fromRGB(255, 255, 255)
	end

	if time <= keypoints[1].Time then
		return keypoints[1].Value
	end

	for index = 2, #keypoints do
		local previous = keypoints[index - 1]
		local current = keypoints[index]

		if time <= current.Time then
			local span = current.Time - previous.Time
			local alpha = if span <= 0 then 0 else (time - previous.Time) / span
			return previous.Value:Lerp(current.Value, math.clamp(alpha, 0, 1))
		end
	end

	return keypoints[#keypoints].Value
end

local function numberAt(sequence: NumberSequence, time: number): number
	local keypoints = sequence.Keypoints

	if #keypoints == 0 then
		return 0
	end

	if time <= keypoints[1].Time then
		return keypoints[1].Value
	end

	for index = 2, #keypoints do
		local previous = keypoints[index - 1]
		local current = keypoints[index]

		if time <= current.Time then
			local span = current.Time - previous.Time
			local alpha = if span <= 0 then 0 else (time - previous.Time) / span
			return previous.Value + ((current.Value - previous.Value) * math.clamp(alpha, 0, 1))
		end
	end

	return keypoints[#keypoints].Value
end

local function collectSequenceTimes(colorA: ColorSequence?, colorB: ColorSequence?, numberA: NumberSequence?, numberB: NumberSequence?): { number }
	local times: { number } = { 0, 1 }

	local function add(time: number)
		local clamped = math.clamp(time, 0, 1)

		for _, existing in ipairs(times) do
			if math.abs(existing - clamped) < 0.001 then
				return
			end
		end

		table.insert(times, clamped)
	end

	local function addColor(sequence: ColorSequence?)
		if sequence == nil then
			return
		end

		for _, keypoint in ipairs(sequence.Keypoints) do
			add(keypoint.Time)
		end
	end

	local function addNumber(sequence: NumberSequence?)
		if sequence == nil then
			return
		end

		for _, keypoint in ipairs(sequence.Keypoints) do
			add(keypoint.Time)
		end
	end

	addColor(colorA)
	addColor(colorB)
	addNumber(numberA)
	addNumber(numberB)
	table.sort(times)

	return times
end

local function lerpColorSequence(fromSequence: ColorSequence, toSequence: ColorSequence, alpha: number): ColorSequence
	local keypoints: { ColorSequenceKeypoint } = {}

	for _, time in ipairs(collectSequenceTimes(fromSequence, toSequence, nil, nil)) do
		table.insert(keypoints, ColorSequenceKeypoint.new(time, colorAt(fromSequence, time):Lerp(colorAt(toSequence, time), alpha)))
	end

	return ColorSequence.new(keypoints)
end

local function lerpNumberSequence(fromSequence: NumberSequence, toSequence: NumberSequence, alpha: number): NumberSequence
	local keypoints: { NumberSequenceKeypoint } = {}

	for _, time in ipairs(collectSequenceTimes(nil, nil, fromSequence, toSequence)) do
		local value = numberAt(fromSequence, time) + ((numberAt(toSequence, time) - numberAt(fromSequence, time)) * alpha)
		table.insert(keypoints, NumberSequenceKeypoint.new(time, math.clamp(value, 0, 1)))
	end

	return NumberSequence.new(keypoints)
end

local function lerpNumber(fromValue: number, toValue: number, alpha: number): number
	return fromValue + ((toValue - fromValue) * alpha)
end

local function findDirectChildOfClass(parent: Instance, className: string): Instance?
	for _, child in ipairs(parent:GetChildren()) do
		if child.ClassName == className then
			return child
		end
	end

	return nil
end

local function captureStyle(button: TextButton, fallback: ResolvedStyle): ResolvedStyle
	local gradient = findDirectChildOfClass(button, "UIGradient") :: UIGradient?
	local stroke = findDirectChildOfClass(button, "UIStroke") :: UIStroke?
	local strokeGradient: UIGradient? = if stroke ~= nil then stroke:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local gloss = button:FindFirstChild("Gloss") :: Frame?
	local glossGradient: UIGradient? = if gloss ~= nil then gloss:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local label = button:FindFirstChild("Label") :: TextLabel?

	return {
		backgroundColor = button.BackgroundColor3,
		backgroundTransparency = button.BackgroundTransparency,
		gradient = if gradient ~= nil then gradient.Color else fallback.gradient,
		gradientRotation = if gradient ~= nil then gradient.Rotation else fallback.gradientRotation,
		strokeColor = if stroke ~= nil then stroke.Color else fallback.strokeColor,
		strokeTransparency = if stroke ~= nil then stroke.Transparency else fallback.strokeTransparency,
		strokeThickness = if stroke ~= nil then stroke.Thickness else fallback.strokeThickness,
		strokeGradient = if strokeGradient ~= nil then strokeGradient.Color else fallback.strokeGradient,
		strokeGradientRotation = if strokeGradient ~= nil then strokeGradient.Rotation else fallback.strokeGradientRotation,
		textColor = if label ~= nil then label.TextColor3 else fallback.textColor,
		textTransparency = if label ~= nil then label.TextTransparency else fallback.textTransparency,
		glossColor = if gloss ~= nil then gloss.BackgroundColor3 else fallback.glossColor,
		glossBackgroundTransparency = if gloss ~= nil then gloss.BackgroundTransparency else fallback.glossBackgroundTransparency,
		glossTransparency = if glossGradient ~= nil then glossGradient.Transparency else fallback.glossTransparency,
	}
end

local function applyStyle(button: TextButton, fromStyle: ResolvedStyle, toStyle: ResolvedStyle, alpha: number)
	local gradient = findDirectChildOfClass(button, "UIGradient") :: UIGradient?
	local stroke = findDirectChildOfClass(button, "UIStroke") :: UIStroke?
	local strokeGradient: UIGradient? = if stroke ~= nil then stroke:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local gloss = button:FindFirstChild("Gloss") :: Frame?
	local glossGradient: UIGradient? = if gloss ~= nil then gloss:FindFirstChildOfClass("UIGradient") :: UIGradient? else nil
	local label = button:FindFirstChild("Label") :: TextLabel?

	button.BackgroundColor3 = fromStyle.backgroundColor:Lerp(toStyle.backgroundColor, alpha)
	button.BackgroundTransparency = lerpNumber(fromStyle.backgroundTransparency, toStyle.backgroundTransparency, alpha)

	if gradient ~= nil then
		gradient.Color = lerpColorSequence(fromStyle.gradient, toStyle.gradient, alpha)
		gradient.Rotation = lerpNumber(fromStyle.gradientRotation, toStyle.gradientRotation, alpha)
	end

	if stroke ~= nil then
		stroke.Color = fromStyle.strokeColor:Lerp(toStyle.strokeColor, alpha)
		stroke.Transparency = lerpNumber(fromStyle.strokeTransparency, toStyle.strokeTransparency, alpha)
		stroke.Thickness = lerpNumber(fromStyle.strokeThickness, toStyle.strokeThickness, alpha)
	end

	if strokeGradient ~= nil then
		strokeGradient.Color = lerpColorSequence(fromStyle.strokeGradient, toStyle.strokeGradient, alpha)
		strokeGradient.Rotation = lerpNumber(fromStyle.strokeGradientRotation, toStyle.strokeGradientRotation, alpha)
	end

	if gloss ~= nil then
		gloss.BackgroundColor3 = fromStyle.glossColor:Lerp(toStyle.glossColor, alpha)
		gloss.BackgroundTransparency = lerpNumber(fromStyle.glossBackgroundTransparency, toStyle.glossBackgroundTransparency, alpha)
	end

	if glossGradient ~= nil then
		glossGradient.Transparency = lerpNumberSequence(fromStyle.glossTransparency, toStyle.glossTransparency, alpha)
	end

	if label ~= nil then
		label.TextColor3 = fromStyle.textColor:Lerp(toStyle.textColor, alpha)
		label.TextTransparency = lerpNumber(fromStyle.textTransparency, toStyle.textTransparency, alpha)
	end
end

local function AnimateTabStyle(options: {
	getStyle: () -> TabVisualStateStyle,
	fallbackStyle: TabVisualStateStyle?,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
})
	local duration = options.duration or 0.18
	local easingStyle = options.easingStyle or Enum.EasingStyle.Sine
	local easingDirection = options.easingDirection or Enum.EasingDirection.InOut

	return action(function(instance: Instance)
		if not instance:IsA("TextButton") then
			return
		end

		local button = instance :: TextButton
		local activeTween: Tween? = nil
		local activeDriver: NumberValue? = nil
		local activeConnection: RBXScriptConnection? = nil
		local firstRun = true

		local function cancelActiveTween()
			if activeTween ~= nil then
				activeTween:Cancel()
				activeTween = nil
			end

			if activeConnection ~= nil then
				activeConnection:Disconnect()
				activeConnection = nil
			end

			if activeDriver ~= nil then
				activeDriver:Destroy()
				activeDriver = nil
			end
		end

		effect(function()
			local targetStyle = resolveStyle(options.getStyle(), options.fallbackStyle)

			if firstRun then
				firstRun = false
				applyStyle(button, targetStyle, targetStyle, 1)
				return
			end

			cancelActiveTween()

			local startStyle = captureStyle(button, targetStyle)
			local driver = Instance.new("NumberValue")
			driver.Name = "TabStyleTweenDriver"
			driver.Value = 0

			activeDriver = driver
			activeConnection = driver:GetPropertyChangedSignal("Value"):Connect(function()
				applyStyle(button, startStyle, targetStyle, math.clamp(driver.Value, 0, 1))
			end)

			local tween = TweenService:Create(driver, TweenInfo.new(duration, easingStyle, easingDirection), {
				Value = 1,
			})

			activeTween = tween
			tween:Play()
		end)

		cleanup(function()
			cancelActiveTween()
		end)
	end)
end

local function TabButton(props: TabButtonProps)
	local hovered = source(false)
	local buttonStyle = mergeButtonStyle(props.style)
	local fallbackStyle = buttonStyle.default or DEFAULT_BUTTON_STYLE.default or {}

	local function currentStyle(): TabVisualStateStyle
		return getStateStyle(props, buttonStyle, hovered)
	end

	local initialStyle = resolveStyle(currentStyle(), fallbackStyle)

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
			return readReactive(props.size, UDim2.fromScale(1, 1))
		end,
		Position = function()
			return readReactive(props.position, UDim2.fromScale(0, 0))
		end,
		AnchorPoint = function()
			return readReactive(props.anchorPoint, Vector2.new(0, 0))
		end,
		Visible = function()
			return readReactive(props.visible, true)
		end,
		LayoutOrder = props.tab.layoutOrder or 0,
		ZIndex = function()
			return readReactive(props.zIndex, 1)
		end,
		Text = "",
		AutoButtonColor = false,
		ClipsDescendants = true,
		BorderSizePixel = 0,
		BackgroundColor3 = initialStyle.backgroundColor,
		BackgroundTransparency = initialStyle.backgroundTransparency,

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

		AnimateTabStyle({
			getStyle = currentStyle,
			fallbackStyle = fallbackStyle,
			duration = (buttonStyle :: any).transitionDuration or Style.Tokens.Timing.Default,
			easingStyle = (buttonStyle :: any).transitionEasingStyle or Enum.EasingStyle.Sine,
			easingDirection = (buttonStyle :: any).transitionEasingDirection or Enum.EasingDirection.InOut,
		}),

		create("UICorner")({
			CornerRadius = buttonStyle.cornerRadius or UDim.new(0.16, 0),
		}),

		create("UIGradient")({
			Color = initialStyle.gradient,
			Rotation = initialStyle.gradientRotation,
		}),

		create("UIStroke")({
			ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
			Color = initialStyle.strokeColor,
			Transparency = initialStyle.strokeTransparency,
			Thickness = initialStyle.strokeThickness,

			create("UIGradient")({
				Color = initialStyle.strokeGradient,
				Rotation = initialStyle.strokeGradientRotation,
			}),
		}),

		create("Frame")({
			Name = "Gloss",
			Size = UDim2.fromScale(1, 1),
			Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundColor3 = initialStyle.glossColor,
			BackgroundTransparency = initialStyle.glossBackgroundTransparency,
			BorderSizePixel = 0,
			ZIndex = function()
				return readReactive(props.zIndex, 1) + 1
			end,

			create("UICorner")({
				CornerRadius = buttonStyle.cornerRadius or UDim.new(0.16, 0),
			}),

			create("UIGradient")({
				Rotation = 90,
				Transparency = initialStyle.glossTransparency,
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
			FontFace = buttonStyle.fontFace or Font.new("rbxasset://fonts/families/Michroma.json", Enum.FontWeight.Bold, Enum.FontStyle.Italic),
			TextColor3 = initialStyle.textColor,
			TextTransparency = initialStyle.textTransparency,
			ZIndex = function()
				return readReactive(props.zIndex, 1) + 2
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
'''


TABS_TYPES_LUA = r'''--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Source = SharedTypes.Source
export type Reactive = SharedTypes.Reactive

export type TabDefinition = {
	id: any,
	label: string,
	layoutOrder: number?,
	disabled: boolean?,
	hasAlert: boolean?,
}

export type TabPadding = {
	top: UDim?,
	bottom: UDim?,
	left: UDim?,
	right: UDim?,
}

export type TabVisualStateStyle = {
	backgroundColor: Color3?,
	backgroundTransparency: number?,
	gradient: ColorSequence?,
	gradientRotation: number?,
	strokeColor: Color3?,
	strokeTransparency: number?,
	strokeThickness: number?,
	strokeGradient: ColorSequence?,
	strokeGradientRotation: number?,
	textColor: Color3?,
	textTransparency: number?,
	glossColor: Color3?,
	glossBackgroundTransparency: number?,
	glossTransparency: NumberSequence?,
}

export type TabButtonStyle = {
	cornerRadius: UDim?,
	fontFace: Font?,
	minTextSize: number?,
	maxTextSize: number?,
	hoverScale: number?,
	hoverDuration: number?,
	transitionDuration: number?,
	transitionEasingStyle: Enum.EasingStyle?,
	transitionEasingDirection: Enum.EasingDirection?,
	textStrokeColor: Color3?,
	textStrokeTransparency: number?,
	textStrokeThickness: number?,
	default: TabVisualStateStyle?,
	hover: TabVisualStateStyle?,
	selected: TabVisualStateStyle?,
	disabled: TabVisualStateStyle?,
}

export type TabStripStyle = {
	backgroundColor: Color3?,
	backgroundTransparency: number?,
	cellSize: UDim2?,
	cellPadding: UDim2?,
	fillDirectionMaxCells: number?,
	horizontalAlignment: Enum.HorizontalAlignment?,
	verticalAlignment: Enum.VerticalAlignment?,
	padding: TabPadding?,
	button: TabButtonStyle?,
}

export type TabButtonProps = {
	tab: TabDefinition,
	selectedTab: Source,
	style: TabButtonStyle?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	onTabSelected: ((any) -> ())?,
}

export type TabStripProps = {
	tabs: { TabDefinition },
	selectedTab: Source,
	style: TabStripStyle?,
	name: string?,
	size: Reactive?,
	position: Reactive?,
	anchorPoint: Reactive?,
	visible: Reactive?,
	zIndex: Reactive?,
	cellSize: Reactive?,
	cellPadding: Reactive?,
	fillDirectionMaxCells: Reactive?,
	onTabSelected: ((any) -> ())?,
}

return {}
'''


TABS_STYLE_LUA = r'''--!strict

local Merge = require(script.Parent.Merge)
local Tokens = require(script.Parent.Tokens)
local Gradients = require(script.Parent.Gradients)
local Types = require(script.Parent.Parent.UITypes.ComponentTypes)

type TabStripStyle = Types.TabStripStyle

local Tabs = {}

Tabs.Presets = {}
Tabs.Layouts = {}

function Tabs.merge(base: any, override: any?): any
	return Merge.deep(base, override)
end

local function colorSequence(points: { any }): ColorSequence
	return Gradients.colorSequence(points :: any)
end

local function orangeMagentaGradient(): ColorSequence
	return colorSequence({
		{ time = 0, color = Color3.fromRGB(255, 179, 0) },
		{ time = 1, color = Color3.fromRGB(255, 0, 144) },
	})
end

local function softPinkStrokeGradient(): ColorSequence
	return colorSequence({
		{ time = 0, color = Color3.fromRGB(255, 208, 255) },
		{ time = 0.5, color = Tokens.Colors.White },
		{ time = 1, color = Color3.fromRGB(255, 208, 255) },
	})
end

local function darkInactiveGradient(): ColorSequence
	return colorSequence({
		{ time = 0, color = Color3.fromRGB(98, 98, 98) },
		{ time = 0.71, color = Color3.fromRGB(66, 66, 57) },
		{ time = 1, color = Color3.fromRGB(25, 25, 25) },
	})
end

local defaultTabVisual = {
	backgroundColor = Tokens.Colors.White,
	backgroundTransparency = 0,
	gradient = orangeMagentaGradient(),
	gradientRotation = 0,
	strokeColor = Tokens.Colors.White,
	strokeTransparency = 0.08,
	strokeThickness = 1,
	strokeGradient = softPinkStrokeGradient(),
	strokeGradientRotation = 0,
	textColor = Tokens.Colors.White,
	textTransparency = 0,
	glossColor = Tokens.Colors.White,
	glossBackgroundTransparency = 0,
	glossTransparency = Gradients.glossTransparency(),
}

Tabs.Presets.CyberDefault = {
	backgroundColor = Tokens.Colors.Black,
	backgroundTransparency = 1,
	cellSize = UDim2.fromScale(0.18, 0.42),
	cellPadding = UDim2.fromScale(0.025, 0.12),
	fillDirectionMaxCells = 5,
	horizontalAlignment = Enum.HorizontalAlignment.Center,
	verticalAlignment = Enum.VerticalAlignment.Center,
	padding = {
		top = UDim.new(0, 0),
		bottom = UDim.new(0, 0),
		left = UDim.new(0, 0),
		right = UDim.new(0, 0),
	},
	button = {
		cornerRadius = Tokens.Corners.Large,
		fontFace = Tokens.Fonts.MichromaBoldItalic,
		minTextSize = 7,
		maxTextSize = 17,
		hoverScale = 1,
		hoverDuration = Tokens.Timing.Hover,
		transitionDuration = Tokens.Timing.Default,
		transitionEasingStyle = Enum.EasingStyle.Sine,
		transitionEasingDirection = Enum.EasingDirection.InOut,
		textStrokeColor = Tokens.Colors.Black,
		textStrokeTransparency = 0.55,
		textStrokeThickness = 1,

		default = defaultTabVisual,
		hover = Tabs.merge(defaultTabVisual, {
			strokeTransparency = 0,
			textColor = Tokens.Colors.White,
		}) :: Types.TabVisualStateStyle,
		selected = Tabs.merge(defaultTabVisual, {
			strokeTransparency = 0,
			textColor = Tokens.Colors.White,
		}) :: Types.TabVisualStateStyle,
		disabled = {
			backgroundColor = Tokens.Colors.White,
			backgroundTransparency = 0,
			gradient = Gradients.claimedGray(),
			gradientRotation = 90,
			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0.18,
			strokeThickness = 1,
			strokeGradient = softPinkStrokeGradient(),
			strokeGradientRotation = 0,
			textColor = Tokens.Colors.Gray300,
			textTransparency = 0.35,
			glossColor = Tokens.Colors.White,
			glossBackgroundTransparency = 0,
			glossTransparency = Gradients.glossTransparency(),
		},
	},
} :: TabStripStyle

Tabs.Presets.CyberCompact = Tabs.merge(Tabs.Presets.CyberDefault, {
	cellSize = UDim2.fromScale(0.18, 0.36),
	cellPadding = UDim2.fromScale(0.02, 0.08),
	button = {
		cornerRadius = Tokens.Corners.Medium,
		minTextSize = 7,
		maxTextSize = 15,
	},
}) :: TabStripStyle

Tabs.Presets.CyberThreeTabs = Tabs.merge(Tabs.Presets.CyberDefault, {
	cellSize = UDim2.fromScale(0.3, 0.7),
	cellPadding = UDim2.fromScale(0.035, 0),
	fillDirectionMaxCells = 3,
}) :: TabStripStyle

Tabs.Layouts.ThreeTop = {
	size = UDim2.fromScale(0.42, 0.08),
	position = UDim2.fromScale(0.5, 0.275),
	anchorPoint = Vector2.new(0.5, 0.5),
	cellSize = UDim2.fromScale(0.3, 0.7),
	cellPadding = UDim2.fromScale(0.035, 0),
	fillDirectionMaxCells = 3,
}

Tabs.Layouts.FiveByTwo = {
	size = UDim2.fromScale(0.74, 0.17),
	position = UDim2.fromScale(0.5, 0.305),
	anchorPoint = Vector2.new(0.5, 0.5),
	cellSize = UDim2.fromScale(0.16, 0.25),
	cellPadding = UDim2.fromScale(0.035, 0.12),
	fillDirectionMaxCells = 5,
}

Tabs.Presets.SettingsPink = Tabs.merge(Tabs.Presets.CyberDefault, {
	cellSize = UDim2.fromScale(0.26, 0.76),
	cellPadding = UDim2.fromScale(0.035, 0),
	fillDirectionMaxCells = 3,
	button = {
		cornerRadius = UDim.new(0.22, 0),
		fontFace = Tokens.Fonts.MichromaBoldItalic,
		minTextSize = 7,
		maxTextSize = 18,
		hoverScale = 1.2,
		hoverDuration = 0.12,
		transitionDuration = Tokens.Timing.Default,
		transitionEasingStyle = Enum.EasingStyle.Sine,
		transitionEasingDirection = Enum.EasingDirection.InOut,
		textStrokeColor = Tokens.Colors.Black,
		textStrokeTransparency = 0.65,
		textStrokeThickness = 1,

		default = {
			backgroundColor = Tokens.Colors.White,
			backgroundTransparency = 0,
			gradient = darkInactiveGradient(),
			gradientRotation = 0,
			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0.18,
			strokeThickness = 1,
			strokeGradient = colorSequence({
				{ time = 0, color = Color3.fromRGB(74, 168, 255) },
				{ time = 1, color = Color3.fromRGB(30, 30, 30) },
			}),
			strokeGradientRotation = 0,
			textColor = Color3.fromRGB(190, 205, 220),
			textTransparency = 0,
			glossColor = Tokens.Colors.Black,
			glossBackgroundTransparency = 0.5,
			glossTransparency = Gradients.glossTransparency(),
		},
		hover = {
			backgroundColor = Tokens.Colors.White,
			backgroundTransparency = 0,
			gradient = darkInactiveGradient(),
			gradientRotation = 0,
			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0.08,
			strokeThickness = 1,
			strokeGradient = colorSequence({
				{ time = 0, color = Color3.fromRGB(74, 168, 255) },
				{ time = 1, color = Color3.fromRGB(30, 30, 30) },
			}),
			strokeGradientRotation = 0,
			textColor = Color3.fromRGB(215, 230, 245),
			textTransparency = 0,
			glossColor = Tokens.Colors.Black,
			glossBackgroundTransparency = 0.5,
			glossTransparency = Gradients.glossTransparency(),
		},
		selected = {
			backgroundColor = Tokens.Colors.White,
			backgroundTransparency = 0,
			gradient = colorSequence({
				{ time = 0, color = Color3.fromRGB(255, 0, 123) },
				{ time = 0.71, color = Color3.fromRGB(220, 0, 106) },
				{ time = 1, color = Color3.fromRGB(134, 0, 65) },
			}),
			gradientRotation = 0,
			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0,
			strokeThickness = 2,
			strokeGradient = colorSequence({
				{ time = 0, color = Color3.fromRGB(255, 0, 123) },
				{ time = 1, color = Color3.fromRGB(238, 0, 255) },
			}),
			strokeGradientRotation = 0,
			textColor = Tokens.Colors.White,
			textTransparency = 0,
			glossColor = Tokens.Colors.Black,
			glossBackgroundTransparency = 0.5,
			glossTransparency = Gradients.glossTransparency(),
		},
		disabled = {
			backgroundColor = Tokens.Colors.White,
			backgroundTransparency = 0,
			gradient = darkInactiveGradient(),
			gradientRotation = 0,
			strokeColor = Tokens.Colors.White,
			strokeTransparency = 0.18,
			strokeThickness = 1,
			strokeGradient = colorSequence({
				{ time = 0, color = Color3.fromRGB(74, 168, 255) },
				{ time = 1, color = Color3.fromRGB(30, 30, 30) },
			}),
			strokeGradientRotation = 0,
			textColor = Color3.fromRGB(190, 205, 220),
			textTransparency = 0.35,
			glossColor = Tokens.Colors.Black,
			glossBackgroundTransparency = 0.5,
			glossTransparency = Gradients.glossTransparency(),
		},
	},
}) :: TabStripStyle

Tabs.Layouts.SettingsThree = {
	size = UDim2.fromScale(0.62, 0.06),
	position = UDim2.fromScale(0.5, 0.25),
	anchorPoint = Vector2.new(0.5, 0.5),
	cellSize = UDim2.fromScale(0.26, 0.76),
	cellPadding = UDim2.fromScale(0.035, 0),
	fillDirectionMaxCells = 3,
}

return Tabs
'''


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


class Patcher:
    def __init__(self, repo: Path, dry_run: bool = False, backup: bool = True) -> None:
        self.repo = repo
        self.dry_run = dry_run
        self.backup = backup
        self.changed: list[str] = []
        self.skipped: list[str] = []
        self.backup_dir: Path | None = None

    def rel(self, rel_path: str) -> Path:
        return self.repo / rel_path

    def ensure_repo(self) -> None:
        required = [
            "default.project.json",
            "src/client/UI/UIManager/init.lua",
            "src/client/UI/UIManager/Menus/Inventory/init.lua",
        ]
        missing = [path for path in required if not self.rel(path).exists()]
        if missing:
            raise SystemExit(
                "This does not look like the Arcadia-Vide repo root. Missing:\n  - "
                + "\n  - ".join(missing)
            )

    def make_backup_dir(self) -> Path:
        if self.backup_dir is None:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.backup_dir = self.repo / ".patch_backups" / f"fix_inventory_v4_ui_{stamp}"
            if not self.dry_run:
                self.backup_dir.mkdir(parents=True, exist_ok=True)
        return self.backup_dir

    def backup_file(self, path: Path) -> None:
        if not self.backup or self.dry_run:
            return

        backup_root = self.make_backup_dir()
        target = backup_root / path.relative_to(self.repo)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    def write_file(self, rel_path: str, content: str, reason: str) -> None:
        path = self.rel(rel_path)
        if not path.exists():
            self.skipped.append(f"{rel_path} (missing)")
            return

        old = normalize_newlines(path.read_text(encoding="utf-8"))
        new = normalize_newlines(content).rstrip() + "\n"

        if old == new:
            self.skipped.append(f"{rel_path} (already up to date)")
            return

        print(f"\n--- {rel_path}: {reason}")
        if self.dry_run:
            diff = difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            )
            for line in list(diff)[:220]:
                print(line)
            if len(list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm=""))) > 220:
                print("... diff truncated ...")
        else:
            self.backup_file(path)
            path.write_text(new, encoding="utf-8")

        self.changed.append(rel_path)

    def replace_text(self, rel_path: str, replacements: list[tuple[str, str]], reason: str) -> None:
        path = self.rel(rel_path)
        if not path.exists():
            self.skipped.append(f"{rel_path} (missing)")
            return

        old = normalize_newlines(path.read_text(encoding="utf-8"))
        new = old
        applied = 0

        for needle, replacement in replacements:
            if needle in new:
                new = new.replace(needle, replacement)
                applied += 1

        if new == old:
            self.skipped.append(f"{rel_path} (no matching text for {reason})")
            return

        print(f"\n--- {rel_path}: {reason} ({applied} replacements)")
        if self.dry_run:
            diff = difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            )
            for line in list(diff)[:220]:
                print(line)
        else:
            self.backup_file(path)
            path.write_text(new, encoding="utf-8")

        self.changed.append(rel_path)

    def regex_replace(self, rel_path: str, substitutions: list[tuple[str, str]], reason: str) -> None:
        path = self.rel(rel_path)
        if not path.exists():
            self.skipped.append(f"{rel_path} (missing)")
            return

        old = normalize_newlines(path.read_text(encoding="utf-8"))
        new = old
        total = 0

        for pattern, replacement in substitutions:
            new, count = re.subn(pattern, replacement, new, flags=re.DOTALL)
            total += count

        if new == old:
            self.skipped.append(f"{rel_path} (no regex match for {reason})")
            return

        print(f"\n--- {rel_path}: {reason} ({total} replacements)")
        if self.dry_run:
            diff = difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            )
            for line in list(diff)[:220]:
                print(line)
        else:
            self.backup_file(path)
            path.write_text(new, encoding="utf-8")

        self.changed.append(rel_path)

    def patch(self) -> None:
        self.ensure_repo()

        # Feature files: safer to overwrite with readable canonical versions.
        self.write_file(
            "src/client/UI/UIManager/Menus/Inventory/SkinCard.lua",
            SKIN_CARD_LUA,
            "remove lock overlay and use centralized rarity colors",
        )
        self.write_file(
            "src/client/UI/UIManager/Menus/Inventory/SelectedSkinInfo.lua",
            SELECTED_SKIN_INFO_LUA,
            "remove owned/locked UI logic and set info pulse to 3x",
        )

        # Inventory handler: Inventory contains owned skins, so equip should not check mock Locked/Owned fields.
        self.regex_replace(
            "src/client/UI/UIManager/Menus/Inventory/init.lua",
            [
                (
                    r"local function equipSkin\(skin: SkinItem\)\s+if skin\.Locked or not skin\.Owned then\s+return\s+end\s+equippedSkinId\(skin\.SkinId\)\s+end",
                    "local function equipSkin(skin: SkinItem) equippedSkinId(skin.SkinId) end",
                )
            ],
            "remove owned/locked equip guard",
        )

        # Mock inventory should match the Inventory assumption: every displayed skin is owned.
        self.replace_text(
            "src/client/UI/UIManager/Menus/Inventory/MockInventory.lua",
            [
                ("Owned = false", "Owned = true"),
                ("Locked = true", "Locked = false"),
            ],
            "normalize mock skins to owned/unlocked",
        )

        # SideKick info can use the same 3x info-pulse behavior as Inventory if this synced pulse system is active.
        self.replace_text(
            "src/client/UI/UIManager/Menus/SideKicks/SideKickInfo.lua",
            [("phaseMultiplier = 1", "phaseMultiplier = 3")],
            "make info stroke pulse 3x per divider cycle",
        )

        # Smooth tab visual transitions and requested tab style.
        self.write_file(
            "src/client/UI/UIManager/Components/Tabs/TabButton.lua",
            TAB_BUTTON_LUA,
            "add tweened tab visual-state transitions",
        )
        self.write_file(
            "src/client/UI/UIManager/UITypes/ComponentTypes/TabsTypes.lua",
            TABS_TYPES_LUA,
            "add tab transition/gloss types and remove loose generic T usage",
        )
        self.write_file(
            "src/client/UI/UIManager/Style/Tabs.lua",
            TABS_STYLE_LUA,
            "set default tab gradient/stroke style to requested colors",
        )

    def report(self) -> None:
        print("\nPatch summary")
        print("=============")

        if self.changed:
            print("Changed files:")
            for item in self.changed:
                print(f"  - {item}")
        else:
            print("No files changed.")

        if self.skipped:
            print("\nSkipped/no-op files:")
            for item in self.skipped:
                print(f"  - {item}")

        if self.backup and not self.dry_run and self.backup_dir is not None:
            print(f"\nBackups saved to: {self.backup_dir}")

        print("\nNext recommended commands:")
        print("  git diff")
        print("  rojo sourcemap default.project.json -o sourcemap.json")
        print("  selene src")
        print("\nThen open Studio and verify Inventory tab switching, skin selection, and equip behavior.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Patch Arcadia-Vide Inventory V4 UI files.")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Path to Arcadia-Vide repo root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .patch_backups copies before writing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo = args.repo.expanduser().resolve()

    patcher = Patcher(repo=repo, dry_run=args.dry_run, backup=not args.no_backup)

    try:
        patcher.patch()
        patcher.report()
    except Exception as exc:  # noqa: BLE001 - command-line tool should print friendly failure.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
