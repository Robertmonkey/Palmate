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
from typing import Any

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


ALLOWED_STEP_TYPES = {
    "assign",
    "base",
    "build",
    "capture",
    "combat",
    "craft",
    "deliver",
    "explore",
    "farm",
    "fight",
    "gather",
    "hunt",
    "plan",
    "prepare",
    "quest",
    "trade",
    "travel",
    "unlock-tech",
}

ALLOWED_TARGET_KINDS = {"boss", "item", "pal", "station", "structure", "tech"}
ALLOWED_MODES = {"normal", "hardcore", "solo", "coop"}


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
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Enable deep validation of routes, catalog entries, and the source registry."
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


def _ensure(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _validate_route(route: dict, errors: list[str]) -> None:
    route_id = route.get("route_id", "<missing id>")

    recommended_level = route.get("recommended_level")
    if isinstance(recommended_level, dict):
        min_level = recommended_level.get("min")
        max_level = recommended_level.get("max")
        _ensure(
            isinstance(min_level, int) and isinstance(max_level, int),
            f"route {route_id} recommended_level must define integer 'min' and 'max' fields",
            errors,
        )
        if isinstance(min_level, int) and isinstance(max_level, int):
            _ensure(
                min_level <= max_level,
                f"route {route_id} recommended_level min ({min_level}) exceeds max ({max_level})",
                errors,
            )
    else:
        errors.append(f"route {route_id} recommended_level must be an object")

    estimated_xp = route.get("estimated_xp_gain")
    if isinstance(estimated_xp, dict):
        xp_min = estimated_xp.get("min")
        xp_max = estimated_xp.get("max")
        _ensure(
            isinstance(xp_min, int) and isinstance(xp_max, int),
            f"route {route_id} estimated_xp_gain must define integer 'min' and 'max' fields",
            errors,
        )
        if isinstance(xp_min, int) and isinstance(xp_max, int):
            _ensure(
                xp_min <= xp_max,
                f"route {route_id} estimated_xp_gain min ({xp_min}) exceeds max ({xp_max})",
                errors,
            )
    else:
        errors.append(f"route {route_id} estimated_xp_gain must be an object")

    estimated_time = route.get("estimated_time_minutes")
    if isinstance(estimated_time, dict):
        for mode in ("solo", "coop"):
            value = estimated_time.get(mode)
            _ensure(
                isinstance(value, int) and value > 0,
                f"route {route_id} estimated_time_minutes['{mode}'] must be a positive integer",
                errors,
            )
    else:
        errors.append(f"route {route_id} estimated_time_minutes must be an object")

    modes = route.get("modes")
    if isinstance(modes, dict):
        missing_modes = ALLOWED_MODES.difference(modes)
        _ensure(
            not missing_modes,
            f"route {route_id} modes missing keys: {', '.join(sorted(missing_modes))}",
            errors,
        )
        for mode_key, value in modes.items():
            _ensure(
                mode_key in ALLOWED_MODES,
                f"route {route_id} modes includes unsupported key '{mode_key}'",
                errors,
            )
            _ensure(
                isinstance(value, bool),
                f"route {route_id} modes['{mode_key}'] must be a boolean",
                errors,
            )
    else:
        errors.append(f"route {route_id} modes must be an object")

    prerequisites = route.get("prerequisites")
    if isinstance(prerequisites, dict):
        for field in ("routes", "tech", "items", "pals"):
            collection = prerequisites.get(field)
            _ensure(
                isinstance(collection, list),
                f"route {route_id} prerequisites['{field}'] must be a list",
                errors,
            )
            if isinstance(collection, list):
                invalid = [value for value in collection if not isinstance(value, str)]
                _ensure(
                    not invalid,
                    f"route {route_id} prerequisites['{field}'] must contain only strings",
                    errors,
                )
    else:
        errors.append(f"route {route_id} prerequisites must be an object")

    failure_penalties = route.get("failure_penalties")
    if isinstance(failure_penalties, dict):
        for mode in ("normal", "hardcore"):
            penalty = failure_penalties.get(mode)
            _ensure(
                isinstance(penalty, str) and penalty.strip(),
                f"route {route_id} failure_penalties['{mode}'] must be a non-empty string",
                errors,
            )
    else:
        errors.append(f"route {route_id} failure_penalties must be an object")

    failure_recovery = route.get("failure_recovery")
    if failure_recovery is not None:
        if isinstance(failure_recovery, dict):
            for mode in ("normal", "hardcore"):
                recovery = failure_recovery.get(mode)
                if recovery is None:
                    continue
                _ensure(
                    isinstance(recovery, str) and recovery.strip(),
                    f"route {route_id} failure_recovery['{mode}'] must be a non-empty string",
                    errors,
                )
        else:
            errors.append(f"route {route_id} failure_recovery must be an object when present")

    supporting_routes = route.get("supporting_routes")
    if supporting_routes is not None:
        if isinstance(supporting_routes, dict):
            for bucket in ("recommended", "optional"):
                entries = supporting_routes.get(bucket, [])
                _ensure(
                    isinstance(entries, list),
                    f"route {route_id} supporting_routes['{bucket}'] must be a list",
                    errors,
                )
                if isinstance(entries, list):
                    invalid_entries = [value for value in entries if not isinstance(value, str)]
                    _ensure(
                        not invalid_entries,
                        f"route {route_id} supporting_routes['{bucket}'] must contain only strings",
                        errors,
                    )
        else:
            errors.append(f"route {route_id} supporting_routes must be an object when present")

    adaptive_guidance = route.get("adaptive_guidance")
    if isinstance(adaptive_guidance, dict):
        for key in ("underleveled", "overleveled", "time_limited"):
            guidance = adaptive_guidance.get(key)
            _ensure(
                isinstance(guidance, str) and guidance.strip(),
                f"route {route_id} adaptive_guidance['{key}'] must be a non-empty string",
                errors,
            )

        shortages = adaptive_guidance.get("resource_shortages", [])
        if shortages is not None:
            _ensure(
                isinstance(shortages, list),
                f"route {route_id} adaptive_guidance.resource_shortages must be a list when present",
                errors,
            )
            if isinstance(shortages, list):
                for shortage in shortages:
                    _ensure(
                        isinstance(shortage, dict),
                        f"route {route_id} resource shortage entries must be objects",
                        errors,
                    )
                    if not isinstance(shortage, dict):
                        continue
                    _ensure(
                        isinstance(shortage.get("item_id"), str) and shortage.get("item_id"),
                        f"route {route_id} resource shortage entries must include a non-empty item_id",
                        errors,
                    )
                    _ensure(
                        isinstance(shortage.get("solution"), str) and shortage.get("solution"),
                        f"route {route_id} resource shortage entries must include a non-empty solution",
                        errors,
                    )
                    subroute_ref = shortage.get("subroute_ref")
                    if subroute_ref is not None:
                        _ensure(
                            isinstance(subroute_ref, str) and subroute_ref,
                            f"route {route_id} resource shortage subroute_ref must be a non-empty string",
                            errors,
                        )

        dynamic_rules = adaptive_guidance.get("dynamic_rules", [])
        if dynamic_rules is not None:
            _ensure(
                isinstance(dynamic_rules, list),
                f"route {route_id} adaptive_guidance.dynamic_rules must be a list when present",
                errors,
            )
            if isinstance(dynamic_rules, list):
                for rule in dynamic_rules:
                    _ensure(
                        isinstance(rule, dict),
                        f"route {route_id} dynamic rule entries must be objects",
                        errors,
                    )
                    if not isinstance(rule, dict):
                        continue
                    for field in ("signal", "condition", "adjustment"):
                        _ensure(
                            isinstance(rule.get(field), str) and rule.get(field),
                            f"route {route_id} dynamic rule must include non-empty '{field}'",
                            errors,
                        )
                    _ensure(
                        isinstance(rule.get("priority"), int) and rule.get("priority") > 0,
                        f"route {route_id} dynamic rule priority must be a positive integer",
                        errors,
                    )
                    mode_scope = rule.get("mode_scope")
                    _ensure(
                        isinstance(mode_scope, list) and mode_scope,
                        f"route {route_id} dynamic rule mode_scope must be a non-empty list",
                        errors,
                    )
                    if isinstance(mode_scope, list):
                        invalid_modes = [mode for mode in mode_scope if mode not in ALLOWED_MODES]
                        _ensure(
                            not invalid_modes,
                            f"route {route_id} dynamic rule references unsupported modes: {', '.join(invalid_modes)}",
                            errors,
                        )
                    related_steps = rule.get("related_steps")
                    _ensure(
                        isinstance(related_steps, list) and related_steps,
                        f"route {route_id} dynamic rule related_steps must be a non-empty list",
                        errors,
                    )
                    if isinstance(related_steps, list):
                        invalid_refs = [step for step in related_steps if not isinstance(step, str)]
                        _ensure(
                            not invalid_refs,
                            f"route {route_id} dynamic rule related_steps must contain only strings",
                            errors,
                        )
                    follow_up = rule.get("follow_up_routes")
                    if follow_up is not None:
                        _ensure(
                            isinstance(follow_up, list),
                            f"route {route_id} dynamic rule follow_up_routes must be a list when present",
                            errors,
                        )
                        if isinstance(follow_up, list):
                            invalid_follow = [value for value in follow_up if not isinstance(value, str)]
                            _ensure(
                                not invalid_follow,
                                f"route {route_id} dynamic rule follow_up_routes must contain only strings",
                                errors,
                            )
    else:
        errors.append(f"route {route_id} adaptive_guidance must be an object")

    checkpoints = route.get("checkpoints", [])
    for checkpoint in checkpoints:
        identifier = checkpoint.get("id")
        _ensure(
            isinstance(identifier, str) and identifier,
            "route {route_id} checkpoints must include non-empty ids".format(route_id=route_id),
            errors,
        )
        summary_value = checkpoint.get("summary") or checkpoint.get("label")
        _ensure(
            isinstance(summary_value, str) and summary_value,
            "route {route_id} checkpoint {identifier} must include a non-empty summary or label".format(
                route_id=route_id, identifier=identifier
            ),
            errors,
        )
        benefits = checkpoint.get("benefits")
        if benefits is not None:
            _ensure(
                isinstance(benefits, list),
                "route {route_id} checkpoint {identifier} benefits must be a list when present".format(
                    route_id=route_id, identifier=identifier
                ),
                errors,
            )
            if isinstance(benefits, list):
                invalid = [entry for entry in benefits if not isinstance(entry, str)]
                _ensure(
                    not invalid,
                    "route {route_id} checkpoint {identifier} benefits must contain only strings".format(
                        route_id=route_id, identifier=identifier
                    ),
                    errors,
                )
        related = checkpoint.get("related_steps")
        includes = checkpoint.get("includes")
        _ensure(
            (isinstance(related, list) and related)
            or (isinstance(includes, list) and includes),
            "route {route_id} checkpoint {identifier} must reference related steps via 'related_steps' or 'includes'".format(
                route_id=route_id, identifier=identifier
            ),
            errors,
        )
        for collection, label in ((related, "related_steps"), (includes, "includes")):
            if collection is None:
                continue
            _ensure(
                isinstance(collection, list) and collection,
                "route {route_id} checkpoint {identifier} {label} must be a non-empty list".format(
                    route_id=route_id, identifier=identifier, label=label
                ),
                errors,
            )
            if isinstance(collection, list):
                invalid = [entry for entry in collection if not isinstance(entry, str)]
                _ensure(
                    not invalid,
                    "route {route_id} checkpoint {identifier} {label} must contain only strings".format(
                        route_id=route_id, identifier=identifier, label=label
                    ),
                    errors,
                )

    for index, step in enumerate(route.get("steps", [])):
        step_id = step.get("step_id", f"index {index}")
        _ensure(
            isinstance(step.get("summary"), str) and step.get("summary"),
            f"route {route_id} step {step_id} must include a non-empty summary",
            errors,
        )
        _ensure(
            isinstance(step.get("detail"), str) and step.get("detail"),
            f"route {route_id} step {step_id} must include a non-empty detail",
            errors,
        )
        step_type = step.get("type")
        _ensure(
            isinstance(step_type, str) and step_type in ALLOWED_STEP_TYPES,
            f"route {route_id} step {step_id} has unsupported type '{step_type}'",
            errors,
        )

        targets = step.get("targets")
        _ensure(
            isinstance(targets, list),
            f"route {route_id} step {step_id} targets must be a list",
            errors,
        )
        if isinstance(targets, list):
            for target in targets:
                _ensure(
                    isinstance(target, dict),
                    f"route {route_id} step {step_id} targets must be objects",
                    errors,
                )
                if not isinstance(target, dict):
                    continue
                kind = target.get("kind")
                _ensure(
                    isinstance(kind, str) and kind in ALLOWED_TARGET_KINDS,
                    f"route {route_id} step {step_id} target has unsupported kind '{kind}'",
                    errors,
                )
                identifier = target.get("id")
                _ensure(
                    isinstance(identifier, str) and identifier,
                    f"route {route_id} step {step_id} targets must include a non-empty id",
                    errors,
                )
                if "qty" in target:
                    qty = target.get("qty")
                    _ensure(
                        isinstance(qty, int) and qty > 0,
                        f"route {route_id} step {step_id} target qty must be a positive integer",
                        errors,
                    )

        locations = step.get("locations", [])
        if locations:
            _ensure(
                isinstance(locations, list),
                f"route {route_id} step {step_id} locations must be a list",
                errors,
            )
            if isinstance(locations, list):
                for loc in locations:
                    _ensure(
                        isinstance(loc, dict),
                        f"route {route_id} step {step_id} locations must be objects",
                        errors,
                    )
                    if not isinstance(loc, dict):
                        continue
                    coords = loc.get("coords")
                    _ensure(
                        isinstance(coords, list)
                        and len(coords) == 2
                        and all(isinstance(value, (int, float)) for value in coords),
                        f"route {route_id} step {step_id} location coords must be a two-element list of numbers",
                        errors,
                    )
                    for field in ("region_id", "time", "weather"):
                        value = loc.get(field)
                        _ensure(
                            isinstance(value, str) and value,
                            f"route {route_id} step {step_id} location must include non-empty '{field}'",
                            errors,
                        )
                    notes = loc.get("notes")
                    if notes is not None:
                        _ensure(
                            isinstance(notes, str) and notes,
                            f"route {route_id} step {step_id} location notes must be a non-empty string when present",
                            errors,
                        )

        mode_adjustments = step.get("mode_adjustments")
        if mode_adjustments is not None:
            _ensure(
                isinstance(mode_adjustments, dict),
                f"route {route_id} step {step_id} mode_adjustments must be an object",
                errors,
            )
            if isinstance(mode_adjustments, dict):
                for mode_key, payload in mode_adjustments.items():
                    _ensure(
                        mode_key in ALLOWED_MODES,
                        f"route {route_id} step {step_id} mode_adjustments contains unsupported mode '{mode_key}'",
                        errors,
                    )
                    _ensure(
                        isinstance(payload, dict) and payload,
                        f"route {route_id} step {step_id} mode_adjustments['{mode_key}'] must be a non-empty object",
                        errors,
                    )


def _validate_catalog_steps(
    steps: list[Any], guide_id: str, errors: list[str]
) -> None:
    for step in steps:
        if not isinstance(step, dict):
            errors.append(
                f"guide {guide_id} steps must be objects; encountered {type(step).__name__}"
            )
            continue
        if "order" in step:
            _ensure(
                isinstance(step.get("order"), int) and step.get("order") > 0,
                f"guide {guide_id} steps must define a positive integer order",
                errors,
            )
            _ensure(
                isinstance(step.get("instruction"), str) and step.get("instruction"),
                f"guide {guide_id} step order {step.get('order')} must include a non-empty instruction",
                errors,
            )
            citations = step.get("citations")
            _ensure(
                isinstance(citations, list),
                f"guide {guide_id} step order {step.get('order')} citations must be a list",
                errors,
            )
            if isinstance(citations, list):
                invalid_citations = [value for value in citations if not isinstance(value, str)]
                _ensure(
                    not invalid_citations,
                    f"guide {guide_id} step order {step.get('order')} citations must contain only strings",
                    errors,
                )
            links = step.get("links")
            if links is not None:
                _ensure(
                    isinstance(links, list),
                    f"guide {guide_id} step order {step.get('order')} links must be a list",
                    errors,
                )
                if isinstance(links, list):
                    for link in links:
                        _ensure(
                            isinstance(link, dict),
                            f"guide {guide_id} step order {step.get('order')} links must be objects",
                            errors,
                        )
                        if not isinstance(link, dict):
                            continue
                        _ensure(
                            isinstance(link.get("type"), str) and link.get("type"),
                            f"guide {guide_id} step order {step.get('order')} link type must be a non-empty string",
                            errors,
                        )
                        identifier = link.get("id")
                        if identifier is not None:
                            _ensure(
                                isinstance(identifier, str) and identifier,
                                f"guide {guide_id} step order {step.get('order')} link id must be a non-empty string",
                                errors,
                            )
        elif "id" in step and "steps" in step:
            nested_id = step.get("id")
            _ensure(
                isinstance(nested_id, str) and nested_id,
                f"guide {guide_id} embedded guide entries must include a non-empty id",
                errors,
            )
            for field in ("title", "trigger"):
                if field in step:
                    _ensure(
                        isinstance(step.get(field), str) and step.get(field),
                        f"embedded guide {nested_id} field '{field}' must be a non-empty string",
                        errors,
                    )
            nested_steps = step.get("steps")
            _ensure(
                isinstance(nested_steps, list) and nested_steps,
                f"embedded guide {nested_id} must include a non-empty steps list",
                errors,
            )
            if isinstance(nested_steps, list):
                _validate_catalog_steps(nested_steps, nested_id or guide_id, errors)
        else:
            errors.append(
                f"guide {guide_id} contains an unrecognised step structure: {sorted(step.keys())}"
            )


def _validate_catalog(catalog: dict, errors: list[str]) -> None:
    guides = catalog.get("guides")
    if not isinstance(guides, list) or not guides:
        errors.append("guide_catalog.json must contain a non-empty 'guides' array")
        return

    seen_ids: set[str] = set()
    for guide in guides:
        guide_id = guide.get("id", "<missing id>")
        _ensure(isinstance(guide, dict), "guide entries must be objects", errors)
        if not isinstance(guide, dict):
            continue
        _ensure(
            isinstance(guide.get("id"), str) and guide.get("id"),
            "guide entries must include a non-empty id",
            errors,
        )
        if isinstance(guide.get("id"), str):
            if guide["id"] in seen_ids:
                errors.append(f"duplicate guide id encountered in guide_catalog.json: {guide['id']}")
            else:
                seen_ids.add(guide["id"])
        for field in ("title", "source_heading", "trigger", "category", "category_group"):
            _ensure(
                isinstance(guide.get(field), str) and guide.get(field),
                f"guide {guide_id} field '{field}' must be a non-empty string",
                errors,
            )
        keywords = guide.get("keywords")
        _ensure(
            isinstance(keywords, list) and keywords,
            f"guide {guide_id} keywords must be a non-empty list",
            errors,
        )
        if isinstance(keywords, list):
            invalid_keywords = [value for value in keywords if not isinstance(value, str) or not value]
            _ensure(
                not invalid_keywords,
                f"guide {guide_id} keywords must contain only non-empty strings",
                errors,
            )

        steps = guide.get("steps")
        _ensure(
            isinstance(steps, list) and steps,
            f"guide {guide_id} steps must be a non-empty list",
            errors,
        )
        if isinstance(steps, list):
            _validate_catalog_steps(steps, guide_id, errors)


def _validate_source_registry(source_registry: dict, errors: list[str]) -> None:
    _ensure(
        isinstance(source_registry, dict) and source_registry,
        "sourceRegistry must be a non-empty object",
        errors,
    )
    if not isinstance(source_registry, dict):
        return
    for source_id, entry in source_registry.items():
        _ensure(
            isinstance(entry, dict),
            f"source registry entry '{source_id}' must be an object",
            errors,
        )
        if not isinstance(entry, dict):
            continue
        for field in ("title", "url", "access_date"):
            _ensure(
                isinstance(entry.get(field), str) and entry.get(field),
                f"source registry entry '{source_id}' must include a non-empty '{field}'",
                errors,
            )
        notes = entry.get("notes")
        if notes is not None:
            _ensure(
                isinstance(notes, str) and notes,
                f"source registry entry '{source_id}' notes must be a non-empty string when present",
                errors,
            )


def run_strict_checks(bundle: dict) -> None:
    errors: list[str] = []

    metadata = bundle.get("metadata", {})
    _ensure(
        isinstance(metadata.get("schema_version"), int),
        "metadata.schema_version must be an integer",
        errors,
    )
    for field in ("game_version", "verified_at_utc"):
        _ensure(
            isinstance(metadata.get(field), str) and metadata.get(field),
            f"metadata.{field} must be a non-empty string",
            errors,
        )
    difficulty_modes = metadata.get("difficulty_modes")
    _ensure(
        isinstance(difficulty_modes, list) and {"normal", "hardcore"}.issubset(difficulty_modes),
        "metadata.difficulty_modes must include 'normal' and 'hardcore'",
        errors,
    )
    party_modes = metadata.get("party_modes")
    _ensure(
        isinstance(party_modes, list) and {"solo", "coop"}.issubset(party_modes),
        "metadata.party_modes must include 'solo' and 'coop'",
        errors,
    )

    routes = bundle.get("routes", [])
    for route in routes:
        _validate_route(route, errors)

    guide_catalog = bundle.get("guideCatalog", {})
    data = guide_catalog.get("data", {})
    if isinstance(data, dict):
        _validate_catalog(data, errors)
    else:
        errors.append("guideCatalog.data must be an object for strict validation")

    source_registry = bundle.get("sourceRegistry")
    if source_registry is not None:
        _validate_source_registry(source_registry, errors)
    else:
        errors.append("bundle is missing sourceRegistry section")

    if errors:
        joined = "\n - ".join(errors[:20])
        message = (
            f"Strict validation failed with {len(errors)} issue(s):\n - {joined}"
        )
        if len(errors) > 20:
            message += "\n - ... (additional issues truncated)"
        raise ValueError(message)


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

    if args.strict:
        try:
            run_strict_checks(bundle)
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
