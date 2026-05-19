#!/usr/bin/env python3
# Fix StatsTree branch nodes to use the SAME honeycomb spacing as the 3 root category hexes.
#
# Run from the Arcadia-Vide repository root:
#   python fix_stats_tree_branch_honeycomb_spacing.py --dry-run
#   python fix_stats_tree_branch_honeycomb_spacing.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua
#
# Why this patch exists:
# - The 3 root category hubs already look correct:
#       Economy
#    Skills  Stamina
# - But the child/stat nodes used half-step lattice coordinates, so they appeared too
#   close together and overlapped.
# - This patch uses the same full diagonal offset for EVERY neighboring hex:
#       NW = (-HEX_DX, -HEX_DY)
#       NE = ( HEX_DX, -HEX_DY)
#       W  = (-HEX_DX * 2, 0)
#       E  = ( HEX_DX * 2, 0)
#       SW = (-HEX_DX,  HEX_DY)
#       SE = ( HEX_DX,  HEX_DY)
#
# Backup:
#   .patch_backups/fix_stats_tree_branch_honeycomb_spacing/<timestamp>/

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path("src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua")


DATA_SOURCE = '''--!strict

export type Requirement = {
\tnodeId: string,
\tminLevel: number,
}

export type NodeKind = "Group" | "Stat"

export type NodeDefinition = {
\tid: string,
\tkind: NodeKind,
\tgroupId: string,

\ttitle: string,
\tsubtitle: string?,
\teffectShort: string?,
\tdescription: string?,

\tmaxLevel: number?,
\tposition: Vector2,

\t-- If present, this stat renders as a mystery ? node until requirements are met.
\trequires: { Requirement }?,
}

-- Full-step honeycomb spacing for the current 148x148 rendered hex assets.
-- The important rule:
--   diagonal neighbors use the SAME offset as the working root layout.
--
-- Root layout:
--          Economy
--     Skills      Stamina
--
-- If the global gap needs tuning, adjust only these two values.
local HEX_DX = 118
local HEX_DY = 68

local function P(origin: Vector2, x: number, y: number): Vector2
\treturn origin + Vector2.new(x * HEX_DX, y * HEX_DY)
end

-- Root category hubs.
local ECONOMY = Vector2.new(0, -HEX_DY)
local SKILLS = Vector2.new(-HEX_DX, 0)
local STAMINA = Vector2.new(HEX_DX, 0)

local nodes: { NodeDefinition } = {
\t-- ============================================================
\t-- ROOT CATEGORY HUBS
\t-- ============================================================
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

\t-- ============================================================
\t-- ECONOMY BRANCH
\t-- Same full honeycomb neighbor pattern around EconomyOpen:
\t--              EXP       Points
\t--       Money     Economy
\t--              Gems      Lucky
\t-- ============================================================
\t{
\t\tid = "MoneyBoost",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Money",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Money per level.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, -2, 0),
\t},
\t{
\t\tid = "ExpBoost",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "EXP",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% EXP per level.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, -1, -1),
\t},
\t{
\t\tid = "PointsBoost",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Points",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Points per level.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, 1, -1),
\t},
\t{
\t\tid = "GemsBoost",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Gems",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Gems per level.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, -1, 1),
\t},
\t{
\t\tid = "Lucky",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Lucky",
\t\teffectShort = "+2%",
\t\tdescription = "+2% Luck per level.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, 1, 1),
\t},
\t{
\t\tid = "CoinIncome",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Coin",
\t\tsubtitle = "Income",
\t\teffectShort = "+5%",
\t\tdescription = "Future economy upgrade.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, -3, -1),
\t\trequires = {
\t\t\t{ nodeId = "MoneyBoost", minLevel = 1 },
\t\t},
\t},
\t{
\t\tid = "UltraLuck",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Ultra",
\t\tsubtitle = "Luck",
\t\teffectShort = "+5%",
\t\tdescription = "Future luck upgrade.",
\t\tmaxLevel = 10,
\t\tposition = P(ECONOMY, 2, 2),
\t\trequires = {
\t\t\t{ nodeId = "Lucky", minLevel = 1 },
\t\t},
\t},

\t-- ============================================================
\t-- SKILLS BRANCH
\t-- Uses the same full honeycomb offsets around SkillsOpen.
\t-- ============================================================
\t{
\t\tid = "SkillHaste",
\t\tkind = "Stat",
\t\tgroupId = "Skills",
\t\ttitle = "Skill",
\t\tsubtitle = "Haste",
\t\teffectShort = "-4%",
\t\tdescription = "-4% Cooldown per level.",
\t\tmaxLevel = 10,
\t\tposition = P(SKILLS, -2, 0),
\t},
\t{
\t\tid = "SkillPower",
\t\tkind = "Stat",
\t\tgroupId = "Skills",
\t\ttitle = "Skill",
\t\tsubtitle = "Power",
\t\teffectShort = "+4%",
\t\tdescription = "+4% Power per level.",
\t\tmaxLevel = 10,
\t\tposition = P(SKILLS, -1, -1),
\t},
\t{
\t\tid = "SkillDuration",
\t\tkind = "Stat",
\t\tgroupId = "Skills",
\t\ttitle = "Skill",
\t\tsubtitle = "Duration",
\t\teffectShort = "+0.5s",
\t\tdescription = "+0.5 seconds Duration per level.",
\t\tmaxLevel = 10,
\t\tposition = P(SKILLS, -1, 1),
\t},
\t{
\t\tid = "SkillOverdrive",
\t\tkind = "Stat",
\t\tgroupId = "Skills",
\t\ttitle = "Skill",
\t\tsubtitle = "Overdrive",
\t\teffectShort = "+5%",
\t\tdescription = "Future skill upgrade.",
\t\tmaxLevel = 10,
\t\tposition = P(SKILLS, -3, -1),
\t\trequires = {
\t\t\t{ nodeId = "SkillPower", minLevel = 1 },
\t\t},
\t},

\t-- ============================================================
\t-- STAMINA BRANCH
\t-- Uses the same full honeycomb offsets around StaminaOpen.
\t-- ============================================================
\t{
\t\tid = "MaxStamina",
\t\tkind = "Stat",
\t\tgroupId = "Stamina",
\t\ttitle = "Max",
\t\tsubtitle = "Stamina",
\t\teffectShort = "+10",
\t\tdescription = "+10 Max Stamina per level.",
\t\tmaxLevel = 10,
\t\tposition = P(STAMINA, 2, 0),
\t},
\t{
\t\tid = "StaminaRecovery",
\t\tkind = "Stat",
\t\tgroupId = "Stamina",
\t\ttitle = "Stamina",
\t\tsubtitle = "Regen",
\t\teffectShort = "+1/s",
\t\tdescription = "+1/sec Regen per level.",
\t\tmaxLevel = 10,
\t\tposition = P(STAMINA, 1, 1),
\t},
\t{
\t\tid = "Endurance",
\t\tkind = "Stat",
\t\tgroupId = "Stamina",
\t\ttitle = "Endurance",
\t\teffectShort = "+5%",
\t\tdescription = "Future survival upgrade.",
\t\tmaxLevel = 10,
\t\tposition = P(STAMINA, 3, 1),
\t\trequires = {
\t\t\t{ nodeId = "MaxStamina", minLevel = 1 },
\t\t},
\t},
}

return {
\tnodes = nodes,
}
'''


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "fix_stats_tree_branch_honeycomb_spacing" / timestamp
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
    parser = argparse.ArgumentParser(
        description="Fix StatsTree branch nodes so every node uses the same honeycomb spacing as the root category hubs."
    )
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
        print("No changes needed. StatsTreeData.lua already uses full-step honeycomb spacing.")
        return 0

    print("Planned change:")
    print("  - Replace StatsTreeData.lua with full-step honeycomb coordinates.")
    print("  - Fixes the child/stat hex overlap caused by half-step lattice coordinates.")
    print("  - Leaves StatsTree/init.lua logic untouched.")
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
    print("  3) Open each StatsTree branch.")
    print("  4) Expected: child stat hexes use the same visual honeycomb spacing as the 3 root category hexes.")
    print("\nTuning:")
    print("  - If the gap is too big/small, edit HEX_DX and HEX_DY at the top of StatsTreeData.lua.")
    print("  - Current values: HEX_DX = 118, HEX_DY = 68")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
