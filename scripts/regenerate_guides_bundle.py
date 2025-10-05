#!/usr/bin/env python3
"""Rebuild ``data/guides.bundle.json`` directly from ``guides.md``.

This script parses the JSON blocks embedded inside ``guides.md`` to
reconstruct the authoritative bundle payload.  It also hydrates the
``guideCatalog`` section with the current ``data/guide_catalog.json``
contents so shortages stay in sync.

Running this script avoids accidental partial writes (such as dumping only
``sourceRegistry``) because it always regenerates the complete bundle.  The
script now validates the reconstructed payload, guards it against data loss
relative to the baseline backup and only replaces the live files once the
bundle passes every check.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
GUIDES_MD = REPO_ROOT / "guides.md"
BUNDLE_PATH = REPO_ROOT / "data" / "guides.bundle.json"
BACKUP_PATH = REPO_ROOT / "data" / "Guide.bundle.backup.JSON"
GUIDE_CATALOG_PATH = REPO_ROOT / "data" / "guide_catalog.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_guides_bundle  # type: ignore  # noqa: E402


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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild data/guides.bundle.json from guides.md and guide_catalog.json "
            "with validation and loss guards."
        )
    )
    parser.add_argument(
        "--bundle",
        type=Path,
        default=BUNDLE_PATH,
        help="Path to the guides bundle to regenerate (defaults to data/guides.bundle.json).",
    )
    parser.add_argument(
        "--backup",
        type=Path,
        default=BACKUP_PATH,
        help="Path to the baseline snapshot used for loss detection (defaults to data/Guide.bundle.backup.JSON).",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip structural validation and loss guarding (not recommended).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate the bundle and report stats without writing any files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not write the regenerated payload to the backup snapshot.",
    )
    return parser.parse_args(argv)


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


def write_text_atomically(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=path.parent
    ) as handle:
        handle.write(payload)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    comps = load_components()
    bundle = build_bundle(comps)
    payload = json.dumps(bundle, indent=2, ensure_ascii=False) + "\n"

    if not args.skip_validation:
        (
            route_count,
            guide_count,
            current_route_ids,
            current_guide_ids,
            current_step_ids,
        ) = check_guides_bundle.check_structure(bundle)
        bundle_size = len(payload.encode("utf-8"))
        check_guides_bundle.guard_against_data_loss(
            route_count=route_count,
            guide_count=guide_count,
            bundle_size=bundle_size,
            backup_path=args.backup,
            current_route_ids=current_route_ids,
            current_guide_ids=current_guide_ids,
            current_step_ids=current_step_ids,
            allow_route_removals=False,
            allow_guide_removals=False,
            allow_step_removals=False,
        )
    else:
        route_count = len(bundle["routes"])
        guide_count = len(bundle["guideCatalog"]["data"].get("guides", []))

    print(
        "Rebuilt guides bundle:",
        f"{route_count} routes,",
        f"{guide_count} catalog guides,",
        f"{len(bundle['extras'])} extras entries.",
    )

    if args.dry_run:
        print("Dry run requested; no files were written.")
        return

    bundle_path = args.bundle
    write_text_atomically(bundle_path, payload)
    print(f"Wrote regenerated bundle to {bundle_path}.")

    if not args.no_backup:
        write_text_atomically(args.backup, payload)
        print(f"Updated backup snapshot at {args.backup}.")


if __name__ == "__main__":
    main()
