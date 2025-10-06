#!/usr/bin/env python3
"""Generate a coverage report for shortage resource guides.

The script inspects guides.md for resource routes, loads the guide
catalog metadata, and compares the two lists. It surfaces resources
missing full route JSON, catalog entries, or both so the agent can
prioritise new work quickly.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Set

FIELD_STEP_TYPES: Set[str] = {
    "hunt",
    "capture",
    "combat",
    "gather",
    "collect",
    "explore",
    "travel",
    "raid",
    "sweep",
    "survey",
    "liberate",
    "escort",
    "scout",
    "farm",
    "harvest",
    "mine",
    "dungeon",
}

NON_FIELD_STEP_TYPES: Set[str] = {
    "base",
    "assign",
    "prepare",
    "craft",
    "build",
    "upgrade",
    "automation",
    "plan",
    "review",
    "stockpile",
    "manage",
    "train",
    "refine",
    "research",
    "talk",
}

REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDES_PATH = REPO_ROOT / "guides.md"
CATALOG_PATH = REPO_ROOT / "data" / "guide_catalog.json"

ROUTE_BLOCK_PATTERN = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


@dataclass(frozen=True)
class ResourceRoute:
    route_id: str
    title: str
    citations: tuple[str, ...]
    field_step_ids: tuple[str, ...]
    missing_field_step_ids: tuple[str, ...]
    exempt_field_step_ids: tuple[str, ...]
    under_cited_field_step_ids: tuple[str, ...]


@dataclass(frozen=True)
class CatalogEntry:
    entry_id: str
    title: str
    shortage_menu: bool


def parse_resource_routes(markdown: str) -> List[ResourceRoute]:
    routes: List[ResourceRoute] = []
    for match in ROUTE_BLOCK_PATTERN.finditer(markdown):
        block = match.group(1)
        try:
            payload = json.loads(block)
        except json.JSONDecodeError:
            # Skip malformed blocks but continue scanning remaining content.
            continue
        route_id = payload.get("route_id")
        if isinstance(route_id, str) and route_id.startswith("resource-"):
            title = payload.get("title", "")
            citations = tuple(_extract_citations(payload))
            (
                field_ids,
                missing_field_ids,
                exempt_ids,
                under_cited_ids,
            ) = _analyse_field_location_gaps(payload)
            routes.append(
                ResourceRoute(
                    route_id=route_id,
                    title=title,
                    citations=citations,
                    field_step_ids=tuple(field_ids),
                    missing_field_step_ids=tuple(missing_field_ids),
                    exempt_field_step_ids=tuple(exempt_ids),
                    under_cited_field_step_ids=tuple(under_cited_ids),
                )
            )
    return routes


def _extract_citations(payload: dict) -> list[str]:
    citations: list[str] = []
    seen: set[str] = set()

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "citations" and isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            item = item.strip()
                            if item and item not in seen:
                                seen.add(item)
                                citations.append(item)
                else:
                    _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(payload)
    return citations


def _analyse_field_location_gaps(
    payload: dict,
) -> tuple[List[str], List[str], List[str], List[str]]:
    steps = payload.get("steps")
    if not isinstance(steps, list):
        return [], [], [], []

    field_ids: List[str] = []
    missing_ids: List[str] = []
    exempt_ids: List[str] = []
    under_cited_ids: List[str] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        step_id = step.get("step_id")
        if not isinstance(step_id, str):
            continue
        if not _is_field_step(step):
            continue
        field_ids.append(step_id)
        location_policy = str(step.get("location_policy", "")).strip().lower()
        if location_policy in {"base-only", "no-map"}:
            exempt_ids.append(step_id)
            continue
        if not _step_has_valid_field_location(step):
            missing_ids.append(step_id)
        citations = step.get("citations")
        unique_citations: Set[str] = set()
        if isinstance(citations, list):
            for citation in citations:
                if isinstance(citation, str):
                    cleaned = citation.strip()
                    if cleaned:
                        unique_citations.add(cleaned)
        if len(unique_citations) < 2:
            under_cited_ids.append(step_id)
    return field_ids, missing_ids, exempt_ids, under_cited_ids


def _is_field_step(step: dict) -> bool:
    step_type = str(step.get("type", "")).strip().lower()
    if step_type in FIELD_STEP_TYPES:
        return True
    if step_type in NON_FIELD_STEP_TYPES:
        return False

    locations = step.get("locations")
    if isinstance(locations, list):
        for location in locations:
            if not isinstance(location, dict):
                continue
            region = str(
                location.get("region_id")
                or location.get("region")
                or ""
            ).strip().lower()
            coords = location.get("coords")
            if region and region != "base":
                return True
            if _coords_are_non_zero(coords):
                return True

    return False


def _coords_are_non_zero(coords: object) -> bool:
    if not isinstance(coords, list) or len(coords) != 2:
        return False
    try:
        x = float(coords[0])
        y = float(coords[1])
    except (TypeError, ValueError):
        return False
    return abs(x) > 1e-6 or abs(y) > 1e-6


def _step_has_valid_field_location(step: dict) -> bool:
    locations = step.get("locations")
    if not isinstance(locations, list) or not locations:
        return False

    for location in locations:
        if not isinstance(location, dict):
            continue
        region = str(
            location.get("region_id") or location.get("region") or ""
        ).strip().lower()
        if region == "base":
            continue
        coords = location.get("coords")
        if _coords_are_non_zero(coords):
            return True
    return False


def _extract_entries(raw_entries: Iterable[dict]) -> Iterable[CatalogEntry]:
    for item in raw_entries:
        entry_id = item.get("id")
        if not isinstance(entry_id, str):
            continue
        if not entry_id.startswith("resource-"):
            continue
        yield CatalogEntry(
            entry_id=entry_id,
            title=item.get("title", ""),
            shortage_menu=bool(item.get("shortage_menu", False)),
        )


def load_catalog_entries() -> List[CatalogEntry]:
    """Return all resource-oriented catalog entries.

    Historic builds of the catalog grouped entries into ``sections``.  The
    current bundle flattens everything under ``guides`` instead.  To keep the
    coverage report resilient we examine both shapes.
    """

    catalog = json.loads(CATALOG_PATH.read_text())
    entries: List[CatalogEntry] = []

    # Legacy structure with named sections.
    for section in catalog.get("sections", []) or []:
        section_entries = section.get("entries", [])
        entries.extend(_extract_entries(section_entries))

    # Flat structure emitted by the latest bundle.
    if "guides" in catalog:
        entries.extend(_extract_entries(catalog["guides"]))

    return entries


def format_text_report(
    missing_routes: Sequence[CatalogEntry],
    missing_catalog: Sequence[ResourceRoute],
    citation_warnings: Sequence[ResourceRoute],
    location_warnings: Sequence[ResourceRoute],
    location_exemptions: Sequence[ResourceRoute],
    step_citation_warnings: Sequence[ResourceRoute],
) -> str:
    lines = ["Resource Coverage Report", "========================", ""]
    lines.append(f"Catalog entries without matching routes: {len(missing_routes)}")
    if missing_routes:
        for entry in missing_routes:
            status = "shortage-menu" if entry.shortage_menu else "catalog-only"
            lines.append(f"  - {entry.entry_id} ({entry.title or 'untitled'}) [{status}]")
    else:
        lines.append("All catalogued resources have matching routes.")

    lines.append("")
    lines.append(f"Routes missing catalog entries: {len(missing_catalog)}")
    if missing_catalog:
        for route in missing_catalog:
            lines.append(f"  - {route.route_id} ({route.title or 'untitled'})")
    else:
        lines.append("All resource routes are present in the catalog.")

    lines.append("")
    lines.append(
        f"Routes with fewer than two citations: {len(citation_warnings)}"
    )
    if citation_warnings:
        for route in citation_warnings:
            lines.append(
                f"  - {route.route_id} ({route.title or 'untitled'}) – "
                f"{len(route.citations)} citation(s)"
            )
    else:
        lines.append("All resource routes include at least two citations.")

    lines.append("")
    lines.append(
        "Routes with field steps lacking dual citations: "
        f"{len(step_citation_warnings)}"
    )
    if step_citation_warnings:
        for route in step_citation_warnings:
            under_cited = ", ".join(route.under_cited_field_step_ids) or "(steps unspecified)"
            lines.append(
                "  - "
                f"{route.route_id} ({route.title or 'untitled'}) – under-cited: {under_cited}"
            )
    else:
        lines.append("All field steps include at least two citations.")

    lines.append("")
    lines.append(
        "Routes with field steps missing coordinates: "
        f"{len(location_warnings)}"
    )
    if location_warnings:
        for route in location_warnings:
            missing = ", ".join(route.missing_field_step_ids) or "(steps unspecified)"
            lines.append(
                f"  - {route.route_id} ({route.title or 'untitled'}) – missing: {missing}"
            )
    else:
        lines.append("All field steps include map coordinates.")

    lines.append("")
    lines.append(
        "Routes with field steps marked coordinate-exempt: "
        f"{len(location_exemptions)}"
    )
    if location_exemptions:
        for route in location_exemptions:
            exempt = ", ".join(route.exempt_field_step_ids) or "(steps unspecified)"
            lines.append(
                f"  - {route.route_id} ({route.title or 'untitled'}) – exempt: {exempt}"
            )
    else:
        lines.append("No coordinate exemptions declared for field steps.")

    return "\n".join(lines)


def format_markdown_report(
    missing_routes: Sequence[CatalogEntry],
    missing_catalog: Sequence[ResourceRoute],
    citation_warnings: Sequence[ResourceRoute],
    location_warnings: Sequence[ResourceRoute],
    location_exemptions: Sequence[ResourceRoute],
    step_citation_warnings: Sequence[ResourceRoute],
) -> str:
    lines = ["# Resource Coverage Report", ""]
    lines.append(f"- Catalog entries without matching routes: **{len(missing_routes)}**")
    lines.append(f"- Routes missing catalog entries: **{len(missing_catalog)}**")
    lines.append(
        f"- Routes with fewer than two citations: **{len(citation_warnings)}**"
    )
    lines.append(
        "- Routes with field steps lacking dual citations: "
        f"**{len(step_citation_warnings)}**"
    )
    lines.append(
        f"- Routes with field steps missing coordinates: **{len(location_warnings)}**"
    )
    lines.append(
        "- Routes with coordinate exemptions: "
        f"**{len(location_exemptions)}**"
    )
    lines.append("")

    if missing_routes:
        lines.append("## Catalog entries without matching routes")
        for entry in missing_routes:
            status = "shortage menu" if entry.shortage_menu else "catalog only"
            lines.append(f"- `{entry.entry_id}` – {entry.title or 'untitled'} ({status})")
        lines.append("")
    else:
        lines.append("All catalogued resources have matching routes.")
        lines.append("")

    if missing_catalog:
        lines.append("## Routes missing catalog entries")
        for route in missing_catalog:
            lines.append(f"- `{route.route_id}` – {route.title or 'untitled'}")
    else:
        lines.append("All resource routes are present in the catalog.")
        lines.append("")

    if citation_warnings:
        lines.append("## Routes with fewer than two citations")
        for route in citation_warnings:
            count = len(route.citations)
            plural = "s" if count != 1 else ""
            lines.append(
                f"- `{route.route_id}` – {route.title or 'untitled'} ({count} citation{plural})"
            )
        lines.append("")
    else:
        lines.append("All resource routes include at least two citations.")
        lines.append("")

    if step_citation_warnings:
        lines.append("## Routes with field steps lacking dual citations")
        for route in step_citation_warnings:
            under_cited = ", ".join(route.under_cited_field_step_ids) or "(steps unspecified)"
            lines.append(
                f"- `{route.route_id}` – {route.title or 'untitled'} (under-cited {under_cited})"
            )
        lines.append("")
    else:
        lines.append("All field steps include at least two citations.")
        lines.append("")

    if location_warnings:
        lines.append("## Routes with field steps missing coordinates")
        for route in location_warnings:
            missing = ", ".join(route.missing_field_step_ids) or "(steps unspecified)"
            lines.append(
                f"- `{route.route_id}` – {route.title or 'untitled'} (missing {missing})"
            )
        lines.append("")
    else:
        lines.append("All field steps include map coordinates.")
        lines.append("")

    if location_exemptions:
        lines.append("## Routes with coordinate exemptions")
        for route in location_exemptions:
            exempt = ", ".join(route.exempt_field_step_ids) or "(steps unspecified)"
            lines.append(
                f"- `{route.route_id}` – {route.title or 'untitled'} (exempt {exempt})"
            )
        lines.append("")
    else:
        lines.append("No coordinate exemptions declared for field steps.")

    return "\n".join(lines)


def format_csv_report(
    missing_routes: Sequence[CatalogEntry],
    missing_catalog: Sequence[ResourceRoute],
    citation_warnings: Sequence[ResourceRoute],
    location_warnings: Sequence[ResourceRoute],
    location_exemptions: Sequence[ResourceRoute],
    step_citation_warnings: Sequence[ResourceRoute],
) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "type",
            "id",
            "title",
            "shortage_menu",
            "citation_count",
            "missing_field_steps",
            "under_cited_field_steps",
        ]
    )
    for entry in missing_routes:
        writer.writerow(
            [
                "catalog_without_route",
                entry.entry_id,
                entry.title,
                "true" if entry.shortage_menu else "false",
                "",
                "",
                "",
            ]
        )
    for route in missing_catalog:
        writer.writerow([
            "route_without_catalog",
            route.route_id,
            route.title,
            "",
            len(route.citations),
            "",
            ";".join(route.under_cited_field_step_ids),
        ])
    for route in citation_warnings:
        writer.writerow(
            [
                "route_citation_warning",
                route.route_id,
                route.title,
                "",
                len(route.citations),
                "",
                ";".join(route.under_cited_field_step_ids),
            ]
        )
    for route in location_warnings:
        writer.writerow(
            [
                "route_missing_field_coords",
                route.route_id,
                route.title,
                "",
                len(route.citations),
                ";".join(route.missing_field_step_ids),
                ";".join(route.under_cited_field_step_ids),
            ]
        )
    for route in location_exemptions:
        writer.writerow(
            [
                "route_field_coord_exempt",
                route.route_id,
                route.title,
                "",
                len(route.citations),
                ";".join(route.exempt_field_step_ids),
                ";".join(route.under_cited_field_step_ids),
            ]
        )
    for route in step_citation_warnings:
        writer.writerow(
            [
                "route_under_cited_field_steps",
                route.route_id,
                route.title,
                "",
                len(route.citations),
                ";".join(route.missing_field_step_ids),
                ";".join(route.under_cited_field_step_ids),
            ]
        )
    return buffer.getvalue().rstrip("\n")


def format_report(
    missing_routes: Iterable[CatalogEntry],
    missing_catalog: Iterable[ResourceRoute],
    citation_warnings: Iterable[ResourceRoute],
    location_warnings: Iterable[ResourceRoute],
    location_exemptions: Iterable[ResourceRoute],
    step_citation_warnings: Iterable[ResourceRoute],
    report_format: str,
) -> str:
    missing_routes_list = list(missing_routes)
    missing_catalog_list = list(missing_catalog)
    citation_warnings_list = list(citation_warnings)
    location_warnings_list = list(location_warnings)
    location_exemptions_list = list(location_exemptions)
    step_citation_warnings_list = list(step_citation_warnings)

    if report_format == "markdown":
        return format_markdown_report(
            missing_routes_list,
            missing_catalog_list,
            citation_warnings_list,
            location_warnings_list,
            location_exemptions_list,
            step_citation_warnings_list,
        )
    if report_format == "csv":
        return format_csv_report(
            missing_routes_list,
            missing_catalog_list,
            citation_warnings_list,
            location_warnings_list,
            location_exemptions_list,
            step_citation_warnings_list,
        )
    return format_text_report(
        missing_routes_list,
        missing_catalog_list,
        citation_warnings_list,
        location_warnings_list,
        location_exemptions_list,
        step_citation_warnings_list,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Summarise resource coverage gaps between guides.md and the shortage catalog."
        )
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "csv"),
        default="text",
        help="Output format. Defaults to human-readable text.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file path to write the report instead of printing to stdout.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    markdown = GUIDES_PATH.read_text(encoding="utf-8")
    routes = parse_resource_routes(markdown)
    entries = load_catalog_entries()

    route_ids: Set[str] = {route.route_id for route in routes}
    catalog_ids: Set[str] = {entry.entry_id for entry in entries}

    missing_routes = [entry for entry in entries if entry.entry_id not in route_ids]
    missing_catalog = [route for route in routes if route.route_id not in catalog_ids]
    citation_warnings = [route for route in routes if len(route.citations) < 2]
    location_warnings = [
        route for route in routes if route.missing_field_step_ids
    ]
    location_exemptions = [
        route for route in routes if route.exempt_field_step_ids
    ]
    step_citation_warnings = [
        route for route in routes if route.under_cited_field_step_ids
    ]

    report = format_report(
        missing_routes,
        missing_catalog,
        citation_warnings,
        location_warnings,
        location_exemptions,
        step_citation_warnings,
        args.format,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        output_text = report if report.endswith("\n") else report + "\n"
        args.output.write_text(output_text, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
