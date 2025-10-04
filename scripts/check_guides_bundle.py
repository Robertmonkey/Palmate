#!/usr/bin/env python3
"""Validate the integrity of data/guides.bundle.json."""
from __future__ import annotations

import json
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


MIN_LINE_RATIO = 0.98
MIN_ROUTE_RATIO = 0.98
MAX_ROUTE_CHANGE_RATIO = 0.4
MAX_GUIDE_CHANGE_RATIO = 0.4
BACKUP_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "Guide.bundle.backup.JSON"
)

BUNDLE_PATH = Path(__file__).resolve().parent.parent / "data" / "guides.bundle.json"

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


def fail(message: str) -> int:
    print(f"[guides bundle validation] {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not BUNDLE_PATH.exists():
        return fail(f"bundle missing at {BUNDLE_PATH}")

    try:
        bundle_text = BUNDLE_PATH.read_text(encoding="utf-8")
        bundle = json.loads(bundle_text)
    except json.JSONDecodeError as exc:
        return fail(f"bundle is not valid JSON: {exc}")

    missing = sorted(REQUIRED_TOP_LEVEL_KEYS.difference(bundle))
    if missing:
        return fail(
            "bundle is missing required top-level sections: " + ", ".join(missing)
        )

    if not isinstance(bundle["routes"], list) or not bundle["routes"]:
        return fail("bundle must contain a non-empty 'routes' array")

    guide_catalog = bundle["guideCatalog"]
    if not isinstance(guide_catalog, dict):
        return fail("'guideCatalog' must be an object")

    for field in ("guide_count", "data"):
        if field not in guide_catalog:
            return fail(f"'guideCatalog' missing '{field}' field")

    guide_data = guide_catalog["data"]
    if not isinstance(guide_data, dict) or "guides" not in guide_data:
        return fail("'guideCatalog.data.guides' array missing")

    guides = guide_data["guides"]
    if not isinstance(guides, list) or not guides:
        return fail("'guideCatalog.data.guides' must be a non-empty array")

    declared_count = guide_catalog["guide_count"]
    if not isinstance(declared_count, int):
        return fail("'guideCatalog.guide_count' must be an integer")

    if declared_count != len(guides):
        return fail(
            "'guideCatalog.guide_count' does not match number of guides ("
            f"{declared_count} declared vs {len(guides)} actual)"
        )

    # Spot check a handful of required metadata fields so truncation is caught early.
    metadata = bundle["metadata"]
    for field in ("schema_version", "verified_at_utc", "game_version"):
        if field not in metadata:
            return fail(f"metadata missing '{field}'")

    bundle_route_count = len(bundle["routes"])
    bundle_line_count = bundle_text.count("\n") + 1

    route_counts: Counter[str] = Counter()
    route_map: dict[str, list[dict]] = {}
    for route in bundle["routes"]:
        if not isinstance(route, dict):
            return fail("every route entry must be an object")
        route_id = route.get("id") or route.get("route_id")
        if not route_id:
            return fail("encountered a route without an 'id'")
        route_counts[route_id] += 1
        route_map.setdefault(route_id, []).append(route)

    guide_counts: Counter[str] = Counter()
    guide_map: dict[str, list[dict]] = {}
    for entry in guides:
        if not isinstance(entry, dict):
            return fail("every guide catalog entry must be an object")
        guide_id = entry.get("id")
        if not guide_id:
            return fail("encountered a catalog entry without an 'id'")
        guide_counts[guide_id] += 1
        guide_map.setdefault(guide_id, []).append(entry)

    if BACKUP_PATH.exists():
        try:
            backup_text = BACKUP_PATH.read_text(encoding="utf-8")
            backup_bundle = json.loads(backup_text)
        except json.JSONDecodeError as exc:
            return fail(f"backup bundle is not valid JSON: {exc}")

        if not isinstance(backup_bundle.get("routes"), list) or not backup_bundle["routes"]:
            return fail("backup bundle has no routes to compare against")

        backup_route_count = len(backup_bundle["routes"])
        backup_guides = backup_bundle.get("guideCatalog", {}).get("data", {}).get(
            "guides", []
        )
        backup_guide_count = len(backup_guides) if isinstance(backup_guides, list) else 0

        backup_route_counts: Counter[str] = Counter()
        backup_route_map: dict[str, list[dict]] = {}
        for route in backup_bundle["routes"]:
            if not isinstance(route, dict):
                continue
            backup_route_id = route.get("id") or route.get("route_id")
            if backup_route_id:
                backup_route_counts[backup_route_id] += 1
                backup_route_map.setdefault(backup_route_id, []).append(route)

        missing_routes = sorted(
            route_id
            for route_id, count in backup_route_counts.items()
            if route_counts[route_id] < count
        )
        if missing_routes:
            preview = ", ".join(missing_routes[:5])
            suffix = "" if len(missing_routes) <= 5 else " …"
            return fail(
                "bundle is missing routes present in the canonical backup ("
                f"{preview}{suffix})"
            )

        if backup_route_count:
            allowed_route_drop = int(backup_route_count * (1 - MIN_ROUTE_RATIO))
            if bundle_route_count + allowed_route_drop < backup_route_count:
                return fail(
                    "route count dropped below backup snapshot "
                    f"({bundle_route_count} vs {backup_route_count})"
                )

        total_backup_routes = sum(backup_route_counts.values())
        changed_routes = 0
        for route_id, backup_entries in backup_route_map.items():
            current_entries = route_map.get(route_id, [])
            for idx, backup_entry in enumerate(backup_entries):
                if idx >= len(current_entries):
                    break
                if backup_entry != current_entries[idx]:
                    changed_routes += 1

        if total_backup_routes and (
            changed_routes / total_backup_routes > MAX_ROUTE_CHANGE_RATIO
        ):
            return fail(
                "bundle rewrote a large share of canonical routes "
                f"({changed_routes} of {total_backup_routes})"
            )

        if backup_guide_count:
            allowed_guide_drop = int(backup_guide_count * (1 - MIN_ROUTE_RATIO))
            if len(guides) + allowed_guide_drop < backup_guide_count:
                return fail(
                    "guide catalog count dropped below backup snapshot "
                    f"({len(guides)} vs {backup_guide_count})"
                )

        backup_guide_counts: Counter[str] = Counter()
        backup_guide_map: dict[str, list[dict]] = {}
        for entry in backup_guides:
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("id")
            if entry_id:
                backup_guide_counts[entry_id] += 1
                backup_guide_map.setdefault(entry_id, []).append(entry)

        missing_guides = sorted(
            guide_id
            for guide_id, count in backup_guide_counts.items()
            if guide_counts[guide_id] < count
        )
        if missing_guides:
            preview = ", ".join(missing_guides[:5])
            suffix = "" if len(missing_guides) <= 5 else " …"
            return fail(
                "guide catalog lost entries compared to the canonical backup ("
                f"{preview}{suffix})"
            )

        total_backup_guides = sum(backup_guide_counts.values())
        changed_guides = 0
        for guide_id, backup_entries in backup_guide_map.items():
            current_entries = guide_map.get(guide_id, [])
            for idx, backup_entry in enumerate(backup_entries):
                if idx >= len(current_entries):
                    break
                if backup_entry != current_entries[idx]:
                    changed_guides += 1

        if total_backup_guides and (
            changed_guides / total_backup_guides > MAX_GUIDE_CHANGE_RATIO
        ):
            return fail(
                "guide catalog rewrote a large share of canonical entries "
                f"({changed_guides} of {total_backup_guides})"
            )

        backup_line_count = backup_text.count("\n") + 1
        min_allowed_lines = int(backup_line_count * MIN_LINE_RATIO)
        if bundle_line_count < min_allowed_lines:
            return fail(
                "bundle line count dropped significantly compared to backup "
                f"({bundle_line_count} vs {backup_line_count})"
            )

        similarity = SequenceMatcher(
            None, backup_text.splitlines(), bundle_text.splitlines()
        ).ratio()
        if similarity < 0.99:
            return fail(
                "bundle content diverged heavily from the canonical backup "
                f"(line similarity score {similarity:.4f} < 0.99)"
            )

    print("guides.bundle.json passed validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
