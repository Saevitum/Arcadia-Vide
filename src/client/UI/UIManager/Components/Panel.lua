--!strict

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)
local Types = require(script.Parent.Parent.UITypes.ComponentTypes)
local Layout = require(script.Parent.Parent.Layout)
local Effects = require(script.Parent.Parent.Effects)

local Background = require(script.Parent.Background)
local Header = require(script.Parent.Header)
local ExitButton = require(script.Parent.ExitButton)

Vide.strict = true

local create = Vide.create

type PanelProps = Types.PanelProps

local function Panel(props: PanelProps)
	local store = props.store
	local menuId = props.menuId

	local name = props.name or `{menuId}Panel`
	local title = props.title or menuId

	local size = props.size or Layout.GetMenuSize()
	local position = props.position or UDim2.fromScale(0.5, 0.5)
	local anchorPoint = props.anchorPoint or Vector2.new(0.5, 0.5)
	local zIndex = props.zIndex or 10
	local aspectRatio = props.aspectRatio or 1.63

	local content = props.content

	local function isOpen(): boolean
		return store.currentMenu() == menuId
	end

	local function closePanel()
		if store.currentMenu() == menuId then
			store.currentMenu(nil)
		end
	end

	if content ~= nil then
		return create("Frame")({
			Name = name,

			AnchorPoint = anchorPoint,
			Position = position,
			Size = size,

			BackgroundTransparency = 1,
			ZIndex = zIndex,

			create("UIAspectRatioConstraint")({
				AspectRatio = aspectRatio,
				DominantAxis = Enum.DominantAxis.Width,
			}),

			Effects.SlideMenu({
				open = isOpen,
				openPosition = props.openPosition,
				enterPosition = props.enterPosition,
				exitPosition = props.exitPosition,
				duration = props.slideDuration,
			}),

			Background(),

			content,

			Header({
				text = title,
			}),

			ExitButton({
				size = props.exitButtonSize or Layout.GetExitButtonSize(),
				position = props.exitButtonPosition,
				anchorPoint = props.exitButtonAnchorPoint,

				onClick = closePanel,
			}),
		})
	end

	return create("Frame")({
		Name = name,

		AnchorPoint = anchorPoint,
		Position = position,
		Size = size,

		BackgroundTransparency = 1,
		ZIndex = zIndex,

		create("UIAspectRatioConstraint")({
			AspectRatio = aspectRatio,
			DominantAxis = Enum.DominantAxis.Width,
		}),

		Effects.SlideMenu({
			open = isOpen,
			openPosition = props.openPosition,
			enterPosition = props.enterPosition,
			exitPosition = props.exitPosition,
			duration = props.slideDuration,
		}),

		Background(),

		Header({
			text = title,
		}),

		ExitButton({
			size = props.exitButtonSize or Layout.GetExitButtonSize(),
			position = props.exitButtonPosition,
			anchorPoint = props.exitButtonAnchorPoint,

			onClick = closePanel,
		}),
	})
end

return Panel
