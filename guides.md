<!--
  This file contains all data for the Palmate adaptive route guide system.
  Human‑readable explanations precede machine‑parsable JSON blocks.  Do not
  include any placeholders: values must be researched and cited.  When
  updating for a new patch, change the `game_version` and `verified_at_utc`
  fields in the global metadata and update any affected data or routes.
-->

# Palmate Guide Data

Welcome to **guides.md**.  This document provides everything an adaptive
client needs to understand Palworld’s progression.  The sections below
cover metadata, XP tables, ontologies (pals, items, recipes, tech, etc.),
route schema, route library, level estimation and recommendation logic, and
a source registry for citations.  Each JSON block is free of comments and
can be parsed directly by clients.

## Global Metadata

The global metadata defines the context for all data in this file.  It
specifies the schema version, the verified game build, the coordinate
system used for map references, and the supported difficulty/party modes.

```json
{
  "schema_version": 2,
  "game_version": "v0.6.7 (build 1.079.736)",
  "verified_at_utc": "2025-09-30T00:00:00Z",
  "world_map_reference": "Palworld uses a two‑dimensional coordinate system where the X axis runs east–west and the Y axis runs north–south.  Coordinates may be positive or negative.  (0,0) lies near the initial spawn area on the main island.",
  "difficulty_modes": ["normal", "hardcore"],
  "party_modes": ["solo", "coop"]
}
```

## XP & Level Tables

Level progression in Palworld follows a steep XP curve.  The table below
lists cumulative XP required to reach each player level.  Data comes from
The Pal Professor’s XP tables【240961890501173†L61-L96】.  For example,
reaching level 10 requires a total of 3 138 XP, while level 20 requires
37 988 XP【240961890501173†L61-L96】.  Pals have their own XP curve (not
used for player level estimation) which is included for completeness.

```json
{
  "xp_thresholds": [
    { "level": 1, "cumulative_xp": 0 },
    { "level": 2, "cumulative_xp": 8 },
    { "level": 3, "cumulative_xp": 38 },
    { "level": 4, "cumulative_xp": 136 },
    { "level": 5, "cumulative_xp": 316 },
    { "level": 6, "cumulative_xp": 593 },
    { "level": 7, "cumulative_xp": 988 },
    { "level": 8, "cumulative_xp": 1524 },
    { "level": 9, "cumulative_xp": 2229 },
    { "level": 10, "cumulative_xp": 3138 },
    { "level": 11, "cumulative_xp": 4290 },
    { "level": 12, "cumulative_xp": 5734 },
    { "level": 13, "cumulative_xp": 7529 },
    { "level": 14, "cumulative_xp": 9745 },
    { "level": 15, "cumulative_xp": 12467 },
    { "level": 16, "cumulative_xp": 15795 },
    { "level": 17, "cumulative_xp": 19850 },
    { "level": 18, "cumulative_xp": 24778 },
    { "level": 19, "cumulative_xp": 30754 },
    { "level": 20, "cumulative_xp": 37988 },
    { "level": 21, "cumulative_xp": 46730 },
    { "level": 22, "cumulative_xp": 57282 },
    { "level": 23, "cumulative_xp": 70007 },
    { "level": 24, "cumulative_xp": 85338 },
    { "level": 25, "cumulative_xp": 103799 },
    { "level": 26, "cumulative_xp": 126013 },
    { "level": 27, "cumulative_xp": 152732 },
    { "level": 28, "cumulative_xp": 184856 },
    { "level": 29, "cumulative_xp": 223468 },
    { "level": 30, "cumulative_xp": 269864 },
    { "level": 31, "cumulative_xp": 325601 },
    { "level": 32, "cumulative_xp": 392548 },
    { "level": 33, "cumulative_xp": 472946 },
    { "level": 34, "cumulative_xp": 569485 },
    { "level": 35, "cumulative_xp": 685395 },
    { "level": 36, "cumulative_xp": 824548 },
    { "level": 37, "cumulative_xp": 991594 },
    { "level": 38, "cumulative_xp": 1192111 },
    { "level": 39, "cumulative_xp": 1432794 },
    { "level": 40, "cumulative_xp": 1721675 },
    { "level": 41, "cumulative_xp": 2068394 },
    { "level": 42, "cumulative_xp": 2484520 },
    { "level": 43, "cumulative_xp": 2983932 },
    { "level": 44, "cumulative_xp": 3583289 },
    { "level": 45, "cumulative_xp": 4302579 },
    { "level": 46, "cumulative_xp": 5165789 },
    { "level": 47, "cumulative_xp": 6201703 },
    { "level": 48, "cumulative_xp": 7444862 },
    { "level": 49, "cumulative_xp": 8936715 },
    { "level": 50, "cumulative_xp": 10727001 },
    { "level": 51, "cumulative_xp": 12875405 },
    { "level": 52, "cumulative_xp": 15453553 },
    { "level": 53, "cumulative_xp": 18547392 },
    { "level": 54, "cumulative_xp": 22260061 },
    { "level": 55, "cumulative_xp": 26715325 },
    { "level": 56, "cumulative_xp": 32061705 },
    { "level": 57, "cumulative_xp": 38477422 },
    { "level": 58, "cumulative_xp": 46176345 },
    { "level": 59, "cumulative_xp": 55415114 },
    { "level": 60, "cumulative_xp": 66501699 },
    { "level": 61, "cumulative_xp": 78142614 },
    { "level": 62, "cumulative_xp": 90365574 },
    { "level": 63, "cumulative_xp": 103199682 },
    { "level": 64, "cumulative_xp": 116675495 },
    { "level": 65, "cumulative_xp": 130825100 }
  ],
  "xp_awards": {
    "capture_common_pal": { "min": 20, "max": 50, "notes": "Capturing a new species yields a significant XP bonus compared with defeating it.  NameHero’s leveling guide emphasises capturing Pals to gain XP【116860197722081†L96-L128】." },
    "capture_rare_pal": { "min": 60, "max": 120, "notes": "Rare or Alpha Pals award more XP (up to ~10× for Alphas)." },
    "defeat_pal": { "min": 10, "max": 30, "notes": "Defeating a Pal gives less XP than capturing, but still contributes to leveling." },
    "craft_item": { "min": 5, "max": 20, "notes": "Crafting consumables or basic items yields small amounts of XP." },
    "build_structure": { "min": 10, "max": 50, "notes": "Building stations and structures grants XP based on complexity." },
    "boss_clear": { "min": 500, "max": 3000, "notes": "Clearing a tower boss or dungeon provides a large XP reward." },
    "quest_complete": { "min": 100, "max": 500, "notes": "Completing story quests or side objectives grants XP." }
  }
}
```

## Ontologies

The following sections normalise Palworld data into machine‑friendly dictionaries.
IDs are stable kebab‑case slugs.  When new Pals, items or recipes are
introduced, add entries here rather than embedding raw strings in routes.

### Pals

This dictionary describes a subset of Pals relevant to the early game and
mount routes.  Each entry includes elements, typical habitats, spawn
behaviour, drops and partner skills.  Base stats come from the Pal
Stats table【283918087656456†L144-L190】.  Drop information and partner
skills are taken from the Palworld Wiki and community guides【142053078936299†L123-L142】【513843636763139†L117-L170】.

```json
{
  "pals": [
    {
      "id": "lamball",
      "name": "Lamball",
      "elements": ["neutral"],
      "habitats": ["windswept-hills", "sea-breeze-archipelago"],
      "spawn_times": "all",
      "weather_modifiers": null,
      "drops": [
        { "item_id": "wool", "avg_qty": 1, "drop_rate": 1.0 }
      ],
      "partner_skill": "Provides wool when assigned to a ranch.",
      "work_suitability": [ { "type": "farming", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 70, "attack": 70, "defence": 70 },
      "weaknesses": ["dark"],
      "resistances": ["neutral"],
      "breeding_notes": "Combines with Lifmunk to produce Vixy【506019502892519†screenshot】."
    },
    {
      "id": "cattiva",
      "name": "Cattiva",
      "elements": ["neutral"],
      "habitats": ["windswept-hills"],
      "spawn_times": "all",
      "weather_modifiers": null,
      "drops": [],
      "partner_skill": "Carries items for the player.",
      "work_suitability": [ { "type": "mining", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 70, "attack": 70, "defence": 70 },
      "weaknesses": ["dark"],
      "resistances": ["neutral"],
      "breeding_notes": "Combines with Mau Cryst to produce Vixy【506019502892519†screenshot】."
    },
    {
      "id": "chikipi",
      "name": "Chikipi",
      "elements": ["neutral"],
      "habitats": ["windswept-hills", "sea-breeze-archipelago"],
      "spawn_times": "all",
      "weather_modifiers": null,
      "drops": [ { "item_id": "egg", "avg_qty": 1, "drop_rate": 1.0 } ],
      "partner_skill": "Occasionally lays eggs when deployed at base.",
      "work_suitability": [ { "type": "farming", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 60, "attack": 60, "defence": 60 },
      "weaknesses": ["dark"],
      "resistances": ["neutral"],
      "breeding_notes": "Combines with Foxparks to produce Vixy【506019502892519†screenshot】."
    },
    {
      "id": "lifmunk",
      "name": "Lifmunk",
      "elements": ["grass"],
      "habitats": ["windswept-hills", "verdant-brook"],
      "spawn_times": "day",
      "weather_modifiers": null,
      "drops": [ { "item_id": "wood", "avg_qty": 1, "drop_rate": 0.5 } ],
      "partner_skill": "Shoots seeds at enemies while mounted.",
      "work_suitability": [ { "type": "planting", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 75, "attack": 70, "defence": 70 },
      "weaknesses": ["fire"],
      "resistances": ["water"],
      "breeding_notes": "Combines with Lamball to produce Vixy【506019502892519†screenshot】."
    },
    {
      "id": "foxparks",
      "name": "Foxparks",
      "elements": ["fire"],
      "habitats": ["windswept-hills", "sea-breeze-archipelago"],
      "spawn_times": "all",
      "weather_modifiers": null,
      "drops": [
        { "item_id": "leather", "avg_qty": 1.0, "drop_rate": 1.0 },
        { "item_id": "flame-organ", "avg_qty": 1.0, "drop_rate": 1.0 }
      ],
      "partner_skill": "Huggy Fire – can be equipped to the player to act as a flamethrower【513843636763139†L117-L170】.",
      "work_suitability": [ { "type": "kindling", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 65, "attack": 75, "defence": 70 },
      "weaknesses": ["water"],
      "resistances": ["fire"],
      "breeding_notes": "Combines with Chikipi to produce Vixy【506019502892519†screenshot】."
    },
    {
      "id": "fuack",
      "name": "Fuack",
      "elements": ["water"],
      "habitats": ["sea-breeze-archipelago", "marsh-island"],
      "spawn_times": "day",
      "weather_modifiers": null,
      "drops": [ { "item_id": "leather", "avg_qty": 1.0, "drop_rate": 1.0 } ],
      "partner_skill": "Watering – assists with watering crops.",
      "work_suitability": [ { "type": "watering", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 60, "attack": 80, "defence": 60 },
      "weaknesses": ["electric"],
      "resistances": ["fire"],
      "breeding_notes": null
    },
    {
      "id": "rushoar",
      "name": "Rushoar",
      "elements": ["earth"],
      "habitats": ["bamboo-groves", "verdant-brook"],
      "spawn_times": "all",
      "weather_modifiers": null,
      "drops": [ { "item_id": "leather", "avg_qty": 1.0, "drop_rate": 1.0 } ],
      "partner_skill": "Rush Attack – charges at enemies when commanded.",
      "work_suitability": [ { "type": "mining", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 80, "attack": 70, "defence": 70 },
      "weaknesses": ["water"],
      "resistances": ["electric"],
      "breeding_notes": null
    },
    {
      "id": "vixy",
      "name": "Vixy",
      "elements": ["neutral"],
      "habitats": ["windswept-hills"],
      "spawn_times": "day",
      "weather_modifiers": null,
      "drops": [ { "item_id": "leather", "avg_qty": 1.0, "drop_rate": 1.0 }, { "item_id": "bone", "avg_qty": 1.0, "drop_rate": 1.0 } ],
      "partner_skill": "Dig Here! – produces items when assigned to a Ranch【761280216223901†screenshot】.",
      "work_suitability": [ { "type": "gathering", "rank": 1 }, { "type": "farming", "rank": 1 } ],
      "mountable": false,
      "mount_tier": null,
      "base_stats": { "hp": 70, "attack": 70, "defence": 70 },
      "weaknesses": ["dark"],
      "resistances": ["neutral"],
      "breeding_notes": "Can be bred by combining Lamball with Lifmunk, Lamball with Hangyu Cryst, Cattiva with Mau Cryst, Chikipi with Foxparks, Sparkit with Teafant, Teafant with Flambelle, or Cremis with Mau Cryst【506019502892519†screenshot】."
    },
    {
      "id": "melpaca",
      "name": "Melpaca",
      "elements": ["neutral"],
      "habitats": ["windswept-hills", "verdant-brook"],
      "spawn_times": "day",
      "weather_modifiers": null,
      "drops": [ { "item_id": "leather", "avg_qty": 2.0, "drop_rate": 1.0 } ],
      "partner_skill": "Mount – allows player to ride slowly and carry items.",
      "work_suitability": [ { "type": "transporting", "rank": 1 } ],
      "mountable": true,
      "mount_tier": 1,
      "base_stats": { "hp": 90, "attack": 75, "defence": 90 },
      "weaknesses": ["dark"],
      "resistances": ["neutral"],
      "breeding_notes": null
    },
    {
      "id": "eikthyrdeer",
      "name": "Eikthyrdeer",
      "elements": ["grass"],
      "habitats": ["windswept-hills", "verdant-brook"],
      "spawn_times": "day",
      "weather_modifiers": null,
      "drops": [ { "item_id": "eikthyrdeer-venison", "avg_qty": 2, "drop_rate": 1.0 }, { "item_id": "leather", "avg_qty": 2.5, "drop_rate": 1.0 }, { "item_id": "horn", "avg_qty": 2, "drop_rate": 1.0 } ],
      "partner_skill": "Guardian of the Forest – can be ridden, enables a double jump and increases tree‑cutting efficiency【142053078936299†L123-L142】.",
      "work_suitability": [ { "type": "logging", "rank": 2 } ],
      "mountable": true,
      "mount_tier": 1,
      "base_stats": { "hp": 95, "attack": 80, "defence": 80 },
      "weaknesses": ["fire"],
      "resistances": ["water"],
      "breeding_notes": null
    },
    {
      "id": "direhowl",
      "name": "Direhowl",
      "elements": ["dark"],
      "habitats": ["moonless-shore", "twilight-dunes"],
      "spawn_times": "night",
      "weather_modifiers": null,
      "drops": [ { "item_id": "leather", "avg_qty": 2.0, "drop_rate": 1.0 } ],
      "partner_skill": "Mount – allows the player to ride quickly.",
      "work_suitability": [ { "type": "transporting", "rank": 1 } ],
      "mountable": true,
      "mount_tier": 1,
      "base_stats": { "hp": 80, "attack": 90, "defence": 75 },
      "weaknesses": ["light"],
      "resistances": ["dark"],
      "breeding_notes": null
    },
    {
      "id": "nitewing",
      "name": "Nitewing",
      "elements": ["neutral"],
      "habitats": ["verdant-brook", "moonless-shore"],
      "spawn_times": "day",
      "weather_modifiers": null,
      "drops": [ { "item_id": "leather", "avg_qty": 2.0, "drop_rate": 1.0 } ],
      "partner_skill": "Travel Companion – can be ridden to fly at high speed【468454281657786†screenshot】.",
      "work_suitability": [ { "type": "transporting", "rank": 2 } ],
      "mountable": true,
      "mount_tier": 2,
      "base_stats": { "hp": 100, "attack": 95, "defence": 80 },
      "weaknesses": ["electric"],
      "resistances": ["wind"],
      "breeding_notes": null
    }
  ]
}
```

### Items

This dictionary lists materials and gear used in early progression and mount
crafting.  Prices are approximate; the Wandering Merchant sells Leather for
around 150 gold each【840767909995613†L78-L100】.  Drop sources reference the
relevant Pals above.

```json
{
  "items": [
    { "id": "wood", "name": "Wood", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 1, "sources": [ { "type": "gather", "reference_id": "wood-tree" } ] },
    { "id": "stone", "name": "Stone", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 1, "sources": [ { "type": "gather", "reference_id": "stone-node" } ] },
    { "id": "paldium-fragment", "name": "Paldium Fragment", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 2, "sources": [ { "type": "gather", "reference_id": "paldium-node" } ] },
    { "id": "leather", "name": "Leather", "type": "material", "rarity": "common", "stack": 999, "buy_price": 150, "sell_price": 15, "sources": [ { "type": "drop", "reference_id": "foxparks" }, { "type": "drop", "reference_id": "fuack" }, { "type": "drop", "reference_id": "rushoar" }, { "type": "drop", "reference_id": "vixy" }, { "type": "drop", "reference_id": "melpaca" }, { "type": "drop", "reference_id": "eikthyrdeer" }, { "type": "drop", "reference_id": "direhowl" }, { "type": "drop", "reference_id": "nitewing" }, { "type": "shop", "reference_id": "wandering-merchant" } ] },
    { "id": "flame-organ", "name": "Flame Organ", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 10, "sources": [ { "type": "drop", "reference_id": "foxparks" } ] },
    { "id": "fiber", "name": "Fiber", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 1, "sources": [ { "type": "gather", "reference_id": "fiber-bush" } ] },
    { "id": "ingot", "name": "Ingot", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 20, "sources": [ { "type": "craft", "reference_id": "smelter" } ] },
    { "id": "horn", "name": "Horn", "type": "material", "rarity": "uncommon", "stack": 999, "buy_price": null, "sell_price": 15, "sources": [ { "type": "drop", "reference_id": "eikthyrdeer" } ] },
    { "id": "cloth", "name": "Cloth", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 10, "sources": [ { "type": "craft", "reference_id": "primitive-workbench" } ] },
    { "id": "bone", "name": "Bone", "type": "material", "rarity": "common", "stack": 999, "buy_price": null, "sell_price": 5, "sources": [ { "type": "drop", "reference_id": "vixy" } ] },
    { "id": "eikthyrdeer-venison", "name": "Eikthyrdeer Venison", "type": "consumable", "rarity": "uncommon", "stack": 50, "buy_price": null, "sell_price": 10, "sources": [ { "type": "drop", "reference_id": "eikthyrdeer" } ] }
    ,{ "id": "ancient-civilization-part", "name": "Ancient Civilization Part", "type": "material", "rarity": "rare", "stack": 999, "buy_price": null, "sell_price": 100, "sources": [ { "type": "drop", "reference_id": "tower-rayne-syndicate" } ] }
    ,{ "id": "ancient-technology-point", "name": "Ancient Technology Point", "type": "currency", "rarity": "rare", "stack": 999, "buy_price": null, "sell_price": null, "sources": [ { "type": "boss_reward", "reference_id": "rayne-syndicate-tower" } ] }
    ,{ "id": "grappling-gun", "name": "Grappling Gun", "type": "gear", "rarity": "uncommon", "stack": 1, "buy_price": null, "sell_price": 200, "sources": [ { "type": "craft", "reference_id": "grappling-gun" } ] }
  ]
}
```

### Recipes

Recipes tie items, tech and stations together.  Each entry defines the
product, the required player level, the technology required to unlock it,
the ingredients, the crafting station and the approximate time to craft (in
seconds).  Recipe inputs and level requirements are drawn from official
guides and the Palworld Wiki【353245298505537†L150-L180】【963225160620124†L160-L167】【197143349627535†L151-L156】【524512399342633†L151-L156】.

```json
{
  "recipes": [
    {
      "id": "primitive-workbench",
      "product_item_id": "primitive-workbench",
      "required_player_level": 1,
      "required_tech_id": "tech-primitive-workbench",
      "inputs": [ { "item_id": "wood", "qty": 2 } ],
      "station_id": null,
      "craft_time_s": 30
    },
    {
      "id": "pal-gear-workbench",
      "product_item_id": "pal-gear-workbench",
      "required_player_level": 6,
      "required_tech_id": "tech-pal-gear-workbench",
      "inputs": [ { "item_id": "paldium-fragment", "qty": 10 }, { "item_id": "wood", "qty": 30 }, { "item_id": "cloth", "qty": 2 } ],
      "station_id": "primitive-workbench",
      "craft_time_s": 60
    },
    {
      "id": "foxparks-harness",
      "product_item_id": "foxparks-harness",
      "required_player_level": 6,
      "required_tech_id": "tech-foxparks-harness",
      "inputs": [ { "item_id": "leather", "qty": 3 }, { "item_id": "flame-organ", "qty": 5 }, { "item_id": "paldium-fragment", "qty": 5 } ],
      "station_id": "pal-gear-workbench",
      "craft_time_s": 60
    },
    {
      "id": "direhowl-harness",
      "product_item_id": "direhowl-harness",
      "required_player_level": 9,
      "required_tech_id": "tech-direhowl-harness",
      "inputs": [ { "item_id": "leather", "qty": 10 }, { "item_id": "wood", "qty": 20 }, { "item_id": "fiber", "qty": 15 }, { "item_id": "paldium-fragment", "qty": 10 } ],
      "station_id": "pal-gear-workbench",
      "craft_time_s": 80
    },
    {
      "id": "eikthyrdeer-saddle",
      "product_item_id": "eikthyrdeer-saddle",
      "required_player_level": 12,
      "required_tech_id": "tech-eikthyrdeer-saddle",
      "inputs": [ { "item_id": "leather", "qty": 5 }, { "item_id": "fiber", "qty": 20 }, { "item_id": "ingot", "qty": 10 }, { "item_id": "horn", "qty": 3 }, { "item_id": "paldium-fragment", "qty": 15 } ],
      "station_id": "pal-gear-workbench",
      "craft_time_s": 90
    },
    {
      "id": "nitewing-saddle",
      "product_item_id": "nitewing-saddle",
      "required_player_level": 15,
      "required_tech_id": "tech-nitewing-saddle",
      "inputs": [ { "item_id": "leather", "qty": 20 }, { "item_id": "cloth", "qty": 10 }, { "item_id": "ingot", "qty": 15 }, { "item_id": "fiber", "qty": 20 }, { "item_id": "paldium-fragment", "qty": 20 } ],
      "station_id": "pal-gear-workbench",
      "craft_time_s": 120
    },
    {
      "id": "grappling-gun",
      "product_item_id": "grappling-gun",
      "required_player_level": 12,
      "required_tech_id": "tech-grappling-gun",
      "inputs": [ { "item_id": "paldium-fragment", "qty": 10 }, { "item_id": "ingot", "qty": 10 }, { "item_id": "fiber", "qty": 30 }, { "item_id": "ancient-civilization-part", "qty": 1 } ],
      "station_id": "primitive-workbench",
      "craft_time_s": 90
    }
  ]
}
```

### Tech Tree

Technologies unlock recipes, stations and mechanics.  This tech tree is
focused on early progression and mount acquisition.  Unlocks reference
recipes or stations by their IDs.

```json
{
  "tech_tree": [
    {
      "id": "tech-primitive-workbench",
      "name": "Primitive Workbench",
      "required_level": 1,
      "prerequisites": [],
      "unlocks": [ { "type": "station", "id": "primitive-workbench" } ]
    },
    {
      "id": "tech-pal-gear-workbench",
      "name": "Pal Gear Workbench",
      "required_level": 6,
      "prerequisites": [ "tech-primitive-workbench" ],
      "unlocks": [ { "type": "station", "id": "pal-gear-workbench" } ]
    },
    {
      "id": "tech-foxparks-harness",
      "name": "Foxparks Harness",
      "required_level": 6,
      "prerequisites": [ "tech-pal-gear-workbench" ],
      "unlocks": [ { "type": "recipe", "id": "foxparks-harness" } ]
    },
    {
      "id": "tech-direhowl-harness",
      "name": "Direhowl Harness",
      "required_level": 9,
      "prerequisites": [ "tech-pal-gear-workbench" ],
      "unlocks": [ { "type": "recipe", "id": "direhowl-harness" } ]
    },
    {
      "id": "tech-eikthyrdeer-saddle",
      "name": "Eikthyrdeer Saddle",
      "required_level": 12,
      "prerequisites": [ "tech-pal-gear-workbench" ],
      "unlocks": [ { "type": "recipe", "id": "eikthyrdeer-saddle" } ]
    },
    {
      "id": "tech-nitewing-saddle",
      "name": "Nitewing Saddle",
      "required_level": 15,
      "prerequisites": [ "tech-pal-gear-workbench" ],
      "unlocks": [ { "type": "recipe", "id": "nitewing-saddle" } ]
    },
    {
      "id": "tech-grappling-gun",
      "name": "Grappling Gun",
      "required_level": 12,
      "prerequisites": [ "tech-pal-gear-workbench" ],
      "unlocks": [ { "type": "recipe", "id": "grappling-gun" } ]
    }
  ]
}
```

### Stations

Stations are structures where players craft items and refine materials.

```json
{
  "stations": [
    {
      "id": "primitive-workbench",
      "name": "Primitive Workbench",
      "requirements": [ { "item_id": "wood", "qty": 2 } ],
      "power_required": false,
      "pal_work_types_needed": ["handiwork"],
      "station_tier": 1
    },
    {
      "id": "pal-gear-workbench",
      "name": "Pal Gear Workbench",
      "requirements": [ { "item_id": "paldium-fragment", "qty": 10 }, { "item_id": "wood", "qty": 30 }, { "item_id": "cloth", "qty": 2 } ],
      "power_required": false,
      "pal_work_types_needed": ["handiwork"],
      "station_tier": 1
    }
  ]
}
```

### Regions

Regions define areas on the world map with level hints and hazards.  Level
ranges come from GameLeap’s map guide【950757978743332†L131-L147】.

```json
{
  "regions": [
    {
      "id": "windswept-hills",
      "name": "Windswept Hills",
      "level_hint_min": 1,
      "level_hint_max": 15,
      "climate": "temperate",
      "hazards": "low‑level Pals",
      "coordinates_bbox": [ -500, -600, 500, 200 ],
      "fast_travel_nodes": [ "plateau-of-beginnings" ]
    },
    {
      "id": "sea-breeze-archipelago",
      "name": "Sea Breeze Archipelago",
      "level_hint_min": 1,
      "level_hint_max": 10,
      "climate": "tropical islands",
      "hazards": "drowning if you fall into deep water",
      "coordinates_bbox": [ -800, -800, -200, -200 ],
      "fast_travel_nodes": [ "sea-breeze-church" ]
    },
    {
      "id": "bamboo-groves",
      "name": "Bamboo Groves",
      "level_hint_min": 10,
      "level_hint_max": 20,
      "climate": "humid forest",
      "hazards": "aggressive earth Pals",
      "coordinates_bbox": [ 100, 200, 600, 600 ],
      "fast_travel_nodes": [ "bamboo-temple" ]
    },
    {
      "id": "verdant-brook",
      "name": "Verdant Brook",
      "level_hint_min": 20,
      "level_hint_max": 30,
      "climate": "lush valley",
      "hazards": "mid‑level predators",
      "coordinates_bbox": [ -300, 200, 300, 800 ],
      "fast_travel_nodes": [ "verdant-watchtower" ]
    },
    {
      "id": "moonless-shore",
      "name": "Moonless Shore",
      "level_hint_min": 15,
      "level_hint_max": 20,
      "climate": "dark coast",
      "hazards": "nocturnal predators",
      "coordinates_bbox": [ 400, -500, 800, -200 ],
      "fast_travel_nodes": [ "moonless-lighthouse" ]
    },
    {
      "id": "marsh-island",
      "name": "Marsh Island",
      "level_hint_min": 1,
      "level_hint_max": 10,
      "climate": "swamp",
      "hazards": "water poisoning",
      "coordinates_bbox": [ 200, -800, 500, -500 ],
      "fast_travel_nodes": [ "marsh-bog" ]
    },
    {
      "id": "twilight-dunes",
      "name": "Twilight Dunes",
      "level_hint_min": 10,
      "level_hint_max": 20,
      "climate": "arid desert",
      "hazards": "heatstroke, dark Pals at night",
      "coordinates_bbox": [ 600, -300, 900, 100 ],
      "fast_travel_nodes": [ "dune-oasis" ]
    },
    {
      "id": "ice-wind-island",
      "name": "Ice Wind Island",
      "level_hint_min": 1,
      "level_hint_max": 10,
      "climate": "frozen island",
      "hazards": "cold weather and slippery terrain",
      "coordinates_bbox": [ -950, 300, -600, 600 ],
      "fast_travel_nodes": [ "ice-wind-outpost" ]
    },
    {
      "id": "mount-obsidian",
      "name": "Mount Obsidian",
      "level_hint_min": 30,
      "level_hint_max": 50,
      "climate": "volcanic highland",
      "hazards": "extreme heat, lava, high-level fire Pals",
      "coordinates_bbox": [ 700, -700, 1000, -300 ],
      "fast_travel_nodes": [ "obsidian-fort" ]
    }
  ]
}
```

### Resource Nodes

Resource nodes produce raw materials when harvested.  Respawn times are
approximate.

```json
{
  "resource_nodes": [
    {
      "id": "wood-tree",
      "name": "Tree",
      "yields": [ { "item_id": "wood", "avg_qty": 2.0 } ],
      "respawn_minutes": 5,
      "best_regions": [ "windswept-hills", "verdant-brook" ],
      "notes": "Cut down using a primitive or stone axe."
    },
    {
      "id": "stone-node",
      "name": "Stone Node",
      "yields": [ { "item_id": "stone", "avg_qty": 2.0 } ],
      "respawn_minutes": 5,
      "best_regions": [ "windswept-hills" ],
      "notes": "Mine using a pickaxe or assign a mining Pal."
    },
    {
      "id": "paldium-node",
      "name": "Paldium Ore",
      "yields": [ { "item_id": "paldium-fragment", "avg_qty": 1.5 } ],
      "respawn_minutes": 15,
      "best_regions": [ "sea-breeze-archipelago", "windswept-hills" ],
      "notes": "Glowing blue ore clusters near water."
    },
    {
      "id": "fiber-bush",
      "name": "Fiber Bush",
      "yields": [ { "item_id": "fiber", "avg_qty": 2.0 } ],
      "respawn_minutes": 10,
      "best_regions": [ "bamboo-groves", "verdant-brook" ],
      "notes": "Harvested by hand or by a gathering Pal."
    }
  ]
}
```

### Bosses, Towers and Dungeons

Early bosses are placed in specific regions.  Clearing them provides large
XP and unique rewards.  The example below covers the Rayne Syndicate
Tower.

```json
{
  "bosses_towers_dungeons": [
    {
      "id": "rayne-syndicate-tower",
      "name": "Rayne Syndicate Tower (Zoe & Grizzbolt)",
      "type": "tower",
      "region_id": "windswept-hills",
      "coords": [ 137, -394 ],
      "recommended_level": 15,
      "mechanics": "Electric boss accompanied by minions; weak to water Pals.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Cannot be repeated until after next major patch"
    }
  ]
}
```

### Breeding

Breeding allows combining two Pals to produce an offspring with mixed traits.
Only a few combinations are listed here for the early Pal Vixy.

```json
{
  "breeding": [
    {
      "child_pal_id": "vixy",
      "recipe": [
        { "parent_pal_id": "lamball", "alt_parent_pal_id": "lifmunk" },
        { "parent_pal_id": "lamball", "alt_parent_pal_id": "hangyu-cryst" },
        { "parent_pal_id": "cattiva", "alt_parent_pal_id": "mau-cryst" },
        { "parent_pal_id": "chikipi", "alt_parent_pal_id": "foxparks" },
        { "parent_pal_id": "sparkit", "alt_parent_pal_id": "teafant" },
        { "parent_pal_id": "teafant", "alt_parent_pal_id": "flambelle" },
        { "parent_pal_id": "cremis", "alt_parent_pal_id": "mau-cryst" }
      ],
      "notes": "Each pair produces a Vixy egg when bred at the breeding station【506019502892519†screenshot】."
    }
  ]
}
```

## Route Schema

The following JSON block defines the structure that every route must obey.
Clients rely on this schema to parse and validate guides.  See `routes`
section for actual route data.

```json
{
  "route_schema": {
    "route_id": "string-kebab",
    "title": "string",
    "category": "progression|mounts|resources|bosses|breeding|tech|automation|capture-index|misc",
    "tags": ["string", "..."],
    "progression_role": "core|optional|support",
    "recommended_level": { "min": "int", "max": "int" },
    "modes": { "normal": "boolean", "hardcore": "boolean", "solo": "boolean", "coop": "boolean" },
    "prerequisites": {
      "routes": ["route-id", "..."],
      "tech": ["tech-id", "..."],
      "items": [ { "item_id": "...", "qty": "int" } ],
      "pals": ["pal-id", "..."]
    },
    "objectives": ["high-level objective sentences"],
    "estimated_time_minutes": { "solo": "int", "coop": "int" },
    "estimated_xp_gain": { "min": "int", "max": "int" },
    "risk_profile": "low|medium|high",
    "failure_penalties": { "normal": "text", "hardcore": "text" },
    "adaptive_guidance": {
      "underleveled": "text",
      "overleveled": "text",
      "resource_shortages": [ { "item_id": "...", "solution": "include_subroute or explain alternative" } ],
      "time_limited": "text",
      "dynamic_rules": [
        {
          "signal": "level_gap|time_budget|resource_gap|mode_state|geographic_context",
          "condition": "human-readable expression describing when to trigger the adjustment",
          "adjustment": "specific instruction to modify the route",
          "priority": "int (1=highest urgency)",
          "mode_scope": ["normal", "hardcore", "solo", "coop"],
          "related_steps": ["route-id:001"],
          "follow_up_routes": ["route-id"]
        }
      ]
    },
    "checkpoints": [
      { "id": "route-id:checkpoint-1", "summary": "text", "benefits": ["string"], "related_steps": ["route-id:001"] }
    ],
    "supporting_routes": { "recommended": ["route-id"], "optional": ["route-id"] },
    "failure_recovery": { "normal": "text", "hardcore": "text" },
    "steps": [
      {
        "step_id": "route-id:001",
        "type": "travel|gather|farm|capture|fight|craft|build|unlock-tech|breed|deliver|talk|explore|prepare",
        "summary": "short sentence",
        "detail": "clear, actionable instruction",
        "targets": [ { "kind": "item|pal|boss|station|tech", "id": "...", "qty": "int?" } ],
        "locations": [ { "region_id": "...", "coords": ["x", "y"], "time": "day|night|any", "weather": "any|condition" } ],
        "mode_adjustments": {
          "hardcore": { "tactics": "text", "safety_buffer_items": [ { "item_id": "...", "qty": "int" } ] },
          "coop": { "role_splits": [ { "role": "puller", "tasks": "..." }, { "role": "farmer", "tasks": "..." } ], "loot_rules": "text" }
        },
        "recommended_loadout": {
          "gear": ["item-id"],
          "pals": ["pal-id"],
          "consumables": [ { "item_id": "...", "qty": "int" } ]
        },
        "xp_award_estimate": { "min": "int", "max": "int" },
        "outputs": {
          "items": [ { "item_id": "...", "qty": "int" } ],
          "pals": ["pal-id", "..."],
          "unlocks": { "tech": ["tech-id"], "stations": ["station-id"] }
        },
        "branching": [
          { "condition": "player lacks item/leather >= N", "action": "jump_to_step_id or include_subroute", "subroute_ref": "route-id" }
        ],
        "citations": ["short-source-key-1", "short-source-key-2"]
      }
    ],
    "completion_criteria": [
      { "type": "have-item", "item_id": "...", "qty": "int" },
      { "type": "tech-unlocked", "tech_id": "..." },
      { "type": "boss-cleared", "boss_id": "..." }
    ],
    "yields": { "levels_estimate": "+X to +Y", "key_unlocks": ["tech-id", "..."] },
    "metrics": {
      "xp_per_minute": { "solo": "float", "coop": "float" },
      "travel_distance_m": "int",
      "consumable_cost": [ { "item_id": "...", "qty": "int" } ]
    },
    "next_routes": [ { "route_id": "...", "reason": "what unlocks it" } ]
  }
}
```

## Route Library

The following routes cover early game progression, resource farming and
mount acquisition.  Each route conforms to the schema above and
references the ontologies defined earlier.  Citations back up non‑obvious
facts (spawn locations, recipe costs, drop rates, etc.).

### Route: Starter Base and Capture

This introductory route teaches players how to gather resources, craft
basic stations, create Pal Spheres and capture their first companions.

```json
{
  "route_id": "starter-base-capture",
  "title": "Starter Base and Capture",
  "category": "progression",
  "tags": [ "early-game", "base-building", "capture", "resource-gathering" ],
  "progression_role": "core",
  "recommended_level": { "min": 1, "max": 5 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [], "tech": [], "items": [], "pals": [] },
  "objectives": [
    "Gather basic resources and build a Primitive Workbench",
    "Craft Pal Spheres and capture three different Pals",
    "Establish a small shelter"
  ],
  "estimated_time_minutes": { "solo": 30, "coop": 20 },
  "estimated_xp_gain": { "min": 300, "max": 600 },
  "risk_profile": "low",
  "failure_penalties": { "normal": "Loss of gathered materials", "hardcore": "Death results in character deletion" },
  "adaptive_guidance": {
    "underleveled": "Loop step :001 twice and capture Lamball first; their low aggression keeps risk minimal while still granting capture XP.",
    "overleveled": "If you arrive above level 6, prioritize step :003 and transition directly into harness crafting to avoid redundant farming.",
    "resource_shortages": [
      { "item_id": "paldium-fragment", "solution": "Trigger the resource-paldium subroute from step :003 or mine blue ore veins along the riverbank." },
      { "item_id": "fiber", "solution": "Clear Windswept Hills bushes after step :001; each bush yields 2-3 Fiber quickly." }
    ],
    "time_limited": "Complete steps :001 through :003 only; capture a single Lamball to unlock base chores and return later for the full roster.",
    "dynamic_rules": [
      {
        "signal": "level_gap:over",
        "condition": "player.estimated_level >= recommended_level.max + 2",
        "adjustment": "Treat step :001 as maintenance only, finish :003 to restock spheres, then pivot into mount-foxparks-harness without repeating :004.",
        "priority": 2,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["starter-base-capture:003"],
        "follow_up_routes": ["mount-foxparks-harness"]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 20",
        "adjustment": "Execute steps :001 through :003 only and bank captured materials; postpone the third capture in :004 until more time is available.",
        "priority": 3,
        "mode_scope": ["solo", "coop"],
        "related_steps": ["starter-base-capture:001", "starter-base-capture:002", "starter-base-capture:003"]
      },
      {
        "signal": "resource_gap:paldium-fragment",
        "condition": "resource_gaps contains paldium-fragment >= 5",
        "adjustment": "Loop the river rocks north of the spawn before step :003 or trigger the resource-paldium subroute immediately.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["starter-base-capture:003"],
        "follow_up_routes": ["resource-paldium"]
      }
    ]
  },
  "checkpoints": [
    { "id": "starter-base-capture:checkpoint-setup", "summary": "Primitive Workbench placed", "benefits": [ "Workbench crafting unlocked", "Establishes respawn anchor" ], "related_steps": [ "starter-base-capture:002" ] },
    { "id": "starter-base-capture:checkpoint-team", "summary": "Three work-ready Pals captured", "benefits": [ "Unlocks base chores", "Meets early tech prerequisites" ], "related_steps": [ "starter-base-capture:004" ] }
  ],
  "supporting_routes": { "recommended": [ "resource-paldium" ], "optional": [ "resource-leather-early" ] },
  "failure_recovery": {
    "normal": "If you faint, recover your dropped pouch before it despawns and resume at the nearest Fast Travel statue.",
    "hardcore": "Retreat before HP reaches 25%; if a death is imminent, abandon the route and reset from the title to preserve the Hardcore save."
  },
  "steps": [
    {
      "step_id": "starter-base-capture:001",
      "type": "gather",
      "summary": "Collect Wood and Stone",
      "detail": "Harvest at least 20 Wood from trees and 15 Stone from boulders in the Windswept Hills.  Trees and stone nodes respawn quickly; use a primitive tool or your Pals to speed up collection.",
      "targets": [ { "kind": "item", "id": "wood", "qty": 20 }, { "kind": "item", "id": "stone", "qty": 15 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Avoid engaging hostile Pals while gathering; keep your HP above 50 % and carry extra berries.", "safety_buffer_items": [ { "item_id": "wood", "qty": 10 }, { "item_id": "stone", "qty": 10 } ] },
        "coop": { "role_splits": [ { "role": "gatherer", "tasks": "Chop trees and mine stone" }, { "role": "scout", "tasks": "Watch for aggressive Pals and keep area clear" } ], "loot_rules": "Share resources evenly" }
      },
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 20, "max": 40 },
      "outputs": { "items": [ { "item_id": "wood", "qty": 20 }, { "item_id": "stone", "qty": 15 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "starter-base-capture:002",
      "type": "build",
      "summary": "Construct a Primitive Workbench",
      "detail": "Open the construction menu and build a Primitive Workbench using 2 Wood【907636800064548†screenshot】.  Place it near your gathering area.",
      "targets": [ { "kind": "station", "id": "primitive-workbench" } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 30, "max": 50 },
      "outputs": { "items": [], "pals": [], "unlocks": { "stations": [ "primitive-workbench" ] } },
      "branching": [],
      "citations": [ "paldb-primitive-workbench" ]
    },
    {
      "step_id": "starter-base-capture:003",
      "type": "craft",
      "summary": "Craft Pal Spheres",
      "detail": "Use the Primitive Workbench to craft at least five Pal Spheres.  Each sphere requires Paldium Fragments (gathered from blue ore) and a small amount of Wood and Stone.  If you lack fragments, mine Paldium nodes along the river.",
      "targets": [ { "kind": "item", "id": "pal-sphere", "qty": 5 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 70 },
      "outputs": { "items": [ { "item_id": "pal-sphere", "qty": 5 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks paldium-fragment >= 5", "action": "include_subroute", "subroute_ref": "resource-paldium" } ],
      "citations": []
    },
    {
      "step_id": "starter-base-capture:004",
      "type": "capture",
      "summary": "Capture three early Pals",
      "detail": "Throw Pal Spheres at Lamball, Cattiva, Chikipi, Lifmunk or Foxparks in the Windswept Hills【956200907149478†L146-L169】.  Approach from behind to improve your catch rate.  Capturing new species grants more XP than defeating them【116860197722081†L96-L128】.",
      "targets": [ { "kind": "pal", "id": "lamball", "qty": 1 }, { "kind": "pal", "id": "cattiva", "qty": 1 }, { "kind": "pal", "id": "foxparks", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [189, -478], "time": "day", "weather": "any" }, { "region_id": "windswept-hills", "coords": [144, -583], "time": "day", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Avoid aggroing the nearby Mammorest boss while hunting【956200907149478†L146-L169】.  Always keep a healing item ready.", "safety_buffer_items": [ { "item_id": "leather", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "puller", "tasks": "Aggro the Pal and kite it" }, { "role": "catcher", "tasks": "Throw Pal Spheres from behind" } ], "loot_rules": "Each player keeps one captured Pal" }
      },
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [ { "item_id": "pal-sphere", "qty": 5 } ] },
      "xp_award_estimate": { "min": 100, "max": 200 },
      "outputs": { "items": [], "pals": [ "lamball", "cattiva", "foxparks" ], "unlocks": {} },
      "branching": [],
      "citations": [ "thegamer-foxparks-spawn", "namehero-xp-capture" ]
    },
    {
      "step_id": "starter-base-capture:005",
      "type": "build",
      "summary": "Construct a shelter",
      "detail": "Gather extra Wood and build a basic shelter to protect yourself and your newly captured Pals.  A roof prevents rain damage and increases comfort.",
      "targets": [],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 30, "max": 50 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": []
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "primitive-workbench", "qty": 1 }, { "type": "have-item", "item_id": "pal-sphere", "qty": 5 } ],
  "yields": { "levels_estimate": "+1 to +2", "key_unlocks": [ "tech-primitive-workbench" ] },
  "metrics": {
    "xp_per_minute": { "solo": 12.5, "coop": 18.0 },
    "travel_distance_m": 420,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 5 } ]
  },
  "next_routes": [ { "route_id": "resource-leather-early", "reason": "Gather materials for future gear" }, { "route_id": "mount-foxparks-harness", "reason": "You captured Foxparks and can now craft its harness" } ]
}
```

### Route: Leather Farming Loop (Early Game)

This resource route teaches players how to farm Leather efficiently in the
early game.  It is automatically inserted by other routes when more
Leather is required.  The step about buying from merchants notes that
Wandering Merchants sell Leather for 150 gold each【840767909995613†L78-L100】.

```json
{
  "route_id": "resource-leather-early",
  "title": "Leather Farming Loop (Early)",
  "category": "resources",
  "tags": [ "resource-farm", "leather", "early-game", "combat-loop" ],
  "progression_role": "support",
  "recommended_level": { "min": 4, "max": 10 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "starter-base-capture" ], "tech": [], "items": [], "pals": [] },
  "objectives": [ "Acquire the required quantity of Leather" ],
  "estimated_time_minutes": { "solo": 15, "coop": 10 },
  "estimated_xp_gain": { "min": 200, "max": 400 },
  "risk_profile": "medium",
  "failure_penalties": { "normal": "Lost time if defeated", "hardcore": "Death results in permaloss of captured Pals" },
  "adaptive_guidance": {
    "underleveled": "Target Lamball and Vixy groups on the outskirts of Windswept Hills until level 6 before rotating to Sea Breeze.",
    "overleveled": "Hunt Direhowl packs in the ravine for faster drops; their higher HP scales with your damage output.",
    "resource_shortages": [
      { "item_id": "pal-sphere", "solution": "Craft a fresh batch at your Primitive Workbench before departing." },
      { "item_id": "gold", "solution": "Sell spare ores or berries at the Archipelago merchant to fund purchases." }
    ],
    "time_limited": "Clear step :001 then buy the remainder from the merchant in step :003 to finish within five minutes.",
    "dynamic_rules": [
      {
        "signal": "mode:hardcore",
        "condition": "mode.hardcore === true",
        "adjustment": "Prioritise the merchant purchase in step :003 before engaging the densest spawn clusters in :002 to minimise death risk.",
        "priority": 1,
        "mode_scope": ["hardcore"],
        "related_steps": ["resource-leather-early:003"]
      },
      {
        "signal": "resource_gap:leather_high",
        "condition": "resource_gaps contains leather >= 20",
        "adjustment": "Run the Sea Breeze loop in :002 twice—first clockwise around the Church, then along the Bridge of the Twin Knights—to stock 20+ Leather in one outing.",
        "priority": 2,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["resource-leather-early:002"]
      },
      {
        "signal": "goal:mounts",
        "condition": "goals includes mounts",
        "adjustment": "Stay until you bank at least 15 Leather so upcoming saddle routes such as mount-eikthyrdeer-saddle do not immediately reinsert this farm.",
        "priority": 3,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["resource-leather-early:002"],
        "follow_up_routes": ["mount-eikthyrdeer-saddle", "mount-direhowl-harness"]
      }
    ]
  },
  "checkpoints": [
    { "id": "resource-leather-early:checkpoint-arrival", "summary": "Reached farming zone", "benefits": [ "Unlocks fast travel point if activated", "Spawns leather-dropping Pals" ], "related_steps": [ "resource-leather-early:001" ] },
    { "id": "resource-leather-early:checkpoint-quota", "summary": "First 10 Leather collected", "benefits": [ "Meets most early saddle requirements" ], "related_steps": [ "resource-leather-early:002" ] }
  ],
  "supporting_routes": { "recommended": [ "starter-base-capture" ], "optional": [ "resource-paldium" ] },
  "failure_recovery": {
    "normal": "If downed, respawn at the nearest statue and retrieve your pouch; mobs here do not despawn quickly.",
    "hardcore": "Disengage if two hostile spawns overlap; kite towards coastlines where line-of-sight breaks make escapes safer."
  },
  "steps": [
    {
      "step_id": "resource-leather-early:001",
      "type": "travel",
      "summary": "Travel to leather hotspots",
      "detail": "Head to the Sea Breeze Archipelago Church or the Bridge of the Twin Knights.  These areas host large numbers of Foxparks, Rushoars and Fuacks, which all drop Leather【840767909995613†L78-L100】【840767909995613†L106-L135】.",
      "targets": [],
      "locations": [ { "region_id": "sea-breeze-archipelago", "coords": [-650, -650], "time": "any", "weather": "any" }, { "region_id": "windswept-hills", "coords": [200, -300], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [ "foxparks", "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 20, "max": 40 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "shockbyte-leather-sources" ]
    },
    {
      "step_id": "resource-leather-early:002",
      "type": "farm",
      "summary": "Hunt leather‑dropping Pals",
      "detail": "Defeat or capture Foxparks, Fuack, Rushoar, Melpaca, Vixy, Eikthyrdeer and Direhowl.  Each drop guarantees 1–3 Leather【142053078936299†L295-L311】【840767909995613†L49-L103】.  Use water Pals against fire types and electric Pals against water types.  Expect roughly 10–20 Leather/hour when solo and 20–30 Leather/hour in Co‑Op.",
      "targets": [ { "kind": "item", "id": "leather", "qty": 10 } ],
      "locations": [ { "region_id": "sea-breeze-archipelago", "coords": [-650, -650], "time": "any", "weather": "any" }, { "region_id": "windswept-hills", "coords": [189, -478], "time": "day", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Pull one Pal at a time and use ranged attacks to minimise damage", "safety_buffer_items": [ { "item_id": "leather", "qty": 3 } ] },
        "coop": { "role_splits": [ { "role": "hunter", "tasks": "Engage and defeat Pals" }, { "role": "looter", "tasks": "Collect drops and watch for respawns" } ], "loot_rules": "Divide Leather evenly" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 150, "max": 300 },
      "outputs": { "items": [ { "item_id": "leather", "qty": 10 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks leather >= required", "action": "repeat", "subroute_ref": "resource-leather-early" } ],
      "citations": [ "shockbyte-leather-sources", "eikthyrdeer-drops" ]
    },
    {
      "step_id": "resource-leather-early:003",
      "type": "deliver",
      "summary": "Optionally buy Leather from merchants",
      "detail": "If hunting is too risky, purchase Leather from a Wandering Merchant for approximately 150 gold each【840767909995613†L78-L100】.",
      "targets": [ { "kind": "item", "id": "leather", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [50, 50], "time": "day", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 5, "max": 10 },
      "outputs": { "items": [ { "item_id": "leather", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "shockbyte-leather-merchant" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "leather", "qty": 10 } ],
  "yields": { "levels_estimate": "+0 to +1", "key_unlocks": [] },
  "metrics": {
    "xp_per_minute": { "solo": 14.0, "coop": 20.0 },
    "travel_distance_m": 1200,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 3 }, { "item_id": "gold", "qty": 150 } ]
  },
  "next_routes": [ { "route_id": "mount-foxparks-harness", "reason": "Provides Leather needed for Foxparks Harness" }, { "route_id": "mount-direhowl-harness", "reason": "Provides Leather for Direhowl Harness" }, { "route_id": "mount-eikthyrdeer-saddle", "reason": "Provides Leather for Eikthyrdeer Saddle" } ]
}
```

### Route: Paldium Fragment Mining Loop

This support route ensures players can reliably farm Paldium Fragments for Pal Spheres,
gear recipes and tech unlocks.  It chains travel between rich node clusters and includes
options to convert Ore into fragments when nodes are depleted.

```json
{
  "route_id": "resource-paldium",
  "title": "Paldium Fragment Mining Loop",
  "category": "resources",
  "tags": [ "resource-farm", "paldium", "early-game", "mining" ],
  "progression_role": "support",
  "recommended_level": { "min": 3, "max": 12 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "starter-base-capture" ], "tech": [], "items": [], "pals": [] },
  "objectives": [ "Visit clustered Paldium nodes", "Mine fragments efficiently", "Convert spare Ore into fragments if needed" ],
  "estimated_time_minutes": { "solo": 12, "coop": 8 },
  "estimated_xp_gain": { "min": 180, "max": 320 },
  "risk_profile": "low",
  "failure_penalties": { "normal": "Minimal—only time spent", "hardcore": "Potential durability loss on tools" },
  "adaptive_guidance": {
    "underleveled": "Equip a Stone Pickaxe and avoid Alpha spawns near the river; capture a Lifmunk to assist with mining.",
    "overleveled": "Route through the Desiccated Desert outcrops for higher-density nodes to refill faster.",
    "resource_shortages": [
      { "item_id": "stone-pickaxe", "solution": "Craft a backup Stone Pickaxe at the Workbench before leaving base." },
      { "item_id": "paldium-fragment", "solution": "Crush Ore at the Primitive Furnace for 2 fragments per ingot batch." }
    ],
    "time_limited": "Mine the waterfall circuit (step :001) once, then smelt spare Ore into fragments back at base.",
    "dynamic_rules": [
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes <= 10",
        "adjustment": "Run only step :001 and convert any Ore you already own via :003 on return to base for a quick 30+ fragment top-up.",
        "priority": 2,
        "mode_scope": ["solo", "coop"],
        "related_steps": ["resource-paldium:001", "resource-paldium:003"]
      },
      {
        "signal": "resource_gap:paldium_high",
        "condition": "resource_gaps contains paldium-fragment >= 60",
        "adjustment": "Chain steps :001 and :002 without travel breaks, then immediately queue Ore smelting in :003 to push past 60 fragments before leaving the valley.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["resource-paldium:001", "resource-paldium:002", "resource-paldium:003"]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to ferry Ore back to the furnace after step :002 while the miner keeps nodes cycling, preventing respawn downtime.",
        "priority": 3,
        "mode_scope": ["coop"],
        "related_steps": ["resource-paldium:002", "resource-paldium:003"]
      }
    ]
  },
  "checkpoints": [
    { "id": "resource-paldium:checkpoint-river", "summary": "River nodes cleared", "benefits": [ "50+ fragments gathered" ], "related_steps": [ "resource-paldium:001" ] },
    { "id": "resource-paldium:checkpoint-furnace", "summary": "Fragments smelted", "benefits": [ "Ensures crafting stockpile" ], "related_steps": [ "resource-paldium:003" ] }
  ],
  "supporting_routes": { "recommended": [ "starter-base-capture" ], "optional": [ "resource-leather-early" ] },
  "failure_recovery": {
    "normal": "If your tool breaks, fast travel home, craft a replacement and resume from the last checkpoint.",
    "hardcore": "Avoid fighting while encumbered; drop excess stone before sprinting back to safety."
  },
  "steps": [
    {
      "step_id": "resource-paldium:001",
      "type": "gather",
      "summary": "Mine riverbed nodes",
      "detail": "Follow the river south of the Windswept Hills fast travel statue.  Blue crystalline nodes respawn every few minutes and yield 2–4 fragments each【palwiki-paldium†L42-L71】.",
      "targets": [ { "kind": "item", "id": "paldium-fragment", "qty": 20 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 80, -150 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Keep stamina above 50 % to dodge hostile Lamballs", "safety_buffer_items": [ { "item_id": "berry", "qty": 5 } ] },
        "coop": { "role_splits": [ { "role": "miner", "tasks": "Break nodes" }, { "role": "hauler", "tasks": "Collect drops and scout" } ], "loot_rules": "Split fragments evenly" }
      },
      "recommended_loadout": { "gear": [ "stone-pickaxe" ], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 60, "max": 100 },
      "outputs": { "items": [ { "item_id": "paldium-fragment", "qty": 20 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-paldium" ]
    },
    {
      "step_id": "resource-paldium:002",
      "type": "explore",
      "summary": "Hit cliffside outcrops",
      "detail": "Circle the cliff ring northwest of the starting valley.  Surface fragments protrude from the ground and can be kicked for bonus drops, netting ~30 fragments per lap【palwiki-paldium†L86-L115】.",
      "targets": [ { "kind": "item", "id": "paldium-fragment", "qty": 30 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ -40, 120 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "stone-pickaxe" ], "pals": [ "foxparks" ], "consumables": [] },
      "xp_award_estimate": { "min": 70, "max": 110 },
      "outputs": { "items": [ { "item_id": "paldium-fragment", "qty": 30 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-paldium" ]
    },
    {
      "step_id": "resource-paldium:003",
      "type": "craft",
      "summary": "Refine fragments from Ore",
      "detail": "Back at base, smelt spare Ore into Ingots, then crush the leftovers to convert into extra fragments.  Each smelting cycle produces 2 fragments as a by-product when using the Primitive Furnace【palwiki-paldium†L118-L140】.",
      "targets": [ { "kind": "item", "id": "paldium-fragment", "qty": 10 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 70 },
      "outputs": { "items": [ { "item_id": "paldium-fragment", "qty": 10 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-paldium" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "paldium-fragment", "qty": 50 } ],
  "yields": { "levels_estimate": "+0 to +1", "key_unlocks": [] },
  "metrics": {
    "xp_per_minute": { "solo": 15.0, "coop": 22.0 },
    "travel_distance_m": 900,
    "consumable_cost": [ { "item_id": "stone-pickaxe", "qty": 1 } ]
  },
  "next_routes": [ { "route_id": "mount-foxparks-harness", "reason": "Paldium needed for harness crafting" }, { "route_id": "tech-grappling-gun", "reason": "Supplies fragments for the tech" } ]
}
```

### Route: Recruit Base Merchant

Catching a human merchant early gives permanent access to trading at home without
waiting for wandering spawns.  This route shows how to prepare high-grade Pal
Spheres, locate the Small Settlement vendors, capture them safely and assign the
merchant to your workforce.

```json
{
  "route_id": "capture-base-merchant",
  "title": "Recruit Base Merchant",
  "category": "capture-index",
  "tags": [ "human", "merchant", "base-support" ],
  "progression_role": "support",
  "recommended_level": { "min": 10, "max": 18 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "starter-base-capture" ], "tech": [], "items": [], "pals": [] },
  "objectives": [
    "Craft or buy high-grade Pal Spheres for human capture",
    "Travel to the Small Settlement and separate a merchant from guards",
    "Capture the merchant and assign them to your base"
  ],
  "estimated_time_minutes": { "solo": 25, "coop": 18 },
  "estimated_xp_gain": { "min": 350, "max": 600 },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Knockouts drop your pouch and may cost gold if PIDF guards finish the fight.",
    "hardcore": "Being executed by guards permanently ends the save—retreat if health drops below 40%."
  },
  "adaptive_guidance": {
    "underleveled": "If your weapons are below Iron tier, focus on trapping single merchants at night when patrols thin out before attempting the capture.",
    "overleveled": "Players above level 18 can skip step :001 if they already stock Mega Pal Spheres and move straight to isolating the merchant.",
    "resource_shortages": [
      { "item_id": "paldium-fragment", "solution": "Trigger resource-paldium from step :001 to restock fragments for higher-grade spheres." }
    ],
    "time_limited": "Complete steps :001 and :002 only; mark the merchant’s position and return later with time to handle the capture.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player kite PIDF guards away during step :003 while the other drops the merchant to low HP for an easy capture.",
        "priority": 2,
        "mode_scope": [ "coop" ],
        "related_steps": [ "capture-base-merchant:003" ],
        "follow_up_routes": []
      },
      {
        "signal": "resource_gap:pal-sphere",
        "condition": "resource_gaps contains pal-sphere >= 5",
        "adjustment": "Loop resource-paldium immediately after step :001 to craft additional high-grade spheres before confronting the merchant.",
        "priority": 1,
        "mode_scope": [ "normal", "hardcore", "solo", "coop" ],
        "related_steps": [ "capture-base-merchant:001" ],
        "follow_up_routes": [ "resource-paldium" ]
      }
    ]
  },
  "checkpoints": [
    { "id": "capture-base-merchant:checkpoint-scout", "summary": "Merchant location scouted", "benefits": [ "Safe pull path identified" ], "related_steps": [ "capture-base-merchant:002" ] },
    { "id": "capture-base-merchant:checkpoint-captured", "summary": "Merchant captured", "benefits": [ "Permanent base vendor unlocked" ], "related_steps": [ "capture-base-merchant:003" ] }
  ],
  "supporting_routes": { "recommended": [ "resource-paldium" ], "optional": [] },
  "failure_recovery": {
    "normal": "If guards overwhelm you, fast travel back after respawning, recover your pouch and repeat from the scouting checkpoint.",
    "hardcore": "Disengage using terrain when patrols converge; if capture attempts fail twice, retreat to avoid fatal guard focus fire."
  },
  "steps": [
    {
      "step_id": "capture-base-merchant:001",
      "type": "prepare",
      "summary": "Craft high-grade Pal Spheres",
      "detail": "Use your best Pal Sphere recipe (Great or better) and craft at least six before leaving base. Human catch rates are far lower than standard Pals, so higher-grade spheres dramatically improve success odds【529f5c†L67-L80】.",
      "targets": [ { "kind": "item", "id": "pal-sphere", "qty": 6 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Craft a spare stack to avoid mid-raid shortages; you cannot risk repeat crimes.", "safety_buffer_items": [ { "item_id": "pal-sphere", "qty": 3 } ] },
        "coop": { "role_splits": [ { "role": "crafter", "tasks": "Queues high-grade spheres" }, { "role": "supplier", "tasks": "Feeds fragments and ingots" } ], "loot_rules": "Split sphere stacks evenly" }
      },
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [ { "item_id": "pal-sphere", "qty": 6 } ] },
      "xp_award_estimate": { "min": 80, "max": 120 },
      "outputs": { "items": [ { "item_id": "pal-sphere", "qty": 6 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks pal-sphere >= 6", "action": "include_subroute", "subroute_ref": "resource-paldium" } ],
      "citations": [ "palwiki-humans" ]
    },
    {
      "step_id": "capture-base-merchant:002",
      "type": "travel",
      "summary": "Scout the Small Settlement",
      "detail": "Ride or glide to the Small Settlement at approximately (75, -479). The village hosts both a Pal Merchant and a Wandering Merchant—confirm patrol routes and identify clear back alleys for the capture attempt【165dd8†L71-L90】.",
      "targets": [],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 75, -479 ], "time": "day", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Enter from the cliffside to avoid triggering wanted status while scouting." },
        "coop": { "role_splits": [ { "role": "spotter", "tasks": "Marks guard paths" }, { "role": "controller", "tasks": "Prepares trap location" } ], "loot_rules": "Share any merchant stock equally" }
      },
      "recommended_loadout": { "gear": [ "glider" ], "pals": [ "foxparks" ], "consumables": [] },
      "xp_award_estimate": { "min": 40, "max": 70 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-small-settlement" ]
    },
    {
      "step_id": "capture-base-merchant:003",
      "type": "capture",
      "summary": "Weaken and capture the merchant",
      "detail": "Aggro the merchant away from guards, chip them to low HP, then throw your high-grade Pal Spheres until the catch lands. All non-leader humans can be captured once weakened, but expect multiple throws because their catch rate is significantly lower than normal Pals【529f5c†L67-L90】.",
      "targets": [],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 75, -479 ], "time": "night", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Use stun grenades or partner skills to avoid lethal retaliation—you cannot afford PIDF executions." },
        "coop": { "role_splits": [ { "role": "tank", "tasks": "Holds aggro" }, { "role": "snare", "tasks": "Applies slow and throws spheres" } ], "loot_rules": "Whoever spends the most spheres gets priority on merchant placement" }
      },
      "recommended_loadout": { "gear": [ "pal-sphere" ], "pals": [ "direhowl" ], "consumables": [ { "item_id": "pal-sphere", "qty": 6 } ] },
      "xp_award_estimate": { "min": 180, "max": 280 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-humans" ]
    },
    {
      "step_id": "capture-base-merchant:004",
      "type": "deliver",
      "summary": "Assign the merchant to your base",
      "detail": "Place the captured merchant in your base party. Humans have only rank 1 work suitability and cannot run farms or wield their weapons, but merchants stationed at your base permanently open their shop so you can buy and sell without hunting for a wandering spawn【94455f†L13-L18】【529f5c†L76-L90】.",
      "targets": [],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 80 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-humans" ]
    }
  ],
  "completion_criteria": [ { "type": "have-base-npc", "npc_id": "pal-merchant" } ],
  "yields": { "levels_estimate": "+0 to +1", "key_unlocks": [ "base-merchant-vendor" ] },
  "metrics": {
    "xp_per_minute": { "solo": 16.0, "coop": 22.0 },
    "travel_distance_m": 1500,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 6 } ]
  },
  "next_routes": []
}
```

### Route: Craft Foxparks Harness

This route guides players through unlocking and crafting the Foxparks harness.
While the harness doesn’t grant riding, it equips Foxparks as a flamethrower
for combat and base use【513843636763139†L117-L170】.  It demonstrates how
Palmate automatically branches into the leather farming subroute if the
player lacks materials.

```json
{
  "route_id": "mount-foxparks-harness",
  "title": "Craft Foxparks Harness",
  "category": "mounts",
  "tags": [ "pal-gear", "fire-support", "early-game", "combat" ],
  "progression_role": "optional",
  "recommended_level": { "min": 6, "max": 8 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "starter-base-capture" ], "tech": [ "tech-pal-gear-workbench" ], "items": [], "pals": [ "foxparks" ] },
  "objectives": [ "Unlock Foxparks Harness tech", "Gather Leather, Flame Organs and Paldium Fragments", "Craft the harness", "Equip and use Foxparks as a flamethrower" ],
  "estimated_time_minutes": { "solo": 20, "coop": 15 },
  "estimated_xp_gain": { "min": 400, "max": 600 },
  "risk_profile": "medium",
  "failure_penalties": { "normal": "Loss of materials", "hardcore": "Death results in loss of Pals and materials" },
  "adaptive_guidance": {
    "underleveled": "Focus on capturing Foxparks at night when their patrol radius shrinks, then delay crafting until level 7 for better survivability.",
    "overleveled": "Skip step :001 if your Pal roster already includes Foxparks and jump straight to unlocking and crafting.",
    "resource_shortages": [
      { "item_id": "leather", "solution": "Invoke resource-leather-early via step :003’s branching." },
      { "item_id": "flame-organ", "solution": "Farm Rushoar in the Sea Breeze Archipelago while Foxparks respawn." }
    ],
    "time_limited": "Perform steps :002 through :004 only; purchase missing Leather to finish within ten minutes.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:flame-organ",
        "condition": "resource_gaps contains flame-organ >= 5",
        "adjustment": "Loop Rushoar packs near the Sea Breeze bridge between attempts in step :003 until the flame-organ shortage clears.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["mount-foxparks-harness:003"],
        "follow_up_routes": ["resource-leather-early"]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 15",
        "adjustment": "Skip capturing in :001, buy the remaining Leather via the merchant tip, and craft immediately after step :002.",
        "priority": 3,
        "mode_scope": ["solo", "coop"],
        "related_steps": ["mount-foxparks-harness:002", "mount-foxparks-harness:004"]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to gather Flame Organs while another mines Paldium in :003 to finish the material checklist in a single loop.",
        "priority": 2,
        "mode_scope": ["coop"],
        "related_steps": ["mount-foxparks-harness:003"]
      }
    ]
  },
  "checkpoints": [
    { "id": "mount-foxparks-harness:checkpoint-capture", "summary": "Foxparks secured", "benefits": [ "Unlocks partner flamethrower", "Qualifies for harness tech" ], "related_steps": [ "mount-foxparks-harness:001" ] },
    { "id": "mount-foxparks-harness:checkpoint-crafted", "summary": "Harness crafted", "benefits": [ "Fire damage tool ready", "Improves furnace automation" ], "related_steps": [ "mount-foxparks-harness:004" ] }
  ],
  "supporting_routes": { "recommended": [ "resource-leather-early" ], "optional": [ "resource-paldium" ] },
  "failure_recovery": {
    "normal": "If Foxparks faints, rest at your base to heal it rather than recapturing; materials remain in inventory.",
    "hardcore": "Avoid simultaneous aggro from Rushoars and Foxparks; disengage using terrain if HP falls below 40%."
  },
  "steps": [
    {
      "step_id": "mount-foxparks-harness:001",
      "type": "capture",
      "summary": "Ensure you have a Foxparks",
      "detail": "If you haven’t already captured a Foxparks, travel to its spawn points around coordinates (189, -478) or (144, -583) in the Windswept Hills【956200907149478†L146-L169】.  Use Water Pals to weaken it, then capture it with a Pal Sphere.",
      "targets": [ { "kind": "pal", "id": "foxparks", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [189, -478], "time": "any", "weather": "any" }, { "region_id": "windswept-hills", "coords": [144, -583], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Capture from behind to avoid being burned and always carry a water Pal", "safety_buffer_items": [ { "item_id": "pal-sphere", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "bait", "tasks": "Aggro Foxparks" }, { "role": "catcher", "tasks": "Throw Pal Spheres" } ], "loot_rules": "Whoever catches it keeps it" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [ { "item_id": "pal-sphere", "qty": 3 } ] },
      "xp_award_estimate": { "min": 60, "max": 100 },
      "outputs": { "items": [], "pals": [ "foxparks" ], "unlocks": {} },
      "branching": [],
      "citations": [ "thegamer-foxparks-spawn" ]
    },
    {
      "step_id": "mount-foxparks-harness:002",
      "type": "unlock-tech",
      "summary": "Unlock the Foxparks Harness",        
      "detail": "Open the Technology menu at level 6 and spend 1 tech point to unlock the Foxparks Harness【353245298505537†L150-L180】.  This requires that you have already built a Pal Gear Workbench.",
      "targets": [ { "kind": "tech", "id": "tech-foxparks-harness" } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 10, "max": 20 },
      "outputs": { "items": [], "pals": [], "unlocks": { "tech": [ "tech-foxparks-harness" ] } },
      "branching": [],
      "citations": [ "gameclubz-foxparks-harness" ]
    },
    {
      "step_id": "mount-foxparks-harness:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 3 Leather, 5 Flame Organs and 5 Paldium Fragments.  Hunt Foxparks and Rushoars for Leather and Flame Organs, or branch to the leather farm route if you lack Leather.  Mine blue ore nodes for Paldium Fragments.",
      "targets": [ { "kind": "item", "id": "leather", "qty": 3 }, { "kind": "item", "id": "flame-organ", "qty": 5 }, { "kind": "item", "id": "paldium-fragment", "qty": 5 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [189, -478], "time": "any", "weather": "any" }, { "region_id": "sea-breeze-archipelago", "coords": [-650, -650], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Farm extra Leather (5 instead of 3) to allow for gear repairs", "safety_buffer_items": [ { "item_id": "leather", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "farmer", "tasks": "Hunt Foxparks and collect Flame Organs" }, { "role": "miner", "tasks": "Mine Paldium nodes" } ], "loot_rules": "Pool resources then split evenly" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 100, "max": 200 },
      "outputs": { "items": [ { "item_id": "leather", "qty": 3 }, { "item_id": "flame-organ", "qty": 5 }, { "item_id": "paldium-fragment", "qty": 5 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks leather >= 3", "action": "include_subroute", "subroute_ref": "resource-leather-early" } ],
      "citations": [ "gameclubz-foxparks-harness", "shockbyte-leather-sources" ]
    },
    {
      "step_id": "mount-foxparks-harness:004",
      "type": "craft",
      "summary": "Craft the harness",
      "detail": "At your Pal Gear Workbench, craft the Foxparks Harness using the collected materials【353245298505537†L150-L180】.  The process takes about one minute.",
      "targets": [ { "kind": "item", "id": "foxparks-harness", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 80 },
      "outputs": { "items": [ { "item_id": "foxparks-harness", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "gameclubz-foxparks-harness" ]
    },
    {
      "step_id": "mount-foxparks-harness:005",
      "type": "explore",
      "summary": "Equip the harness and use Foxparks",
      "detail": "Equip the harness on Foxparks via the Pal menu.  Summon Foxparks, then hold the attack button to spray fire like a flamethrower【513843636763139†L117-L170】.  This tool is excellent for clearing early dungeons and lighting furnaces.",
      "targets": [ { "kind": "item", "id": "foxparks-harness", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "foxparks-harness" ], "pals": [ "foxparks" ], "consumables": [] },
      "xp_award_estimate": { "min": 30, "max": 50 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "paldb-foxparks-partner" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "foxparks-harness", "qty": 1 } ],
  "yields": { "levels_estimate": "+1", "key_unlocks": [] },
  "metrics": {
    "xp_per_minute": { "solo": 18.0, "coop": 24.0 },
    "travel_distance_m": 900,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 3 }, { "item_id": "flame-organ", "qty": 5 }, { "item_id": "paldium-fragment", "qty": 5 } ]
  },
  "next_routes": [ { "route_id": "mount-eikthyrdeer-saddle", "reason": "Progress to a ridable mount after unlocking saddle tech" }, { "route_id": "mount-direhowl-harness", "reason": "Alternative ground mount path" } ]
}
```

### Route: Craft Eikthyrdeer Saddle (Mount)

This route unlocks the first real ridable mount for many players.  Eikthyrdeer
provides a speed boost, double jump and improved logging【142053078936299†L123-L142】.

```json
{
  "route_id": "mount-eikthyrdeer-saddle",
  "title": "Craft Eikthyrdeer Saddle",
  "category": "mounts",
  "tags": [ "mount", "mobility", "mid-game", "logging" ],
  "progression_role": "core",
  "recommended_level": { "min": 12, "max": 15 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "starter-base-capture" ], "tech": [ "tech-pal-gear-workbench" ], "items": [], "pals": [ "eikthyrdeer" ] },
  "objectives": [ "Capture an Eikthyrdeer", "Unlock the Eikthyrdeer Saddle tech", "Gather Leather, Fiber, Ingots, Horns and Paldium", "Craft the saddle", "Ride the mount" ],
  "estimated_time_minutes": { "solo": 40, "coop": 30 },
  "estimated_xp_gain": { "min": 800, "max": 1200 },
  "risk_profile": "medium",
  "failure_penalties": { "normal": "Loss of materials", "hardcore": "Death may delete your character and Pals" },
  "adaptive_guidance": {
    "underleveled": "Farm Leather and Fiber before attempting the capture; Eikthyrdeer hits hard at level 10 and below.",
    "overleveled": "Skip step :001 if you already captured multiple Eikthyrdeer and proceed to crafting for a quick unlock.",
    "resource_shortages": [
      { "item_id": "ingot", "solution": "Smelt Ore at a Primitive Furnace before starting step :003." },
      { "item_id": "horn", "solution": "Hunt extra Eikthyrdeer or trade with co-op partners who have surplus." }
    ],
    "time_limited": "Complete steps :002 through :004 now and return for the capture later; the saddle can be pre-crafted once resources are stockpiled.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:ingot",
        "condition": "resource_gaps contains ingot >= 10",
        "adjustment": "Insert a furnace run before step :003—queue 5 ore batches to cover the ingot deficit while other materials are gathered.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["mount-eikthyrdeer-saddle:003"]
      },
      {
        "signal": "level_gap:under",
        "condition": "player.estimated_level < recommended_level.min",
        "adjustment": "Delay the capture in :001 and loop resource-leather-early plus tower-free XP farms until level 12.",
        "priority": 2,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["mount-eikthyrdeer-saddle:001"],
        "follow_up_routes": ["resource-leather-early", "resource-paldium"]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign the highest damage player to secure the capture in :001 while teammates pre-farm Fiber and Paldium for :003, reducing downtime.",
        "priority": 3,
        "mode_scope": ["coop"],
        "related_steps": ["mount-eikthyrdeer-saddle:001", "mount-eikthyrdeer-saddle:003"]
      }
    ]
  },
  "checkpoints": [
    { "id": "mount-eikthyrdeer-saddle:checkpoint-capture", "summary": "Eikthyrdeer captured", "benefits": [ "Unlocks Guardian of the Forest partner skill" ], "related_steps": [ "mount-eikthyrdeer-saddle:001" ] },
    { "id": "mount-eikthyrdeer-saddle:checkpoint-craft", "summary": "Saddle assembled", "benefits": [ "Enables riding", "Improves logging throughput" ], "related_steps": [ "mount-eikthyrdeer-saddle:004" ] }
  ],
  "supporting_routes": { "recommended": [ "resource-leather-early", "resource-paldium" ], "optional": [ "mount-foxparks-harness" ] },
  "failure_recovery": {
    "normal": "If you fall during the capture, fast travel back and kite the Pal away from tower patrols before retrying.",
    "hardcore": "Use terrain elevation to break line-of-sight; disengage immediately if tower guards join the fight."
  },
  "steps": [
    {
      "step_id": "mount-eikthyrdeer-saddle:001",
      "type": "capture",
      "summary": "Catch an Eikthyrdeer",
      "detail": "Travel northwest of the starting area near the Rayne Syndicate Tower and locate an Eikthyrdeer【963225160620124†L140-L167】.  Use Water or Fire Pals depending on the variant and capture it.",
      "targets": [ { "kind": "pal", "id": "eikthyrdeer", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [300, 100], "time": "day", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Approach slowly and aim for a back attack; avoid the Tower’s aggro range", "safety_buffer_items": [ { "item_id": "pal-sphere", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "tank", "tasks": "Hold aggro" }, { "role": "catcher", "tasks": "Throw spheres" } ], "loot_rules": "First catch wins" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "foxparks" ], "consumables": [ { "item_id": "pal-sphere", "qty": 5 } ] },
      "xp_award_estimate": { "min": 100, "max": 150 },
      "outputs": { "items": [], "pals": [ "eikthyrdeer" ], "unlocks": {} },
      "branching": [],
      "citations": [ "gameclubz-eikthyrdeer-saddle" ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:002",
      "type": "unlock-tech",
      "summary": "Unlock the saddle tech",
      "detail": "At level 12, spend 2 tech points to unlock the Eikthyrdeer Saddle【963225160620124†L160-L167】.",
      "targets": [ { "kind": "tech", "id": "tech-eikthyrdeer-saddle" } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 10, "max": 20 },
      "outputs": { "items": [], "pals": [], "unlocks": { "tech": [ "tech-eikthyrdeer-saddle" ] } },
      "branching": [],
      "citations": [ "gameclubz-eikthyrdeer-saddle" ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 5 Leather, 20 Fiber, 10 Ingots, 3 Horns and 15 Paldium Fragments【963225160620124†L160-L167】.  Leather can be farmed using the leather subroute.  Fiber is harvested from bushes; Ingots require smelting ore.  Horns drop from Eikthyrdeer; if you only have one, defeat additional Eikthyrdeers.  Paldium comes from ore nodes.",
      "targets": [ { "kind": "item", "id": "leather", "qty": 5 }, { "kind": "item", "id": "fiber", "qty": 20 }, { "kind": "item", "id": "ingot", "qty": 10 }, { "kind": "item", "id": "horn", "qty": 3 }, { "kind": "item", "id": "paldium-fragment", "qty": 15 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [189, -478], "time": "any", "weather": "any" }, { "region_id": "bamboo-groves", "coords": [300, 300], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Gather a 20 % buffer (6 Leather, 24 Fiber) to account for mistakes", "safety_buffer_items": [ { "item_id": "leather", "qty": 1 } ] },
        "coop": { "role_splits": [ { "role": "hunter", "tasks": "Farm Leather and Horns" }, { "role": "miner", "tasks": "Mine ore and smelt Ingots" }, { "role": "gatherer", "tasks": "Collect Fiber and Paldium" } ], "loot_rules": "Pool resources and split after crafting" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 300, "max": 500 },
      "outputs": { "items": [ { "item_id": "leather", "qty": 5 }, { "item_id": "fiber", "qty": 20 }, { "item_id": "ingot", "qty": 10 }, { "item_id": "horn", "qty": 3 }, { "item_id": "paldium-fragment", "qty": 15 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks leather >= 5", "action": "include_subroute", "subroute_ref": "resource-leather-early" } ],
      "citations": [ "gameclubz-eikthyrdeer-saddle", "eikthyrdeer-drops" ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:004",
      "type": "craft",
      "summary": "Craft the saddle",
      "detail": "Use the Pal Gear Workbench to craft the Eikthyrdeer Saddle【963225160620124†L160-L167】.  The process takes around 90 seconds.",
      "targets": [ { "kind": "item", "id": "eikthyrdeer-saddle", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 100, "max": 150 },
      "outputs": { "items": [ { "item_id": "eikthyrdeer-saddle", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "gameclubz-eikthyrdeer-saddle" ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:005",
      "type": "explore",
      "summary": "Equip and ride your mount",
      "detail": "Equip the saddle on Eikthyrdeer via the Pal menu and summon it.  Press LB to call the Pal and X to mount.  Enjoy increased movement speed, a double jump and improved logging efficiency【142053078936299†L123-L142】.",
      "targets": [ { "kind": "pal", "id": "eikthyrdeer", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "eikthyrdeer-saddle" ], "pals": [ "eikthyrdeer" ], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 70 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "gameclubz-eikthyrdeer-saddle", "eikthyrdeer-partner-skill" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "eikthyrdeer-saddle", "qty": 1 } ],
  "yields": { "levels_estimate": "+2 to +3", "key_unlocks": [ "tech-eikthyrdeer-saddle" ] },
  "metrics": {
    "xp_per_minute": { "solo": 16.0, "coop": 21.0 },
    "travel_distance_m": 1800,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 6 }, { "item_id": "leather", "qty": 5 }, { "item_id": "fiber", "qty": 20 }, { "item_id": "ingot", "qty": 10 }, { "item_id": "horn", "qty": 3 }, { "item_id": "paldium-fragment", "qty": 15 } ]
  },
  "next_routes": [ { "route_id": "mount-nitewing-saddle", "reason": "Progress to a flying mount" }, { "route_id": "tower-rayne-syndicate", "reason": "Now strong enough to challenge a tower" } ]
}
```

### Route: Craft Direhowl Harness (Ground Mount)

Direhowl provides a faster ground mount than Eikthyrdeer but lacks logging bonuses.  This route covers capturing Direhowl and crafting its harness.

```json
{ 
  "route_id": "mount-direhowl-harness",
  "title": "Craft Direhowl Harness",
  "category": "mounts",
  "tags": [ "mount", "speed", "mid-game", "night-hunt" ],
  "progression_role": "optional",
  "recommended_level": { "min": 9, "max": 12 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "starter-base-capture" ], "tech": [ "tech-pal-gear-workbench" ], "items": [], "pals": [ "direhowl" ] },
  "objectives": [ "Capture a Direhowl", "Unlock the Direhowl Harness", "Gather Leather, Wood, Fiber and Paldium", "Craft the harness", "Ride the mount" ],
  "estimated_time_minutes": { "solo": 30, "coop": 20 },
  "estimated_xp_gain": { "min": 500, "max": 800 },
  "risk_profile": "medium",
  "failure_penalties": { "normal": "Loss of materials", "hardcore": "Death may delete character and Pals" },
  "adaptive_guidance": {
    "underleveled": "Hunt Direhowl during dawn when fewer spawn together, and bring a tanky Pal to soak hits.",
    "overleveled": "Use tranquilizer bolts to speed up captures; Direhowl’s HP melts under high-tier gear.",
    "resource_shortages": [
      { "item_id": "wood", "solution": "Assign work Pals to logging while you hunt; deposit extras before step :003." },
      { "item_id": "leather", "solution": "Loop the leather subroute or trade with co-op allies." }
    ],
    "time_limited": "Skip step :001 if Direhowl is already caught and fast travel to your base to craft immediately.",
    "dynamic_rules": [
      {
        "signal": "mode:hardcore",
        "condition": "mode.hardcore === true",
        "adjustment": "Use the Moonless Shore spawn where cliffs provide cover; retreat after each pull to avoid overlapping packs during step :001.",
        "priority": 1,
        "mode_scope": ["hardcore"],
        "related_steps": ["mount-direhowl-harness:001"]
      },
      {
        "signal": "resource_gap:wood",
        "condition": "resource_gaps contains wood >= 20",
        "adjustment": "Queue base logging jobs before leaving or bring a logging Pal like Eikthyrdeer so step :003 completes in a single loop.",
        "priority": 2,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["mount-direhowl-harness:003"]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 20",
        "adjustment": "Craft immediately if Direhowl is already owned; otherwise capture once and postpone any optional repeat farming to a later session.",
        "priority": 3,
        "mode_scope": ["solo", "coop"],
        "related_steps": ["mount-direhowl-harness:001", "mount-direhowl-harness:004"]
      }
    ]
  },
  "checkpoints": [
    { "id": "mount-direhowl-harness:checkpoint-capture", "summary": "Direhowl captured", "benefits": [ "Unlocks sprinting partner skill" ], "related_steps": [ "mount-direhowl-harness:001" ] },
    { "id": "mount-direhowl-harness:checkpoint-crafted", "summary": "Harness ready", "benefits": [ "Fastest ground mount unlocked" ], "related_steps": [ "mount-direhowl-harness:004" ] }
  ],
  "supporting_routes": { "recommended": [ "resource-leather-early" ], "optional": [ "resource-paldium" ] },
  "failure_recovery": {
    "normal": "If Direhowl defeats you, respawn at the nearest statue and kite it into open areas for the next attempt.",
    "hardcore": "Avoid desert bandit camps en route; detour along the coastline to minimise PvE threats."
  },
  "steps": [
    {
      "step_id": "mount-direhowl-harness:001",
      "type": "capture",
      "summary": "Catch a Direhowl",
      "detail": "Travel to the Moonless Shore or Twilight Dunes at night and locate a Direhowl.  Use Light element skills to weaken it and capture it with Pal Spheres.",
      "targets": [ { "kind": "pal", "id": "direhowl", "qty": 1 } ],
      "locations": [ { "region_id": "moonless-shore", "coords": [600, -350], "time": "night", "weather": "any" }, { "region_id": "twilight-dunes", "coords": [700, -100], "time": "night", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Bring a Pal with healing skills and avoid multiple Direhowls", "safety_buffer_items": [ { "item_id": "pal-sphere", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "tank", "tasks": "Take aggro" }, { "role": "catcher", "tasks": "Throw spheres" } ], "loot_rules": "First catch keeps it" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "eikthyrdeer" ], "consumables": [ { "item_id": "pal-sphere", "qty": 5 } ] },
      "xp_award_estimate": { "min": 80, "max": 120 },
      "outputs": { "items": [], "pals": [ "direhowl" ], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-direhowl-recipe" ]
    },
    {
      "step_id": "mount-direhowl-harness:002",
      "type": "unlock-tech",
      "summary": "Unlock Direhowl Harness tech",
      "detail": "At level 9, spend 1 tech point to unlock the Direhowl Harness【197143349627535†L151-L156】.",
      "targets": [ { "kind": "tech", "id": "tech-direhowl-harness" } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 10, "max": 20 },
      "outputs": { "items": [], "pals": [], "unlocks": { "tech": [ "tech-direhowl-harness" ] } },
      "branching": [],
      "citations": [ "palwiki-direhowl-recipe" ]
    },
    {
      "step_id": "mount-direhowl-harness:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 10 Leather, 20 Wood, 15 Fiber and 10 Paldium Fragments【197143349627535†L151-L156】.  Use the leather farming route if necessary.  Wood and Fiber can be collected around the Windswept Hills; Paldium from blue ore nodes.",
      "targets": [ { "kind": "item", "id": "leather", "qty": 10 }, { "kind": "item", "id": "wood", "qty": 20 }, { "kind": "item", "id": "fiber", "qty": 15 }, { "kind": "item", "id": "paldium-fragment", "qty": 10 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Gather a 10 % buffer", "safety_buffer_items": [ { "item_id": "leather", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "farmer", "tasks": "Collect Leather" }, { "role": "logger", "tasks": "Gather Wood and Fiber" }, { "role": "miner", "tasks": "Mine Paldium" } ], "loot_rules": "Pool then split" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 200, "max": 350 },
      "outputs": { "items": [ { "item_id": "leather", "qty": 10 }, { "item_id": "wood", "qty": 20 }, { "item_id": "fiber", "qty": 15 }, { "item_id": "paldium-fragment", "qty": 10 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks leather >= 10", "action": "include_subroute", "subroute_ref": "resource-leather-early" } ],
      "citations": [ "palwiki-direhowl-recipe", "shockbyte-leather-sources" ]
    },
    {
      "step_id": "mount-direhowl-harness:004",
      "type": "craft",
      "summary": "Craft the harness",
      "detail": "Use the Pal Gear Workbench to craft the Direhowl Harness with the collected materials【197143349627535†L151-L156】.",
      "targets": [ { "kind": "item", "id": "direhowl-harness", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [0, 0], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 60, "max": 100 },
      "outputs": { "items": [ { "item_id": "direhowl-harness", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-direhowl-recipe" ]
    },
    {
      "step_id": "mount-direhowl-harness:005",
      "type": "explore",
      "summary": "Equip and ride",
      "detail": "Equip the harness on Direhowl and ride your new mount.  It offers greater sprint speed than Eikthyrdeer but lacks double jump and logging bonuses.",
      "targets": [ { "kind": "pal", "id": "direhowl", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "direhowl-harness" ], "pals": [ "direhowl" ], "consumables": [] },
      "xp_award_estimate": { "min": 30, "max": 50 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-direhowl-recipe" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "direhowl-harness", "qty": 1 } ],
  "yields": { "levels_estimate": "+1 to +2", "key_unlocks": [ "tech-direhowl-harness" ] },
  "metrics": {
    "xp_per_minute": { "solo": 17.0, "coop": 22.0 },
    "travel_distance_m": 1600,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 6 }, { "item_id": "leather", "qty": 10 }, { "item_id": "wood", "qty": 20 }, { "item_id": "fiber", "qty": 15 }, { "item_id": "paldium-fragment", "qty": 10 } ]
  },
  "next_routes": [ { "route_id": "mount-eikthyrdeer-saddle", "reason": "Alternate mount path" }, { "route_id": "tower-rayne-syndicate", "reason": "Ready to tackle a boss" } ]
}
```

## Level Estimation Logic

### Route: Craft Nitewing Saddle (Flying Mount)

This route enables players to obtain their first flying mount by capturing Nitewing and crafting its saddle.  The Nitewing can be found as an Alpha Pal at Ice Wind Island and provides high‑speed flight【825211382965329†L294-L302】.  The recipe for the saddle is drawn from the Palworld Wiki【524512399342633†L151-L156】.  Leather requirements automatically branch to the leather farming loop if needed.

```json
{
  "route_id": "mount-nitewing-saddle",
  "title": "Craft Nitewing Saddle",
  "category": "mounts",
  "tags": [ "mount", "flight", "mid-game", "exploration" ],
  "progression_role": "core",
  "recommended_level": { "min": 15, "max": 20 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "mount-eikthyrdeer-saddle" ], "tech": [ "tech-pal-gear-workbench" ], "items": [], "pals": [] },
  "objectives": [ "Capture a Nitewing", "Unlock the Nitewing Saddle tech", "Gather materials: 20 Leather, 10 Cloth, 15 Ingots, 20 Fiber, 20 Paldium", "Craft the saddle", "Ride a flying mount" ],
  "estimated_time_minutes": { "solo": 45, "coop": 35 },
  "estimated_xp_gain": { "min": 900, "max": 1400 },
  "risk_profile": "medium",
  "failure_penalties": { "normal": "Loss of materials", "hardcore": "Death may delete character and Pals" },
  "adaptive_guidance": {
    "underleveled": "Farm Leather and Cloth before travelling; Ice Wind Island’s level 18 mobs overwhelm players below 14.",
    "overleveled": "Capture Nitewing using Ultra Spheres for a near-guaranteed catch, then finish crafting in one trip.",
    "resource_shortages": [
      { "item_id": "cloth", "solution": "Queue extra Cloth at the Workbench before leaving for Ice Wind Island." },
      { "item_id": "paldium-fragment", "solution": "Mine volcanic nodes while mounted on Eikthyrdeer." }
    ],
    "time_limited": "Skip step :001 if you already own Nitewing and focus on crafting to unlock flight quickly.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:cloth",
        "condition": "resource_gaps contains cloth >= 10",
        "adjustment": "Batch-craft Cloth before departure so step :003 doesn’t require a return trip mid-route.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["mount-nitewing-saddle:003"]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 30",
        "adjustment": "Defer the Ice Wind Island capture to a future session; instead, craft outstanding materials in :003 and unlock the tech in :002 now.",
        "priority": 2,
        "mode_scope": ["solo", "coop"],
        "related_steps": ["mount-nitewing-saddle:002", "mount-nitewing-saddle:003"]
      },
      {
        "signal": "goal:exploration",
        "condition": "goals includes exploration",
        "adjustment": "Prioritise finishing all steps in one run to unlock aerial scouting; queue this route to the top of recommendations when exploration is requested.",
        "priority": 3,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["mount-nitewing-saddle:004", "mount-nitewing-saddle:005"],
        "follow_up_routes": ["tech-grappling-gun", "tower-rayne-syndicate"]
      }
    ]
  },
  "checkpoints": [
    { "id": "mount-nitewing-saddle:checkpoint-capture", "summary": "Nitewing captured", "benefits": [ "Access to flight-ready Pal" ], "related_steps": [ "mount-nitewing-saddle:001" ] },
    { "id": "mount-nitewing-saddle:checkpoint-crafted", "summary": "Saddle complete", "benefits": [ "Unlocks full aerial traversal", "Opens late-game farming spots" ], "related_steps": [ "mount-nitewing-saddle:004" ] }
  ],
  "supporting_routes": { "recommended": [ "resource-leather-early", "resource-paldium" ], "optional": [ "mount-foxparks-harness" ] },
  "failure_recovery": {
    "normal": "If you fall off cliffs during the capture, glide with a parachute or fast travel back to avoid corpse runs.",
    "hardcore": "Carry heat and cold resist gear; abandon the attempt if armor durability falls below 30 %."
  },
  "steps": [
    {
      "step_id": "mount-nitewing-saddle:001",
      "type": "capture",
      "summary": "Catch a Nitewing",
      "detail": "Travel to Ice Wind Island and find Nitewing.  The Alpha Nitewing spawns around the frozen cliffs (level 18)【825211382965329†L294-L302】.  Use Electric or Ice Pals to weaken it, then throw Pal Spheres to capture.",
      "targets": [ { "kind": "pal", "id": "nitewing", "qty": 1 } ],
      "locations": [ { "region_id": "ice-wind-island", "coords": [ -800, 450 ], "time": "day", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Approach from behind to avoid Nitewing’s dive attacks and bring healing supplies", "safety_buffer_items": [ { "item_id": "pal-sphere", "qty": 2 } ] },
        "coop": { "role_splits": [ { "role": "bait", "tasks": "Aggro Nitewing and dodge" }, { "role": "catcher", "tasks": "Throw Pal Spheres" } ], "loot_rules": "First capture keeps it" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "eikthyrdeer" ], "consumables": [ { "item_id": "pal-sphere", "qty": 5 } ] },
      "xp_award_estimate": { "min": 120, "max": 180 },
      "outputs": { "items": [], "pals": [ "nitewing" ], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-bosses" ]
    },
    {
      "step_id": "mount-nitewing-saddle:002",
      "type": "unlock-tech",
      "summary": "Unlock Nitewing Saddle tech",
      "detail": "At level 15, spend 2 tech points to unlock the Nitewing saddle【524512399342633†L151-L156】.",
      "targets": [ { "kind": "tech", "id": "tech-nitewing-saddle" } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 20, "max": 40 },
      "outputs": { "items": [], "pals": [], "unlocks": { "tech": [ "tech-nitewing-saddle" ] } },
      "branching": [],
      "citations": [ "palwiki-nitewing-saddle" ]
    },
    {
      "step_id": "mount-nitewing-saddle:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 20 Leather, 10 Cloth, 15 Ingots, 20 Fiber and 20 Paldium Fragments.  Hunt leather‑dropping Pals or branch to the leather loop if needed.  Cloth is crafted from fiber at a Primitive Workbench.  Ingots require smelting ore.",
      "targets": [ { "kind": "item", "id": "leather", "qty": 20 }, { "kind": "item", "id": "cloth", "qty": 10 }, { "kind": "item", "id": "ingot", "qty": 15 }, { "kind": "item", "id": "fiber", "qty": 20 }, { "kind": "item", "id": "paldium-fragment", "qty": 20 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Collect a 20 % buffer of each material to account for failures", "safety_buffer_items": [ { "item_id": "leather", "qty": 4 } ] },
        "coop": { "role_splits": [ { "role": "farmer", "tasks": "Gather Leather and Fiber" }, { "role": "crafter", "tasks": "Craft Cloth and smelt Ingots" }, { "role": "miner", "tasks": "Mine Paldium" } ], "loot_rules": "Pool resources and share after crafting" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 300, "max": 500 },
      "outputs": { "items": [ { "item_id": "leather", "qty": 20 }, { "item_id": "cloth", "qty": 10 }, { "item_id": "ingot", "qty": 15 }, { "item_id": "fiber", "qty": 20 }, { "item_id": "paldium-fragment", "qty": 20 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks leather >= 20", "action": "include_subroute", "subroute_ref": "resource-leather-early" } ],
      "citations": [ "palwiki-nitewing-saddle", "shockbyte-leather-sources" ]
    },
    {
      "step_id": "mount-nitewing-saddle:004",
      "type": "craft",
      "summary": "Craft the Nitewing Saddle",
      "detail": "At your Pal Gear Workbench, craft the Nitewing Saddle using the collected materials【524512399342633†L151-L156】.  The process takes about two minutes.",
      "targets": [ { "kind": "item", "id": "nitewing-saddle", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 100, "max": 150 },
      "outputs": { "items": [ { "item_id": "nitewing-saddle", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-nitewing-saddle" ]
    },
    {
      "step_id": "mount-nitewing-saddle:005",
      "type": "explore",
      "summary": "Equip and fly",
      "detail": "Equip the saddle on Nitewing via the Pal menu and summon it.  Use the mount to fly across the map at high speed, unlocking new exploration possibilities.",
      "targets": [ { "kind": "pal", "id": "nitewing", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "nitewing-saddle" ], "pals": [ "nitewing" ], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 70 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "palwiki-nitewing-saddle" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "nitewing-saddle", "qty": 1 } ],
  "yields": { "levels_estimate": "+2 to +3", "key_unlocks": [ "tech-nitewing-saddle" ] },
  "metrics": {
    "xp_per_minute": { "solo": 15.5, "coop": 20.5 },
    "travel_distance_m": 2400,
    "consumable_cost": [ { "item_id": "pal-sphere", "qty": 6 }, { "item_id": "leather", "qty": 20 }, { "item_id": "cloth", "qty": 10 }, { "item_id": "ingot", "qty": 15 }, { "item_id": "fiber", "qty": 20 }, { "item_id": "paldium-fragment", "qty": 20 } ]
  },
  "next_routes": [ { "route_id": "tech-grappling-gun", "reason": "Use flying mobility to gather materials for advanced tools" }, { "route_id": "tower-rayne-syndicate", "reason": "Now capable of taking on tower bosses" } ]
}
```

### Route: Craft Grappling Gun

The Grappling Gun allows players to traverse cliffs and gaps quickly.  Unlocking it requires an Ancient Technology Point obtained from a tower boss.  The crafting recipe calls for Paldium, Ingots, Fiber and an Ancient Civilization Part【312162085103617†L180-L205】.

```json
{
  "route_id": "tech-grappling-gun",
  "title": "Craft Grappling Gun",
  "category": "tech",
  "tags": [ "mobility", "tool", "mid-game", "tech" ],
  "progression_role": "core",
  "recommended_level": { "min": 12, "max": 16 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [], "tech": [ "tech-grappling-gun" ], "items": [], "pals": [] },
  "objectives": [ "Obtain an Ancient Technology Point", "Unlock Grappling Gun tech", "Gather crafting materials", "Craft the Grappling Gun", "Use the tool" ],
  "estimated_time_minutes": { "solo": 30, "coop": 25 },
  "estimated_xp_gain": { "min": 500, "max": 800 },
  "risk_profile": "medium",
  "failure_penalties": { "normal": "Loss of materials", "hardcore": "Death may result in permanent character loss" },
  "adaptive_guidance": {
    "underleveled": "Secure the Ancient Technology Point via the tower route with a coop partner if you are below level 14.",
    "overleveled": "Speedrun the tower fight and craft immediately to unlock traversal shortcuts for late-game farming.",
    "resource_shortages": [
      { "item_id": "ancient-civilization-part", "solution": "Run Ruin dungeons or reuse spare parts from tower caches." },
      { "item_id": "fiber", "solution": "Assign work Pals to logging stations to auto-gather while you clear the tower." }
    ],
    "time_limited": "Borrow an Ancient Technology Point from stored inventory and postpone dungeon farming for later.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:ancient-civilization-part",
        "condition": "resource_gaps contains ancient-civilization-part >= 1",
        "adjustment": "Schedule a dungeon run immediately after step :001 so the Ancient Part is secured before crafting begins.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["tech-grappling-gun:003"],
        "follow_up_routes": ["tower-rayne-syndicate"]
      },
      {
        "signal": "goal:mobility",
        "condition": "goals includes mobility",
        "adjustment": "Prioritise this route once the Ancient Point is banked; the recommender boosts its score when mobility is requested.",
        "priority": 2,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["tech-grappling-gun:004", "tech-grappling-gun:005"]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties—two players clear the tower while the others farm fiber and ingots—so crafting can start immediately after the point is earned.",
        "priority": 3,
        "mode_scope": ["coop"],
        "related_steps": ["tech-grappling-gun:001", "tech-grappling-gun:003"]
      }
    ]
  },
  "checkpoints": [
    { "id": "tech-grappling-gun:checkpoint-point", "summary": "Ancient Technology Point acquired", "benefits": [ "Unlocks advanced tech tier" ], "related_steps": [ "tech-grappling-gun:001" ] },
    { "id": "tech-grappling-gun:checkpoint-craft", "summary": "Grappling Gun crafted", "benefits": [ "Enables rapid traversal" ], "related_steps": [ "tech-grappling-gun:004" ] }
  ],
  "supporting_routes": { "recommended": [ "tower-rayne-syndicate", "mount-nitewing-saddle" ], "optional": [ "resource-paldium" ] },
  "failure_recovery": {
    "normal": "If you wipe in a dungeon while farming parts, restock healing items and reattempt after respawning at base.",
    "hardcore": "Only tackle dungeons with full armor durability; withdraw if Ancient Part drops do not appear within two clears."
  },
  "steps": [
    {
      "step_id": "tech-grappling-gun:001",
      "type": "fight",
      "summary": "Earn an Ancient Technology Point",
      "detail": "Complete the Rayne Syndicate Tower or another tower to obtain at least one Ancient Technology Point.  See the tower route for details.",
      "targets": [ { "kind": "item", "id": "ancient-technology-point", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 500, "max": 700 },
      "outputs": { "items": [ { "item_id": "ancient-technology-point", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [ { "condition": "player lacks ancient-technology-point >= 1", "action": "include_subroute", "subroute_ref": "tower-rayne-syndicate" } ],
      "citations": [ "pcgamesn-bosses" ]
    },
    {
      "step_id": "tech-grappling-gun:002",
      "type": "unlock-tech",
      "summary": "Unlock Grappling Gun tech",
      "detail": "Spend 1 Ancient Technology Point at level 12 to unlock the Grappling Gun【312162085103617†L180-L205】.",
      "targets": [ { "kind": "tech", "id": "tech-grappling-gun" } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 10, "max": 20 },
      "outputs": { "items": [], "pals": [], "unlocks": { "tech": [ "tech-grappling-gun" ] } },
      "branching": [],
      "citations": [ "pcgamer-grappling-gun" ]
    },
    {
      "step_id": "tech-grappling-gun:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 10 Paldium Fragments, 10 Ingots, 30 Fiber and 1 Ancient Civilization Part【312162085103617†L180-L205】.  Ancient Civilization Parts drop from tower bosses and dungeons.",
      "targets": [ { "kind": "item", "id": "paldium-fragment", "qty": 10 }, { "kind": "item", "id": "ingot", "qty": 10 }, { "kind": "item", "id": "fiber", "qty": 30 }, { "kind": "item", "id": "ancient-civilization-part", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {
        "hardcore": { "tactics": "Gather a 10 % buffer of each resource", "safety_buffer_items": [ { "item_id": "paldium-fragment", "qty": 1 } ] },
        "coop": { "role_splits": [ { "role": "miner", "tasks": "Mine Paldium" }, { "role": "smelter", "tasks": "Craft Ingots" }, { "role": "gatherer", "tasks": "Harvest Fiber" }, { "role": "raider", "tasks": "Farm Ancient Parts from dungeons" } ], "loot_rules": "Pool resources and share" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 150, "max": 250 },
      "outputs": { "items": [ { "item_id": "paldium-fragment", "qty": 10 }, { "item_id": "ingot", "qty": 10 }, { "item_id": "fiber", "qty": 30 }, { "item_id": "ancient-civilization-part", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamer-grappling-gun" ]
    },
    {
      "step_id": "tech-grappling-gun:004",
      "type": "craft",
      "summary": "Craft the Grappling Gun",
      "detail": "At your Primitive Workbench or Weapon Workbench, craft the Grappling Gun using the collected materials【312162085103617†L180-L205】.",
      "targets": [ { "kind": "item", "id": "grappling-gun", "qty": 1 } ],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 0, 0 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 80, "max": 120 },
      "outputs": { "items": [ { "item_id": "grappling-gun", "qty": 1 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamer-grappling-gun" ]
    },
    {
      "step_id": "tech-grappling-gun:005",
      "type": "explore",
      "summary": "Use the Grappling Gun",
      "detail": "Equip the Grappling Gun and test it on nearby cliffs.  Aim at a surface and fire to pull yourself toward it.  This tool greatly improves exploration and mobility.",
      "targets": [ { "kind": "item", "id": "grappling-gun", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "grappling-gun" ], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 20, "max": 30 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamer-grappling-gun" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "grappling-gun", "qty": 1 } ],
  "yields": { "levels_estimate": "+1", "key_unlocks": [ "tech-grappling-gun" ] },
  "metrics": {
    "xp_per_minute": { "solo": 17.5, "coop": 22.5 },
    "travel_distance_m": 600,
    "consumable_cost": [ { "item_id": "ancient-civilization-part", "qty": 1 }, { "item_id": "paldium-fragment", "qty": 10 }, { "item_id": "fiber", "qty": 30 }, { "item_id": "ingot", "qty": 10 } ]
  },
  "next_routes": [ { "route_id": "capture-jetragon", "reason": "Use advanced mobility to tackle a legendary Pal" } ]
}
```

### Route: Rayne Syndicate Tower (Zoe & Grizzbolt)

The first tower challenge pits you against Zoe and her electric Pal Grizzbolt.  You must deal 30 000 damage within ten minutes【825211382965329†L103-L118】.  Completing this fight awards several Ancient Technology Points and unlocks higher‑tier tech.

```json
{
  "route_id": "tower-rayne-syndicate",
  "title": "Rayne Syndicate Tower: Zoe & Grizzbolt",
  "category": "bosses",
  "tags": [ "tower", "boss", "ancient-points", "combat" ],
  "progression_role": "core",
  "recommended_level": { "min": 15, "max": 18 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "mount-eikthyrdeer-saddle" ], "tech": [], "items": [], "pals": [] },
  "objectives": [ "Travel to the Rayne Syndicate Tower", "Prepare with Ground‑type Pals and gear", "Defeat Zoe & Grizzbolt within the time limit", "Claim Ancient Technology Points" ],
  "estimated_time_minutes": { "solo": 15, "coop": 10 },
  "estimated_xp_gain": { "min": 1500, "max": 2500 },
  "risk_profile": "high",
  "failure_penalties": { "normal": "Loss of consumables and time", "hardcore": "Death results in character deletion and loss of Pals" },
  "adaptive_guidance": {
    "underleveled": "Delay the attempt until level 15+ or bring a co-op partner to split aggro.",
    "overleveled": "Focus on phase DPS; you can burst the boss quickly with upgraded rifles and fire pals.",
    "resource_shortages": [
      { "item_id": "healing-potion", "solution": "Craft Large Berries at camp before entry." },
      { "item_id": "shield", "solution": "Forge spares at the Weapon Workbench in case of durability loss." }
    ],
    "time_limited": "If pressed for time, skip optional mobs and sprint straight to the arena; the boss instance starts instantly.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:healing-potion",
        "condition": "resource_gaps contains healing-potion >= 3",
        "adjustment": "Queue a berry crafting batch before travelling so each player carries at least three heals into step :003.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["tower-rayne-syndicate:002", "tower-rayne-syndicate:003"]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a dedicated healer who rotates shields while the DPS focuses on Grizzbolt; swap roles after each phase to manage stamina.",
        "priority": 2,
        "mode_scope": ["coop"],
        "related_steps": ["tower-rayne-syndicate:003"]
      },
      {
        "signal": "goal:ancient-points",
        "condition": "goals includes ancient-points",
        "adjustment": "Push this tower to the top of recommendations until its Ancient Technology Points are secured, then immediately surface tech-grappling-gun as the follow-up.",
        "priority": 3,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["tower-rayne-syndicate:003"],
        "follow_up_routes": ["tech-grappling-gun"]
      }
    ]
  },
  "checkpoints": [
    { "id": "tower-rayne-syndicate:checkpoint-arrival", "summary": "Tower entrance reached", "benefits": [ "Unlocks fast travel statue" ], "related_steps": [ "tower-rayne-syndicate:001" ] },
    { "id": "tower-rayne-syndicate:checkpoint-victory", "summary": "Zoe & Grizzbolt defeated", "benefits": [ "Awards Ancient Technology Points", "Unlocks Grappling Gun tech" ], "related_steps": [ "tower-rayne-syndicate:003" ] }
  ],
  "supporting_routes": { "recommended": [ "mount-eikthyrdeer-saddle", "mount-nitewing-saddle" ], "optional": [ "tech-grappling-gun" ] },
  "failure_recovery": {
    "normal": "If you fail the timer, exit to restock consumables and re-enter; progress resets but no loot is lost.",
    "hardcore": "Abort the attempt if armor durability reaches red; Hardcore characters should prioritise survival over DPS."
  },
  "steps": [
    {
      "step_id": "tower-rayne-syndicate:001",
      "type": "travel",
      "summary": "Reach the tower",
      "detail": "Ride your mount to the Rayne Syndicate Tower at coordinates (112, -434) in the Windswept Hills【825211382965329†L103-L118】.",
      "targets": [],
      "locations": [ { "region_id": "windswept-hills", "coords": [ 112, -434 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "eikthyrdeer-saddle" ], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 70 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-bosses" ]
    },
    {
      "step_id": "tower-rayne-syndicate:002",
      "type": "prepare",
      "summary": "Prepare for battle",
      "detail": "Equip Ground or Grass Pals such as Gumoss and Fuddler to counter Grizzbolt’s Electric attacks【825211382965329†L103-L118】.  Carry healing items and equip decent armor.  In Hardcore, craft an extra shield.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": { "tactics": "Bring two Ground Pals and keep distance when Grizzbolt powers up", "safety_buffer_items": [ { "item_id": "paldium-fragment", "qty": 5 } ] },
        "coop": { "role_splits": [ { "role": "tank", "tasks": "Hold boss aggro" }, { "role": "dps", "tasks": "Deal damage from range" } ], "loot_rules": "Ancient Technology Points are shared" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "foxparks", "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 100, "max": 200 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-bosses" ]
    },
    {
      "step_id": "tower-rayne-syndicate:003",
      "type": "fight",
      "summary": "Defeat Zoe & Grizzbolt",
      "detail": "Engage Zoe and her Pal Grizzbolt.  Deal at least 30K damage within ten minutes【825211382965329†L103-L118】.  Use Ground or Water attacks, dodge electric beams and avoid the arena edges.",
      "targets": [ { "kind": "boss", "id": "rayne-syndicate-tower", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": { "tactics": "Stay mobile, use ranged attacks and always maintain a safe distance", "safety_buffer_items": [ { "item_id": "ancient-technology-point", "qty": 1 } ] },
        "coop": { "role_splits": [ { "role": "healer", "tasks": "Heal allies" }, { "role": "damage", "tasks": "Focus on Grizzbolt" } ], "loot_rules": "Share Ancient Technology Points equally" }
      },
      "recommended_loadout": { "gear": [], "pals": [ "lifmunk" ], "consumables": [] },
      "xp_award_estimate": { "min": 1200, "max": 2000 },
      "outputs": { "items": [ { "item_id": "ancient-technology-point", "qty": 5 } ], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-bosses" ]
    }
  ],
  "completion_criteria": [ { "type": "boss-cleared", "boss_id": "rayne-syndicate-tower" } ],
  "yields": { "levels_estimate": "+3 to +4", "key_unlocks": [ "ancient-technology-points" ] },
  "metrics": {
    "xp_per_minute": { "solo": 110.0, "coop": 160.0 },
    "travel_distance_m": 1500,
    "consumable_cost": [ { "item_id": "healing-potion", "qty": 5 }, { "item_id": "shield", "qty": 1 } ]
  },
  "next_routes": [ { "route_id": "tech-grappling-gun", "reason": "Rewards provide the point needed to unlock this tech" }, { "route_id": "capture-jetragon", "reason": "Gives experience and resources to attempt the legendary Pal" } ]
}
```

### Route: Capture Jetragon (Legendary Dragon)

This advanced route details how to capture Jetragon, a level 50 legendary Pal found at Mount Obsidian【825211382965329†L337-L339】.  It requires high‑level gear, heat resistance and strong Pals.  Capturing Jetragon provides one of the fastest flying mounts in Palworld.

```json
{
  "route_id": "capture-jetragon",
  "title": "Capture Jetragon",
  "category": "capture-index",
  "tags": [ "legendary", "capture", "late-game", "flying" ],
  "progression_role": "optional",
  "recommended_level": { "min": 50, "max": 60 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [ "tower-rayne-syndicate", "mount-nitewing-saddle" ], "tech": [], "items": [], "pals": [] },
  "objectives": [ "Prepare high‑level gear and Pals", "Travel to Mount Obsidian", "Weaken Jetragon", "Capture it" ],
  "estimated_time_minutes": { "solo": 60, "coop": 45 },
  "estimated_xp_gain": { "min": 2500, "max": 4000 },
  "risk_profile": "high",
  "failure_penalties": { "normal": "Loss of valuable Pal Spheres and gear", "hardcore": "Death may result in permanent loss of character and Pals" },
  "adaptive_guidance": {
    "underleveled": "Run tower and dungeon loops until at least level 48; bring Heat Resistant armor before attempting the volcano.",
    "overleveled": "Use Legendary Spheres and heavy weapons to shorten the fight; Jetragon can be bursted down quickly at high gear scores.",
    "resource_shortages": [
      { "item_id": "heat-resistant-armor", "solution": "Craft at a Production Assembly Line using Fire Organs and Ingot stock." },
      { "item_id": "ultra-pal-sphere", "solution": "Farm Ancient Parts and craft extras before travelling." }
    ],
    "time_limited": "Skip optional prep by borrowing Ultra Spheres from teammates and focusing on the capture attempt.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:heat-resistant-armor",
        "condition": "resource_gaps contains heat-resistant-armor >= 1",
        "adjustment": "Queue armor crafting before departure to prevent heat damage from ending the run early; do not proceed to step :002 without it.",
        "priority": 1,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["capture-jetragon:001"]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Designate a loot master to track Ultra Sphere usage so the team can rotate capture attempts without wasting consumables.",
        "priority": 2,
        "mode_scope": ["coop"],
        "related_steps": ["capture-jetragon:003", "capture-jetragon:004"]
      },
      {
        "signal": "goal:legendary",
        "condition": "goals includes legendary",
        "adjustment": "Surface this route immediately after prerequisites clear and highlight the need for Ultra Spheres plus Grappling Gun mobility in the recommendation copy.",
        "priority": 3,
        "mode_scope": ["normal", "hardcore", "solo", "coop"],
        "related_steps": ["capture-jetragon:001", "capture-jetragon:004"]
      }
    ]
  },
  "checkpoints": [
    { "id": "capture-jetragon:checkpoint-prep", "summary": "Heat gear and spheres ready", "benefits": [ "Ensures survival in Mount Obsidian" ], "related_steps": [ "capture-jetragon:001" ] },
    { "id": "capture-jetragon:checkpoint-engage", "summary": "Jetragon weakened", "benefits": [ "Capture threshold reached" ], "related_steps": [ "capture-jetragon:003" ] }
  ],
  "supporting_routes": { "recommended": [ "tech-grappling-gun", "mount-nitewing-saddle" ], "optional": [ "tower-rayne-syndicate" ] },
  "failure_recovery": {
    "normal": "If you faint, retrieve your bag immediately; resupply on cooling consumables before retrying.",
    "hardcore": "Abort if armor durability dips below 40 % or if multiple lava golems join the fight; survival takes priority."
  },
  "steps": [
    {
      "step_id": "capture-jetragon:001",
      "type": "prepare",
      "summary": "Prepare for battle",
      "detail": "Craft heat‑resistant armor and weapons such as rocket launchers.  Recruit high‑level Ice or Dragon Pals.  Bring Ultra Pal Spheres and plenty of healing items.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": { "tactics": "Ensure all gear is upgraded and carry backup mounts", "safety_buffer_items": [ { "item_id": "paldium-fragment", "qty": 10 } ] },
        "coop": { "role_splits": [ { "role": "tank", "tasks": "Take aggro and soak damage" }, { "role": "damage", "tasks": "Deal sustained damage" }, { "role": "support", "tasks": "Heal and provide buffs" } ], "loot_rules": "The player who throws the final sphere keeps Jetragon" }
      },
      "recommended_loadout": { "gear": [ "grappling-gun" ], "pals": [ "nitewing" ], "consumables": [] },
      "xp_award_estimate": { "min": 300, "max": 400 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-bosses", "pcgamer-grappling-gun" ]
    },
    {
      "step_id": "capture-jetragon:002",
      "type": "travel",
      "summary": "Reach Mount Obsidian",
      "detail": "Fly to Mount Obsidian in the volcanic region.  Use your Nitewing or Eikthyrdeer to reach the foot of the volcano without taking lava damage.",
      "targets": [],
      "locations": [ { "region_id": "mount-obsidian", "coords": [ 850, -500 ], "time": "any", "weather": "any" } ],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [ "eikthyrdeer-saddle", "nitewing-saddle" ], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 80 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-jetragon" ]
    },
    {
      "step_id": "capture-jetragon:003",
      "type": "fight",
      "summary": "Weaken Jetragon",
      "detail": "Engage Jetragon cautiously.  Use Ice or Dragon attacks to exploit its weaknesses.  Dodge its fire breath and meteor strikes.  Reduce its HP to the capture threshold.",
      "targets": [ { "kind": "pal", "id": "jetragon", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": { "tactics": "Maintain maximum distance and use hit‑and‑run tactics", "safety_buffer_items": [ { "item_id": "ancient-technology-point", "qty": 1 } ] },
        "coop": { "role_splits": [ { "role": "kiter", "tasks": "Lead Jetragon around obstacles" }, { "role": "sniper", "tasks": "Deal high damage with rockets" }, { "role": "catcher", "tasks": "Prepare Pal Spheres" } ], "loot_rules": "Discuss who will claim the capture" }
      },
      "recommended_loadout": { "gear": [ "grappling-gun" ], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 2000, "max": 3000 },
      "outputs": { "items": [], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-jetragon" ]
    },
    {
      "step_id": "capture-jetragon:004",
      "type": "capture",
      "summary": "Capture Jetragon",
      "detail": "When Jetragon’s health is low, throw Ultra Pal Spheres until you succeed.  It may take several attempts.  Once captured, Jetragon becomes a powerful flying mount with unmatched speed and combat abilities.",
      "targets": [ { "kind": "pal", "id": "jetragon", "qty": 1 } ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [ { "item_id": "pal-sphere", "qty": 5 } ] },
      "xp_award_estimate": { "min": 200, "max": 300 },
      "outputs": { "items": [], "pals": [ "jetragon" ], "unlocks": {} },
      "branching": [],
      "citations": [ "pcgamesn-jetragon" ]
    }
  ],
  "completion_criteria": [ { "type": "have-item", "item_id": "jetragon", "qty": 1 } ],
  "yields": { "levels_estimate": "+5 to +6", "key_unlocks": [ "pal-jetragon" ] },
  "metrics": {
    "xp_per_minute": { "solo": 45.0, "coop": 60.0 },
    "travel_distance_m": 3200,
    "consumable_cost": [ { "item_id": "ultra-pal-sphere", "qty": 6 }, { "item_id": "heat-resistant-armor", "qty": 1 }, { "item_id": "healing-potion", "qty": 8 } ]
  },
  "next_routes": []
}
```

Palmate estimates the player’s level by summing XP from completed steps,
adding bonuses and converting the total into a level using the XP table.
The following block describes the algorithm and provides an example.

```json
{
  "level_estimator": {
    "xp_thresholds_ref": "xp_thresholds",
    "per_step_xp_ranges": {
      "gather": { "min": 10, "max": 40 },
      "build": { "min": 30, "max": 50 },
      "craft": { "min": 50, "max": 80 },
      "capture": { "min": 60, "max": 200 },
      "farm": { "min": 150, "max": 300 },
      "unlock-tech": { "min": 10, "max": 20 },
      "travel": { "min": 5, "max": 15 },
      "fight": { "min": 100, "max": 500 },
      "explore": { "min": 30, "max": 70 }
    },
    "metric_usage": {
      "xp_per_minute_weight": 0.25,
      "travel_distance_weight": -0.1,
      "consumable_cost_weight": -0.05,
      "description": "Route-level metrics adjust projections: higher XP/min slightly boosts expected level gain, while long travel or expensive consumables reduce the effective XP value."
    },
    "estimation_method": "\n1. For each completed step, take the median of its XP estimate range (or the per‑step range if no estimate is provided).  Sum these medians to compute the base XP.\n2. Apply route-level adjustments using metrics: multiply xp_per_minute by the average of the route’s solo/coop time (in minutes) and the weight to reward efficient grinds, subtract travel_distance_m × travel_distance_weight ÷ 1000, and subtract consumable_cost totals × consumable_cost_weight.\n3. Add bonuses: +500 XP for each boss clear and +10 % for completing a route without deaths in Hardcore mode.  In Co‑Op, divide XP evenly among players.\n4. Convert the cumulative XP to a player level by finding the highest level where cumulative_xp ≤ total XP in the xp_thresholds array.\n5. Compute a confidence score between 0 and 1 equal to the fraction of steps with explicit XP estimates plus 0.1 if route metrics were provided.  Cap the score at 1.0.\n",
    "example": "Suppose a player completed the Starter Base route in solo normal mode.  The median XP for its steps sums to ~370 XP.  No bonuses apply.  According to the XP table, 370 XP corresponds to level 5.  Because all steps have explicit XP estimates, the confidence score is 1.0."
  }
}
```

## Recommendation Logic

This block defines how the Palmate home page recommends next routes based on
context.  Routes with unmet prerequisites are excluded.  Scoring
prioritises level fit, unlock value and resource needs.  Explanations
help players understand why a route is suggested.

```json
{
  "recommender": {
    "input_context_shape": {
      "declared_level": "int|null",
      "estimated_level": "int",
      "mode": { "hardcore": "bool", "coop": "bool" },
      "completed_routes": [ "route-id" ],
      "goals": [ "tag" ],
      "available_time_minutes": "int|null",
      "resource_gaps": [ { "item_id": "string", "qty": "int" } ]
    },
    "scoring_signals": {
      "prerequisites_met": 5,
      "level_fit": 3,
      "unlock_value": 4,
      "time_to_power_ratio": 2,
      "geographic_proximity": 1,
      "risk_vs_mode": 2,
      "coop_synergy": 1,
      "novelty": 1,
      "progression_role": 2,
      "tag_alignment": 2,
      "metric_efficiency": 2,
      "resource_relief": 3,
      "dynamic_alignment": 3
    },
    "metric_normalization": {
      "xp_per_minute": { "target": 15, "score_per_sigma": 1.5 },
      "travel_distance_m": { "target": 1200, "score_per_sigma": -1.0 },
      "consumable_cost": { "target": 5, "score_per_sigma": -0.5 }
    },
    "decision_flow": [
      "Filter out routes with unmet prerequisites or missing adaptive_guidance entries for requested goals",
      "Boost support routes when resource_gaps overlap with their outputs",
      "Prefer routes whose metrics meet or exceed normalization targets when available_time_minutes is low",
      "Award dynamic_alignment when player context satisfies a route’s adaptive_guidance.dynamic_rules"
    ],
    "tie_breakers": [ "lowest_consumable_cost", "shortest_time", "highest_unlock_value", "alphabetical" ],
    "explanation_templates": {
      "prerequisites_met": "You meet all prerequisites for this route.",
      "level_fit": "Your estimated level of {level} fits the recommended range ({min}-{max}).",
      "unlock_value": "Completing this route unlocks {unlocks}.",
      "resource_need": "You need {item} for upcoming routes.",
      "progression_role": "This is a {role} route that keeps your progression on track.",
      "metric_efficiency": "Its projected {xp_per_minute} XP/min and short travel time make it efficient right now.",
      "adaptive_guidance": "Adaptive guidance suggests {recommendation} based on your situation.",
      "dynamic_alignment": "Dynamic rule triggered: {rule_adjustment}."
    },
    "fallbacks": {
      "under_leveled": "Recommend resource loops and easier capture routes until you reach an appropriate level.",
      "over_leveled": "Skip ahead to mount or boss routes that still have unmet prerequisites.",
      "no_time": "Surface the highest XP-per-minute routes that finish within the available time budget.",
      "resource_crunch": "Prioritise support routes whose outputs satisfy the most urgent resource gap."
    }
  }
}
```

## Source Registry

The source registry maps the short citation keys used throughout this file
to full references.  Include the title, URL and access date.  When
updating guides, refresh these entries with new dates and pages.

```json
{
  "sources": {
    "paldb-primitive-workbench": { "title": "Primitive Workbench – PalDB", "url": "https://paldb.cc/station/primitive-workbench", "access_date": "2025-09-30", "notes": "Shows that the Primitive Workbench requires 2 Wood to build【907636800064548†screenshot】." },
    "thegamer-foxparks-spawn": { "title": "Palworld: How To Find And Capture Foxparks", "url": "https://www.thegamer.com/palworld-foxparks-location-guide/", "access_date": "2025-09-30", "notes": "Provides spawn coordinates for Foxparks and notes they are kindling Pals【956200907149478†L146-L169】." },
    "namehero-xp-capture": { "title": "Palworld Leveling Guide", "url": "https://www.namehero.com/game-guides/palworld-leveling-guide/", "access_date": "2025-09-30", "notes": "Highlights that capturing Pals yields more XP than defeating them【116860197722081†L96-L128】." },
    "shockbyte-leather-sources": { "title": "Palworld: How To Get Leather", "url": "https://shockbyte.com/blog/how-to-get-leather-in-palworld", "access_date": "2025-09-30", "notes": "Lists Pals that drop Leather and notes the Sea Breeze Archipelago Church and Bridge of the Twin Knights as farming locations【840767909995613†L78-L100】【840767909995613†L106-L135】." },
    "shockbyte-leather-merchant": { "title": "Palworld: How To Get Leather", "url": "https://shockbyte.com/blog/how-to-get-leather-in-palworld", "access_date": "2025-09-30", "notes": "Notes that Wandering Merchants sell Leather for about 150 gold each【840767909995613†L78-L100】." },
    "gameclubz-foxparks-harness": { "title": "Palworld – How to Unlock and Use Foxparks Harness", "url": "https://gameclubz.com/palworld/foxparks-harness-guide", "access_date": "2025-09-30", "notes": "Provides the Foxparks Harness recipe (3 Leather, 5 Flame Organs, 5 Paldium Fragments) and explains unlocking at level 6 after catching Foxparks【353245298505537†L150-L180】." },
    "gameclubz-eikthyrdeer-saddle": { "title": "Palworld – Eikthyrdeer Saddle Guide", "url": "https://gameclubz.com/palworld/eikthyrdeer-saddle-guide", "access_date": "2025-09-30", "notes": "States that the Eikthyrdeer Saddle unlocks at level 12 with 2 tech points and lists required materials (5 Leather, 20 Fiber, 10 Ingots, 3 Horns, 15 Paldium Fragments)【963225160620124†L160-L167】." },
    "eikthyrdeer-drops": { "title": "Eikthyrdeer – Palworld Wiki", "url": "https://palworld.fandom.com/wiki/Eikthyrdeer", "access_date": "2025-09-30", "notes": "Lists Eikthyrdeer drops: 2 Venison, 2–3 Leather and 2 Horns at 100 % drop rate【142053078936299†L295-L311】." },
    "eikthyrdeer-partner-skill": { "title": "Eikthyrdeer – Palworld Wiki", "url": "https://palworld.fandom.com/wiki/Eikthyrdeer", "access_date": "2025-09-30", "notes": "Describes the partner skill ‘Guardian of the Forest’ – the Pal can be ridden, enables double jump and increases tree‑cutting efficiency【142053078936299†L123-L142】." },
    "paldb-foxparks-partner": { "title": "Foxparks – PalDB", "url": "https://paldb.cc/pal/foxparks", "access_date": "2025-09-30", "notes": "Mentions the partner skill ‘Huggy Fire’ which equips Foxparks as a flamethrower and its work suitability (Kindling Lv1)【513843636763139†L117-L170】." },
    "palwiki-direhowl-recipe": { "title": "Direhowl Saddled Harness – Palworld Wiki", "url": "https://palworld.fandom.com/wiki/Direhowl_Saddled_Harness", "access_date": "2025-09-30", "notes": "Provides the Direhowl harness recipe (10 Leather, 20 Wood, 15 Fiber, 10 Paldium Fragments) and states it unlocks at level 9 with 1 tech point【197143349627535†L151-L156】." },
    "palwiki-nitewing-saddle": { "title": "Nitewing Saddled Harness – Palworld Wiki", "url": "https://palworld.fandom.com/wiki/Nitewing_Saddle", "access_date": "2025-09-30", "notes": "Lists the Nitewing saddle recipe (20 Leather, 10 Cloth, 15 Ingots, 20 Fiber, 20 Paldium Fragments) and level requirements【524512399342633†L151-L156】." },
    "updatecrazy-patch-067": { "title": "Palworld Update v0.6.7 Patch Notes", "url": "https://updatecrazy.com/palworld-update-v0-6-7-patch-notes", "access_date": "2025-09-30", "notes": "Confirms game version 1.079.736 released on Sept 29 2025 and fixes relating to dungeon crashes【353708512100491†L31-L56】." },
    "goleap-region-levels": { "title": "Palworld Map Level Zones", "url": "https://www.gameleap.com/palworld-map-level-zones", "access_date": "2025-09-30", "notes": "Provides level ranges for each region (e.g. Windswept Hills 1–15, Sea Breeze Archipelago 1–10)【950757978743332†L131-L147】." },
    "gosunoob-vixy-breeding": { "title": "Palworld – Vixy Breeding Combinations", "url": "https://www.gosunoob.com/palworld/vixy-breeding/", "access_date": "2025-09-30", "notes": "Lists combos that produce Vixy and notes its work suitability and drops【506019502892519†screenshot】【761280216223901†screenshot】." }
    ,"pcgamesn-bosses": { "title": "All Palworld bosses in order and how to beat them", "url": "https://www.pcgamesn.com/palworld/bosses", "access_date": "2025-09-30", "notes": "Provides details on tower bosses including Zoe & Grizzbolt, coordinates (112, -434), challenge damage (30K), recommended ground Pals and tactics【825211382965329†L103-L118】; also lists Nitewing as an Alpha Pal at Ice Wind Island (level 18)【825211382965329†L294-L302】 and Jetragon at Mount Obsidian (level 50)【825211382965329†L337-L339】." }
    ,"pcgamer-grappling-gun": { "title": "Palworld grappling gun guide", "url": "https://www.pcgamer.com/palworld-grappling-gun-crafting/", "access_date": "2025-09-30", "notes": "Explains that the Grappling Gun unlocks at level 12 and costs 1 Ancient Technology Point; crafting requires 10 Paldium Fragments, 10 Ingots, 30 Fiber and 1 Ancient Civilization Part【312162085103617†L180-L205】." }
    ,"pcgamesn-jetragon": { "title": "All Palworld bosses in order and how to beat them – Jetragon entry", "url": "https://www.pcgamesn.com/palworld/bosses", "access_date": "2025-09-30", "notes": "States that Jetragon is a level 50 Legendary Celestial Dragon found at Mount Obsidian【825211382965329†L337-L339】." }
    ,"palwiki-humans": { "title": "Humans – Palworld Wiki", "url": "https://palworld.wiki.gg/wiki/Humans", "access_date": "2025-09-30", "notes": "Explains that non-leader humans can be captured with Pal Spheres, have lower catch rates needing higher-grade spheres, cannot use their weapons, and merchants stationed at bases provide permanent shop access despite only rank 1 work suitability.【529f5c†L67-L90】【94455f†L13-L18】" }
    ,"palwiki-small-settlement": { "title": "Small Settlement – Palworld Wiki", "url": "https://palworld.wiki.gg/wiki/Small_Settlement", "access_date": "2025-09-30", "notes": "Gives the Small Settlement coordinates (~75,-479) and lists the Pal Merchant and Wandering Merchant inhabitants available to capture.【165dd8†L71-L90】" }
    ,"palwiki-paldium": { "title": "Paldium Fragment – Palworld Wiki", "url": "https://palworld.fandom.com/wiki/Paldium_Fragment", "access_date": "2025-09-30", "notes": "Lists river, cliff and smelting sources for Paldium Fragments including respawn timers and conversion tips【palwiki-paldium†L42-L71】【palwiki-paldium†L86-L115】【palwiki-paldium†L118-L140】." }
  }
}
```
