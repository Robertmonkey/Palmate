#!/usr/bin/env python3
"""Fetch newly added pals from Palworld wiki.gg and update the dataset."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import quote

import mwparserfromhell
import requests

DATA_PATH = Path('data/palworld_complete_data_final.json')
BASE_DATA_PATH = Path('data/palworld_complete_data.json')
ENHANCED_DATA_PATH = Path('data/palworld_complete_data_enhanced.json')
BASE_URL = 'https://palworld.wiki.gg/wiki'
RAW_FETCH_PREFIX = 'https://r.jina.ai/https://palworld.wiki.gg/wiki'
DIRECT_FETCH_PREFIX = 'https://palworld.wiki.gg/wiki'

LIST_PAGES: Tuple[str, ...] = (
    'Palpedia/Regular_Pals',
    'Palpedia/Pal_Subspecies',
    'Palpedia/Terraria_Monsters',
)

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


def fetch_raw_page(page: str) -> str:
    """Return the raw wikitext for a page, bypassing Cloudflare hurdles when possible."""

    encoded = quote(page.replace(' ', '_'))
    direct_url = f"{DIRECT_FETCH_PREFIX}/{encoded}?action=raw"
    headers = {
        'User-Agent': 'Palmate pal synchroniser',
        'Accept': 'text/plain',
    }
    for url in (direct_url, f"{RAW_FETCH_PREFIX}/{encoded}?action=raw"):
        try:
            response = requests.get(url, timeout=120, headers=headers if url == direct_url else None)
        except requests.RequestException:
            continue
        if response.status_code != 200:
            continue
        text = response.text
        # jina.ai responses include metadata wrappers we need to strip away.
        marker = 'Markdown Content:\n'
        if marker in text:
            text = text.split(marker, 1)[1]
        if 'Just a moment...' in text and 'Cloudflare' in text:
            # Cloudflare challenge page, try the next fallback.
            continue
        return text
    raise RuntimeError(f'Unable to fetch raw wiki text for {page}')


def fetch_pal_template(page: str) -> Tuple[str, mwparserfromhell.nodes.Template]:
    wikitext = fetch_raw_page(page)
    code = mwparserfromhell.parse(wikitext)
    for template in code.filter_templates():
        name = template.name.strip().lower()
        if name in {'pal', 'monster'}:
            return name, template
    raise RuntimeError(f'Pal template missing for {page}')


def fetch_list_entries(page: str) -> List[str]:
    wikitext = fetch_raw_page(page)
    return re.findall(r"PalListEntry\+\|([^}|]+)", wikitext)


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
        if not value and source == 'medicine_production':
            # Some templates still use the legacy "med_prod" parameter.
            value = extract(template, 'med_prod')
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


def sort_key_for_entry(name: str, template: mwparserfromhell.nodes.Template) -> Tuple[int, str, str]:
    raw = extract(template, 'no')
    digits = ''.join(ch for ch in raw if ch.isdigit())
    letters = ''.join(ch for ch in raw if ch.isalpha())
    try:
        numeric = int(digits)
    except ValueError:
        numeric = 10_000  # place unknown IDs at the end in a stable order
    return (numeric, letters.lower(), name.lower())


def gather_missing_names(existing: Iterable[str]) -> List[str]:
    names: set[str] = set()
    for page in LIST_PAGES:
        try:
            names.update(fetch_list_entries(page))
        except Exception as exc:  # pragma: no cover - network failure surface
            raise RuntimeError(f'Failed to fetch pal list from {page}') from exc
    missing = sorted(names - set(existing))
    return missing


def clone_section(data: dict, keys: Sequence[str]) -> dict:
    return {key: json.loads(json.dumps(data[key])) for key in keys}


def sync_dataset_variants(final_data: dict) -> None:
    subset_keys: Sequence[str] = ('pals', 'items', 'tech', 'passiveDetails', 'skillsDetails')

    base_payload = clone_section(final_data, subset_keys)
    for pal in base_payload['pals'].values():
        pal.pop('breedingCombos', None)
        pal.pop('spawnAreas', None)
    BASE_DATA_PATH.write_text(json.dumps(base_payload, indent=2, ensure_ascii=False))
    print(f'Synchronised {BASE_DATA_PATH}')

    enhanced_payload = clone_section(final_data, subset_keys)
    for pal in enhanced_payload['pals'].values():
        pal.pop('spawnAreas', None)
    ENHANCED_DATA_PATH.write_text(json.dumps(enhanced_payload, indent=2, ensure_ascii=False))
    print(f'Synchronised {ENHANCED_DATA_PATH}')


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    existing = data['pals']
    skill_lookup = build_skill_lookup(existing)

    current_names = {pal['name'] for pal in existing.values()}
    to_add = gather_missing_names(current_names)

    max_id = max(int(key) for key in existing.keys())
    fetched_templates: List[Tuple[str, str, mwparserfromhell.nodes.Template]] = []
    failures: List[str] = []

    for name in to_add:
        try:
            template_type, template = fetch_pal_template(name)
        except Exception as exc:  # pragma: no cover - network failure surface
            print(f'Failed to fetch data for {name}: {exc}')
            failures.append(name)
            continue
        fetched_templates.append((name, template_type, template))

    fetched_templates.sort(key=lambda item: sort_key_for_entry(item[0], item[2]))

    changed = False
    for name, template_type, template in fetched_templates:
        max_id += 1
        entry = build_entry(max_id, name, template_type, template, skill_lookup)
        existing[str(max_id)] = entry
        print(f'Added {name} as #{max_id}')
        changed = True

    if failures:
        print('\nThe following pals could not be processed:')
        for name in failures:
            print(f'  - {name}')

    if changed:
        DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f'Updated dataset written to {DATA_PATH}')
    else:
        print('No new pals to add!')

    sync_dataset_variants(data)


if __name__ == '__main__':
    main()
