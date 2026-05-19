#!/usr/bin/env python3
# StatsTree V5: true hex-neighbor branch paths.
#
# Run from the Arcadia-Vide repository root:
#   python update_stats_tree_v5_neighbor_paths.py --dry-run
#   python update_stats_tree_v5_neighbor_paths.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua
#
# What this fixes:
# - Every subtype Tier I starts in one of the 6 neighbor slots around the category hub:
#
#           NW      NE
#
#       W      HUB      E
#
#           SW      SE
#
# - Tier II, III, IV... no longer grow by a naive straight pixel vector.
# - Instead, every branch walks through valid neighboring hex sides using a growthPath.
# - This keeps the honeycomb structure intact while still being procedural:
#     MAX_TIER = 10
#     change MAX_TIER later and all branches generate more/less nodes automatically.
#
# Backup:
#   .patch_backups/update_stats_tree_v5_neighbor_paths/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua")


DATA_SOURCE = '''--!strict

export type NodeKind = "Group" | "Stat"
export type DirectionName = "NW" | "NE" | "W" | "E" | "SW" | "SE"

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

\t-- Tier I starts in this neighbor slot around the category hub.
\tfirstSlot: DirectionName,

\t-- Tier II+ walks from the previous tier through these valid neighbor sides.
\t-- The path repeats if maxTier is longer than the list.
\tgrowthPath: { DirectionName },

\tmaxTier: number?,
}

-- Change this later if the stat cap changes.
local MAX_TIER = 10

-- Visual neighbor offsets for the current 148x148 rendered hex assets.
-- These values are intentionally based on the root category layout that looked correct.
--
-- If the global honeycomb gap needs tuning, adjust these only.
local DIAGONAL_X = 118
local DIAGONAL_Y = 68
local HORIZONTAL_X = 180

local DIRECTIONS: { [DirectionName]: Vector2 } = {
\tNW = Vector2.new(-DIAGONAL_X, -DIAGONAL_Y),
\tNE = Vector2.new(DIAGONAL_X, -DIAGONAL_Y),
\tW = Vector2.new(-HORIZONTAL_X, 0),
\tE = Vector2.new(HORIZONTAL_X, 0),
\tSW = Vector2.new(-DIAGONAL_X, DIAGONAL_Y),
\tSE = Vector2.new(DIAGONAL_X, DIAGONAL_Y),
}

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

local function dir(name: DirectionName): Vector2
\treturn DIRECTIONS[name]
end

local function branchPosition(
\torigin: Vector2,
\tfirstSlot: DirectionName,
\tgrowthPath: { DirectionName },
\ttier: number
): Vector2
\tlocal position = origin + dir(firstSlot)

\tif tier <= 1 then
\t\treturn position
\tend

\tfor stepIndex = 2, tier do
\t\tlocal pathIndex = ((stepIndex - 2) % #growthPath) + 1
\t\tposition = position + dir(growthPath[pathIndex])
\tend

\treturn position
end

-- Root category hubs:
--          Economy
--     Skills      Stamina
local ECONOMY = Vector2.new(0, -DIAGONAL_Y)
local SKILLS = ECONOMY + dir("SW")
local STAMINA = ECONOMY + dir("SE")

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
\t-- ============================================================
\t-- ECONOMY
\t-- Tier I nodes occupy neighbor slots around Economy.
\t-- Tier II+ walks through available outer sides of each branch.
\t-- ============================================================
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "MoneyBoost",
\t\ttitle = "Money",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Money per tier.",
\t\torigin = ECONOMY,
\t\tfirstSlot = "W",
\t\tgrowthPath = { "W", "NW", "W", "SW" },
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "ExpBoost",
\t\ttitle = "EXP",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% EXP per tier.",
\t\torigin = ECONOMY,
\t\tfirstSlot = "NW",
\t\tgrowthPath = { "NW", "W" },
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "PointsBoost",
\t\ttitle = "Points",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Points per tier.",
\t\torigin = ECONOMY,
\t\tfirstSlot = "NE",
\t\tgrowthPath = { "NE", "E" },
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "GemsBoost",
\t\ttitle = "Gems",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Gems per tier.",
\t\torigin = ECONOMY,
\t\tfirstSlot = "SW",
\t\tgrowthPath = { "SW", "W" },
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "Lucky",
\t\ttitle = "Lucky",
\t\teffectShort = "+2%",
\t\tdescription = "+2% Luck per tier.",
\t\torigin = ECONOMY,
\t\tfirstSlot = "SE",
\t\tgrowthPath = { "SE", "E" },
\t},

\t-- ============================================================
\t-- SKILLS
\t-- Tier I nodes occupy neighbor slots around Skills.
\t-- ============================================================
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillHaste",
\t\ttitle = "Skill",
\t\tsubtitle = "Haste",
\t\teffectShort = "-4%",
\t\tdescription = "-4% Cooldown per tier.",
\t\torigin = SKILLS,
\t\tfirstSlot = "W",
\t\tgrowthPath = { "W", "NW", "W", "SW" },
\t},
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillPower",
\t\ttitle = "Skill",
\t\tsubtitle = "Power",
\t\teffectShort = "+4%",
\t\tdescription = "+4% Power per tier.",
\t\torigin = SKILLS,
\t\tfirstSlot = "NW",
\t\tgrowthPath = { "NW", "W" },
\t},
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillDuration",
\t\ttitle = "Skill",
\t\tsubtitle = "Duration",
\t\teffectShort = "+0.5s",
\t\tdescription = "+0.5 seconds Duration per tier.",
\t\torigin = SKILLS,
\t\tfirstSlot = "SW",
\t\tgrowthPath = { "SW", "W" },
\t},

\t-- ============================================================
\t-- STAMINA
\t-- Tier I nodes occupy neighbor slots around Stamina.
\t-- ============================================================
\t{
\t\tgroupId = "Stamina",
\t\tbranchId = "MaxStamina",
\t\ttitle = "Max",
\t\tsubtitle = "Stamina",
\t\teffectShort = "+10",
\t\tdescription = "+10 Max Stamina per tier.",
\t\torigin = STAMINA,
\t\tfirstSlot = "NE",
\t\tgrowthPath = { "NE", "E" },
\t},
\t{
\t\tgroupId = "Stamina",
\t\tbranchId = "StaminaRecovery",
\t\ttitle = "Stamina",
\t\tsubtitle = "Regen",
\t\teffectShort = "+1/s",
\t\tdescription = "+1/sec Regen per tier.",
\t\torigin = STAMINA,
\t\tfirstSlot = "SE",
\t\tgrowthPath = { "SE", "E" },
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
\t\t\tposition = branchPosition(branch.origin, branch.firstSlot, branch.growthPath, tier),
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


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "update_stats_tree_v5_neighbor_paths" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path


def print_diff(path: Path, before: str, after: str) -> None:
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
    )
    print("".join(diff))


def main() -> int:
    parser = argparse.ArgumentParser(description="Update StatsTreeData.lua to true hex-neighbor branch paths.")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backup before writing.")
    args = parser.parse_args()

    path = Path.cwd() / TARGET

    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    before = path.read_text(encoding="utf-8")
    after = DATA_SOURCE

    if before == after:
        print("No changes needed. StatsTreeData.lua already uses V5 neighbor-path layout.")
        return 0

    print("Planned change:")
    print("  - Rewrite StatsTreeData.lua with true hex-neighbor branch paths.")
    print("  - Tier I starts in one of the 6 slots around the category hub.")
    print("  - Tier II+ walks through valid neighbor sides using each branch growthPath.")
    print("  - MAX_TIER remains procedural and easy to change.")
    print("  - StatsTree/init.lua is not changed.")

    print("\nDiff:\n")
    print_diff(TARGET, before, after)

    if args.dry_run:
        print("\nDry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        backup_path = make_backup(path)
        print(f"Backup created: {backup_path}")

    path.write_text(after, encoding="utf-8")
    print(f"Updated: {TARGET}")

    print("\nNext steps:")
    print("  1) Check: git diff")
    print("  2) Refresh Studio/Hoarcekat")
    print("  3) Open each branch and spend a few points.")
    print("  4) Expected:")
    print("     - Tier I nodes start directly around the category hub.")
    print("     - Tier II+ continues through valid honeycomb neighbor sides.")
    print("     - Mystery ? nodes stay attached to the branch path.")
    print("\nTuning inside StatsTreeData.lua:")
    print("  local DIAGONAL_X = 118")
    print("  local DIAGONAL_Y = 68")
    print("  local HORIZONTAL_X = 180")
    print("  branch.growthPath = { ... }")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
