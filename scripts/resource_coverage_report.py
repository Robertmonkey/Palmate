#!/usr/bin/env python3
"""Generate a coverage report for shortage resource guides.

The script inspects guides.md for resource routes, loads the guide
catalog metadata, and compares the two lists. It surfaces resources
missing full route JSON, catalog entries, or both so the agent can
prioritise new work quickly.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set

REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDES_PATH = REPO_ROOT / "guides.md"
CATALOG_PATH = REPO_ROOT / "data" / "guide_catalog.json"

ROUTE_BLOCK_PATTERN = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


@dataclass(frozen=True)
class ResourceRoute:
    route_id: str
    title: str


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
            routes.append(ResourceRoute(route_id=route_id, title=title))
    return routes


def load_catalog_entries() -> List[CatalogEntry]:
    catalog = json.loads(CATALOG_PATH.read_text())
    entries: List[CatalogEntry] = []
    for section in catalog.get("sections", []):
        for item in section.get("entries", []):
            entry_id = item.get("id")
            if not isinstance(entry_id, str):
                continue
            if not entry_id.startswith("resource-"):
                continue
            entries.append(
                CatalogEntry(
                    entry_id=entry_id,
                    title=item.get("title", ""),
                    shortage_menu=bool(item.get("shortage_menu", False)),
                )
            )
    return entries


def format_report(missing_routes: Iterable[CatalogEntry], missing_catalog: Iterable[ResourceRoute]) -> str:
    lines = ["Resource Coverage Report"]
    lines.append("========================\n")

    missing_route_list = list(missing_routes)
    if missing_route_list:
        lines.append("Catalog entries without matching routes:")
        for entry in missing_route_list:
            status = "shortage-menu" if entry.shortage_menu else "catalog-only"
            lines.append(f"  - {entry.entry_id} ({entry.title or 'untitled'}) [{status}]")
    else:
        lines.append("All catalogued resources have matching routes.")

    lines.append("")

    missing_catalog_list = list(missing_catalog)
    if missing_catalog_list:
        lines.append("Routes missing catalog entries:")
        for route in missing_catalog_list:
            lines.append(f"  - {route.route_id} ({route.title or 'untitled'})")
    else:
        lines.append("All resource routes are present in the catalog.")

    return "\n".join(lines)


def main() -> None:
    markdown = GUIDES_PATH.read_text(encoding="utf-8")
    routes = parse_resource_routes(markdown)
    entries = load_catalog_entries()

    route_ids: Set[str] = {route.route_id for route in routes}
    catalog_ids: Set[str] = {entry.entry_id for entry in entries}

    missing_routes = [entry for entry in entries if entry.entry_id not in route_ids]
    missing_catalog = [route for route in routes if route.route_id not in catalog_ids]

    report = format_report(missing_routes, missing_catalog)
    print(report)


if __name__ == "__main__":
    main()
