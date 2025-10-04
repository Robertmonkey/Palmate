#!/usr/bin/env python3
"""Validate the integrity of data/guides.bundle.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path


MIN_LINE_RATIO = 0.98
MIN_ROUTE_RATIO = 0.98
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
        with BUNDLE_PATH.open("r", encoding="utf-8") as handle:
            bundle = json.load(handle)
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
    with BUNDLE_PATH.open("r", encoding="utf-8") as handle:
        bundle_line_count = sum(1 for _ in handle)

    if BACKUP_PATH.exists():
        try:
            with BACKUP_PATH.open("r", encoding="utf-8") as handle:
                backup_bundle = json.load(handle)
        except json.JSONDecodeError as exc:
            return fail(f"backup bundle is not valid JSON: {exc}")

        if not isinstance(backup_bundle.get("routes"), list) or not backup_bundle["routes"]:
            return fail("backup bundle has no routes to compare against")

        backup_route_count = len(backup_bundle["routes"])
        backup_guides = backup_bundle.get("guideCatalog", {}).get("data", {}).get(
            "guides", []
        )
        backup_guide_count = len(backup_guides) if isinstance(backup_guides, list) else 0

        if backup_route_count:
            allowed_route_drop = int(backup_route_count * (1 - MIN_ROUTE_RATIO))
            if bundle_route_count + allowed_route_drop < backup_route_count:
                return fail(
                    "route count dropped below backup snapshot "
                    f"({bundle_route_count} vs {backup_route_count})"
                )

        if backup_guide_count:
            allowed_guide_drop = int(backup_guide_count * (1 - MIN_ROUTE_RATIO))
            if len(guides) + allowed_guide_drop < backup_guide_count:
                return fail(
                    "guide catalog count dropped below backup snapshot "
                    f"({len(guides)} vs {backup_guide_count})"
                )

        with BACKUP_PATH.open("r", encoding="utf-8") as handle:
            backup_line_count = sum(1 for _ in handle)
        min_allowed_lines = int(backup_line_count * MIN_LINE_RATIO)
        if bundle_line_count < min_allowed_lines:
            return fail(
                "bundle line count dropped significantly compared to backup "
                f"({bundle_line_count} vs {backup_line_count})"
            )

    print("guides.bundle.json passed validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
