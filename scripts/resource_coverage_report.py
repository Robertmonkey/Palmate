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

REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDES_PATH = REPO_ROOT / "guides.md"
CATALOG_PATH = REPO_ROOT / "data" / "guide_catalog.json"

ROUTE_BLOCK_PATTERN = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
CITATION_INLINE_PATTERN = re.compile(r"【([^】]+)】")


@dataclass(frozen=True)
class ResourceRoute:
    route_id: str
    title: str
    citation_keys: frozenset[str]


@dataclass(frozen=True)
class CatalogEntry:
    entry_id: str
    title: str
    shortage_menu: bool


def _normalise_citation(raw: str) -> str | None:
    """Return the canonical citation identifier if ``raw`` is usable."""

    if not isinstance(raw, str):
        return None
    key = raw.split("\u2020", 1)[0]  # strip †-style suffixes if present
    key = key.split("†", 1)[0]  # defensive in case plain ASCII dagger is used
    key = key.strip()
    return key or None


def extract_citations(payload: object) -> Set[str]:
    """Recursively gather citation identifiers from a JSON payload."""

    collected: Set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "citations" and isinstance(value, list):
                    for entry in value:
                        normalised = _normalise_citation(entry)
                        if normalised:
                            collected.add(normalised)
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, str):
            for match in CITATION_INLINE_PATTERN.finditer(node):
                raw_key = match.group(1)
                normalised = _normalise_citation(raw_key)
                if normalised:
                    collected.add(normalised)

    walk(payload)
    return collected


@dataclass(frozen=True)
class CitationWarning:
    route_id: str
    title: str
    citation_count: int


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
            citations = frozenset(extract_citations(payload))
            routes.append(
                ResourceRoute(route_id=route_id, title=title, citation_keys=citations)
            )
    return routes


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
    citation_warnings: Sequence[CitationWarning],
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
        f"Resource routes lacking at least two citations: {len(citation_warnings)}"
    )
    if citation_warnings:
        for warning in citation_warnings:
            count = warning.citation_count
            plural = "citation" if count == 1 else "citations"
            lines.append(
                f"  - {warning.route_id} ({warning.title or 'untitled'}) – {count} {plural}"
            )
    else:
        lines.append("All resource routes include at least two citations.")

    return "\n".join(lines)


def format_markdown_report(
    missing_routes: Sequence[CatalogEntry],
    missing_catalog: Sequence[ResourceRoute],
    citation_warnings: Sequence[CitationWarning],
) -> str:
    lines = ["# Resource Coverage Report", ""]
    lines.append(f"- Catalog entries without matching routes: **{len(missing_routes)}**")
    lines.append(f"- Routes missing catalog entries: **{len(missing_catalog)}**")
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
        lines.append("")
    else:
        lines.append("All resource routes are present in the catalog.")
        lines.append("")

    if citation_warnings:
        lines.append("## Citation coverage warnings")
        for warning in citation_warnings:
            count = warning.citation_count
            plural = "citation" if count == 1 else "citations"
            lines.append(
                f"- `{warning.route_id}` – {warning.title or 'untitled'} ({count} {plural})"
            )
    else:
        lines.append("All resource routes include at least two citations.")

    return "\n".join(lines)


def format_csv_report(
    missing_routes: Sequence[CatalogEntry],
    missing_catalog: Sequence[ResourceRoute],
    citation_warnings: Sequence[CitationWarning],
) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["type", "id", "title", "shortage_menu"])
    for entry in missing_routes:
        writer.writerow(
            [
                "catalog_without_route",
                entry.entry_id,
                entry.title,
                "true" if entry.shortage_menu else "false",
            ]
        )
    for route in missing_catalog:
        writer.writerow(
            [
                "route_without_catalog",
                route.route_id,
                route.title,
                "",
            ]
        )
    for warning in citation_warnings:
        writer.writerow(
            [
                "citation_warning",
                warning.route_id,
                warning.title,
                str(warning.citation_count),
            ]
        )
    return buffer.getvalue().rstrip("\n")


def format_report(
    missing_routes: Iterable[CatalogEntry],
    missing_catalog: Iterable[ResourceRoute],
    citation_warnings: Iterable[CitationWarning],
    report_format: str,
) -> str:
    missing_routes_list = list(missing_routes)
    missing_catalog_list = list(missing_catalog)
    citation_warnings_list = list(citation_warnings)

    if report_format == "markdown":
        return format_markdown_report(
            missing_routes_list, missing_catalog_list, citation_warnings_list
        )
    if report_format == "csv":
        return format_csv_report(
            missing_routes_list, missing_catalog_list, citation_warnings_list
        )
    return format_text_report(
        missing_routes_list, missing_catalog_list, citation_warnings_list
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

    citation_warnings = [
        CitationWarning(
            route_id=route.route_id,
            title=route.title,
            citation_count=len(route.citation_keys),
        )
        for route in routes
        if len(route.citation_keys) < 2
    ]

    report = format_report(missing_routes, missing_catalog, citation_warnings, args.format)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        output_text = report if report.endswith("\n") else report + "\n"
        args.output.write_text(output_text, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
