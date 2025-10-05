#!/usr/bin/env python3
"""Apply safe, validated updates to ``data/guide_catalog.json``."""

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
DEFAULT_CATALOG_PATH = REPO_ROOT / "data" / "guide_catalog.json"
DEFAULT_BACKUP_PATH = REPO_ROOT / "data" / "guide_catalog.backup.json"
DEFAULT_BUNDLE_PATH = REPO_ROOT / "data" / "guides.bundle.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_guides_bundle  # type: ignore  # noqa: E402


class PatchError(RuntimeError):
    """Raised when a patch payload is malformed."""


@dataclass
class PatchSummary:
    """Collects log messages describing applied operations."""

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
            "Apply a structured patch to data/guide_catalog.json with validation, "
            "loss guarding, and strict schema checks."
        )
    )
    parser.add_argument(
        "patch",
        type=Path,
        help="Path to the JSON patch describing catalog edits.",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_CATALOG_PATH,
        help="Path to the catalog file (defaults to data/guide_catalog.json).",
    )
    parser.add_argument(
        "--backup",
        type=Path,
        default=DEFAULT_BACKUP_PATH,
        help="Baseline snapshot used for loss detection (defaults to data/guide_catalog.backup.json).",
    )
    parser.add_argument(
        "--bundle",
        type=Path,
        default=DEFAULT_BUNDLE_PATH,
        help=(
            "Path to data/guides.bundle.json used for strict validation. "
            "The script patches the bundle in-memory to reuse the validator."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the computed changes without writing the catalog to disk.",
    )
    parser.add_argument(
        "--skip-guard",
        action="store_true",
        help="Skip loss guarding against the backup snapshot (not recommended).",
    )
    parser.add_argument(
        "--allow-removals",
        action="store_true",
        help="Permit removing catalog entries when intentionally pruning them.",
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


def ensure_list(container: dict[str, Any], key: str) -> list[Any]:
    value = container.get(key)
    if value is None:
        value = []
        container[key] = value
    if not isinstance(value, list):
        raise PatchError(f"Catalog field '{key}' must be an array.")
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
    index = {item[id_field]: idx for idx, item in enumerate(items) if id_field in item}

    def rebuild_index() -> None:
        index.clear()
        index.update({item[id_field]: idx for idx, item in enumerate(items) if id_field in item})

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
        items[:] = [item for item in items if item[id_field] not in to_remove]
        summary.append(f"Removed {len(to_remove)} {entity_label} entries.")
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


def apply_patch(catalog: dict[str, Any], patch: dict[str, Any]) -> PatchSummary:
    summary = PatchSummary(lines=[])

    if "set" in patch:
        set_payload = patch["set"]
        if not isinstance(set_payload, dict):
            raise PatchError("'set' payload must be an object.")
        deep_merge(catalog, set_payload)
        summary.add("Merged top-level catalog fields via set payload.")

    if "guides" in patch:
        guides_ops = patch["guides"]
        if not isinstance(guides_ops, dict):
            raise PatchError("'guides' patch must be an object describing operations.")
        guides = ensure_list(catalog, "guides")
        summary.extend(
            apply_indexed_list_patch(
                items=guides,
                id_field="id",
                ops=guides_ops,
                entity_label="guide catalog",
            )
        )

    expected_count = patch.get("expected_final_count")
    guides_list = catalog.get("guides")
    if isinstance(guides_list, list):
        actual_count = len(guides_list)
        if expected_count is not None and expected_count != actual_count:
            raise PatchError(
                "expected_final_count does not match resulting guide count "
                f"({expected_count} expected vs {actual_count} actual)."
            )
    elif expected_count is not None:
        raise PatchError("Catalog must include a 'guides' array when asserting final count.")

    return summary


def guard_against_data_loss(
    *,
    updated_catalog: dict[str, Any],
    backup_path: Path,
    allow_removals: bool,
) -> None:
    if not backup_path.exists():
        print(
            "[guide catalog update] No baseline snapshot found; skipping loss guard.",
            file=sys.stderr,
        )
        return

    try:
        baseline = load_json(backup_path)
    except json.JSONDecodeError as exc:
        raise PatchError(f"Backup catalog is not valid JSON: {exc}") from exc

    baseline_guides = baseline.get("guides", []) or []
    if not isinstance(baseline_guides, list):
        raise PatchError("Backup catalog 'guides' field must be a list.")

    new_guides = updated_catalog.get("guides", []) or []
    if not isinstance(new_guides, list):
        raise PatchError("Updated catalog 'guides' field must be a list.")

    baseline_ids = {guide.get("id") for guide in baseline_guides if isinstance(guide, dict)}
    new_ids = {guide.get("id") for guide in new_guides if isinstance(guide, dict)}

    removed = sorted(identifier for identifier in baseline_ids - new_ids if identifier)
    added = sorted(identifier for identifier in new_ids - baseline_ids if identifier)

    if removed:
        message = (
            "Guide catalog entries removed relative to baseline: "
            + ", ".join(removed[:10])
        )
        if len(removed) > 10:
            message += f" ... (+{len(removed) - 10} more)"
        if allow_removals:
            print(f"[guide catalog update] {message}")
        else:
            raise PatchError(message)

    if added:
        print(
            "[guide catalog update] New guide catalog entries relative to baseline: "
            + ", ".join(added[:10])
            + (" ..." if len(added) > 10 else "")
        )

    serialized = json.dumps(updated_catalog, ensure_ascii=False, indent=2)
    new_size = len(serialized.encode("utf-8"))
    backup_size = backup_path.stat().st_size
    if backup_size and new_size < backup_size:
        ratio = new_size / backup_size
        if ratio < 0.9:
            raise PatchError(
                "Catalog file size shrank dramatically "
                f"({backup_size} -> {new_size}; ratio {ratio:.2%})."
            )


def validate_catalog_strict(
    catalog: dict[str, Any], *, bundle_path: Path
) -> None:
    if not bundle_path.exists():
        raise PatchError(
            f"Guides bundle missing at {bundle_path}; cannot run strict validation."
        )

    try:
        bundle = load_json(bundle_path)
    except json.JSONDecodeError as exc:
        raise PatchError(f"Guides bundle is not valid JSON: {exc}") from exc

    working_bundle = deepcopy(bundle)
    guide_catalog = working_bundle.get("guideCatalog")
    if not isinstance(guide_catalog, dict):
        raise PatchError("Guides bundle is missing the 'guideCatalog' section.")

    guide_catalog["data"] = catalog
    guide_catalog["guide_count"] = len(catalog.get("guides", []))

    try:
        check_guides_bundle.check_structure(working_bundle)
        check_guides_bundle.run_strict_checks(working_bundle)
    except ValueError as exc:
        raise PatchError(f"Strict validation failed: {exc}") from exc


def write_catalog(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=path.parent
    ) as handle:
        handle.write(payload)
        temp_path = Path(handle.name)
    shutil.move(str(temp_path), path)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    catalog_path = args.catalog.resolve()
    backup_path = args.backup.resolve()
    bundle_path = args.bundle.resolve()

    if not catalog_path.exists():
        print(f"Catalog missing at {catalog_path}", file=sys.stderr)
        return 1

    try:
        catalog = load_json(catalog_path)
    except json.JSONDecodeError as exc:
        print(f"Failed to parse catalog JSON: {exc}", file=sys.stderr)
        return 1

    try:
        patch_payload = validate_patch_payload(load_json(args.patch))
    except (json.JSONDecodeError, PatchError) as exc:
        print(f"Patch file invalid: {exc}", file=sys.stderr)
        return 1

    working_catalog = deepcopy(catalog)

    try:
        summary = apply_patch(working_catalog, patch_payload)
    except PatchError as exc:
        print(f"Patch application failed: {exc}", file=sys.stderr)
        return 1

    try:
        validate_catalog_strict(working_catalog, bundle_path=bundle_path)
    except PatchError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    serialized = json.dumps(working_catalog, ensure_ascii=False, indent=2) + "\n"

    if not args.skip_guard:
        try:
            guard_against_data_loss(
                updated_catalog=working_catalog,
                backup_path=backup_path,
                allow_removals=args.allow_removals,
            )
        except PatchError as exc:
            print(f"Loss guard failed: {exc}", file=sys.stderr)
            return 1

    print("Patch applied successfully:")
    if summary:
        print("\n".join(f"- {line}" for line in summary.lines))
    else:
        print("- No structural changes detected (patch may have only adjusted ordering).")

    print(f"Resulting catalog contains {len(working_catalog.get('guides', []))} guides.")

    if args.dry_run:
        print("Dry run requested; catalog not written.")
        return 0

    write_catalog(catalog_path, serialized)
    print(f"Wrote updated catalog to {catalog_path}.")

    if args.update_backup:
        write_catalog(backup_path, serialized)
        print(f"Updated backup snapshot at {backup_path}.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
