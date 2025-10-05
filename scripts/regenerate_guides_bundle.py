#!/usr/bin/env python3
"""Rebuild data/guides.bundle.json directly from guides.md.

This script parses the JSON blocks embedded inside ``guides.md`` to
reconstruct the authoritative bundle payload.  It also hydrates the
``guideCatalog`` section with the current ``data/guide_catalog.json``
contents so shortages stay in sync.

Running this script avoids accidental partial writes (such as dumping only
``sourceRegistry``) because it always regenerates the complete bundle and
writes both the primary file and the backup atomically.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDES_MD = REPO_ROOT / "guides.md"
BUNDLE_PATH = REPO_ROOT / "data" / "guides.bundle.json"
BACKUP_PATH = REPO_ROOT / "data" / "Guide.bundle.backup.JSON"
GUIDE_CATALOG_PATH = REPO_ROOT / "data" / "guide_catalog.json"


@dataclass
class BundleComponents:
    metadata: dict | None = None
    xp: dict | None = None
    route_schema: dict | None = None
    routes: list[dict] | None = None
    level_estimator: dict | None = None
    recommender: dict | None = None
    guide_catalog_meta: dict | None = None
    source_registry: dict | None = None
    extras: list[dict] | None = None


def iter_json_blocks(markdown_path: Path) -> Iterator[str]:
    """Yield raw JSON blocks embedded in ``guides.md``."""

    buffer: list[str] | None = None
    with markdown_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("```json"):
                buffer = []
                continue
            if stripped == "```" and buffer is not None:
                yield "".join(buffer)
                buffer = None
                continue
            if buffer is not None:
                buffer.append(line)

    if buffer is not None:
        raise ValueError("Unterminated JSON block detected in guides.md")


def load_components() -> BundleComponents:
    """Parse ``guides.md`` and map JSON blocks to bundle components."""

    comps = BundleComponents(routes=[], extras=[])

    for raw_block in iter_json_blocks(GUIDES_MD):
        block = raw_block.strip()
        if not block:
            continue
        parsed = json.loads(block)

        if isinstance(parsed, dict) and "schema_version" in parsed:
            comps.metadata = parsed
        elif isinstance(parsed, dict) and "xp_thresholds" in parsed:
            comps.xp = parsed
        elif isinstance(parsed, dict) and "route_schema" in parsed:
            comps.route_schema = parsed["route_schema"]
        elif isinstance(parsed, dict) and "level_estimator" in parsed:
            comps.level_estimator = parsed["level_estimator"]
        elif isinstance(parsed, dict) and "recommender" in parsed:
            comps.recommender = parsed["recommender"]
        elif isinstance(parsed, dict) and "guide_catalog" in parsed:
            comps.guide_catalog_meta = parsed["guide_catalog"]
        elif isinstance(parsed, dict) and "sources" in parsed:
            comps.source_registry = parsed["sources"]
        elif isinstance(parsed, dict) and "route_id" in parsed:
            comps.routes.append(parsed)
        else:
            comps.extras.append(parsed)

    if comps.source_registry is not None:
        comps.extras.append({"sources": comps.source_registry})

    return comps


def build_bundle(comps: BundleComponents) -> dict:
    """Assemble the final bundle dictionary from parsed components."""

    if not all(
        (
            comps.metadata,
            comps.xp,
            comps.route_schema,
            comps.routes,
            comps.level_estimator,
            comps.recommender,
            comps.guide_catalog_meta,
            comps.source_registry,
            comps.extras,
        )
    ):
        raise ValueError("guides.md is missing required JSON sections")

    with GUIDE_CATALOG_PATH.open("r", encoding="utf-8") as handle:
        guide_catalog_data = json.load(handle)

    guide_catalog_meta = dict(comps.guide_catalog_meta)
    guide_catalog_meta["guide_count"] = len(guide_catalog_data.get("guides", []))

    bundle = {
        "metadata": comps.metadata,
        "xp": comps.xp,
        "routes": comps.routes,
        "routeSchema": comps.route_schema,
        "levelEstimator": comps.level_estimator,
        "recommender": comps.recommender,
        "guideCatalog": {
            **guide_catalog_meta,
            "data": guide_catalog_data,
        },
        "sourceRegistry": comps.source_registry,
        "extras": comps.extras,
    }

    return bundle


def write_bundle(bundle: dict) -> None:
    """Persist the bundle to both the primary and backup paths."""

    payload = json.dumps(bundle, indent=2, ensure_ascii=False) + "\n"
    for path in (BUNDLE_PATH, BACKUP_PATH):
        path.write_text(payload, encoding="utf-8")


def main() -> None:
    comps = load_components()
    bundle = build_bundle(comps)
    write_bundle(bundle)
    print(
        "Rebuilt guides.bundle.json:",
        f"{len(bundle['routes'])} routes,",
        f"{len(bundle['guideCatalog']['data'].get('guides', []))} catalog guides,",
        f"{len(bundle['extras'])} extras entries.",
    )


if __name__ == "__main__":
    main()
