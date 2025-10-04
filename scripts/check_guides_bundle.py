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
    return parser.parse_args(argv)


def fail(message: str) -> int:
    print(f"[guides bundle validation] {message}", file=sys.stderr)
    return 1


def load_bundle(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_structure(bundle: dict) -> tuple[int, int]:
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS.difference(bundle))
    if missing:
        raise ValueError(
            "bundle is missing required top-level sections: " + ", ".join(missing)
        )

    routes = bundle.get("routes")
    if not isinstance(routes, list) or not routes:
        raise ValueError("bundle must contain a non-empty 'routes' array")

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

    return len(routes), len(guides)


def guard_against_data_loss(
    *,
    route_count: int,
    guide_count: int,
    bundle_size: int,
    backup_path: Path,
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

    backup_route_count = len(backup_bundle.get("routes", []))
    backup_guide_count = len(
        backup_bundle.get("guideCatalog", {})
        .get("data", {})
        .get("guides", [])
    )
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
        route_count, guide_count = check_structure(bundle)
    except ValueError as exc:
        return fail(str(exc))

    bundle_size = bundle_path.stat().st_size

    try:
        guard_against_data_loss(
            route_count=route_count,
            guide_count=guide_count,
            bundle_size=bundle_size,
            backup_path=backup_path,
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
