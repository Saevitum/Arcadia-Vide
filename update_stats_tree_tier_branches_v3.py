#!/usr/bin/env python3
# StatsTree V3: procedural tier branches.
#
# Run from the Arcadia-Vide repository root:
#   python update_stats_tree_tier_branches_v3.py --dry-run
#   python update_stats_tree_tier_branches_v3.py
#
# Targets:
#   src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua
#   src/client/UI/UIManager/Menus/StatsTree/init.lua
#
# What it changes:
# - Replaces "one hex with 0/10" with procedural 10-tier branches:
#     Skill Power I -> Skill Power II -> ... -> Skill Power X
# - Each tier costs exactly 1 point.
# - Each tier is its own hex.
# - Each stat branch grows in a straight honeycomb direction from its category hub.
# - At any point each branch shows:
#     Blue owned tiers
#     Gray known/clickable next tier
#     Gray ? one future tier
#     deeper future tiers hidden
# - MAX_TIER is a single constant in StatsTreeData.lua, so later you can change it
#   from 10 to another number and all branches generate automatically.
#
# Backup:
#   .patch_backups/update_stats_tree_tier_branches_v3/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DATA_PATH = Path("src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua")
INIT_PATH = Path("src/client/UI/UIManager/Menus/StatsTree/init.lua")
ASSETS_PATH = Path("src/client/UI/UIManager/Menus/StatsTree/StatsTreeAssets.lua")


DATA_SOURCE = '''--!strict

export type NodeKind = "Group" | "Stat"

export type NodeDefinition = {
\tid: string,
\tkind: NodeKind,
\tgroupId: string,

\ttitle: string,
\tsubtitle: string?,
\teffectShort: string?,
\tdescription: string?,

\tposition: Vector2,

\t-- Tier branch metadata. Stat nodes are generated from BranchDefinition.
\tbranchId: string?,
\ttier: number?,
\tmaxTier: number?,
}

type BranchDefinition = {
\tgroupId: string,
\tbranchId: string,

\ttitle: string,
\tsubtitle: string?,
\teffectShort: string,
\tdescription: string,

\torigin: Vector2,
\tdirection: Vector2,
\tmaxTier: number?,
}

-- Change this later if the stat cap changes.
local MAX_TIER = 10

-- Full-step honeycomb spacing for the current 148x148 rendered hex assets.
-- These are the same offsets that make the 3 root category hubs line up correctly.
local HEX_DX = 118
local HEX_DY = 68

local ROMAN: { [number]: string } = {
\t[1] = "I",
\t[2] = "II",
\t[3] = "III",
\t[4] = "IV",
\t[5] = "V",
\t[6] = "VI",
\t[7] = "VII",
\t[8] = "VIII",
\t[9] = "IX",
\t[10] = "X",
}

local function roman(value: number): string
\treturn ROMAN[value] or tostring(value)
end

local function P(origin: Vector2, x: number, y: number): Vector2
\treturn origin + Vector2.new(x * HEX_DX, y * HEX_DY)
end

local function step(origin: Vector2, direction: Vector2, tier: number): Vector2
\treturn P(origin, direction.X * tier, direction.Y * tier)
end

-- Root category hubs:
--          Economy
--     Skills      Stamina
local ECONOMY = Vector2.new(0, -HEX_DY)
local SKILLS = Vector2.new(-HEX_DX, 0)
local STAMINA = Vector2.new(HEX_DX, 0)

local nodes: { NodeDefinition } = {
\t{
\t\tid = "EconomyOpen",
\t\tkind = "Group",
\t\tgroupId = "Economy",
\t\ttitle = "Economy",
\t\tsubtitle = "Open",
\t\tdescription = "Open the Economy tree.",
\t\tposition = ECONOMY,
\t},
\t{
\t\tid = "SkillsOpen",
\t\tkind = "Group",
\t\tgroupId = "Skills",
\t\ttitle = "Skills",
\t\tsubtitle = "Open",
\t\tdescription = "Open the Skills tree.",
\t\tposition = SKILLS,
\t},
\t{
\t\tid = "StaminaOpen",
\t\tkind = "Group",
\t\tgroupId = "Stamina",
\t\ttitle = "Stamina",
\t\tsubtitle = "Open",
\t\tdescription = "Open the Stamina tree.",
\t\tposition = STAMINA,
\t},
}

local branches: { BranchDefinition } = {
\t-- Economy branches.
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "MoneyBoost",
\t\ttitle = "Money",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Money per tier.",
\t\torigin = ECONOMY,
\t\tdirection = Vector2.new(-2, 0),
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "ExpBoost",
\t\ttitle = "EXP",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% EXP per tier.",
\t\torigin = ECONOMY,
\t\tdirection = Vector2.new(-1, -1),
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "PointsBoost",
\t\ttitle = "Points",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Points per tier.",
\t\torigin = ECONOMY,
\t\tdirection = Vector2.new(1, -1),
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "GemsBoost",
\t\ttitle = "Gems",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Gems per tier.",
\t\torigin = ECONOMY,
\t\tdirection = Vector2.new(-1, 1),
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "Lucky",
\t\ttitle = "Lucky",
\t\teffectShort = "+2%",
\t\tdescription = "+2% Luck per tier.",
\t\torigin = ECONOMY,
\t\tdirection = Vector2.new(1, 1),
\t},

\t-- Skills branches.
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillHaste",
\t\ttitle = "Skill",
\t\tsubtitle = "Haste",
\t\teffectShort = "-4%",
\t\tdescription = "-4% Cooldown per tier.",
\t\torigin = SKILLS,
\t\tdirection = Vector2.new(-2, 0),
\t},
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillPower",
\t\ttitle = "Skill",
\t\tsubtitle = "Power",
\t\teffectShort = "+4%",
\t\tdescription = "+4% Power per tier.",
\t\torigin = SKILLS,
\t\tdirection = Vector2.new(-1, -1),
\t},
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillDuration",
\t\ttitle = "Skill",
\t\tsubtitle = "Duration",
\t\teffectShort = "+0.5s",
\t\tdescription = "+0.5 seconds Duration per tier.",
\t\torigin = SKILLS,
\t\tdirection = Vector2.new(-1, 1),
\t},

\t-- Stamina branches.
\t{
\t\tgroupId = "Stamina",
\t\tbranchId = "MaxStamina",
\t\ttitle = "Max",
\t\tsubtitle = "Stamina",
\t\teffectShort = "+10",
\t\tdescription = "+10 Max Stamina per tier.",
\t\torigin = STAMINA,
\t\tdirection = Vector2.new(2, 0),
\t},
\t{
\t\tgroupId = "Stamina",
\t\tbranchId = "StaminaRecovery",
\t\ttitle = "Stamina",
\t\tsubtitle = "Regen",
\t\teffectShort = "+1/s",
\t\tdescription = "+1/sec Regen per tier.",
\t\torigin = STAMINA,
\t\tdirection = Vector2.new(1, 1),
\t},
}

for _, branch in ipairs(branches) do
\tlocal maxTier = branch.maxTier or MAX_TIER

\tfor tier = 1, maxTier do
\t\tlocal tierRoman = roman(tier)

\t\ttable.insert(nodes, {
\t\t\tid = branch.branchId .. "_" .. tostring(tier),
\t\t\tkind = "Stat",
\t\t\tgroupId = branch.groupId,
\t\t\ttitle = branch.title,
\t\t\tsubtitle = if branch.subtitle ~= nil then branch.subtitle .. " " .. tierRoman else tierRoman,
\t\t\teffectShort = branch.effectShort,
\t\t\tdescription = branch.description,
\t\t\tposition = step(branch.origin, branch.direction, tier),
\t\t\tbranchId = branch.branchId,
\t\t\ttier = tier,
\t\t\tmaxTier = maxTier,
\t\t})
\tend
end

return {
\tnodes = nodes,
\tmaxTier = MAX_TIER,
}
'''


INIT_SOURCE = '''--!strict

local ContextActionService = game:GetService("ContextActionService")
local UserInputService = game:GetService("UserInputService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Vide = require(ReplicatedStorage.Packages.vide)

local Assets = require(script.StatsTreeAssets)
local Data = require(script.StatsTreeData)

Vide.strict = true

local create = Vide.create
local source = Vide.source
local action = Vide.action
local cleanup = Vide.cleanup

type Source<T> = (() -> T) & ((T) -> ())

type NodeKind = "Group" | "Stat"

type NodeDefinition = {
\tid: string,
\tkind: NodeKind,
\tgroupId: string,

\ttitle: string,
\tsubtitle: string?,
\teffectShort: string?,
\tdescription: string?,

\tposition: Vector2,

\tbranchId: string?,
\ttier: number?,
\tmaxTier: number?,
}

export type StatsTreeMenuProps = {
\tstore: any?,
\tvisible: (() -> boolean)?,
}

local NODES: { NodeDefinition } = Data.nodes :: { NodeDefinition }

local CANVAS_SIZE = Vector2.new(3600, 2600)
local CANVAS_CENTER = CANVAS_SIZE / 2
local NODE_SIZE = UDim2.fromOffset(148, 148)
local MIN_ZOOM = 0.45
local MAX_ZOOM = 1.8
local INITIAL_POINTS = 10
local WHEEL_ACTION_NAME = "ArcadiaStatsTreeSinkMouseWheel"

local function getLevel(levels: { [string]: number }, nodeId: string): number
\treturn levels[nodeId] or 0
end

local function getPreviousTierId(node: NodeDefinition): string?
\tif node.branchId == nil or node.tier == nil or node.tier <= 1 then
\t\treturn nil
\tend

\treturn node.branchId .. "_" .. tostring(node.tier - 1)
end

local function getOwnedTierCount(branchId: string, levels: { [string]: number }): number
\tlocal count = 0

\tfor _, node in ipairs(NODES) do
\t\tif node.kind == "Stat" and node.branchId == branchId and node.tier ~= nil then
\t\t\tif getLevel(levels, node.id) > 0 then
\t\t\t\tcount += 1
\t\t\tend
\t\tend
\tend

\treturn count
end

local function isKnown(node: NodeDefinition, levels: { [string]: number }): boolean
\tif node.kind == "Group" then
\t\treturn true
\tend

\tif node.tier == nil then
\t\treturn true
\tend

\tif node.tier == 1 then
\t\treturn true
\tend

\tlocal previousTierId = getPreviousTierId(node)

\tif previousTierId == nil then
\t\treturn true
\tend

\treturn getLevel(levels, previousTierId) > 0
end

local function isNodeVisible(node: NodeDefinition, activeGroup: string?, levels: { [string]: number }): boolean
\tif node.kind == "Group" then
\t\treturn activeGroup == nil or activeGroup == node.groupId
\tend

\tif activeGroup ~= node.groupId then
\t\treturn false
\tend

\tif node.branchId == nil or node.tier == nil then
\t\treturn true
\tend

\t-- Show owned tiers, the next known tier, and one mystery future tier.
\t-- Example:
\t--   owned I      -> Blue
\t--   next II      -> Gray known/clickable
\t--   future III   -> Gray ?
\t--   IV+          -> hidden
\tlocal ownedCount = getOwnedTierCount(node.branchId, levels)

\treturn node.tier <= ownedCount + 2
end

local function getNodeImage(
\tnode: NodeDefinition,
\tactiveGroup: string?,
\tlevels: { [string]: number }
): string
\tif node.kind == "Group" then
\t\tif activeGroup == node.groupId then
\t\t\treturn Assets.RedHex
\t\tend

\t\treturn Assets.YellowHex
\tend

\tif not isKnown(node, levels) then
\t\treturn Assets.GrayQuestionHex
\tend

\tif getLevel(levels, node.id) > 0 then
\t\treturn Assets.BlueHex
\tend

\treturn Assets.GrayHex
end

local function makeText(
\tname: string,
\ttext: string | (() -> string),
\tposition: UDim2,
\tsize: UDim2,
\tzIndex: number,
\tvisible: boolean | (() -> boolean)?,
\tmaxTextSize: number,
\tcolor: Color3?
)
\treturn create("TextLabel")({
\t\tName = name,
\t\tSize = size,
\t\tPosition = position,
\t\tAnchorPoint = Vector2.new(0.5, 0.5),
\t\tBackgroundTransparency = 1,
\t\tBorderSizePixel = 0,
\t\tText = text,
\t\tVisible = if visible == nil then true else visible,
\t\tTextScaled = true,
\t\tTextWrapped = false,
\t\tTextXAlignment = Enum.TextXAlignment.Center,
\t\tTextYAlignment = Enum.TextYAlignment.Center,
\t\tFontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy),
\t\tTextColor3 = color or Color3.fromRGB(255, 255, 255),
\t\tZIndex = zIndex,

\t\tcreate("UITextSizeConstraint")({
\t\t\tMinTextSize = 7,
\t\t\tMaxTextSize = maxTextSize,
\t\t}),

\t\tcreate("UIStroke")({
\t\t\tApplyStrokeMode = Enum.ApplyStrokeMode.Contextual,
\t\t\tColor = Color3.fromRGB(0, 0, 0),
\t\t\tTransparency = 0.04,
\t\t\tThickness = 3,
\t\t}),
\t})
end

local function nodeView(
\tnode: NodeDefinition,
\tactiveGroup: Source<string?>,
\tlevels: Source<{ [string]: number }>,
\tpoints: Source<number>,
\tonClick: (NodeDefinition) -> (),
\tzIndex: number
)
\tlocal hovered: Source<boolean> = source(false)

\tlocal function known(): boolean
\t\treturn isKnown(node, levels())
\tend

\treturn create("ImageButton")({
\t\tName = "StatsTreeNode_" .. node.id,
\t\tSize = NODE_SIZE,
\t\tPosition = UDim2.fromOffset(
\t\t\tCANVAS_CENTER.X + node.position.X,
\t\t\tCANVAS_CENTER.Y + node.position.Y
\t\t),
\t\tAnchorPoint = Vector2.new(0.5, 0.5),
\t\tBackgroundTransparency = 1,
\t\tBorderSizePixel = 0,
\t\tImage = function()
\t\t\treturn getNodeImage(node, activeGroup(), levels())
\t\tend,
\t\tScaleType = Enum.ScaleType.Fit,
\t\tAutoButtonColor = false,
\t\tVisible = function()
\t\t\treturn isNodeVisible(node, activeGroup(), levels())
\t\tend,
\t\tZIndex = zIndex,

\t\tActivated = function()
\t\t\tonClick(node)
\t\tend,

\t\tMouseEnter = function()
\t\t\thovered(true)
\t\tend,

\t\tMouseLeave = function()
\t\t\thovered(false)
\t\tend,

\t\tcreate("UIScale")({
\t\t\tScale = function()
\t\t\t\tif hovered() then
\t\t\t\t\treturn 1.045
\t\t\t\tend

\t\t\t\treturn 1
\t\t\tend,
\t\t}),

\t\tmakeText(
\t\t\t"QuestionMark",
\t\t\t"?",
\t\t\tUDim2.fromScale(0.5, 0.48),
\t\t\tUDim2.fromScale(0.62, 0.62),
\t\t\tzIndex + 4,
\t\t\tfunction()
\t\t\t\treturn node.kind == "Stat" and not known()
\t\t\tend,
\t\t\t62,
\t\t\tColor3.fromRGB(238, 241, 250)
\t\t),

\t\tmakeText(
\t\t\t"Effect",
\t\t\tfunction()
\t\t\t\treturn node.effectShort or ""
\t\t\tend,
\t\t\tUDim2.fromScale(0.5, 0.29),
\t\t\tUDim2.fromScale(0.74, 0.19),
\t\t\tzIndex + 4,
\t\t\tfunction()
\t\t\t\treturn node.kind == "Stat" and known() and node.effectShort ~= nil
\t\t\tend,
\t\t\t19,
\t\t\tColor3.fromRGB(255, 255, 255)
\t\t),

\t\tmakeText(
\t\t\t"Title",
\t\t\tnode.title,
\t\t\tUDim2.fromScale(0.5, 0.57),
\t\t\tUDim2.fromScale(0.86, 0.22),
\t\t\tzIndex + 4,
\t\t\tfunction()
\t\t\t\treturn known()
\t\t\tend,
\t\t\t18,
\t\t\tColor3.fromRGB(255, 255, 255)
\t\t),

\t\tmakeText(
\t\t\t"Subtitle",
\t\t\tnode.subtitle or "",
\t\t\tUDim2.fromScale(0.5, 0.73),
\t\t\tUDim2.fromScale(0.86, 0.18),
\t\t\tzIndex + 4,
\t\t\tfunction()
\t\t\t\treturn known() and node.subtitle ~= nil
\t\t\tend,
\t\t\t15,
\t\t\tColor3.fromRGB(255, 255, 255)
\t\t),

\t\tmakeText(
\t\t\t"NoPoints",
\t\t\t"NO POINTS",
\t\t\tUDim2.fromScale(0.5, 0.88),
\t\t\tUDim2.fromScale(0.76, 0.15),
\t\t\tzIndex + 5,
\t\t\tfunction()
\t\t\t\treturn node.kind == "Stat"
\t\t\t\t\tand known()
\t\t\t\t\tand getLevel(levels(), node.id) <= 0
\t\t\t\t\tand points() <= 0
\t\t\tend,
\t\t\t13,
\t\t\tColor3.fromRGB(255, 70, 70)
\t\t),
\t})
end

local function StatsTreeMenu(rawProps: StatsTreeMenuProps?)
\tlocal props: StatsTreeMenuProps = rawProps or {}

\tlocal activeGroup: Source<string?> = source(nil :: string?)
\tlocal levels: Source<{ [string]: number }> = source({})
\tlocal points: Source<number> = source(INITIAL_POINTS)
\tlocal pan: Source<Vector2> = source(Vector2.new(0, 0))
\tlocal zoom: Source<number> = source(1)

\tlocal function menuVisible(): boolean
\t\tlocal visible = props.visible

\t\tif visible ~= nil then
\t\t\treturn visible()
\t\tend

\t\tlocal store = props.store

\t\tif store ~= nil then
\t\t\tlocal currentMenu = store.currentMenu

\t\t\tif currentMenu ~= nil then
\t\t\t\treturn currentMenu() == "StatsTree"
\t\t\tend
\t\tend

\t\treturn true
\tend

\tlocal function spendPoint(node: NodeDefinition)
\t\tif node.kind ~= "Stat" then
\t\t\treturn
\t\tend

\t\tif not isKnown(node, levels()) then
\t\t\treturn
\t\tend

\t\tif points() <= 0 then
\t\t\treturn
\t\tend

\t\tif getLevel(levels(), node.id) > 0 then
\t\t\treturn
\t\tend

\t\tlocal nextLevels: { [string]: number } = table.clone(levels()) :: { [string]: number }
\t\tnextLevels[node.id] = 1

\t\tlevels(nextLevels)
\t\tpoints(math.max(0, points() - 1))
\tend

\tlocal function clickNode(node: NodeDefinition)
\t\tif node.kind == "Group" then
\t\t\tif activeGroup() == node.groupId then
\t\t\t\tactiveGroup(nil)
\t\t\telse
\t\t\t\tactiveGroup(node.groupId)
\t\t\tend

\t\t\treturn
\t\tend

\t\tspendPoint(node)
\tend

\tlocal canvasChildren: { any } = {}

\tfor _, node in ipairs(NODES) do
\t\ttable.insert(canvasChildren, nodeView(node, activeGroup, levels, points, clickNode, 110))
\tend

\treturn create("Frame")({
\t\tName = "StatsTreeMenu",
\t\tSize = UDim2.fromScale(1, 1),
\t\tPosition = UDim2.fromScale(0.5, 0.5),
\t\tAnchorPoint = Vector2.new(0.5, 0.5),
\t\tVisible = menuVisible,
\t\tBackgroundColor3 = Color3.fromRGB(0, 0, 0),
\t\tBackgroundTransparency = 0.34,
\t\tBorderSizePixel = 0,
\t\tClipsDescendants = true,
\t\tActive = true,
\t\tZIndex = 100,

\t\taction(function(instance: Instance)
\t\t\tif not instance:IsA("GuiObject") then
\t\t\t\treturn
\t\t\tend

\t\t\tlocal gui = instance :: GuiObject
\t\t\tlocal dragging = false
\t\t\tlocal lastPosition: Vector2? = nil

\t\t\tContextActionService:BindActionAtPriority(
\t\t\t\tWHEEL_ACTION_NAME,
\t\t\t\tfunction(_actionName: string, inputState: Enum.UserInputState, inputObject: InputObject)
\t\t\t\t\tif not menuVisible() then
\t\t\t\t\t\treturn Enum.ContextActionResult.Pass
\t\t\t\t\tend

\t\t\t\t\tif inputState == Enum.UserInputState.Change then
\t\t\t\t\t\tlocal nextZoom = zoom()

\t\t\t\t\t\tif inputObject.Position.Z > 0 then
\t\t\t\t\t\t\tnextZoom *= 1.1
\t\t\t\t\t\telse
\t\t\t\t\t\t\tnextZoom /= 1.1
\t\t\t\t\t\tend

\t\t\t\t\t\tzoom(math.clamp(nextZoom, MIN_ZOOM, MAX_ZOOM))
\t\t\t\t\tend

\t\t\t\t\treturn Enum.ContextActionResult.Sink
\t\t\t\tend,
\t\t\t\tfalse,
\t\t\t\t3000,
\t\t\t\tEnum.UserInputType.MouseWheel
\t\t\t)

\t\t\tlocal inputBegan = gui.InputBegan:Connect(function(input: InputObject)
\t\t\t\tif input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
\t\t\t\t\tdragging = true
\t\t\t\t\tlastPosition = Vector2.new(input.Position.X, input.Position.Y)
\t\t\t\tend
\t\t\tend)

\t\t\tlocal inputChanged = UserInputService.InputChanged:Connect(function(input: InputObject)
\t\t\t\tif not dragging then
\t\t\t\t\treturn
\t\t\t\tend

\t\t\t\tif input.UserInputType ~= Enum.UserInputType.MouseMovement and input.UserInputType ~= Enum.UserInputType.Touch then
\t\t\t\t\treturn
\t\t\t\tend

\t\t\t\tlocal currentPosition = Vector2.new(input.Position.X, input.Position.Y)

\t\t\t\tif lastPosition == nil then
\t\t\t\t\tlastPosition = currentPosition
\t\t\t\t\treturn
\t\t\t\tend

\t\t\t\tlocal delta = currentPosition - lastPosition
\t\t\t\tlastPosition = currentPosition

\t\t\t\tpan(pan() + delta)
\t\t\tend)

\t\t\tlocal inputEnded = UserInputService.InputEnded:Connect(function(input: InputObject)
\t\t\t\tif input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
\t\t\t\t\tdragging = false
\t\t\t\t\tlastPosition = nil
\t\t\t\tend
\t\t\tend)

\t\t\tcleanup(function()
\t\t\t\tContextActionService:UnbindAction(WHEEL_ACTION_NAME)
\t\t\t\tinputBegan:Disconnect()
\t\t\t\tinputChanged:Disconnect()
\t\t\t\tinputEnded:Disconnect()
\t\t\tend)
\t\tend),

\t\tcreate("Frame")({
\t\t\tName = "Canvas",
\t\t\tSize = UDim2.fromOffset(CANVAS_SIZE.X, CANVAS_SIZE.Y),
\t\t\tPosition = function()
\t\t\t\tlocal value = pan()

\t\t\t\treturn UDim2.new(0.5, value.X, 0.5, value.Y)
\t\t\tend,
\t\t\tAnchorPoint = Vector2.new(0.5, 0.5),
\t\t\tBackgroundTransparency = 1,
\t\t\tBorderSizePixel = 0,
\t\t\tZIndex = 101,

\t\t\tcreate("UIScale")({
\t\t\t\tScale = zoom,
\t\t\t}),

\t\t\ttable.unpack(canvasChildren),
\t\t}),

\t\tcreate("Frame")({
\t\t\tName = "TopBar",
\t\t\tSize = UDim2.fromScale(0.36, 0.08),
\t\t\tPosition = UDim2.fromScale(0.5, 0.035),
\t\t\tAnchorPoint = Vector2.new(0.5, 0),
\t\t\tBackgroundColor3 = Color3.fromRGB(0, 0, 0),
\t\t\tBackgroundTransparency = 0.42,
\t\t\tBorderSizePixel = 0,
\t\t\tZIndex = 220,

\t\t\tcreate("UICorner")({
\t\t\t\tCornerRadius = UDim.new(0.2, 0),
\t\t\t}),

\t\t\tcreate("UIStroke")({
\t\t\t\tColor = Color3.fromRGB(0, 229, 255),
\t\t\t\tTransparency = 0.25,
\t\t\t\tThickness = 2,
\t\t\t}),

\t\t\tmakeText(
\t\t\t\t"Title",
\t\t\t\t"STATS TREE",
\t\t\t\tUDim2.fromScale(0.5, 0.3),
\t\t\t\tUDim2.fromScale(0.95, 0.46),
\t\t\t\t221,
\t\t\t\ttrue,
\t\t\t\t34,
\t\t\t\tColor3.fromRGB(255, 255, 255)
\t\t\t),

\t\t\tmakeText(
\t\t\t\t"Points",
\t\t\t\tfunction()
\t\t\t\t\treturn "Available Points: " .. tostring(points())
\t\t\t\tend,
\t\t\t\tUDim2.fromScale(0.5, 0.73),
\t\t\t\tUDim2.fromScale(0.95, 0.34),
\t\t\t\t221,
\t\t\t\ttrue,
\t\t\t\t22,
\t\t\t\tColor3.fromRGB(0, 229, 255)
\t\t\t),
\t\t}),

\t\tmakeText(
\t\t\t"Hint",
\t\t\t"CLICK HEXES TO SPEND POINTS  |  DRAG TO MOVE  |  MOUSE WHEEL TO ZOOM",
\t\t\tUDim2.fromScale(0.5, 0.925),
\t\t\tUDim2.fromScale(0.5, 0.045),
\t\t\t230,
\t\t\ttrue,
\t\t\t18,
\t\t\tColor3.fromRGB(255, 255, 255)
\t\t),

\t\tcreate("TextButton")({
\t\t\tName = "CloseButton",
\t\t\tSize = UDim2.fromScale(0.16, 0.075),
\t\t\tPosition = UDim2.fromScale(0.5, 0.975),
\t\t\tAnchorPoint = Vector2.new(0.5, 1),
\t\t\tBackgroundColor3 = Color3.fromRGB(255, 30, 30),
\t\t\tBorderSizePixel = 0,
\t\t\tText = "CLOSE",
\t\t\tTextScaled = true,
\t\t\tFontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy),
\t\t\tTextColor3 = Color3.fromRGB(255, 255, 255),
\t\t\tAutoButtonColor = true,
\t\t\tZIndex = 230,

\t\t\tActivated = function()
\t\t\t\tlocal store = props.store

\t\t\t\tif store == nil then
\t\t\t\t\treturn
\t\t\t\tend

\t\t\t\tlocal currentMenu = store.currentMenu

\t\t\t\tif currentMenu ~= nil then
\t\t\t\t\tcurrentMenu(nil)
\t\t\t\tend
\t\t\tend,

\t\t\tcreate("UICorner")({
\t\t\t\tCornerRadius = UDim.new(0.14, 0),
\t\t\t}),

\t\t\tcreate("UIStroke")({
\t\t\t\tColor = Color3.fromRGB(0, 0, 0),
\t\t\t\tTransparency = 0,
\t\t\t\tThickness = 4,
\t\t\t}),
\t\t}),
\t})
end

return StatsTreeMenu
'''


@dataclass(frozen=True)
class Patch:
    path: Path
    before: str
    after: str
    notes: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def make_backup(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    safe_name = "__".join(path.parts[-5:])
    backup_path = backup_root / safe_name
    shutil.copy2(path, backup_path)
    return backup_path


def unified_diff(path: Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"{path} (before)",
            tofile=f"{path} (after)",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Update StatsTree to procedural tier branches.")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backup before writing.")
    args = parser.parse_args()

    repo_root = Path.cwd()
    required = [DATA_PATH, INIT_PATH, ASSETS_PATH]

    missing = [path for path in required if not (repo_root / path).exists()]
    if missing:
        print("ERROR: Missing expected files:")
        for path in missing:
            print(f"  - {path}")
        print("\\nRun this script from the Arcadia-Vide repository root.")
        return 1

    patches = [
        Patch(
            DATA_PATH,
            read_text(repo_root / DATA_PATH),
            DATA_SOURCE,
            ["Replaced StatsTreeData.lua with procedural 10-tier branch generation."],
        ),
        Patch(
            INIT_PATH,
            read_text(repo_root / INIT_PATH),
            INIT_SOURCE,
            ["Updated StatsTree renderer for tier-node progression: blue owned, gray next, ? future."],
        ),
    ]

    changed = [patch for patch in patches if patch.before != patch.after]

    print("Patch notes:")
    for patch in patches:
        print(f"\\n{patch.path}")
        for note in patch.notes:
            print(f"  - {note}")

    if not changed:
        print("\\nNo changes needed.")
        return 0

    print("\\nDiff:\\n")
    for patch in changed:
        print(unified_diff(patch.path, patch.before, patch.after))

    if args.dry_run:
        print("\\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = Path(".patch_backups") / "update_stats_tree_tier_branches_v3" / timestamp

        for patch in changed:
            backup_path = make_backup(repo_root / patch.path, backup_root)
            print(f"Backup created: {backup_path}")

    for patch in changed:
        write_text(repo_root / patch.path, patch.after)
        print(f"Updated: {patch.path}")

    print("\\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Studio/Hoarcekat")
    print("  3) Open StatsTree and open each group.")
    print("  4) Expected per branch:")
    print("     - Tier I known gray")
    print("     - Tier II mystery ?")
    print("     - Click Tier I: it becomes blue, Tier II becomes known gray, Tier III becomes ?")
    print("\\nFuture tuning:")
    print("  - Change MAX_TIER in StatsTreeData.lua if the max level changes.")
    print("  - Change branch directions in the `branches` table if you want different honeycomb growth paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
