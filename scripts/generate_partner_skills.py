#!/usr/bin/env python3
"""Fetch partner skill data from the Palworld wiki and refresh data/partner_skills.json."""
from __future__ import annotations

import json
import re
import unicodedata
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List

SOURCE_URL = "https://palworld.wiki.gg/wiki/Partner_Skills"
FETCH_URL = "https://r.jina.ai/https://palworld.wiki.gg/wiki/Partner_Skills"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "partner_skills.json"


def fetch_markdown() -> str:
    request = urllib.request.Request(
        FETCH_URL,
        headers={"User-Agent": "Palmate partner skill synchroniser"},
    )
    with urllib.request.urlopen(request) as response:  # noqa: S310
        payload = response.read()
    return payload.decode("utf-8")


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    cleaned = "".join(ch for ch in normalized if ch.isalnum() or ch in {" ", "-", "_"})
    cleaned = cleaned.replace("_", " ")
    return re.sub(r"\s+", "-", cleaned).strip("-")


def clean_markdown(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_partner_skills(markdown: str) -> List[Dict]:
    rows: Dict[str, Dict] = {}
    link_pattern = re.compile(r"\[(?!\!)([^\]]+?)\]\(https://palworld.wiki.gg/wiki/[^)]+\)")
    for line in markdown.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 5 or parts[0] in {"Skill Name", "---"}:
            continue
        number = parts[2]
        if not number.isdigit():
            continue
        skill_name = parts[0]
        pal_names = [name for name in link_pattern.findall(parts[1]) if name.lower() != "pal"]
        type_text = clean_markdown(parts[3])
        description = clean_markdown(parts[4])
        record = rows.setdefault(
            skill_name,
            {
                "id": slugify(skill_name),
                "number": int(number),
                "name": skill_name,
                "pals": set(),
                "type": type_text,
                "categories": set(),
                "description": description,
            },
        )
        record["pals"].update(pal_names)
        for chunk in type_text.split("/"):
            label = chunk.strip()
            if label:
                record["categories"].add(label)
    output: List[Dict] = []
    for entry in rows.values():
        output.append(
            {
                "id": entry["id"],
                "number": entry["number"],
                "name": entry["name"],
                "pals": sorted(entry["pals"]),
                "type": entry["type"],
                "categories": sorted(entry["categories"], key=str.lower),
                "description": entry["description"],
            }
        )
    output.sort(key=lambda item: item["number"])
    return output


def main() -> None:
    markdown = fetch_markdown()
    records = parse_partner_skills(markdown)
    OUTPUT_PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        display_path = OUTPUT_PATH.relative_to(Path.cwd())
    except ValueError:
        display_path = OUTPUT_PATH
    print(f"Wrote {len(records)} partner skills to {display_path}")


if __name__ == "__main__":
    main()
