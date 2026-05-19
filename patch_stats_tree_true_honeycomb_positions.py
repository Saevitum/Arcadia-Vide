#!/usr/bin/env python3
# Patch StatsTreeData.lua to use a true side-touching honeycomb layout.
#
# Run from the Arcadia-Vide repository root:
#   python patch_stats_tree_true_honeycomb_positions.py --dry-run
#   python patch_stats_tree_true_honeycomb_positions.py
#
# Target:
#   src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua
#
# What it changes:
# - Repositions the 3 starter category hubs so their diagonal sides line up:
#     Economy top
#     Skills bottom-left
#     Stamina bottom-right
# - Uses a flat-top hex honeycomb spacing instead of the previous triangle spacing.
# - Repositions each category's branch nodes around its hub with the same honeycomb offsets.
# - Does NOT touch StatsTree/init.lua logic.
# - Does NOT re-add lines/details/Add button.
#
# Geometry:
# - Current visual hex image is rendered around 148x148.
# - Good side-matching offset for this asset is roughly:
#     x = 112
#     y = 64
# - We use a tiny extra gap:
#     x = 118
#     y = 68
#
# Backup:
#   .patch_backups/patch_stats_tree_true_honeycomb_positions/<timestamp>/

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

-- Flat-top hex honeycomb spacing for the current 148x148 rendered hex assets.
-- Neighbor positions are intentionally close so diagonal sides visually match.
local HX = 118
local HY = 68

-- Root category layout:
--       Economy
--  Skills     Stamina
local ECONOMY = Vector2.new(0, -HY)
local SKILLS = Vector2.new(-HX, 0)
local STAMINA = Vector2.new(HX, 0)

local nodes: { NodeDefinition } = {
\t-- Category hubs. These are always visible at root.
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

\t-- Economy cluster around EconomyOpen.
\t-- First-tier known stats form a compact honeycomb around the red/yellow hub.
\t{
\t\tid = "MoneyBoost",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Money",
\t\tsubtitle = "Boost",
\t\teffectShort = "+3%",
\t\tdescription = "+3% Money per level.",
\t\tmaxLevel = 10,
\t\tposition = ECONOMY + Vector2.new(-HX, 0),
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
\t\tposition = ECONOMY + Vector2.new(-HX / 2, -HY),
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
\t\tposition = ECONOMY + Vector2.new(HX / 2, -HY),
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
\t\tposition = ECONOMY + Vector2.new(-HX / 2, HY),
\t},
\t{
\t\tid = "Lucky",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Lucky",
\t\teffectShort = "+2%",
\t\tdescription = "+2% Luck per level.",
\t\tmaxLevel = 10,
\t\tposition = ECONOMY + Vector2.new(HX / 2, HY),
\t},

\t-- Economy future nodes.
\t-- They are visible as ? until the requirement is met, then become known Gray stat hexes.
\t{
\t\tid = "CoinIncome",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Coin",
\t\tsubtitle = "Income",
\t\teffectShort = "+5%",
\t\tdescription = "Future economy upgrade.",
\t\tmaxLevel = 10,
\t\tposition = ECONOMY + Vector2.new(-HX * 1.5, -HY),
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
\t\tposition = ECONOMY + Vector2.new(HX * 1.5, HY),
\t\trequires = {
\t\t\t{ nodeId = "Lucky", minLevel = 1 },
\t\t},
\t},

\t-- Skills cluster around SkillsOpen.
\t{
\t\tid = "SkillHaste",
\t\tkind = "Stat",
\t\tgroupId = "Skills",
\t\ttitle = "Skill",
\t\tsubtitle = "Haste",
\t\teffectShort = "-4%",
\t\tdescription = "-4% Cooldown per level.",
\t\tmaxLevel = 10,
\t\tposition = SKILLS + Vector2.new(-HX, 0),
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
\t\tposition = SKILLS + Vector2.new(-HX / 2, -HY),
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
\t\tposition = SKILLS + Vector2.new(-HX / 2, HY),
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
\t\tposition = SKILLS + Vector2.new(-HX * 1.5, -HY),
\t\trequires = {
\t\t\t{ nodeId = "SkillPower", minLevel = 1 },
\t\t},
\t},

\t-- Stamina cluster around StaminaOpen.
\t{
\t\tid = "MaxStamina",
\t\tkind = "Stat",
\t\tgroupId = "Stamina",
\t\ttitle = "Max",
\t\tsubtitle = "Stamina",
\t\teffectShort = "+10",
\t\tdescription = "+10 Max Stamina per level.",
\t\tmaxLevel = 10,
\t\tposition = STAMINA + Vector2.new(HX, 0),
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
\t\tposition = STAMINA + Vector2.new(HX / 2, HY),
\t},
\t{
\t\tid = "Endurance",
\t\tkind = "Stat",
\t\tgroupId = "Stamina",
\t\ttitle = "Endurance",
\t\teffectShort = "+5%",
\t\tdescription = "Future survival upgrade.",
\t\tmaxLevel = 10,
\t\tposition = STAMINA + Vector2.new(HX * 1.5, HY),
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
    backup_dir = Path(".patch_backups") / "patch_stats_tree_true_honeycomb_positions" / timestamp
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
        description="Patch StatsTreeData.lua to true honeycomb node positions."
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
        print("No changes needed. StatsTreeData.lua already has the true honeycomb layout.")
        return 0

    print("Planned change:")
    print("  - Replace StatsTreeData.lua positions with side-matching honeycomb coordinates.")
    print("  - Economy remains top, Skills bottom-left, Stamina bottom-right.")
    print("  - Category branch nodes use the same honeycomb spacing around each hub.")
    print("  - StatsTree/init.lua is not touched.")

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
    print("  3) Open StatsTree.")
    print("  4) Expected root layout:")
    print("         Economy")
    print("      Skills  Stamina")
    print("     with the diagonal sides visually lining up like a honeycomb.")
    print("\nTuning note:")
    print("  - If the gap is too small/large, adjust HX/HY at the top of StatsTreeData.lua.")
    print("  - Current values: HX = 118, HY = 68.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
