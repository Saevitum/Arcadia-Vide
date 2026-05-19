#!/usr/bin/env python3
"""
Rewrite StatsTreeData.lua so EVERY node uses the same flat-top honeycomb lattice.

Run from the Arcadia-Vide repo root:
    python update_stats_tree_all_hexes_honeycomb.py --dry-run
    python update_stats_tree_all_hexes_honeycomb.py

Target:
    src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua

What this fixes:
- The 3 starter category hubs already use a honeycomb layout.
- This patch makes ALL branch nodes use the exact same lattice too.
- Unknown / future nodes are also placed on that same lattice, so they do not float
  or overlap awkwardly.
- Economy, Skills, and Stamina branches all expand with visually matching hex spacing.

Notes:
- This rewrites StatsTreeData.lua fully on purpose, because the layout is easier to
  maintain cleanly when it is described from one coordinate system.
- It does NOT touch StatsTree/init.lua logic.
- You can tune spacing with HEX_STEP_X / HEX_STEP_Y inside the generated Lua file.
"""

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime
from pathlib import Path

TARGET = Path("src/client/UI/UIManager/Menus/StatsTree/StatsTreeData.lua")

NEW_LUA = """--!strict

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

-- Flat-top hex honeycomb spacing.
-- Adjust these two values only if you want the global gap tighter or wider.
local HEX_STEP_X = 118
local HEX_STEP_Y = 68

-- Build a consistent honeycomb lattice.
-- Basis vectors:
--   east      = ( HEX_STEP_X, 0 )
--   southEast = ( HEX_STEP_X/2, HEX_STEP_Y )
-- This lets every node live on the same hex grid.
local function H(origin: Vector2, q: number, r: number): Vector2
\treturn origin + Vector2.new(
\t\t(q * HEX_STEP_X) + (r * (HEX_STEP_X / 2)),
\t\tr * HEX_STEP_Y
\t)
end

-- Root layout:
--          Economy
--     Skills      Stamina
--
-- These are already in honeycomb relation and now ALL child nodes follow the same system.
local ECONOMY = Vector2.new(0, -HEX_STEP_Y)
local SKILLS = Vector2.new(-HEX_STEP_X, 0)
local STAMINA = Vector2.new(HEX_STEP_X, 0)

local nodes: { NodeDefinition } = {
\t-- Root category hubs.
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
\t-- ECONOMY BRANCH (all nodes on same honeycomb lattice)
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
\t\tposition = H(ECONOMY, -1, 0),
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
\t\tposition = H(ECONOMY, 0, -1),
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
\t\tposition = H(ECONOMY, 1, -1),
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
\t\tposition = H(ECONOMY, -1, 1),
\t},
\t{
\t\tid = "Lucky",
\t\tkind = "Stat",
\t\tgroupId = "Economy",
\t\ttitle = "Lucky",
\t\teffectShort = "+2%",
\t\tdescription = "+2% Luck per level.",
\t\tmaxLevel = 10,
\t\tposition = H(ECONOMY, 0, 1),
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
\t\tposition = H(ECONOMY, -2, 0),
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
\t\tposition = H(ECONOMY, 0, 2),
\t\trequires = {
\t\t\t{ nodeId = "Lucky", minLevel = 1 },
\t\t},
\t},

\t-- ============================================================
\t-- SKILLS BRANCH (same honeycomb structure)
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
\t\tposition = H(SKILLS, -1, 0),
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
\t\tposition = H(SKILLS, 0, -1),
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
\t\tposition = H(SKILLS, -1, 1),
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
\t\tposition = H(SKILLS, -1, -1),
\t\trequires = {
\t\t\t{ nodeId = "SkillPower", minLevel = 1 },
\t\t},
\t},

\t-- ============================================================
\t-- STAMINA BRANCH (same honeycomb structure)
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
\t\tposition = H(STAMINA, 1, 0),
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
\t\tposition = H(STAMINA, 0, 1),
\t},
\t{
\t\tid = "Endurance",
\t\tkind = "Stat",
\t\tgroupId = "Stamina",
\t\ttitle = "Endurance",
\t\teffectShort = "+5%",
\t\tdescription = "Future survival upgrade.",
\t\tmaxLevel = 10,
\t\tposition = H(STAMINA, 1, 1),
\t\trequires = {
\t\t\t{ nodeId = "MaxStamina", minLevel = 1 },
\t\t},
\t},
}

return {
\tnodes = nodes,
}
"""

def unified_diff(path: Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"{path} (before)",
            tofile=f"{path} (after)",
        )
    )

def backup_file(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(".patch_backups") / "update_stats_tree_all_hexes_honeycomb" / stamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / path.name
    shutil.copy2(path, backup_path)
    return backup_path

def main() -> int:
    parser = argparse.ArgumentParser(description="Make all StatsTree nodes follow the same honeycomb structure.")
    parser.add_argument("--dry-run", action="store_true", help="Show the diff only.")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation.")
    args = parser.parse_args()

    path = Path.cwd() / TARGET
    if not path.exists():
        print(f"ERROR: Could not find {TARGET}")
        print("Run this script from the Arcadia-Vide repository root.")
        return 1

    before = path.read_text(encoding="utf-8")
    after = NEW_LUA

    if before == after:
        print("No changes needed. StatsTreeData.lua already uses the full honeycomb layout.")
        return 0

    print("Planned update:")
    print("  - Rewrite StatsTreeData.lua so EVERY node uses the same flat-top honeycomb lattice.")
    print("  - Root category hubs remain honeycomb aligned.")
    print("  - Economy / Skills / Stamina child nodes also use honeycomb neighbor offsets.")
    print("  - Future '?' nodes stay on that same lattice, so their placement matches too.")
    print()
    print(unified_diff(TARGET, before, after))

    if args.dry_run:
        print("Dry run complete. No files were changed.")
        return 0

    if not args.no_backup:
        backup_path = backup_file(path)
        print(f"Backup created: {backup_path}")

    path.write_text(after, encoding="utf-8")
    print(f"Updated: {TARGET}")
    print()
    print("If you want the hexes slightly tighter or looser, edit inside StatsTreeData.lua:")
    print("  local HEX_STEP_X = 118")
    print("  local HEX_STEP_Y = 68")
    print()
    print("Recommended check after patch:")
    print("  1) Open StatsTree root and open each branch.")
    print("  2) Verify Economy / Skills / Stamina child nodes now sit on the same honeycomb structure.")
    print("  3) If one cluster feels too wide or tight, adjust HEX_STEP_X / HEX_STEP_Y a little.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
