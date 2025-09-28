#!/usr/bin/env python3
"""Fetch newly added pals from Palworld wiki.gg and update the dataset."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

import mwparserfromhell
import requests
from bs4 import BeautifulSoup

DATA_PATH = Path('data/palworld_complete_data_final.json')
BASE_URL = 'https://palworld.wiki.gg/wiki'

PAL_INFOS = [
    (141, 'Prunelia'),
    (142, 'Nyafia'),
    (143, 'Gildane'),
    (144, 'Herbil'),
    (145, 'Icelyn'),
    (146, 'Frostplume'),
    (147, 'Palumba'),
    (148, 'Braloha'),
    (149, 'Munchill'),
    (150, 'Polapup'),
    (151, 'Turtacle'),
    (152, 'Turtacle Terra'),
    (153, 'Jellroy'),
    (154, 'Jelliette'),
    (155, 'Gloopie'),
    (156, 'Finsider'),
    (157, 'Finsider Ignis'),
    (158, 'Ghangler'),
    (159, 'Ghangler Ignis'),
    (160, 'Whalaska'),
    (161, 'Whalaska Ignis'),
    (162, 'Neptilius'),
    (163, 'Fuack Ignis'),
    (164, 'Pengullet Lux'),
    (165, 'Penking Lux'),
    (166, 'Killamari Primo'),
    (167, 'Celaray Lux'),
    (168, 'Dumud Gild'),
    (169, 'Azurobe Cryst'),
    (170, 'Croajiro Noct'),
    (171, 'Eye of Cthulhu'),
    (172, 'Enchanted Sword'),
    (173, 'Illuminant Slime'),
    (174, 'Illuminant Bat'),
    (175, 'Rainbow Slime'),
    (176, 'Cave Bat'),
    (177, 'Red Slime'),
    (178, 'Purple Slime'),
    (179, 'Demon Eye'),
    (180, 'Green Slime'),
    (181, 'Blue Slime'),
]

WORK_FIELDS = {
    'handiwork': 'handiwork',
    'watering': 'watering',
    'planting': 'planting',
    'kindling': 'kindling',
    'lumbering': 'lumbering',
    'gathering': 'gathering',
    'mining': 'mining',
    'medicine_production': 'medicine_production',
    'transporting': 'transporting',
    'cooling': 'cooling',
    'farming': 'farming',
    'generating_electricity': 'generating_electricity',
}

STAT_FIELDS = ['hp', 'attack', 'defense', 'stamina', 'support']

SKILL_LEVEL_RE = re.compile(r'^activeskill(\d+)$', re.IGNORECASE)


def slugify(value: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '_', value.lower()).strip('_')
    return slug or value.lower()


def parse_number(raw: str) -> Optional[float]:
    if raw is None:
        return None
    text = raw.strip()
    if not text or text in {'?', '???'}:
        return None
    text = text.replace(',', '')
    try:
        if '.' in text:
            return float(text)
        return float(int(text))
    except ValueError:
        return None


def fetch_pal_template(page: str) -> Tuple[str, mwparserfromhell.nodes.Template]:
    url = f"{BASE_URL}/{quote(page)}?action=edit"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    textarea = soup.select_one('#wpTextbox1')
    if textarea is None:
        raise RuntimeError(f'No editable content found for {page}')
    code = mwparserfromhell.parse(textarea.text)
    for template in code.filter_templates():
        name = template.name.strip().lower()
        if name in {'pal', 'monster'}:
            return name, template
    raise RuntimeError(f'Pal template missing for {page}')


def extract(template: mwparserfromhell.nodes.Template, key: str) -> str:
    try:
        return template.get(key).value.strip()
    except ValueError:
        return ''


def build_skill_lookup(existing: Dict[str, dict]) -> Dict[str, Dict[str, float]]:
    lookup: Dict[str, Dict[str, float]] = {}
    for pal in existing.values():
        for skill in pal.get('skills', []):
            name = skill.get('name')
            if not name:
                continue
            slug = slugify(name)
            if slug not in lookup:
                lookup[slug] = {
                    'power': skill.get('power'),
                    'cooldown': skill.get('cooldown'),
                }
    return lookup


def parse_skills(template: mwparserfromhell.nodes.Template, skill_lookup: Dict[str, Dict[str, float]]) -> List[dict]:
    skills: List[dict] = []
    for param in template.params:
        key = param.name.strip()
        match = SKILL_LEVEL_RE.match(key)
        if not match:
            continue
        level = int(match.group(1))
        name = param.value.strip()
        if not name:
            continue
        slug = slugify(name)
        defaults = skill_lookup.get(slug, {'power': None, 'cooldown': None})
        skills.append({
            'name': slug,
            'level': level,
            'power': defaults['power'],
            'cooldown': defaults['cooldown'],
        })
    skills.sort(key=lambda item: item['level'])
    return skills


def parse_drops(template: mwparserfromhell.nodes.Template) -> List[str]:
    drops: List[str] = []
    for idx in range(1, 6):
        value = extract(template, f'drop{idx}')
        if value:
            drops.append(slugify(value))
    seen = set()
    unique = []
    for drop in drops:
        if drop not in seen:
            seen.add(drop)
            unique.append(drop)
    return unique


def parse_work(template: mwparserfromhell.nodes.Template) -> Dict[str, int]:
    work: Dict[str, int] = {}
    for source, target in WORK_FIELDS.items():
        value = extract(template, source)
        if value and value.isdigit():
            amount = int(value)
            if amount:
                work[target] = amount
    return work


def parse_stats(template: mwparserfromhell.nodes.Template, food: Optional[float]) -> Dict[str, Optional[float]]:
    stats: Dict[str, Optional[float]] = {}
    for field in STAT_FIELDS:
        stats[field] = parse_number(extract(template, field))
    stats['speed'] = (
        parse_number(extract(template, 'run_speed'))
        or parse_number(extract(template, 'walk_speed'))
        or parse_number(extract(template, 'slow_walk_speed'))
    )
    stats['food'] = food
    return stats


def build_entry(info_id: int, name: str, template_type: str, template: mwparserfromhell.nodes.Template, skill_lookup: Dict[str, Dict[str, float]]) -> dict:
    page = name.replace(' ', '_')
    types: List[str] = []
    ele1 = extract(template, 'ele1').title()
    ele2 = extract(template, 'ele2').title()
    if ele1:
        types.append(ele1)
    if ele2:
        types.append(ele2)
    food = parse_number(extract(template, 'food'))
    drops = parse_drops(template)
    work = parse_work(template)
    stats = parse_stats(template, food)
    breeding_rank = parse_number(extract(template, 'breeding_rank'))
    key_value = extract(template, 'no') or slugify(name)
    if key_value and '_' not in key_value and any(ch.isalpha() for ch in key_value):
        key_value = key_value.upper()
    image_url = f"{BASE_URL}/Special:FilePath/{quote(name)}.png"

    entry = {
        'id': info_id,
        'key': key_value,
        'name': name,
        'wiki': f'{BASE_URL}/{quote(page)}',
        'image': image_url,
        'genus': 'unknown',
        'rarity': None,
        'price': parse_number(extract(template, 'price')),
        'size': None,
        'stats': stats,
        'work': work,
        'skills': parse_skills(template, skill_lookup),
        'drops': drops,
        'breeding': {
            'power': breeding_rank,
            'type1': types[0] if types else None,
            'type2': types[1] if len(types) > 1 else None,
        },
        'types': types,
        'localImage': None,
        'breedingCombos': [],
        'spawnAreas': [],
    }

    if template_type == 'monster':
        entry['genus'] = 'terraria'
    return entry


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    existing = data['pals']
    skill_lookup = build_skill_lookup(existing)

    for info_id, name in PAL_INFOS:
        template_type, template = fetch_pal_template(name.replace(' ', '_'))
        entry = build_entry(info_id, name, template_type, template, skill_lookup)
        existing[str(info_id)] = entry
        print(f'Updated {name} (#{info_id})')

    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
