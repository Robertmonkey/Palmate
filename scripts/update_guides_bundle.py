#!/usr/bin/env python3
"""Apply structured patches to ``data/guides.bundle.json`` safely."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_BUNDLE_PATH = REPO_ROOT / "data" / "guides.bundle.json"
DEFAULT_BACKUP_PATH = REPO_ROOT / "data" / "Guide.bundle.backup.JSON"

# Make ``scripts`` importable so we can reuse the validator helpers.
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_guides_bundle  # type: ignore  # noqa: E402


class PatchError(RuntimeError):
    """Raised when a patch payload is malformed."""


@dataclass
class PatchSummary:
    """Human-readable summary of the applied operations."""

    lines: list[str]

    def add(self, message: str) -> None:
        self.lines.append(message)

    def extend(self, messages: Iterable[str]) -> None:
        self.lines.extend(messages)

    def __bool__(self) -> bool:  # pragma: no cover - convenience only
        return bool(self.lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Apply a structured patch to data/guides.bundle.json without risking "
            "wholesale data loss."
        )
    )
    parser.add_argument(
        "patch",
        type=Path,
        help="Path to the JSON patch describing the desired bundle edits.",
    )
    parser.add_argument(
        "--bundle",
        type=Path,
        default=DEFAULT_BUNDLE_PATH,
        help="Path to the bundle file to update (defaults to data/guides.bundle.json).",
    )
    parser.add_argument(
        "--backup",
        type=Path,
        default=DEFAULT_BACKUP_PATH,
        help=(
            "Baseline snapshot used for loss detection (defaults to "
            "data/Guide.bundle.backup.JSON)."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the computed changes without writing the bundle to disk.",
    )
    parser.add_argument(
        "--skip-guard",
        action="store_true",
        help="Skip the baseline loss guard (not recommended).",
    )
    parser.add_argument(
        "--allow-route-removals",
        action="store_true",
        help="Permit removing existing routes when intentionally deprecating them.",
    )
    parser.add_argument(
        "--allow-step-removals",
        action="store_true",
        help="Permit removing existing route steps when intentionally pruning them.",
    )
    parser.add_argument(
        "--allow-guide-removals",
        action="store_true",
        help="Permit removing existing guide catalog entries when pruning them.",
    )
    parser.add_argument(
        "--update-backup",
        action="store_true",
        help="Refresh the baseline snapshot after a successful write.",
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_patch_payload(patch: Any) -> dict[str, Any]:
    if not isinstance(patch, dict):
        raise PatchError("Patch payload must be a JSON object at the top level.")
    return patch


def ensure_section(bundle: dict[str, Any], key: str, expected_type: type) -> Any:
    value = bundle.get(key)
    if value is None:
        if expected_type is dict:
            value = {}
        elif expected_type is list:
            value = []
        else:
            value = expected_type()
        bundle[key] = value
    if not isinstance(value, expected_type):
        raise PatchError(
            f"Bundle section '{key}' must be a {expected_type.__name__}, found {type(value).__name__}."
        )
    return value


def deep_merge(target: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


def apply_indexed_list_patch(
    *,
    items: list[dict[str, Any]],
    id_field: str,
    ops: dict[str, Any],
    entity_label: str,
) -> list[str]:
    summary: list[str] = []
    index: dict[Any, int] = {}

    def rebuild_index() -> None:
        index.clear()
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            identifier = item.get(id_field)
            if identifier is not None:
                index[identifier] = idx

    rebuild_index()

    if "remove" in ops:
        removals = ops["remove"]
        if not isinstance(removals, list):
            raise PatchError(f"'{entity_label}.remove' must be a list of identifiers.")
        missing = [identifier for identifier in removals if identifier not in index]
        if missing:
            raise PatchError(
                f"Cannot remove {entity_label} entries that do not exist: {', '.join(missing)}"
            )
        to_remove = set(removals)
        original_len = len(items)
        items[:] = [
            item
            for item in items
            if not isinstance(item, dict)
            or item.get(id_field) not in to_remove
        ]
        removed_count = original_len - len(items)
        if removed_count:
            summary.append(f"Removed {removed_count} {entity_label} entries.")
        rebuild_index()

    if "merge" in ops:
        merges = ops["merge"]
        if not isinstance(merges, dict):
            raise PatchError(f"'{entity_label}.merge' must be an object keyed by identifier.")
        for identifier, fragment in merges.items():
            if identifier not in index:
                raise PatchError(
                    f"Cannot merge into unknown {entity_label} entry '{identifier}'."
                )
            if not isinstance(fragment, dict):
                raise PatchError(
                    f"Merge fragment for {entity_label} '{identifier}' must be an object."
                )
            deep_merge(items[index[identifier]], fragment)
        if merges:
            summary.append(f"Merged updates into {len(merges)} {entity_label} entries.")

    if "replace" in ops:
        replacements = ops["replace"]
        if not isinstance(replacements, list):
            raise PatchError(f"'{entity_label}.replace' must be a list of objects.")
        replaced = 0
        for entry in replacements:
            if not isinstance(entry, dict):
                raise PatchError(
                    f"Every object in '{entity_label}.replace' must be a dictionary."
                )
            identifier = entry.get(id_field)
            if not isinstance(identifier, str) or not identifier:
                raise PatchError(
                    f"Replacement entries must include a non-empty '{id_field}'."
                )
            if identifier not in index:
                raise PatchError(
                    f"Cannot replace unknown {entity_label} entry '{identifier}'."
                )
            items[index[identifier]] = entry
            replaced += 1
        if replaced:
            summary.append(f"Replaced {replaced} {entity_label} entries.")
        rebuild_index()

    if "add" in ops:
        additions = ops["add"]
        if not isinstance(additions, list):
            raise PatchError(f"'{entity_label}.add' must be a list of objects.")
        added = 0
        for entry in additions:
            if not isinstance(entry, dict):
                raise PatchError(
                    f"Every object in '{entity_label}.add' must be a dictionary."
                )
            identifier = entry.get(id_field)
            if not isinstance(identifier, str) or not identifier:
                raise PatchError(
                    f"Added entries must include a non-empty '{id_field}'."
                )
            if identifier in index:
                raise PatchError(
                    f"Cannot add duplicate {entity_label} entry '{identifier}'."
                )
            items.append(entry)
            index[identifier] = len(items) - 1
            added += 1
        if added:
            summary.append(f"Added {added} new {entity_label} entries.")

    return summary


def apply_routes_patch(bundle: dict[str, Any], ops: dict[str, Any]) -> list[str]:
    routes = ensure_section(bundle, "routes", list)
    return apply_indexed_list_patch(
        items=routes,
        id_field="route_id",
        ops=ops,
        entity_label="route",
    )


def apply_catalog_patch(bundle: dict[str, Any], patch: dict[str, Any]) -> list[str]:
    guide_catalog = ensure_section(bundle, "guideCatalog", dict)
    summary: list[str] = []

    if "set" in patch:
        set_payload = patch["set"]
        if not isinstance(set_payload, dict):
            raise PatchError("'guideCatalog.set' must be an object.")
        deep_merge(guide_catalog, set_payload)
        summary.append("Updated guideCatalog metadata fields via merge.")

    guides_ops = patch.get("guides")
    if guides_ops is not None:
        if not isinstance(guides_ops, dict):
            raise PatchError("'guideCatalog.guides' must be an object describing operations.")
        data = ensure_section(guide_catalog, "data", dict)
        guides = ensure_section(data, "guides", list)
        summary.extend(
            apply_indexed_list_patch(
                items=guides,
                id_field="id",
                ops=guides_ops,
                entity_label="guide catalog",
            )
        )

    expected_count = patch.get("expected_final_count")
    guides_list = guide_catalog.get("data", {}).get("guides")
    if isinstance(guides_list, list):
        actual_count = len(guides_list)
        guide_catalog["guide_count"] = actual_count
        if expected_count is not None and expected_count != actual_count:
            raise PatchError(
                "guideCatalog.expected_final_count does not match the resulting "
                f"guide count ({expected_count} expected vs {actual_count} actual)."
            )
    elif expected_count is not None:
        raise PatchError("guideCatalog.data.guides must exist when asserting a final count.")

    return summary


def apply_generic_section(
    bundle: dict[str, Any], key: str, payload: Any, summary: PatchSummary
) -> None:
    current = bundle.get(key)
    if isinstance(payload, dict) and isinstance(current, dict):
        deep_merge(current, payload)
        summary.add(f"Merged updates into existing '{key}' section.")
    else:
        bundle[key] = payload
        action = "Replaced" if current is not None else "Set"
        summary.add(f"{action} bundle section '{key}'.")


def apply_patch(bundle: dict[str, Any], patch: dict[str, Any]) -> PatchSummary:
    summary = PatchSummary(lines=[])
    for key, value in patch.items():
        if key == "routes":
            if not isinstance(value, dict):
                raise PatchError("'routes' patch must be an object of operations.")
            summary.extend(apply_routes_patch(bundle, value))
        elif key == "guideCatalog":
            if not isinstance(value, dict):
                raise PatchError("'guideCatalog' patch must be an object of operations.")
            summary.extend(apply_catalog_patch(bundle, value))
        else:
            apply_generic_section(bundle, key, value, summary)
    return summary


def format_summary(summary: PatchSummary) -> str:
    if not summary.lines:
        return "No changes were applied."
    return "\n".join(f"- {line}" for line in summary.lines)


def write_bundle(path: Path, serialized: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as handle:
        handle.write(serialized)
        temp_path = Path(handle.name)
    shutil.move(str(temp_path), path)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bundle_path = args.bundle.resolve()
    backup_path = args.backup.resolve()

    if not bundle_path.exists():
        print(f"Bundle missing at {bundle_path}", file=sys.stderr)
        return 1

    try:
        bundle = load_json(bundle_path)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        print(f"Failed to parse bundle JSON: {exc}", file=sys.stderr)
        return 1

    try:
        patch_payload = validate_patch_payload(load_json(args.patch))
    except (json.JSONDecodeError, PatchError) as exc:
        print(f"Patch file invalid: {exc}", file=sys.stderr)
        return 1

    working_bundle = deepcopy(bundle)

    try:
        summary = apply_patch(working_bundle, patch_payload)
    except PatchError as exc:
        print(f"Patch application failed: {exc}", file=sys.stderr)
        return 1

    try:
        (
            route_count,
            guide_count,
            current_route_ids,
            current_guide_ids,
            current_step_ids,
        ) = check_guides_bundle.check_structure(working_bundle)
    except ValueError as exc:
        print(f"Resulting bundle is invalid: {exc}", file=sys.stderr)
        return 1

    serialized_text = json.dumps(working_bundle, indent=2, ensure_ascii=False) + "\n"
    bundle_size = len(serialized_text.encode("utf-8"))

    if not args.skip_guard:
        try:
            check_guides_bundle.guard_against_data_loss(
                route_count=route_count,
                guide_count=guide_count,
                bundle_size=bundle_size,
                backup_path=backup_path,
                current_route_ids=current_route_ids,
                current_guide_ids=current_guide_ids,
                current_step_ids=current_step_ids,
                allow_route_removals=args.allow_route_removals,
                allow_guide_removals=args.allow_guide_removals,
                allow_step_removals=args.allow_step_removals,
            )
        except ValueError as exc:
            print(f"Loss guard failed: {exc}", file=sys.stderr)
            return 1

    print("Patch applied successfully:")
    print(format_summary(summary))
    print(
        f"Resulting bundle stats: {route_count} routes, {guide_count} catalog entries, "
        f"{bundle_size} bytes."
    )

    if args.dry_run:
        print("Dry run requested; bundle not written.")
        return 0

    write_bundle(bundle_path, serialized_text)
    print(f"Wrote updated bundle to {bundle_path}.")

    if args.update_backup:
        check_guides_bundle.refresh_backup(bundle_path, backup_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
