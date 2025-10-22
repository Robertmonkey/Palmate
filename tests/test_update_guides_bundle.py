import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.regenerate_guides_bundle as regen
from scripts import update_guide_catalog as catalog
from scripts import update_guides_bundle as bundle


class UpdateGuidesBundleApplyIndexedListPatchTests(unittest.TestCase):
    def test_remove_handles_entries_without_identifier(self) -> None:
        items = [
            {"route_id": "route-alpha", "value": 1},
            {"legacy": True},
        ]
        summary = bundle.apply_indexed_list_patch(
            items=items,
            id_field="route_id",
            ops={"remove": ["route-alpha"]},
            entity_label="route",
        )

        self.assertEqual(items, [{"legacy": True}])
        self.assertEqual(summary, ["Removed 1 route entries."])

    def test_merge_with_empty_payload_does_not_emit_summary(self) -> None:
        items = [{"route_id": "route-beta", "value": 2}]

        summary = bundle.apply_indexed_list_patch(
            items=items,
            id_field="route_id",
            ops={"merge": {}},
            entity_label="route",
        )

        self.assertEqual(summary, [])


class UpdateGuideCatalogApplyIndexedListPatchTests(unittest.TestCase):
    def test_remove_handles_missing_identifiers(self) -> None:
        items = [
            {"id": "resource-honey"},
            {"name": "legacy-entry"},
        ]

        summary = catalog.apply_indexed_list_patch(
            items=items,
            id_field="id",
            ops={"remove": ["resource-honey"]},
            entity_label="guide catalog",
        )

        self.assertEqual(items, [{"name": "legacy-entry"}])
        self.assertEqual(summary, ["Removed 1 guide catalog entries."])


class RegenerateGuidesBundleBuildBundleTests(unittest.TestCase):
    def test_build_bundle_allows_empty_extras_list(self) -> None:
        components = regen.BundleComponents(
            metadata={"schema_version": 1},
            xp={"xp_thresholds": []},
            route_schema={"fields": []},
            routes=[{"route_id": "route-test"}],
            level_estimator={"levels": []},
            recommender={"routes": []},
            guide_catalog_meta={"guide_count": 0},
            source_registry={},
            extras=[],
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            catalog_path = Path(tmpdir) / "guide_catalog.json"
            catalog_path.write_text(json.dumps({"guides": []}), encoding="utf-8")

            with patch.object(regen, "GUIDE_CATALOG_PATH", catalog_path):
                bundle_payload = regen.build_bundle(components)

        self.assertEqual(bundle_payload["extras"], [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
