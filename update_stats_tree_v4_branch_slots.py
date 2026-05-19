#!/usr/bin/env python3
# StatsTree V4: proper branch-slot honeycomb layout.
#
# Run from the Arcadia-Vide repository root:
#   python update_stats_tree_v4_branch_slots.py --dry-run
#   python update_stats_tree_v4_branch_slots.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua
#
# What this fixes:
# - First-tier subtypes now sit in the neighbor slots around the main category hub.
# - Each subtype then grows outward from its own starting slot in the same honeycomb direction.
# - This avoids "floating" branches and keeps the tree readable:
#
#       Economy:
#             EXP I        Points I
#       Money I   Economy   Lucky I
#             Gems I
#
#       Skills:
#             Skill Power I
#       Skill Haste I   Skills
#             Skill Duration I
#
# - Each branch still procedurally generates I -> X.
# - Each tier still costs 1 point.
# - MAX_TIER is still one constant.
#
# Backup:
#   .patch_backups/update_stats_tree_v4_branch_slots/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua")


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

-- Visual honeycomb spacing for the current 148x148 rendered hex assets.
--
-- The category root triangle already looked correct with:
--   Economy -> Skills  = SW
--   Economy -> Stamina = SE
--
-- Branches use the same neighbor slots around their category hub.
-- Horizontal branches need their own spacing so they do not feel too far away.
local DIAGONAL_X = 118
local DIAGONAL_Y = 68
local HORIZONTAL_X = 180

local DIRECTIONS = {
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

local function branchPosition(origin: Vector2, direction: Vector2, tier: number): Vector2
\treturn origin + (direction * tier)
end

-- Root category hubs:
--          Economy
--     Skills      Stamina
local ECONOMY = Vector2.new(0, -DIAGONAL_Y)
local SKILLS = ECONOMY + DIRECTIONS.SW
local STAMINA = ECONOMY + DIRECTIONS.SE

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
\t-- First-tier subtypes populate the ring around Economy.
\t-- Each subtype then continues outward from that ring slot.
\t-- ============================================================
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "MoneyBoost",
\t\ttitle = "Money",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Money per tier.",
\t\torigin = ECONOMY,
\t\tdirection = DIRECTIONS.W,
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "ExpBoost",
\t\ttitle = "EXP",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% EXP per tier.",
\t\torigin = ECONOMY,
\t\tdirection = DIRECTIONS.NW,
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "PointsBoost",
\t\ttitle = "Points",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Points per tier.",
\t\torigin = ECONOMY,
\t\tdirection = DIRECTIONS.NE,
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "GemsBoost",
\t\ttitle = "Gems",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Gems per tier.",
\t\torigin = ECONOMY,
\t\tdirection = DIRECTIONS.SW,
\t},
\t{
\t\tgroupId = "Economy",
\t\tbranchId = "Lucky",
\t\ttitle = "Lucky",
\t\teffectShort = "+2%",
\t\tdescription = "+2% Luck per tier.",
\t\torigin = ECONOMY,
\t\tdirection = DIRECTIONS.SE,
\t},

\t-- ============================================================
\t-- SKILLS
\t-- First-tier subtypes populate slots around Skills.
\t-- ============================================================
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillHaste",
\t\ttitle = "Skill",
\t\tsubtitle = "Haste",
\t\teffectShort = "-4%",
\t\tdescription = "-4% Cooldown per tier.",
\t\torigin = SKILLS,
\t\tdirection = DIRECTIONS.W,
\t},
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillPower",
\t\ttitle = "Skill",
\t\tsubtitle = "Power",
\t\teffectShort = "+4%",
\t\tdescription = "+4% Power per tier.",
\t\torigin = SKILLS,
\t\tdirection = DIRECTIONS.NW,
\t},
\t{
\t\tgroupId = "Skills",
\t\tbranchId = "SkillDuration",
\t\ttitle = "Skill",
\t\tsubtitle = "Duration",
\t\teffectShort = "+0.5s",
\t\tdescription = "+0.5 seconds Duration per tier.",
\t\torigin = SKILLS,
\t\tdirection = DIRECTIONS.SW,
\t},

\t-- ============================================================
\t-- STAMINA
\t-- Only two current subtype branches, but still uses ring slots.
\t-- ============================================================
\t{
\t\tgroupId = "Stamina",
\t\tbranchId = "MaxStamina",
\t\ttitle = "Max",
\t\tsubtitle = "Stamina",
\t\teffectShort = "+10",
\t\tdescription = "+10 Max Stamina per tier.",
\t\torigin = STAMINA,
\t\tdirection = DIRECTIONS.E,
\t},
\t{
\t\tgroupId = "Stamina",
\t\tbranchId = "StaminaRecovery",
\t\ttitle = "Stamina",
\t\tsubtitle = "Regen",
\t\teffectShort = "+1/s",
\t\tdescription = "+1/sec Regen per tier.",
\t\torigin = STAMINA,
\t\tdirection = DIRECTIONS.SE,
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
\t\t\tposition = branchPosition(branch.origin, branch.direction, tier),
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
    backup_dir = Path(".patch_backups") / "update_stats_tree_v4_branch_slots" / timestamp
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
    parser = argparse.ArgumentParser(description="Update StatsTreeData.lua to branch-slot honeycomb tier layout.")
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
        print("No changes needed. StatsTreeData.lua already uses V4 branch-slot honeycomb layout.")
        return 0

    print("Planned change:")
    print("  - Rewrite StatsTreeData.lua with branch-slot honeycomb layout.")
    print("  - First-tier subtype hexes populate the neighbor ring around the category hub.")
    print("  - Later tiers continue outward from their starting slot.")
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
    print("  3) Open Economy / Skills / Stamina.")
    print("  4) Expected: subtype I nodes sit around the hub, and II/III/X continue outward from them.")
    print("\nTuning inside StatsTreeData.lua:")
    print("  local DIAGONAL_X = 118")
    print("  local DIAGONAL_Y = 68")
    print("  local HORIZONTAL_X = 180")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
