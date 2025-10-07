#!/usr/bin/env python3
"""Synchronise the Palworld technology table with the local dataset."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import mwparserfromhell  # type: ignore
import requests
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FINAL_DATA = DATA_DIR / "palworld_complete_data_final.json"
ENHANCED_DATA = DATA_DIR / "palworld_complete_data_enhanced.json"
OVERRIDES_DATA = DATA_DIR / "tech_overrides.json"
FANDOM_API = (
    "https://palworld.fandom.com/api.php"
    "?action=parse&page=Technology&prop=wikitext&format=json"
)
IMAGE_BASE = "https://palworld.fandom.com/wiki/Special:FilePath/"

TYPE_LABELS = {
    "s": "Structure",
    "i": "Item",
    "S": "Structure",
    "I": "Item",
}
CATEGORY_DEFAULTS = {
    "s": "Base Building",
    "i": "Equipment",
    "S": "Base Building",
    "I": "Equipment",
}


@dataclass
class TechInfo:
    name: str
    branch: str
    type_code: str
    points: int
    image: Optional[str]
    enhanced: Dict[str, object]

    @property
    def slug(self) -> str:
        return slugify(self.name)

    @property
    def id(self) -> str:
        value = self.enhanced.get("id") if isinstance(self.enhanced, dict) else None
        if isinstance(value, str) and value:
            return value
        return self.slug

    @property
    def category(self) -> str:
        if isinstance(self.enhanced, dict):
            value = self.enhanced.get("category")
            if isinstance(value, str) and value.strip():
                return value
        default = CATEGORY_DEFAULTS.get(self.type_code, "Technology")
        if self.branch == "Ancient Technology":
            return "Ancient Tech"
        return default

    @property
    def group(self) -> str:
        return TYPE_LABELS.get(self.type_code, "Item")

    @property
    def description(self) -> str:
        if isinstance(self.enhanced, dict):
            value = self.enhanced.get("description")
            if isinstance(value, str) and value.strip():
                return value.strip()
        if self.branch == "Ancient Technology":
            return f"Unlocks the ancient blueprint for the {self.name}."
        if self.group == "Structure":
            return f"Unlocks the {self.name} structure at your base."
        return f"Unlocks the recipe for {self.name}."

    @property
    def materials(self) -> Optional[Dict[str, int]]:
        if isinstance(self.enhanced, dict):
            value = self.enhanced.get("materials")
            if isinstance(value, dict) and value:
                # Ensure integer quantities where possible
                cleaned: Dict[str, int] = {}
                for material, qty in value.items():
                    try:
                        cleaned[str(material)] = int(qty)
                    except (TypeError, ValueError):
                        continue
                if cleaned:
                    return cleaned
        return None

    @property
    def image_url(self) -> Optional[str]:
        if not self.image:
            return None
        file_name = self.image.replace(" ", "_")
        return IMAGE_BASE + quote(file_name)

    def to_payload(self) -> Dict[str, object]:
        data: Dict[str, object] = {
            "id": self.id,
            "name": self.name,
            "branch": self.branch,
            "group": self.group,
            "category": self.category,
            "techPoints": self.points,
            "description": self.description,
            "isAncient": self.branch == "Ancient Technology",
        }
        materials = self.materials
        if materials:
            data["materials"] = materials
        image_url = self.image_url
        if image_url:
            data["image"] = image_url
        return data


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_points(raw: Optional[str]) -> int:
    if not raw:
        return 0
    match = re.search(r"\d+", raw)
    return int(match.group()) if match else 0


def load_enhanced_map() -> Dict[str, Dict[str, object]]:
    if not ENHANCED_DATA.exists():
        mapping: Dict[str, Dict[str, object]] = {}
    else:
        payload = json.loads(ENHANCED_DATA.read_text(encoding="utf-8"))
        mapping = {}
        for level in payload.get("tech", []):
            items = level.get("items") if isinstance(level, dict) else None
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                if not isinstance(name, str):
                    continue
                mapping[slugify(name)] = item

    if OVERRIDES_DATA.exists():
        overrides = json.loads(OVERRIDES_DATA.read_text(encoding="utf-8"))
        for key, value in overrides.items():
            if not isinstance(value, dict):
                continue
            slug = slugify(key)
            target = mapping.setdefault(slug, {})
            target.update(value)
    return mapping


def fetch_wikitext() -> str:
    response = requests.get(FANDOM_API, timeout=30, headers={"User-Agent": "Palmate Tech Sync/1.0"})
    response.raise_for_status()
    payload = response.json()
    return payload["parse"]["wikitext"]["*"]


def extract_table(wikitext: str) -> str:
    marker = '{| class="fandom-table" width="100%"'
    start = wikitext.find(marker)
    if start == -1:
        raise RuntimeError("Could not locate technology table in wikitext")
    end = wikitext.find("|}", start)
    if end == -1:
        raise RuntimeError("Technology table appears to be truncated")
    return wikitext[start:end]


def parse_techboxes(block: str) -> Iterable[mwparserfromhell.nodes.Template]:
    code = mwparserfromhell.parse(block)
    for template in code.filter_templates():
        if template.name.strip().lower() == "techbox":
            yield template


def build_items(
    block: str,
    branch: str,
    enhanced_map: Dict[str, Dict[str, object]],
    seen: set[str],
) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    for template in parse_techboxes(block):
        name = str(template.get("name").value).strip() if template.has("name") else ""
        if not name:
            continue
        type_code = str(template.get("type").value).strip() if template.has("type") else ""
        points_raw = str(template.get("points").value).strip() if template.has("points") else ""
        image = str(template.get("image").value).strip() if template.has("image") else None
        info = TechInfo(
            name=name,
            branch=branch,
            type_code=type_code,
            points=parse_points(points_raw),
            image=image,
            enhanced=enhanced_map.get(slugify(name), {}),
        )
        slug = info.slug
        if slug in seen:
            continue
        seen.add(slug)
        items.append(info.to_payload())
    return items


def build_levels(wikitext: str, enhanced_map: Dict[str, Dict[str, object]]) -> List[Dict[str, object]]:
    table = extract_table(wikitext)
    rows = table.split("\n|-\n")
    # First entry before the first row is the header metadata; skip it.
    rows = rows[1:]
    levels: List[Dict[str, object]] = []
    seen_slugs: set[str] = set()
    for raw_row in rows:
        parts = re.split(r"\n\|", raw_row)
        if not parts:
            continue
        level_raw = parts[0].split("|")[-1].strip()
        if not level_raw:
            continue
        try:
            level_number = int(level_raw)
        except ValueError:
            continue
        standard_block = parts[1] if len(parts) > 1 else ""
        ancient_block = parts[2] if len(parts) > 2 else ""
        standard_items = build_items(standard_block, "Technology", enhanced_map, seen_slugs)
        ancient_items = build_items(ancient_block, "Ancient Technology", enhanced_map, seen_slugs)
        combined = standard_items + ancient_items
        level_entry: Dict[str, object] = {
            "level": level_number,
            "items": combined,
        }
        if combined:
            levels.append(level_entry)
    levels.sort(key=lambda entry: entry.get("level", 0))
    return levels


def update_dataset(levels: List[Dict[str, object]]) -> None:
    payload = json.loads(FINAL_DATA.read_text(encoding="utf-8"))
    payload["tech"] = levels
    FINAL_DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    enhanced_map = load_enhanced_map()
    wikitext = fetch_wikitext()
    levels = build_levels(wikitext, enhanced_map)
    if not levels:
        raise RuntimeError("No technology levels were parsed")
    update_dataset(levels)
    print(f"Updated {FINAL_DATA.relative_to(ROOT)} with {len(levels)} technology tiers.")


if __name__ == "__main__":
    main()
