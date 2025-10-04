#!/usr/bin/env python3
"""Validate the integrity of data/guides.bundle.json."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

BUNDLE_PATH = Path(__file__).resolve().parent.parent / "data" / "guides.bundle.json"
BACKUP_BUNDLE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "Guide.bundle.backup.JSON"
)
GUIDES_PATH = Path(__file__).resolve().parent.parent / "guides.md"

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


def extract_source_registry() -> dict[str, Any]:
    """Load the source registry JSON block from guides.md."""

    if not GUIDES_PATH.exists():
        raise FileNotFoundError(f"guides.md missing at {GUIDES_PATH}")

    text = GUIDES_PATH.read_text(encoding="utf-8")
    match = re.search(r"## Source Registry.*?```json\n(.*?)\n```", text, flags=re.S)
    if not match:
        raise ValueError("unable to locate source registry JSON block in guides.md")

    block = json.loads(match.group(1))
    sources = block.get("sources") if isinstance(block, dict) else None
    if not isinstance(sources, dict) or not sources:
        raise ValueError("source registry block in guides.md is malformed")

    return sources


def load_bundle(path: Path, label: str) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"{label} missing at {path}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {exc}") from exc


def validate_bundle(bundle: dict[str, Any], label: str) -> tuple[set[str], int]:
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS.difference(bundle))
    if missing:
        raise ValueError(
            f"{label} is missing required top-level sections: {', '.join(missing)}"
        )

    if not isinstance(bundle.get("routes"), list) or not bundle["routes"]:
        raise ValueError(f"{label} must contain a non-empty 'routes' array")

    guide_catalog = bundle.get("guideCatalog")
    if not isinstance(guide_catalog, dict):
        raise ValueError(f"{label} 'guideCatalog' must be an object")

    for field in ("guide_count", "data"):
        if field not in guide_catalog:
            raise ValueError(f"{label} 'guideCatalog' missing '{field}' field")

    guide_data = guide_catalog["data"]
    if not isinstance(guide_data, dict) or "guides" not in guide_data:
        raise ValueError(f"{label} 'guideCatalog.data.guides' array missing")

    guides = guide_data["guides"]
    if not isinstance(guides, list) or not guides:
        raise ValueError(
            f"{label} 'guideCatalog.data.guides' must be a non-empty array"
        )

    declared_count = guide_catalog["guide_count"]
    if not isinstance(declared_count, int):
        raise ValueError(f"{label} 'guideCatalog.guide_count' must be an integer")

    if declared_count != len(guides):
        raise ValueError(
            f"{label} 'guideCatalog.guide_count' does not match number of guides ("
            f"{declared_count} declared vs {len(guides)} actual)"
        )

    metadata = bundle.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"{label} metadata must be an object")

    for field in ("schema_version", "verified_at_utc", "game_version"):
        if field not in metadata:
            raise ValueError(f"{label} metadata missing '{field}'")

    source_registry = bundle.get("sourceRegistry")
    if not isinstance(source_registry, dict) or not source_registry:
        raise ValueError(f"{label} 'sourceRegistry' must be a non-empty object")

    return set(source_registry.keys()), declared_count


def main() -> int:
    try:
        source_registry_reference = extract_source_registry()
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return fail(str(exc))

    reference_keys = set(source_registry_reference.keys())

    try:
        bundle = load_bundle(BUNDLE_PATH, "guides.bundle.json")
        bundle_source_keys, bundle_count = validate_bundle(bundle, "guides.bundle.json")
    except (FileNotFoundError, ValueError) as exc:
        return fail(str(exc))

    try:
        backup_bundle = load_bundle(
            BACKUP_BUNDLE_PATH, "Guide.bundle.backup.JSON"
        )
        backup_source_keys, backup_count = validate_bundle(
            backup_bundle, "Guide.bundle.backup.JSON"
        )
    except (FileNotFoundError, ValueError) as exc:
        return fail(str(exc))

    missing_from_bundle = sorted(reference_keys - bundle_source_keys)
    if missing_from_bundle:
        preview = ", ".join(missing_from_bundle[:10])
        if len(missing_from_bundle) > 10:
            preview += ", ..."
        return fail(
            "guides.bundle.json 'sourceRegistry' missing entries present in guides.md: "
            + preview
        )

    missing_from_backup = sorted(reference_keys - backup_source_keys)
    if missing_from_backup:
        preview = ", ".join(missing_from_backup[:10])
        if len(missing_from_backup) > 10:
            preview += ", ..."
        return fail(
            "Guide.bundle.backup.JSON 'sourceRegistry' missing entries present in guides.md: "
            + preview
        )

    if bundle_source_keys != backup_source_keys:
        preview = ", ".join(sorted((bundle_source_keys ^ backup_source_keys))[:10])
        if len(bundle_source_keys ^ backup_source_keys) > 10:
            preview += ", ..."
        return fail(
            "Mismatch between guides.bundle.json and Guide.bundle.backup.JSON 'sourceRegistry' entries: "
            + preview
        )

    if bundle_count != backup_count:
        return fail(
            "guideCatalog.guide_count differs between guides.bundle.json and Guide.bundle.backup.JSON"
        )

    print(
        "guides.bundle.json and Guide.bundle.backup.JSON passed validation",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
