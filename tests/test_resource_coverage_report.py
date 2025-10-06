import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.resource_coverage_report import (
    CatalogEntry,
    ResourceRoute,
    format_csv_report,
)


class FormatCsvReportTests(unittest.TestCase):
    def test_format_csv_report_covers_all_sections(self) -> None:
        missing_routes = [
            CatalogEntry(
                entry_id="resource-honey",
                title="Honey Farming Loop",
                shortage_menu=True,
            )
        ]
        missing_catalog = [
            ResourceRoute(
                route_id="resource-pal-oil",
                title="Oil Sweep",
                citations=("palwiki-pal-oil",),
                field_step_ids=("resource-pal-oil:001",),
                missing_field_step_ids=(),
                exempt_field_step_ids=(),
                under_cited_field_step_ids=("resource-pal-oil:001",),
            )
        ]
        citation_warnings = [
            ResourceRoute(
                route_id="resource-ore",
                title="Ore Mining",
                citations=(),
                field_step_ids=("resource-ore:002",),
                missing_field_step_ids=(),
                exempt_field_step_ids=(),
                under_cited_field_step_ids=("resource-ore:002",),
            )
        ]
        location_warnings = [
            ResourceRoute(
                route_id="resource-quartz",
                title="Quartz Astral Ridge",
                citations=("palwiki-quartz", "palfandom-quartz"),
                field_step_ids=("resource-quartz:003", "resource-quartz:004"),
                missing_field_step_ids=("resource-quartz:004",),
                exempt_field_step_ids=(),
                under_cited_field_step_ids=("resource-quartz:004",),
            )
        ]
        location_exemptions = [
            ResourceRoute(
                route_id="resource-lifmunk-effigy",
                title="Effigy Cleanup",
                citations=("palwiki-effigy", "palfandom-effigy"),
                field_step_ids=("resource-effigy:001",),
                missing_field_step_ids=(),
                exempt_field_step_ids=("resource-effigy:001",),
                under_cited_field_step_ids=(),
            )
        ]
        step_citation_warnings = [
            ResourceRoute(
                route_id="resource-leather",
                title="Leather Farms",
                citations=("palwiki-leather", "palfandom-leather"),
                field_step_ids=("resource-leather:001", "resource-leather:002"),
                missing_field_step_ids=(),
                exempt_field_step_ids=(),
                under_cited_field_step_ids=("resource-leather:001",),
            )
        ]

        csv_output = format_csv_report(
            missing_routes,
            missing_catalog,
            citation_warnings,
            location_warnings,
            location_exemptions,
            step_citation_warnings,
        )

        expected_rows = [
            [
                "type",
                "id",
                "title",
                "shortage_menu",
                "citation_count",
                "missing_field_steps",
                "under_cited_field_steps",
            ],
            [
                "catalog_without_route",
                "resource-honey",
                "Honey Farming Loop",
                "true",
                "",
                "",
                "",
            ],
            [
                "route_without_catalog",
                "resource-pal-oil",
                "Oil Sweep",
                "",
                "1",
                "",
                "resource-pal-oil:001",
            ],
            [
                "route_citation_warning",
                "resource-ore",
                "Ore Mining",
                "",
                "0",
                "",
                "resource-ore:002",
            ],
            [
                "route_missing_field_coords",
                "resource-quartz",
                "Quartz Astral Ridge",
                "",
                "2",
                "resource-quartz:004",
                "resource-quartz:004",
            ],
            [
                "route_field_coord_exempt",
                "resource-lifmunk-effigy",
                "Effigy Cleanup",
                "",
                "2",
                "resource-effigy:001",
                "",
            ],
            [
                "route_under_cited_field_steps",
                "resource-leather",
                "Leather Farms",
                "",
                "2",
                "",
                "resource-leather:001",
            ],
        ]

        reader = csv.reader(io.StringIO(csv_output))
        self.assertEqual(list(reader), expected_rows)


class CliCsvOutputTests(unittest.TestCase):
    def test_cli_emits_expected_header_and_shape(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "scripts" / "resource_coverage_report.py"
        result = subprocess.run(
            [sys.executable, str(script_path), "--format", "csv"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = result.stdout.strip()
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        self.assertGreaterEqual(len(rows), 1)
        self.assertEqual(
            rows[0],
            [
                "type",
                "id",
                "title",
                "shortage_menu",
                "citation_count",
                "missing_field_steps",
                "under_cited_field_steps",
            ],
        )
        for row in rows[1:]:
            self.assertEqual(len(row), 7)


if __name__ == "__main__":
    unittest.main()
