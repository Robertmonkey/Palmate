#!/usr/bin/env python3
"""Validate and safeguard the fallback guide bundle.

This script performs structural validation of ``data/guides.bundle.json`` and,
when a baseline snapshot is available, ensures the new bundle has not lost a
large number of routes or catalog entries.  It can optionally refresh the
baseline once the current bundle passes all checks.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

BUNDLE_PATH = Path(__file__).resolve().parent.parent / "data" / "guides.bundle.json"
BACKUP_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "Guide.bundle.backup.JSON"
)

REQUIRED_TOP_LEVEL_KEYS = {
    "metadata",
    "xp",
    "routes",
    "routeSchema",
    "levelEstimator",
    "recommender",
    "guideCatalog",
    "sourceRegistry",
    "extras",
}

REQUIRED_ROUTE_FIELDS = {
    "route_id",
    "title",
    "category",
    "tags",
    "progression_role",
    "recommended_level",
    "modes",
    "prerequisites",
    "objectives",
    "estimated_time_minutes",
    "estimated_xp_gain",
    "risk_profile",
    "failure_penalties",
    "adaptive_guidance",
    "checkpoints",
    "steps",
    "completion_criteria",
    "yields",
    "metrics",
    "next_routes",
}

OPTIONAL_ROUTE_FIELDS = {"supporting_routes", "failure_recovery"}

ROUTE_FIELD_TYPES = {
    "route_id": str,
    "title": str,
    "category": str,
    "tags": list,
    "progression_role": str,
    "recommended_level": dict,
    "modes": dict,
    "prerequisites": dict,
    "objectives": list,
    "estimated_time_minutes": dict,
    "estimated_xp_gain": dict,
    "risk_profile": str,
    "failure_penalties": dict,
    "adaptive_guidance": dict,
    "checkpoints": list,
    "steps": list,
    "completion_criteria": list,
    "yields": dict,
    "metrics": dict,
    "next_routes": list,
}

REQUIRED_STEP_FIELDS = {"step_id", "type", "summary", "detail"}

REQUIRED_GUIDE_FIELDS = {
    "id",
    "title",
    "source_heading",
    "category",
    "category_group",
    "trigger",
    "keywords",
    "steps",
}


def _counter_differences(
    baseline: Counter[str], current: Counter[str]
) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    """Return entries removed from and added to ``baseline`` relative to ``current``."""

    removed: list[tuple[str, int]] = []
    for key, count in baseline.items():
        delta = count - current.get(key, 0)
        if delta > 0:
            removed.append((key, delta))

    added: list[tuple[str, int]] = []
    for key, count in current.items():
        delta = count - baseline.get(key, 0)
        if delta > 0:
            added.append((key, delta))

    removed.sort(key=lambda item: item[0])
    added.sort(key=lambda item: item[0])
    return removed, added


def _format_counter_entries(entries: list[tuple[str, int]]) -> str:
    """Render counter differences with multiplicities when counts exceed one."""

    if not entries:
        return ""

    display = []
    for key, count in entries[:10]:
        if count > 1:
            display.append(f"{key} (x{count})")
        else:
            display.append(key)

    if len(entries) > 10:
        remaining = sum(count for _, count in entries[10:])
        display.append(f"...(+{remaining} more)")

    return ", ".join(display)


def analyze_routes(
    bundle: dict, *, emit_duplicate_warnings: bool = True
) -> tuple[Counter[str], Counter[str]]:
    """Validate route structures and return route/step identifiers."""

    routes = bundle.get("routes")
    if not isinstance(routes, list) or not routes:
        raise ValueError("bundle must contain a non-empty 'routes' array")

    route_ids: Counter[str] = Counter()
    step_ids: Counter[str] = Counter()

    for index, route in enumerate(routes):
        if not isinstance(route, dict):
            raise ValueError(f"route at index {index} must be an object")

        missing_fields = REQUIRED_ROUTE_FIELDS.difference(route)
        if missing_fields:
            identifier = route.get("route_id", f"index {index}")
            raise ValueError(
                "route "
                f"{identifier} missing required fields: "
                + ", ".join(sorted(missing_fields))
            )

        unknown_fields = set(route.keys()) - (
            REQUIRED_ROUTE_FIELDS | OPTIONAL_ROUTE_FIELDS
        )
        if unknown_fields:
            # Unknown keys are likely schema additions; warn loudly so the
            # validator can be kept in sync instead of silently ignoring them.
            print(
                "[guides bundle validation] Warning: route "
                f"{route['route_id']} includes unrecognised fields: "
                + ", ".join(sorted(unknown_fields)),
                file=sys.stderr,
            )

        route_id = route["route_id"]
        if not isinstance(route_id, str) or not route_id:
            raise ValueError(
                f"route at index {index} has an invalid route_id: {route_id!r}"
            )
        prior_count = route_ids[route_id]
        route_ids[route_id] += 1
        if prior_count and emit_duplicate_warnings:
            print(
                "[guides bundle validation] Warning: duplicate route_id encountered: "
                f"{route_id} (count now {route_ids[route_id]})",
                file=sys.stderr,
            )

        for field, expected_type in ROUTE_FIELD_TYPES.items():
            value = route[field]
            if not isinstance(value, expected_type):
                raise ValueError(
                    f"route {route_id} field '{field}' must be a "
                    f"{expected_type.__name__}"
                )
            if field in {"objectives", "steps", "completion_criteria", "checkpoints", "tags"} and not value:
                raise ValueError(
                    f"route {route_id} field '{field}' must not be empty"
                )

        for optional_field in OPTIONAL_ROUTE_FIELDS:
            if optional_field in route and not isinstance(route[optional_field], dict):
                raise ValueError(
                    f"route {route_id} field '{optional_field}' must be an object"
                )

        steps = route["steps"]
        for step_index, step in enumerate(steps):
            if not isinstance(step, dict):
                raise ValueError(
                    f"route {route_id} step at index {step_index} must be an object"
                )
            missing_step_fields = REQUIRED_STEP_FIELDS.difference(step)
            if missing_step_fields:
                raise ValueError(
                    "route "
                    f"{route_id} step at index {step_index} missing required fields: "
                    + ", ".join(sorted(missing_step_fields))
                )
            step_id = step["step_id"]
            if not isinstance(step_id, str) or not step_id:
                raise ValueError(
                    f"route {route_id} step at index {step_index} has an invalid step_id: {step_id!r}"
                )
            prior_step_count = step_ids[step_id]
            step_ids[step_id] += 1
            if prior_step_count and emit_duplicate_warnings:
                print(
                    "[guides bundle validation] Warning: duplicate step_id encountered: "
                    f"{step_id} (count now {step_ids[step_id]})",
                    file=sys.stderr,
                )

    return route_ids, step_ids


def extract_catalog_ids(bundle: dict) -> set[str]:
    """Validate guide catalog entries and return their identifiers."""

    guide_catalog = bundle.get("guideCatalog", {})
    guides = guide_catalog.get("data", {}).get("guides", []) or []
    guide_ids: set[str] = set()

    for index, guide in enumerate(guides):
        if not isinstance(guide, dict):
            raise ValueError(
                f"guide catalog entry at index {index} must be an object"
            )

        missing_fields = REQUIRED_GUIDE_FIELDS.difference(guide)
        if missing_fields:
            identifier = guide.get("id", f"index {index}")
            raise ValueError(
                "guide catalog entry "
                f"{identifier} missing required fields: "
                + ", ".join(sorted(missing_fields))
            )

        guide_id = guide["id"]
        if not isinstance(guide_id, str) or not guide_id:
            raise ValueError(
                "guide catalog entry at index "
                f"{index} has an invalid id: {guide_id!r}"
            )
        if guide_id in guide_ids:
            raise ValueError(f"duplicate guide catalog id encountered: {guide_id}")
        guide_ids.add(guide_id)

        for field in ("title", "source_heading", "trigger"):
            value = guide[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"guide catalog entry {guide_id} field '{field}' must be a non-empty string"
                )

        if not isinstance(guide["keywords"], list) or not guide["keywords"]:
            raise ValueError(
                f"guide catalog entry {guide_id} must include at least one keyword"
            )

        if not isinstance(guide["steps"], list) or not guide["steps"]:
            raise ValueError(
                f"guide catalog entry {guide_id} must include a non-empty steps array"
            )

        if "shortage_menu" in guide and not isinstance(guide["shortage_menu"], bool):
            raise ValueError(
                f"guide catalog entry {guide_id} field 'shortage_menu' must be a boolean"
            )

    return guide_ids

MIN_ROUTE_RATIO = 0.95
MIN_GUIDE_RATIO = 0.95
MAX_ROUTE_DROP = 2
MAX_GUIDE_DROP = 2
MIN_SIZE_RATIO = 0.9


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the fallback guide bundle and guard against inadvertent data loss.",
    )
    parser.add_argument(
        "--bundle",
        type=Path,
        default=BUNDLE_PATH,
        help="Path to the bundle to validate (defaults to data/guides.bundle.json).",
    )
    parser.add_argument(
        "--backup",
        type=Path,
        default=BACKUP_PATH,
        help=(
            "Path to the baseline snapshot used for loss detection."
            " Defaults to data/Guide.bundle.backup.JSON."
        ),
    )
    parser.add_argument(
        "--update-backup",
        action="store_true",
        help="Refresh the baseline snapshot after validation succeeds.",
    )
    parser.add_argument(
        "--allow-route-removals",
        action="store_true",
        help=(
            "Permit removing existing routes when intentionally deprecating them."
        ),
    )
    parser.add_argument(
        "--allow-guide-removals",
        action="store_true",
        help=(
            "Permit removing existing guide catalog entries when intentionally pruning them."
        ),
    )
    parser.add_argument(
        "--allow-step-removals",
        action="store_true",
        help=(
            "Permit removing existing route steps when intentionally restructuring them."
        ),
    )
    return parser.parse_args(argv)


def fail(message: str) -> int:
    print(f"[guides bundle validation] {message}", file=sys.stderr)
    return 1


def load_bundle(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_structure(
    bundle: dict,
) -> tuple[int, int, Counter[str], set[str], Counter[str]]:
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS.difference(bundle))
    if missing:
        raise ValueError(
            "bundle is missing required top-level sections: " + ", ".join(missing)
        )

    guide_catalog = bundle.get("guideCatalog")
    if not isinstance(guide_catalog, dict):
        raise ValueError("'guideCatalog' must be an object")

    for field in ("guide_count", "data"):
        if field not in guide_catalog:
            raise ValueError(f"'guideCatalog' missing '{field}' field")

    guide_data = guide_catalog["data"]
    if not isinstance(guide_data, dict) or "guides" not in guide_data:
        raise ValueError("'guideCatalog.data.guides' array missing")

    guides = guide_data["guides"]
    if not isinstance(guides, list) or not guides:
        raise ValueError("'guideCatalog.data.guides' must be a non-empty array")

    declared_count = guide_catalog["guide_count"]
    if not isinstance(declared_count, int):
        raise ValueError("'guideCatalog.guide_count' must be an integer")

    if declared_count != len(guides):
        raise ValueError(
            "'guideCatalog.guide_count' does not match number of guides ("
            f"{declared_count} declared vs {len(guides)} actual)"
        )

    metadata = bundle.get("metadata", {})
    for field in ("schema_version", "verified_at_utc", "game_version"):
        if field not in metadata:
            raise ValueError(f"metadata missing '{field}'")

    for field, expected_type in (
        ("xp", dict),
        ("routeSchema", dict),
        ("levelEstimator", dict),
        ("recommender", dict),
    ):
        if not isinstance(bundle.get(field), expected_type):
            raise ValueError(
                f"bundle field '{field}' must be a {expected_type.__name__}"
            )

    extras = bundle.get("extras")
    if not isinstance(extras, list):
        raise ValueError("bundle field 'extras' must be an array")

    route_ids, step_ids = analyze_routes(bundle)
    guide_ids = extract_catalog_ids(bundle)

    routes = bundle["routes"]

    return len(routes), len(guides), route_ids, guide_ids, step_ids


def guard_against_data_loss(
    *,
    route_count: int,
    guide_count: int,
    bundle_size: int,
    backup_path: Path,
    current_route_ids: Counter[str],
    current_guide_ids: set[str],
    current_step_ids: Counter[str],
    allow_route_removals: bool,
    allow_guide_removals: bool,
    allow_step_removals: bool,
) -> None:
    if not backup_path.exists():
        print(
            "[guides bundle validation] No baseline snapshot found; skipping loss guard.",
            file=sys.stderr,
        )
        return

    try:
        backup_bundle = load_bundle(backup_path)
    except json.JSONDecodeError as exc:
        raise ValueError(f"backup bundle is not valid JSON: {exc}") from exc

    backup_route_ids, backup_step_ids = analyze_routes(
        backup_bundle, emit_duplicate_warnings=False
    )
    backup_route_count = len(backup_bundle.get("routes", []))
    backup_guide_ids = extract_catalog_ids(backup_bundle)
    backup_guides = (
        backup_bundle.get("guideCatalog", {})
        .get("data", {})
        .get("guides", [])
    )
    backup_guide_count = len(backup_guides)
    backup_size = backup_path.stat().st_size

    print(
        "Current bundle stats: "
        f"{route_count} routes, {guide_count} catalog entries, "
        f"{bundle_size} bytes.",
    )
    print(
        "Baseline snapshot stats: "
        f"{backup_route_count} routes, {backup_guide_count} catalog entries, "
        f"{backup_size} bytes.",
    )

    removed_route_ids, new_route_ids = _counter_differences(
        backup_route_ids, current_route_ids
    )
    if removed_route_ids:
        message = (
            "Routes removed relative to baseline: "
            + _format_counter_entries(removed_route_ids)
        )
        if allow_route_removals:
            print(f"[guides bundle validation] {message}")
        else:
            raise ValueError(message)

    if new_route_ids:
        print(
            "[guides bundle validation] New routes relative to baseline: "
            + _format_counter_entries(new_route_ids)
        )

    removed_step_ids, new_step_ids = _counter_differences(
        backup_step_ids, current_step_ids
    )
    if removed_step_ids:
        message = (
            "Route step_ids removed relative to baseline: "
            + _format_counter_entries(removed_step_ids)
        )
        if allow_step_removals:
            print(f"[guides bundle validation] {message}")
        else:
            raise ValueError(message)

    if new_step_ids:
        print(
            "[guides bundle validation] New route step_ids relative to baseline: "
            + _format_counter_entries(new_step_ids)
        )

    removed_guide_ids = sorted(backup_guide_ids.difference(current_guide_ids))
    new_guide_ids = sorted(current_guide_ids.difference(backup_guide_ids))
    if removed_guide_ids:
        message = (
            "Guide catalog entries removed relative to baseline: "
            + ", ".join(removed_guide_ids[:10])
        )
        if len(removed_guide_ids) > 10:
            message += f" ... (+{len(removed_guide_ids) - 10} more)"
        if allow_guide_removals:
            print(f"[guides bundle validation] {message}")
        else:
            raise ValueError(message)

    if new_guide_ids:
        print(
            "[guides bundle validation] New guide catalog entries relative to baseline: "
            + ", ".join(new_guide_ids[:10])
            + (" ..." if len(new_guide_ids) > 10 else "")
        )

    if route_count < backup_route_count:
        drop = backup_route_count - route_count
        ratio = route_count / backup_route_count if backup_route_count else 1.0
        if drop > MAX_ROUTE_DROP and ratio < MIN_ROUTE_RATIO:
            raise ValueError(
                "route count dropped unexpectedly ("
                f"{backup_route_count} -> {route_count}; drop {drop}, ratio {ratio:.2%})"
            )

    if guide_count < backup_guide_count:
        drop = backup_guide_count - guide_count
        ratio = guide_count / backup_guide_count if backup_guide_count else 1.0
        if drop > MAX_GUIDE_DROP and ratio < MIN_GUIDE_RATIO:
            raise ValueError(
                "guideCatalog entries dropped unexpectedly ("
                f"{backup_guide_count} -> {guide_count}; drop {drop}, ratio {ratio:.2%})"
            )

    if backup_size and bundle_size < backup_size:
        ratio = bundle_size / backup_size
        if ratio < MIN_SIZE_RATIO:
            raise ValueError(
                "bundle file size shrank dramatically ("
                f"{backup_size} -> {bundle_size}; ratio {ratio:.2%})"
            )


def refresh_backup(bundle_path: Path, backup_path: Path) -> None:
    backup_path.write_text(bundle_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Updated baseline snapshot at {backup_path}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bundle_path = args.bundle.resolve()
    backup_path = args.backup.resolve()

    if not bundle_path.exists():
        return fail(f"bundle missing at {bundle_path}")

    try:
        bundle = load_bundle(bundle_path)
    except json.JSONDecodeError as exc:
        return fail(f"bundle is not valid JSON: {exc}")

    try:
        (
            route_count,
            guide_count,
            current_route_ids,
            current_guide_ids,
            current_step_ids,
        ) = check_structure(bundle)
    except ValueError as exc:
        return fail(str(exc))

    bundle_size = bundle_path.stat().st_size

    try:
        guard_against_data_loss(
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
        return fail(str(exc))

    print(
        f"{bundle_path.name} passed validation ("
        f"{route_count} routes, {guide_count} catalog entries)."
    )

    if args.update_backup:
        if not backup_path.parent.exists():
            backup_path.parent.mkdir(parents=True, exist_ok=True)
        refresh_backup(bundle_path, backup_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
