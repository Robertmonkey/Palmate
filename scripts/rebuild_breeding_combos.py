#!/usr/bin/env python3
"""Rebuild breeding combos from breeding power values.

This helper enforces Palworld's breeding formula—average the parent
breeding power, round down, then select the pal whose power is closest to
that floor. Running the script keeps our stored combos aligned with the
actual game results and strips out unverified recipes.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import inf
from pathlib import Path
from typing import Iterable, List, Mapping, MutableMapping, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_DATASETS = (
    DATA_DIR / "palworld_complete_data_final.json",
    DATA_DIR / "palworld_complete_data_enhanced.json",
)
MAX_COMBOS = 12


@dataclass(frozen=True)
class Pal:
    id: int
    name: str
    power: int


def load_dataset(path: Path) -> MutableMapping[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_breeding_pals(dataset: Mapping[str, object]) -> Iterable[Pal]:
    pals = dataset.get("pals", {})
    for pal in pals.values():
        breeding = pal.get("breeding") if isinstance(pal, dict) else None
        power = breeding.get("power") if isinstance(breeding, dict) else None
        name = pal.get("name") if isinstance(pal, dict) else None
        if not isinstance(power, (int, float)):
            continue
        if not isinstance(name, str):
            continue
        pal_id = pal.get("id")
        if not isinstance(pal_id, int):
            continue
        yield Pal(id=pal_id, name=name, power=int(power))


def build_child_lookup(pals: Sequence[Pal]) -> Mapping[int, List[Tuple[str, str]]]:
    combos = {pal.id: set() for pal in pals}
    pals_by_id = sorted(pals, key=lambda p: p.id)

    for index, left in enumerate(pals_by_id):
        for right in pals_by_id[index:]:
            avg_power = (left.power + right.power) // 2
            closest = pals_by_id[0]
            diff = abs(closest.power - avg_power)
            for candidate in pals_by_id[1:]:
                delta = abs(candidate.power - avg_power)
                if delta < diff:
                    closest = candidate
                    diff = delta
            pair = tuple(sorted((left.name, right.name)))
            combos.setdefault(closest.id, set()).add(pair)

    return {pal_id: sorted(pairs) for pal_id, pairs in combos.items()}


def update_dataset(dataset: MutableMapping[str, object], combos: Mapping[int, List[Tuple[str, str]]], max_combos: int) -> bool:
    changed = False
    pals = dataset.get("pals")
    if not isinstance(pals, dict):
        return False

    name_to_power = {
        pal.name: pal.power
        for pal in iter_breeding_pals(dataset)
    }

    for pal_data in pals.values():
        if not isinstance(pal_data, dict):
            continue
        pal_id = pal_data.get("id")
        if not isinstance(pal_id, int):
            continue
        breeding = pal_data.get("breeding") if isinstance(pal_data, dict) else None
        power = breeding.get("power") if isinstance(breeding, dict) else None
        if not isinstance(power, (int, float)):
            # Preserve existing combos for pals without numeric breeding power
            continue

        pair_list = combos.get(pal_id, [])
        # Sort by total breeding power so the easiest combinations surface first
        pair_list = sorted(
            pair_list,
            key=lambda pair: (
                name_to_power.get(pair[0], inf) + name_to_power.get(pair[1], inf),
                pair[0],
                pair[1],
            ),
        )
        limited = [list(pair) for pair in pair_list[:max_combos]]
        if pal_data.get("breedingCombos") != limited:
            pal_data["breedingCombos"] = limited
            changed = True

    return changed


def save_dataset(path: Path, dataset: Mapping[str, object]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(dataset, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Dataset files to update (defaults to final and enhanced datasets)",
    )
    parser.add_argument(
        "--max-combos",
        type=int,
        default=MAX_COMBOS,
        help="Limit the number of combos stored per pal",
    )
    args = parser.parse_args()

    targets_raw = args.paths or list(DEFAULT_DATASETS)
    targets = []
    for path in targets_raw:
        resolved = path if path.is_absolute() else (ROOT / path)
        targets.append(resolved)
    if not targets:
        raise SystemExit("No dataset paths supplied")

    any_changed = False
    for dataset_path in targets:
        dataset = load_dataset(dataset_path)
        pals_for_file = list(iter_breeding_pals(dataset))
        if not pals_for_file:
            print(f"Skipping {dataset_path}: no pals with breeding power")
            continue
        combos_for_file = build_child_lookup(pals_for_file)
        changed = update_dataset(dataset, combos_for_file, args.max_combos)
        if changed:
            save_dataset(dataset_path, dataset)
            try:
                display_path = dataset_path.relative_to(ROOT)
            except ValueError:
                display_path = dataset_path
            print(f"Updated breeding combos in {display_path}")
            any_changed = True
        else:
            try:
                display_path = dataset_path.relative_to(ROOT)
            except ValueError:
                display_path = dataset_path
            print(f"No breeding combo changes needed for {display_path}")

    if not any_changed:
        print("Breeding combos already up to date")


if __name__ == "__main__":
    main()
