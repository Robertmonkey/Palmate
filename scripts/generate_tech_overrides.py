import json
import re
from pathlib import Path
from typing import Dict, Iterable, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "tech_overrides.json"
FINAL_DATA = DATA_DIR / "palworld_complete_data_final.json"

WIKI_LINK_RE = re.compile(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]")
TEMPLATE_LINK_RE = re.compile(r"\{\{[^{}|]+\|([^{}]+?)\}\}")
HTML_TAG_RE = re.compile(r"<[^>]+>")
BR_SPLIT_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
COUNT_THEN_NAME_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*(.+)$")
NAME_THEN_COUNT_RE = re.compile(r"^(.+?)[\sx×]*(\d+(?:\.\d+)?)$", re.IGNORECASE)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def clean_text(value: str) -> str:
    if not value:
        return ""
    # Replace HTML line breaks with spaces before stripping tags
    value = BR_SPLIT_RE.sub(" ", value)
    # Replace wiki links [[display|target]] -> display
    value = WIKI_LINK_RE.sub(r"\1", value)
    # Replace simple templates like {{i|Cooling}} -> Cooling
    value = TEMPLATE_LINK_RE.sub(r"\1", value)
    # Remove HTML tags
    value = HTML_TAG_RE.sub("", value)
    # Collapse whitespace
    value = re.sub(r"\s+", " ", value)
    # Ensure punctuation is followed by a space when the wiki markup omitted one
    value = re.sub(r"(?<=[a-z0-9])\.(?=[A-Z])", ". ", value)
    value = value.replace("Chasnge", "Change")
    return value.strip()


def parse_structure_block(text: str) -> Dict[str, str]:
    start = text.find("{{Structure")
    if start == -1:
        return {}
    depth = 0
    idx = start
    end = None
    while idx < len(text):
        if text.startswith("{{", idx):
            depth += 1
            idx += 2
            continue
        if text.startswith("}}", idx):
            depth -= 1
            idx += 2
            if depth == 0:
                end = idx
                break
            continue
        idx += 1
    if end is None:
        return {}
    block = text[start:end]
    lines = block.splitlines()
    data: Dict[str, str] = {}
    for line in lines:
        if not line.startswith("|"):
            continue
        if "=" not in line:
            continue
        key, raw_value = line[1:].split("=", 1)
        data[key.strip()] = raw_value.strip()
    return data


def parse_generic_block(text: str, template_names: Iterable[str]) -> Dict[str, str]:
    for name in template_names:
        marker = "{{" + name
        start = text.find(marker)
        if start == -1:
            continue
        depth = 0
        idx = start
        end = None
        while idx < len(text):
            if text.startswith("{{", idx):
                depth += 1
                idx += 2
                continue
            if text.startswith("}}", idx):
                depth -= 1
                idx += 2
                if depth == 0:
                    end = idx
                    break
                continue
            idx += 1
        if end is None:
            continue
        block = text[start:end]
        data: Dict[str, str] = {}
        for line in block.splitlines():
            if not line.startswith("|") or "=" not in line:
                continue
            key, raw_value = line[1:].split("=", 1)
            data[key.strip().lower()] = raw_value.strip()
        if data:
            return data
    return {}


def parse_materials_from_template(data: Dict[str, str]) -> Dict[str, int]:
    materials: Dict[str, int] = {}
    for index in range(1, 8):
        mat_key = f"mat{index}"
        qty_key = f"qty{index}"
        material = clean_text(data.get(mat_key, ""))
        qty_raw = data.get(qty_key)
        if not material:
            continue
        try:
            quantity = int(float(qty_raw)) if qty_raw else None
        except ValueError:
            quantity = None
        if quantity is None:
            continue
        materials[material] = quantity
    return materials


def parse_materials_field(raw: Optional[str]) -> Dict[str, int]:
    if not raw:
        return {}
    parts = BR_SPLIT_RE.split(raw)
    materials: Dict[str, int] = {}
    for part in parts:
        text = clean_text(part)
        if not text:
            continue
        match = COUNT_THEN_NAME_RE.match(text)
        if match:
            quantity = int(float(match.group(1)))
            material = match.group(2).strip()
            if material:
                materials[material] = quantity
            continue
        match = NAME_THEN_COUNT_RE.match(text)
        if match:
            material = match.group(1).strip()
            quantity = int(float(match.group(2)))
            if material:
                materials[material] = quantity
            continue
    return materials


def extract_first_paragraph(text: str) -> str:
    sections = text.split("}}", 1)
    body = sections[1] if len(sections) > 1 else text
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("="):
            continue
        cleaned = clean_text(stripped)
        if cleaned:
            return cleaned
    return ""


def fetch_wikitext(name: str) -> Optional[str]:
    try:
        url = (
            "https://palworld.fandom.com/api.php?action=parse&page="
            + quote(name.replace(" ", "_"))
            + "&prop=wikitext&format=json"
        )
        req = Request(url, headers={"User-Agent": "Palmate Tech Override/1.0"})
        with urlopen(req, timeout=20) as resp:
            data = json.load(resp)
        return data["parse"]["wikitext"]["*"]
    except (HTTPError, URLError, KeyError, json.JSONDecodeError, TimeoutError):
        return None


def parse_page_payload(text: str) -> Dict[str, object]:
    template = parse_structure_block(text)
    if not template:
        template = parse_generic_block(
            text,
            (
                "Infobox Structure",
                "Infobox structure",
                "Infobox_Structure",
                "Infobox Item",
                "Infobox_Item",
            ),
        )
    if not template:
        return {}
    description = clean_text(
        template.get("description")
        or template.get("effects")
        or template.get("effect")
        or ""
    )
    if not description:
        description = extract_first_paragraph(text)
    materials = parse_materials_from_template(template)
    if not materials:
        materials = parse_materials_field(template.get("materials"))
    payload: Dict[str, object] = {}
    if description:
        payload["description"] = description
    if materials:
        payload["materials"] = materials
    return payload


def main() -> None:
    overrides: Dict[str, Dict[str, object]] = {}
    for path in SOURCES.glob("palwiki-*-raw.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        data = parse_structure_block(text)
        if not data:
            continue
        tech_name = clean_text(data.get("tech_name", ""))
        if not tech_name:
            continue
        description = clean_text(data.get("description", ""))
        materials: Dict[str, int] = {}
        for index in range(1, 7):
            mat_key = f"mat{index}"
            qty_key = f"qty{index}"
            material = clean_text(data.get(mat_key, ""))
            qty_raw = data.get(qty_key)
            if not material:
                continue
            try:
                quantity = int(float(qty_raw)) if qty_raw else None
            except ValueError:
                quantity = None
            if quantity is None:
                continue
            materials[material] = quantity
        entry: Dict[str, object] = {}
        if description:
            entry["description"] = description
        if materials:
            entry["materials"] = materials
        if not entry:
            continue
        slug = slugify(tech_name)
        overrides[slug] = entry

    if not FINAL_DATA.exists():
        ordered = dict(sorted(overrides.items()))
        OUTPUT.write_text(
            json.dumps(ordered, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return

    dataset = json.loads(FINAL_DATA.read_text(encoding="utf-8"))
    tech_levels = dataset.get("tech", [])
    for level in tech_levels:
        items = level.get("items") if isinstance(level, dict) else None
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            group = item.get("group")
            if not isinstance(name, str) or group != "Structure":
                continue
            slug = slugify(name)
            if slug in overrides:
                continue
            page_text = fetch_wikitext(name)
            if not page_text:
                continue
            entry = parse_page_payload(page_text)
            if not entry:
                continue
            overrides[slug] = entry
            print(f"Fetched overrides for {name}")
    ordered = dict(sorted(overrides.items()))
    OUTPUT.write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
