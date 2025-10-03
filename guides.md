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
    ,{ "id": "tomato-seeds", "name": "Tomato Seeds", "type": "material", "rarity": "common", "stack": 999, "buy_price": 200, "sell_price": 20, "sources": [ { "type": "shop", "reference_id": "wandering-merchant" } ] }
    ,{ "id": "tomato", "name": "Tomato", "type": "consumable", "rarity": "common", "stack": 50, "buy_price": 150, "sell_price": 15, "sources": [ { "type": "farm", "reference_id": "tomato-plantation" }, { "type": "shop", "reference_id": "wandering-merchant" } ] }
    ,{ "id": "lettuce-seeds", "name": "Lettuce Seeds", "type": "material", "rarity": "common", "stack": 999, "buy_price": 200, "sell_price": 20, "sources": [ { "type": "shop", "reference_id": "wandering-merchant" } ] }
    ,{ "id": "lettuce", "name": "Lettuce", "type": "consumable", "rarity": "common", "stack": 50, "buy_price": 150, "sell_price": 15, "sources": [ { "type": "farm", "reference_id": "lettuce-plantation" }, { "type": "shop", "reference_id": "wandering-merchant" } ] }
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
    },
    {
      "id": "tomato-plantation",
      "name": "Tomato Plantation",
      "requirements": [
        { "item_id": "tomato-seeds", "qty": 3 },
        { "item_id": "wood", "qty": 70 },
        { "item_id": "stone", "qty": 50 },
        { "item_id": "pal-fluids", "qty": 5 }
      ],
      "power_required": false,
      "pal_work_types_needed": ["planting", "watering", "gathering"],
      "station_tier": 21
    },
    {
      "id": "lettuce-plantation",
      "name": "Lettuce Plantation",
      "requirements": [
        { "item_id": "lettuce-seeds", "qty": 3 },
        { "item_id": "wood", "qty": 100 },
        { "item_id": "stone", "qty": 70 },
        { "item_id": "pal-fluids", "qty": 10 }
      ],
      "power_required": false,
      "pal_work_types_needed": ["planting", "watering", "gathering"],
      "station_tier": 25
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
    },
    {
      "id": "sakurajima-island",
      "name": "Sakurajima Island",
      "level_hint_min": 50,
      "level_hint_max": 60,
      "climate": "volcanic archipelago",
      "hazards": "constant night, elite syndicate patrols",
      "coordinates_bbox": [ -700, 0, -400, 400 ],
      "fast_travel_nodes": [ "moonflower-tower-entrance" ]
    },
    {
      "id": "feybreak",
      "name": "Feybreak Expanse",
      "level_hint_min": 55,
      "level_hint_max": 60,
      "climate": "cursed wasteland",
      "hazards": "poison mists, relentless raids",
      "coordinates_bbox": [ -1500, -1900, -1100, -1400 ],
      "fast_travel_nodes": [ "feybreak-tower-entrance" ]
    },
    {
      "id": "wildlife-sanctuary-1",
      "name": "No. 1 Wildlife Sanctuary",
      "level_hint_min": 20,
      "level_hint_max": 25,
      "climate": "island sanctuary",
      "hazards": "Trespassing triggers PIDF patrols",
      "coordinates_bbox": [ 90, -735, 90, -735 ],
      "fast_travel_nodes": []
    },
    {
      "id": "wildlife-sanctuary-2",
      "name": "No. 2 Wildlife Sanctuary",
      "level_hint_min": 50,
      "level_hint_max": 50,
      "climate": "island sanctuary",
      "hazards": "Trespassing triggers elite PIDF patrols",
      "coordinates_bbox": [ -675, -113, -675, -113 ],
      "fast_travel_nodes": []
    },
    {
      "id": "wildlife-sanctuary-3",
      "name": "No. 3 Wildlife Sanctuary",
      "level_hint_min": 50,
      "level_hint_max": 50,
      "climate": "island sanctuary",
      "hazards": "Trespassing triggers elite PIDF patrols",
      "coordinates_bbox": [ 669, 640, 669, 640 ],
      "fast_travel_nodes": []
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
    },
    {
      "id": "free-pal-alliance-tower",
      "name": "Free Pal Alliance Tower (Lily & Lyleen)",
      "type": "tower",
      "region_id": "verdant-brook",
      "coords": [ 181, 29 ],
      "recommended_level": 25,
      "mechanics": "Grass boss that summons roots; fire attacks melt Lyleen quickly.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Weekly respawn timer"
    },
    {
      "id": "eternal-pyre-tower",
      "name": "Eternal Pyre Tower (Axel & Orserk)",
      "type": "tower",
      "region_id": "mount-obsidian",
      "coords": [ -587, -517 ],
      "recommended_level": 40,
      "mechanics": "Fire boss with lava hazards; ice damage staggers Orserk.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Weekly respawn timer"
    },
    {
      "id": "pidf-tower",
      "name": "PIDF Tower (Marcus & Faleris)",
      "type": "tower",
      "region_id": "twilight-dunes",
      "coords": [ 556, 336 ],
      "recommended_level": 45,
      "mechanics": "Fire/Dragon boss with explosives; water suppression keeps Faleris controlled.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Weekly respawn timer"
    },
    {
      "id": "pal-research-tower",
      "name": "PAL Research Tower (Victor & Shadowbeak)",
      "type": "tower",
      "region_id": "ice-wind-island",
      "coords": [ -146, 448 ],
      "recommended_level": 50,
      "mechanics": "Dark/Ice boss supported by drones; dragon damage breaks shields.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Weekly respawn timer"
    },
    {
      "id": "moonflower-tower",
      "name": "Moonflower Tower (Saya & Selyne)",
      "type": "tower",
      "region_id": "sakurajima-island",
      "coords": [ -597, 203 ],
      "recommended_level": 55,
      "mechanics": "Dark phoenix boss fought at night; dragon bursts and ranged DPS shine.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Weekly respawn timer"
    },
    {
      "id": "feybreak-tower",
      "name": "Feybreak Tower (Bjorn & Bastigor)",
      "type": "tower",
      "region_id": "feybreak",
      "coords": [ -1294, -1669 ],
      "recommended_level": 60,
      "mechanics": "Dragon/Ice boss with toxic fields; fire payloads end the fight quickly.",
      "rewards": [ { "item_id": "ancient-technology-points", "qty": 5 } ],
      "repeatable": false,
      "reset_rule": "Weekly respawn timer"
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
    "tags": [
      "string",
      "..."
    ],
    "progression_role": "core|optional|support",
    "recommended_level": {
      "min": "int",
      "max": "int"
    },
    "modes": {
      "normal": "boolean",
      "hardcore": "boolean",
      "solo": "boolean",
      "coop": "boolean"
    },
    "prerequisites": {
      "routes": [
        "route-id",
        "..."
      ],
      "tech": [
        "tech-id",
        "..."
      ],
      "items": [
        {
          "item_id": "...",
          "qty": "int"
        }
      ],
      "pals": [
        "pal-id",
        "..."
      ]
    },
    "objectives": [
      "high-level objective sentences"
    ],
    "estimated_time_minutes": {
      "solo": "int",
      "coop": "int"
    },
    "estimated_xp_gain": {
      "min": "int",
      "max": "int"
    },
    "risk_profile": "low|medium|high",
    "failure_penalties": {
      "normal": "text",
      "hardcore": "text"
    },
    "adaptive_guidance": {
      "underleveled": "text",
      "overleveled": "text",
      "resource_shortages": [
        {
          "item_id": "...",
          "solution": "include_subroute or explain alternative"
        }
      ],
      "time_limited": "text",
      "dynamic_rules": [
        {
          "signal": "level_gap|time_budget|resource_gap|mode_state|geographic_context",
          "condition": "human-readable expression describing when to trigger the adjustment",
          "adjustment": "specific instruction to modify the route",
          "priority": "int (1=highest urgency)",
          "mode_scope": [
            "normal",
            "hardcore",
            "solo",
            "coop"
          ],
          "related_steps": [
            "route-id:001"
          ],
          "follow_up_routes": [
            "route-id"
          ]
        }
      ]
    },
    "checkpoints": [
      {
        "id": "route-id:checkpoint-1",
        "summary": "text",
        "benefits": [
          "string"
        ],
        "related_steps": [
          "route-id:001"
        ]
      }
    ],
    "supporting_routes": {
      "recommended": [
        "route-id"
      ],
      "optional": [
        "route-id"
      ]
    },
    "failure_recovery": {
      "normal": "text",
      "hardcore": "text"
    },
    "steps": [
      {
        "step_id": "route-id:001",
        "type": "travel|gather|farm|capture|fight|craft|build|unlock-tech|breed|deliver|talk|explore|prepare|quest",
        "summary": "short sentence",
        "detail": "clear, actionable instruction",
        "targets": [
          {
            "kind": "item|pal|boss|station|tech",
            "id": "...",
            "qty": "int?"
          }
        ],
        "locations": [
          {
            "region_id": "...",
            "coords": [
              "x",
              "y"
            ],
            "time": "day|night|any",
            "weather": "any|condition"
          }
        ],
        "mode_adjustments": {
          "hardcore": {
            "tactics": "text",
            "safety_buffer_items": [
              {
                "item_id": "...",
                "qty": "int"
              }
            ]
          },
          "coop": {
            "role_splits": [
              {
                "role": "puller",
                "tasks": "..."
              },
              {
                "role": "farmer",
                "tasks": "..."
              }
            ],
            "loot_rules": "text"
          }
        },
        "recommended_loadout": {
          "gear": [
            "item-id"
          ],
          "pals": [
            "pal-id"
          ],
          "consumables": [
            {
              "item_id": "...",
              "qty": "int"
            }
          ]
        },
        "xp_award_estimate": {
          "min": "int",
          "max": "int"
        },
        "outputs": {
          "items": [
            {
              "item_id": "...",
              "qty": "int"
            }
          ],
          "pals": [
            "pal-id",
            "..."
          ],
          "unlocks": {
            "tech": [
              "tech-id"
            ],
            "stations": [
              "station-id"
            ]
          }
        },
        "branching": [
          {
            "condition": "player lacks item/leather >= N",
            "action": "jump_to_step_id or include_subroute",
            "subroute_ref": "route-id"
          }
        ],
        "citations": [
          "short-source-key-1",
          "short-source-key-2"
        ]
      }
    ],
    "completion_criteria": [
      {
        "type": "have-item",
        "item_id": "...",
        "qty": "int"
      },
      {
        "type": "tech-unlocked",
        "tech_id": "..."
      },
      {
        "type": "boss-cleared",
        "boss_id": "..."
      },
      {
        "type": "quest-chain",
        "quest_id": "..."
      }
    ],
    "yields": {
      "levels_estimate": "+X to +Y",
      "key_unlocks": [
        "tech-id",
        "..."
      ]
    },
    "metrics": {
      "progress_segments": "int",
      "boss_targets": "int",
      "quest_nodes": "int"
    },
    "next_routes": [
      {
        "route_id": "...",
        "reason": "what unlocks it"
      }
    ]
  }
}
```

## Route Library

The following routes cover early game progression, resource farming and
mount acquisition.  Each route conforms to the schema above and
references the ontologies defined earlier.  Citations back up non‑obvious
facts (spawn locations, recipe costs, drop rates, etc.).

## Guide Catalogue Integration

To support intent-driven prompting, every guide described in
`palworld_complete_guide.md` has been normalised into a machine-readable
catalogue.  The parsed dataset contains **201** guide entries and lives at
`data/guide_catalog.json`.  Each entry tracks its canonical title,
category, trigger phrases, keyword set and numbered instructions (with
citations preserved where they existed in the source material).

```json
{
  "guide_catalog": {
    "path": "data/guide_catalog.json",
    "guide_count": 201,
    "fields": [
      "id",
      "title",
      "source_heading",
      "category",
      "category_group",
      "trigger",
      "keywords",
      "steps"
    ],
    "step_fields": ["order", "instruction", "citations"],
    "source": "palworld_complete_guide.md"
  }
}
```

Clients can load the JSON directly to surface a complete list of
available guides, map player utterances to triggers/keywords, and feed
the numbered instructions into adaptive routing logic.

### Route: Starter Base and Capture

This introductory route teaches players how to gather resources, craft
basic stations, create Pal Spheres and capture their first companions.

```json
{
  "route_id": "starter-base-capture",
  "title": "Starter Base and Capture",
  "category": "progression",
  "tags": [
    "early-game",
    "base-building",
    "capture",
    "resource-gathering"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 1,
    "max": 5
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Gather basic resources and build a Primitive Workbench",
    "Craft Pal Spheres and capture three different Pals",
    "Establish a small shelter"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 20
  },
  "estimated_xp_gain": {
    "min": 300,
    "max": 600
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Loss of gathered materials",
    "hardcore": "Death results in character deletion"
  },
  "adaptive_guidance": {
    "underleveled": "Loop step :001 twice and capture Lamball first; their low aggression keeps risk minimal while still granting capture XP.",
    "overleveled": "If you arrive above level 6, prioritize step :003 and transition directly into harness crafting to avoid redundant farming.",
    "resource_shortages": [
      {
        "item_id": "paldium-fragment",
        "solution": "Trigger the resource-paldium subroute from step :003 or mine blue ore veins along the riverbank."
      },
      {
        "item_id": "fiber",
        "solution": "Clear Windswept Hills bushes after step :001; each bush yields 2-3 Fiber quickly."
      }
    ],
    "time_limited": "Complete steps :001 through :003 only; capture a single Lamball to unlock base chores and return later for the full roster.",
    "dynamic_rules": [
      {
        "signal": "level_gap:over",
        "condition": "player.estimated_level >= recommended_level.max + 2",
        "adjustment": "Treat step :001 as maintenance only, finish :003 to restock spheres, then pivot into mount-foxparks-harness without repeating :004.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "starter-base-capture:003"
        ],
        "follow_up_routes": [
          "mount-foxparks-harness"
        ]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 20",
        "adjustment": "Execute steps :001 through :003 only and bank captured materials; postpone the third capture in :004 until more time is available.",
        "priority": 3,
        "mode_scope": [
          "solo",
          "coop"
        ],
        "related_steps": [
          "starter-base-capture:001",
          "starter-base-capture:002",
          "starter-base-capture:003"
        ]
      },
      {
        "signal": "resource_gap:paldium-fragment",
        "condition": "resource_gaps contains paldium-fragment >= 5",
        "adjustment": "Loop the river rocks north of the spawn before step :003 or trigger the resource-paldium subroute immediately.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "starter-base-capture:003"
        ],
        "follow_up_routes": [
          "resource-paldium"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "starter-base-capture:checkpoint-setup",
      "summary": "Primitive Workbench placed",
      "benefits": [
        "Workbench crafting unlocked",
        "Establishes respawn anchor"
      ],
      "related_steps": [
        "starter-base-capture:002"
      ]
    },
    {
      "id": "starter-base-capture:checkpoint-team",
      "summary": "Three work-ready Pals captured",
      "benefits": [
        "Unlocks base chores",
        "Meets early tech prerequisites"
      ],
      "related_steps": [
        "starter-base-capture:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-paldium"
    ],
    "optional": [
      "resource-leather-early"
    ]
  },
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
      "targets": [
        {
          "kind": "item",
          "id": "wood",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "stone",
          "qty": 15
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Avoid engaging hostile Pals while gathering; keep your HP above 50 % and carry extra berries.",
          "safety_buffer_items": [
            {
              "item_id": "wood",
              "qty": 10
            },
            {
              "item_id": "stone",
              "qty": 10
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "gatherer",
              "tasks": "Chop trees and mine stone"
            },
            {
              "role": "scout",
              "tasks": "Watch for aggressive Pals and keep area clear"
            }
          ],
          "loot_rules": "Share resources evenly"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 40
      },
      "outputs": {
        "items": [
          {
            "item_id": "wood",
            "qty": 20
          },
          {
            "item_id": "stone",
            "qty": 15
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "starter-base-capture:002",
      "type": "build",
      "summary": "Construct a Primitive Workbench",
      "detail": "Open the construction menu and build a Primitive Workbench using 2 Wood【907636800064548†screenshot】.  Place it near your gathering area.",
      "targets": [
        {
          "kind": "station",
          "id": "primitive-workbench"
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 50
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "stations": [
            "primitive-workbench"
          ]
        }
      },
      "branching": [],
      "citations": [
        "paldb-primitive-workbench"
      ]
    },
    {
      "step_id": "starter-base-capture:003",
      "type": "craft",
      "summary": "Craft Pal Spheres",
      "detail": "Use the Primitive Workbench to craft at least five Pal Spheres.  Each sphere requires Paldium Fragments (gathered from blue ore) and a small amount of Wood and Stone.  If you lack fragments, mine Paldium nodes along the river.",
      "targets": [
        {
          "kind": "item",
          "id": "pal-sphere",
          "qty": 5
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks paldium-fragment >= 5",
          "action": "include_subroute",
          "subroute_ref": "resource-paldium"
        }
      ],
      "citations": []
    },
    {
      "step_id": "starter-base-capture:004",
      "type": "capture",
      "summary": "Capture three early Pals",
      "detail": "Throw Pal Spheres at Lamball, Cattiva, Chikipi, Lifmunk or Foxparks in the Windswept Hills【956200907149478†L146-L169】.  Approach from behind to improve your catch rate.  Capturing new species grants more XP than defeating them【116860197722081†L96-L128】.",
      "targets": [
        {
          "kind": "pal",
          "id": "lamball",
          "qty": 1
        },
        {
          "kind": "pal",
          "id": "cattiva",
          "qty": 1
        },
        {
          "kind": "pal",
          "id": "foxparks",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            189,
            -478
          ],
          "time": "day",
          "weather": "any"
        },
        {
          "region_id": "windswept-hills",
          "coords": [
            144,
            -583
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Avoid aggroing the nearby Mammorest boss while hunting【956200907149478†L146-L169】.  Always keep a healing item ready.",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "puller",
              "tasks": "Aggro the Pal and kite it"
            },
            {
              "role": "catcher",
              "tasks": "Throw Pal Spheres from behind"
            }
          ],
          "loot_rules": "Each player keeps one captured Pal"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ]
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 200
      },
      "outputs": {
        "items": [],
        "pals": [
          "lamball",
          "cattiva",
          "foxparks"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "thegamer-foxparks-spawn",
        "namehero-xp-capture"
      ]
    },
    {
      "step_id": "starter-base-capture:005",
      "type": "build",
      "summary": "Construct a shelter",
      "detail": "Gather extra Wood and build a basic shelter to protect yourself and your newly captured Pals.  A roof prevents rain damage and increases comfort.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 50
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "starter-base-capture:006",
      "type": "quest",
      "summary": "Register your starter base with the Investigator board",
      "detail": "Visit the Investigator board in the Small Settlement to hand in the \"First Settlement\" request. This unlocks the story tracker and marks your base as recognised.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 260
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "primitive-workbench",
      "qty": 1
    },
    {
      "type": "have-item",
      "item_id": "pal-sphere",
      "qty": 5
    }
  ],
  "yields": {
    "levels_estimate": "+1 to +2",
    "key_unlocks": [
      "tech-primitive-workbench"
    ]
  },
  "metrics": {
    "progress_segments": 6,
    "boss_targets": 0,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "resource-leather-early",
      "reason": "Gather materials for future gear"
    },
    {
      "route_id": "mount-foxparks-harness",
      "reason": "You captured Foxparks and can now craft its harness"
    }
  ]
}
```

### Route: Main Story Progression: Palbox to Feybreak

This long-form route condenses the updated mission walkthrough from `Newguides.md`, guiding players from the opening base setup through every syndicate tower to the Feybreak finale.  It assumes familiarity with the starter capture loop and layers Hardcore/Co-Op adjustments onto each milestone.

```json
{
  "route_id": "quest-main-story-early",
  "title": "Main Story Progression: Palbox to Feybreak",
  "category": "progression",
  "tags": [
    "main-story",
    "missions",
    "tower",
    "completion"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 1,
    "max": 60
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Finish the tutorial missions and establish a resilient starter base",
    "Hunt Alpha bosses and clear every tower from Zoe through Bjorn",
    "Maintain food, gear and stat growth to survive Hardcore scaling"
  ],
  "estimated_time_minutes": {
    "solo": 1080,
    "coop": 840
  },
  "estimated_xp_gain": {
    "min": 15000,
    "max": 260000
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Mission resets can cost consumables and travel time.",
    "hardcore": "Deaths delete characters; abort tower runs before wipes."
  },
  "adaptive_guidance": {
    "underleveled": "Prioritise capture XP loops between steps :006 and :009 before attempting tower bosses.",
    "overleveled": "Skip optional capture padding and sprint to tower encounters; convert extra mats into ammo and medkits.",
    "resource_shortages": [
      {
        "item_id": "paldium-fragment",
        "solution": "Farm riverside ore after step :007 or trigger resource-paldium subroute."
      },
      {
        "item_id": "fiber",
        "solution": "Clear Windswept Hills bushes at dusk or assign Lamballs to gathering posts."
      }
    ],
    "time_limited": "Complete checkpoints one at a time; wrap after step :010 if you only have a short session.",
    "dynamic_rules": [
      {
        "signal": "mode_state",
        "condition": "hardcore and player.hp_potions < 5",
        "adjustment": "Delay tower attempts and loop crafting of Large Recovery Meds before engaging bosses.",
        "priority": 1,
        "mode_scope": [
          "hardcore"
        ],
        "related_steps": [
          "quest-main-story-early:011",
          "quest-main-story-early:012",
          "quest-main-story-early:013",
          "quest-main-story-early:019"
        ],
        "follow_up_routes": [
          "tech-grappling-gun"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "quest-main-story-early:tutorial",
      "summary": "Tutorial missions complete and base automation online",
      "benefits": [
        "Unlocks base chores",
        "Opens access to gliding and shields"
      ],
      "related_steps": [
        "quest-main-story-early:001",
        "quest-main-story-early:006"
      ]
    },
    {
      "id": "quest-main-story-early:alpha-chillet",
      "summary": "Alpha Chillet defeated or captured",
      "benefits": [
        "Large EXP spike",
        "Ancient parts for advanced tech"
      ],
      "related_steps": [
        "quest-main-story-early:010"
      ]
    },
    {
      "id": "quest-main-story-early:all-towers",
      "summary": "All syndicate towers cleared including Feybreak",
      "benefits": [
        "Ancient Technology Point income",
        "Unlocks Investigator finale"
      ],
      "related_steps": [
        "quest-main-story-early:013",
        "quest-main-story-early:019"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-paldium",
      "mount-direhowl-harness",
      "mount-nitewing-saddle"
    ],
    "optional": [
      "mount-eikthyrdeer-saddle",
      "tower-rayne-syndicate"
    ]
  },
  "failure_recovery": {
    "normal": "Use fast-travel statues to recover lost gear and restock before reattempting objectives.",
    "hardcore": "Retreat via glider or mount when HP drops below 40%; preserve character by abandoning failed tower runs early."
  },
  "steps": [
    {
      "step_id": "quest-main-story-early:001",
      "type": "build",
      "summary": "Establish the first Palbox base",
      "detail": "Select a flat Windswept Hills clearing, place the Palbox and mark the base boundary so chores unlock immediately.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            80,
            -420
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Scout the area first to avoid syndicate raids during setup.",
          "safety_buffer_items": [
            {
              "item_id": "wood",
              "qty": 10
            },
            {
              "item_id": "stone",
              "qty": 10
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place Palbox and essential stations"
            },
            {
              "role": "lookout",
              "tasks": "Keep mobs away while base radius activates"
            }
          ],
          "loot_rules": "Shared base unlock"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:002",
      "type": "quest",
      "summary": "Assign a Pal to base work",
      "detail": "Open the Palbox management screen and deploy your first worker Pal to automate gathering and crafting jobs.",
      "targets": [
        {
          "kind": "pal",
          "id": "lamball",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            80,
            -420
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "manager",
              "tasks": "Handle Pal assignments"
            },
            {
              "role": "scout",
              "tasks": "Capture extra workers if needed"
            }
          ],
          "loot_rules": "Share early captures"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:003",
      "type": "gather",
      "summary": "Secure early food stores",
      "detail": "Harvest berry bushes and cook simple meals so everyone can eat to clear the hunger tutorial objective.",
      "targets": [
        {
          "kind": "item",
          "id": "fiber",
          "qty": 5
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            60,
            -400
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Keep at least two cooked meals on the hotbar to offset faster hunger drain.",
          "safety_buffer_items": [
            {
              "item_id": "fiber",
              "qty": 10
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:004",
      "type": "craft",
      "summary": "Prepare protective clothing",
      "detail": "Unlock basic armor and craft traveler clothes using fiber and leather to survive incoming raids and cold nights.",
      "targets": [
        {
          "kind": "item",
          "id": "fiber",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "leather",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            85,
            -430
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Craft a spare armor set and stash it before traveling at night.",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 5
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 30
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:005",
      "type": "prepare",
      "summary": "Allocate stat points",
      "detail": "Level up through early chores and invest stat points into health, stamina and weight to unlock the Enhance Stats mission.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Prioritise HP and stamina to reduce one-shot risk during raids."
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 5,
        "max": 5
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:006",
      "type": "capture",
      "summary": "Capture five Lamballs",
      "detail": "Hunt the docile Lamballs near spawn, weaken them and throw Pal Spheres until five are secured for wool and chores.",
      "targets": [
        {
          "kind": "pal",
          "id": "lamball",
          "qty": 5
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            120,
            -360
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "trapper",
              "tasks": "Weaken Lamballs"
            },
            {
              "role": "catcher",
              "tasks": "Throw spheres at low HP"
            }
          ],
          "loot_rules": "Alternate catches"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 35,
        "max": 35
      },
      "outputs": {
        "items": [
          {
            "item_id": "fiber",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:007",
      "type": "gather",
      "summary": "Mine Paldium and craft a shield",
      "detail": "Farm glowing blue ore by rivers, craft the Paldium Shield at a workbench and equip it for incoming fights.",
      "targets": [
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "wood",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            140,
            -390
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Craft extra shields to replace durability loss mid-run.",
          "safety_buffer_items": [
            {
              "item_id": "paldium-fragment",
              "qty": 10
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 50
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:008",
      "type": "craft",
      "summary": "Unlock gliding for mobility",
      "detail": "Spend a tech point on the Glider blueprint, craft it and practice takeoffs to enable safer travel and escapes.",
      "targets": [
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "fiber",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            90,
            -440
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "crafter",
              "tasks": "Assemble glider"
            },
            {
              "role": "tester",
              "tasks": "Scout glide paths"
            }
          ],
          "loot_rules": "Each player crafts their own"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 100
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:009",
      "type": "capture",
      "summary": "Expand the Palpedia to thirty species",
      "detail": "Tour nearby biomes and capture unique species until the roster hits thirty, diversifying work skills and XP gains.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            50,
            -380
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "sea-breeze-archipelago",
          "coords": [
            -320,
            -420
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "scout",
              "tasks": "Locate unique species"
            },
            {
              "role": "catcher",
              "tasks": "Secure captures"
            }
          ],
          "loot_rules": "Assign captures based on needed work skills"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 400,
        "max": 600
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:010",
      "type": "fight",
      "summary": "Defeat the Alpha Chillet",
      "detail": "Travel to the Steppe and battle the Alpha Chillet known as Dancer on the Steppe, leveraging fire damage for a quick kill or capture.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            174,
            -419
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Bring a fire Pal to stagger the Alpha quickly and avoid extended melee trades."
        },
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Hold aggro"
            },
            {
              "role": "breaker",
              "tasks": "Apply fire damage"
            }
          ],
          "loot_rules": "All players tag for drops"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 500,
        "max": 500
      },
      "outputs": {
        "items": [
          {
            "item_id": "fiber",
            "qty": 20
          },
          {
            "item_id": "paldium-fragment",
            "qty": 20
          },
          {
            "item_id": "leather",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:011",
      "type": "craft",
      "summary": "Upgrade cooking and ration planning",
      "detail": "Build a Cooking Pot, prepare portable meals and stock lunchboxes so hunger never interrupts long expeditions.",
      "targets": [
        {
          "kind": "item",
          "id": "ingot",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "wood",
          "qty": 15
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            82,
            -412
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Keep emergency bentos ready to counter increased hunger drain.",
          "safety_buffer_items": [
            {
              "item_id": "ingot",
              "qty": 5
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 150
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:012",
      "type": "fight",
      "summary": "Clear the Rayne Syndicate Tower",
      "detail": "Approach Zoe & Grizzbolt, counter with ground damage and finish within the time limit to secure the first tower clear.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            113,
            -431
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry shock resist potions and stay behind pillars to avoid lethal bursts."
        },
        "coop": {
          "role_splits": [
            {
              "role": "kiter",
              "tasks": "Hold Zoe"
            },
            {
              "role": "breaker",
              "tasks": "Focus Grizzbolt"
            }
          ],
          "loot_rules": "Ensure everyone tags the boss"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 2000,
        "max": 2200
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:013",
      "type": "fight",
      "summary": "Defeat Lily & Lyleen at Free Pal Alliance Tower",
      "detail": "Travel to the snowy Free Pal Alliance tower and melt Lyleen with fire Pals while dodging Lily\u2019s ranged shots.",
      "targets": [],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            181,
            29
          ],
          "time": "any",
          "weather": "snow"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use heat-resistant armor and rotate aggro to survive extended fights."
        },
        "coop": {
          "role_splits": [
            {
              "role": "burn",
              "tasks": "Maintain fire DoTs on Lyleen"
            },
            {
              "role": "suppression",
              "tasks": "Keep Lily busy"
            }
          ],
          "loot_rules": "Split cosmetics if they drop"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 2600,
        "max": 2800
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:014",
      "type": "fight",
      "summary": "Overcome Axel & Orserk at Eternal Pyre Tower",
      "detail": "Scale Mount Obsidian, exploit Orserk\u2019s weakness to ice and manage Axel\u2019s melee assaults to take the volcanic tower.",
      "targets": [],
      "locations": [
        {
          "region_id": "mount-obsidian",
          "coords": [
            -587,
            -517
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shields and maintain chill effects to suppress Orserk."
        },
        "coop": {
          "role_splits": [
            {
              "role": "kiter",
              "tasks": "Lead Axel away"
            },
            {
              "role": "breaker",
              "tasks": "Burst Orserk with ice"
            }
          ],
          "loot_rules": "Share heat cores"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 3200,
        "max": 3400
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:015",
      "type": "fight",
      "summary": "Break Marcus & Faleris at PIDF Tower",
      "detail": "Storm the desert tower, drench Faleris with water attacks and outmaneuver Marcus\u2019s explosives for the fourth clear.",
      "targets": [],
      "locations": [
        {
          "region_id": "twilight-dunes",
          "coords": [
            556,
            336
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry high-tier water ammo and dodge splash damage aggressively."
        },
        "coop": {
          "role_splits": [
            {
              "role": "hose",
              "tasks": "Keep Faleris soaked"
            },
            {
              "role": "sapper",
              "tasks": "Disable Marcus"
            }
          ],
          "loot_rules": "Distribute cosmetics"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 3600,
        "max": 3800
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:016",
      "type": "fight",
      "summary": "Topple Victor & Shadowbeak at PAL Research",
      "detail": "Climb the frozen tower, deploy dragon Pals against Shadowbeak and suppress Victor\u2019s gadgets to secure Ancient tech.",
      "targets": [],
      "locations": [
        {
          "region_id": "ice-wind-island",
          "coords": [
            -146,
            448
          ],
          "time": "any",
          "weather": "snow"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Cycle dragon shields and use cover to avoid laser volleys."
        },
        "coop": {
          "role_splits": [
            {
              "role": "dragon-handler",
              "tasks": "Focus Shadowbeak"
            },
            {
              "role": "suppression",
              "tasks": "Interrupt Victor"
            }
          ],
          "loot_rules": "Coordinate Ancient part drops"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 4000,
        "max": 4200
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:017",
      "type": "fight",
      "summary": "Win the Moonlit Duel against Saya & Selyne",
      "detail": "Sail to Sakurajima, overpower Selyne with dragon Pals and keep Saya at range to liberate the Moonflower tower.",
      "targets": [],
      "locations": [
        {
          "region_id": "sakurajima-island",
          "coords": [
            -597,
            203
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Chain crowd control on Saya to prevent lethal melee combos."
        },
        "coop": {
          "role_splits": [
            {
              "role": "dragon",
              "tasks": "Burst Selyne"
            },
            {
              "role": "marksman",
              "tasks": "Suppress Saya"
            }
          ],
          "loot_rules": "Distribute cosmetics"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 4200,
        "max": 4500
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story-early:018",
      "type": "fight",
      "summary": "Seize the Feybreak Tower",
      "detail": "Assault Bjorn & Bastigor, stacking firepower to melt the dragon and closing in to finish the final syndicate leader.",
      "targets": [],
      "locations": [
        {
          "region_id": "feybreak",
          "coords": [
            -1294,
            -1669
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Stack fire resist and rotate turret mounts to keep pressure on Bastigor."
        },
        "coop": {
          "role_splits": [
            {
              "role": "turret",
              "tasks": "Man base defenses"
            },
            {
              "role": "striker",
              "tasks": "Focus Bjorn"
            }
          ],
          "loot_rules": "Split final rewards"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 5000,
        "max": 5200
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    }
  ],
  "completion_criteria": [
    {
      "type": "quest-chain",
      "quest_id": "main-story-feybreak"
    }
  ],
  "yields": {
    "levels_estimate": "+20 to +25",
    "key_unlocks": [
      "ancient-technology-points",
      "main-story-clear"
    ]
  },
  "metrics": {
    "progress_segments": 6,
    "boss_targets": 6,
    "quest_nodes": 13
  },
  "next_routes": [
    {
      "route_id": "quest-main-story",
      "reason": "Log the Investigator board epilogue after finishing Feybreak"
    }
  ]
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
  "tags": [
    "resource-farm",
    "leather",
    "early-game",
    "combat-loop"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 4,
    "max": 10
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Acquire the required quantity of Leather"
  ],
  "estimated_time_minutes": {
    "solo": 15,
    "coop": 10
  },
  "estimated_xp_gain": {
    "min": 200,
    "max": 400
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Lost time if defeated",
    "hardcore": "Death results in permaloss of captured Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Target Lamball and Vixy groups on the outskirts of Windswept Hills until level 6 before rotating to Sea Breeze.",
    "overleveled": "Hunt Direhowl packs in the ravine for faster drops; their higher HP scales with your damage output.",
    "resource_shortages": [
      {
        "item_id": "pal-sphere",
        "solution": "Craft a fresh batch at your Primitive Workbench before departing."
      },
      {
        "item_id": "gold",
        "solution": "Sell spare ores or berries at the Archipelago merchant to fund purchases."
      }
    ],
    "time_limited": "Clear step :001 then buy the remainder from the merchant in step :003 to finish within five minutes.",
    "dynamic_rules": [
      {
        "signal": "mode:hardcore",
        "condition": "mode.hardcore === true",
        "adjustment": "Prioritise the merchant purchase in step :003 before engaging the densest spawn clusters in :002 to minimise death risk.",
        "priority": 1,
        "mode_scope": [
          "hardcore"
        ],
        "related_steps": [
          "resource-leather-early:003"
        ]
      },
      {
        "signal": "resource_gap:leather_high",
        "condition": "resource_gaps contains leather >= 20",
        "adjustment": "Run the Sea Breeze loop in :002 twice—first clockwise around the Church, then along the Bridge of the Twin Knights—to stock 20+ Leather in one outing.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-leather-early:002"
        ]
      },
      {
        "signal": "goal:mounts",
        "condition": "goals includes mounts",
        "adjustment": "Stay until you bank at least 15 Leather so upcoming saddle routes such as mount-eikthyrdeer-saddle do not immediately reinsert this farm.",
        "priority": 3,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-leather-early:002"
        ],
        "follow_up_routes": [
          "mount-eikthyrdeer-saddle",
          "mount-direhowl-harness"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-leather-early:checkpoint-arrival",
      "summary": "Reached farming zone",
      "benefits": [
        "Unlocks fast travel point if activated",
        "Spawns leather-dropping Pals"
      ],
      "related_steps": [
        "resource-leather-early:001"
      ]
    },
    {
      "id": "resource-leather-early:checkpoint-quota",
      "summary": "First 10 Leather collected",
      "benefits": [
        "Meets most early saddle requirements"
      ],
      "related_steps": [
        "resource-leather-early:002"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "starter-base-capture"
    ],
    "optional": [
      "resource-paldium"
    ]
  },
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
      "locations": [
        {
          "region_id": "sea-breeze-archipelago",
          "coords": [
            -650,
            -650
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "windswept-hills",
          "coords": [
            200,
            -300
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "foxparks",
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 40
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "shockbyte-leather-sources"
      ]
    },
    {
      "step_id": "resource-leather-early:002",
      "type": "farm",
      "summary": "Hunt leather‑dropping Pals",
      "detail": "Defeat or capture Foxparks, Fuack, Rushoar, Melpaca, Vixy, Eikthyrdeer and Direhowl.  Each drop guarantees 1–3 Leather【142053078936299†L295-L311】【840767909995613†L49-L103】.  Use water Pals against fire types and electric Pals against water types.  Expect roughly 10–20 Leather/hour when solo and 20–30 Leather/hour in Co‑Op.",
      "targets": [
        {
          "kind": "item",
          "id": "leather",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "sea-breeze-archipelago",
          "coords": [
            -650,
            -650
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "windswept-hills",
          "coords": [
            189,
            -478
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Pull one Pal at a time and use ranged attacks to minimise damage",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 3
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "hunter",
              "tasks": "Engage and defeat Pals"
            },
            {
              "role": "looter",
              "tasks": "Collect drops and watch for respawns"
            }
          ],
          "loot_rules": "Divide Leather evenly"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 300
      },
      "outputs": {
        "items": [
          {
            "item_id": "leather",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks leather >= required",
          "action": "repeat",
          "subroute_ref": "resource-leather-early"
        }
      ],
      "citations": [
        "shockbyte-leather-sources",
        "eikthyrdeer-drops"
      ]
    },
    {
      "step_id": "resource-leather-early:003",
      "type": "deliver",
      "summary": "Optionally buy Leather from merchants",
      "detail": "If hunting is too risky, purchase Leather from a Wandering Merchant for approximately 150 gold each【840767909995613†L78-L100】.",
      "targets": [
        {
          "kind": "item",
          "id": "leather",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            50,
            50
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 5,
        "max": 10
      },
      "outputs": {
        "items": [
          {
            "item_id": "leather",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "shockbyte-leather-merchant"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "leather",
      "qty": 10
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": []
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "mount-foxparks-harness",
      "reason": "Provides Leather needed for Foxparks Harness"
    },
    {
      "route_id": "mount-direhowl-harness",
      "reason": "Provides Leather for Direhowl Harness"
    },
    {
      "route_id": "mount-eikthyrdeer-saddle",
      "reason": "Provides Leather for Eikthyrdeer Saddle"
    }
  ]
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
  "tags": [
    "resource-farm",
    "paldium",
    "early-game",
    "mining"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 3,
    "max": 12
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Visit clustered Paldium nodes",
    "Mine fragments efficiently",
    "Convert spare Ore into fragments if needed"
  ],
  "estimated_time_minutes": {
    "solo": 12,
    "coop": 8
  },
  "estimated_xp_gain": {
    "min": 180,
    "max": 320
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Minimal—only time spent",
    "hardcore": "Potential durability loss on tools"
  },
  "adaptive_guidance": {
    "underleveled": "Equip a Stone Pickaxe and avoid Alpha spawns near the river; capture a Lifmunk to assist with mining.",
    "overleveled": "Route through the Desiccated Desert outcrops for higher-density nodes to refill faster.",
    "resource_shortages": [
      {
        "item_id": "stone-pickaxe",
        "solution": "Craft a backup Stone Pickaxe at the Workbench before leaving base."
      },
      {
        "item_id": "paldium-fragment",
        "solution": "Crush Ore at the Primitive Furnace for 2 fragments per ingot batch."
      }
    ],
    "time_limited": "Mine the waterfall circuit (step :001) once, then smelt spare Ore into fragments back at base.",
    "dynamic_rules": [
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes <= 10",
        "adjustment": "Run only step :001 and convert any Ore you already own via :003 on return to base for a quick 30+ fragment top-up.",
        "priority": 2,
        "mode_scope": [
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-paldium:001",
          "resource-paldium:003"
        ]
      },
      {
        "signal": "resource_gap:paldium_high",
        "condition": "resource_gaps contains paldium-fragment >= 60",
        "adjustment": "Chain steps :001 and :002 without travel breaks, then immediately queue Ore smelting in :003 to push past 60 fragments before leaving the valley.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-paldium:001",
          "resource-paldium:002",
          "resource-paldium:003"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to ferry Ore back to the furnace after step :002 while the miner keeps nodes cycling, preventing respawn downtime.",
        "priority": 3,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-paldium:002",
          "resource-paldium:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-paldium:checkpoint-river",
      "summary": "River nodes cleared",
      "benefits": [
        "50+ fragments gathered"
      ],
      "related_steps": [
        "resource-paldium:001"
      ]
    },
    {
      "id": "resource-paldium:checkpoint-furnace",
      "summary": "Fragments smelted",
      "benefits": [
        "Ensures crafting stockpile"
      ],
      "related_steps": [
        "resource-paldium:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "starter-base-capture"
    ],
    "optional": [
      "resource-leather-early"
    ]
  },
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
      "targets": [
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 20
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            80,
            -150
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Keep stamina above 50 % to dodge hostile Lamballs",
          "safety_buffer_items": [
            {
              "item_id": "berry",
              "qty": 5
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break nodes"
            },
            {
              "role": "hauler",
              "tasks": "Collect drops and scout"
            }
          ],
          "loot_rules": "Split fragments evenly"
        }
      },
      "recommended_loadout": {
        "gear": [
          "stone-pickaxe"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 100
      },
      "outputs": {
        "items": [
          {
            "item_id": "paldium-fragment",
            "qty": 20
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-paldium"
      ]
    },
    {
      "step_id": "resource-paldium:002",
      "type": "explore",
      "summary": "Hit cliffside outcrops",
      "detail": "Circle the cliff ring northwest of the starting valley.  Surface fragments protrude from the ground and can be kicked for bonus drops, netting ~30 fragments per lap【palwiki-paldium†L86-L115】.",
      "targets": [
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 30
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -40,
            120
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "stone-pickaxe"
        ],
        "pals": [
          "foxparks"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 70,
        "max": 110
      },
      "outputs": {
        "items": [
          {
            "item_id": "paldium-fragment",
            "qty": 30
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-paldium"
      ]
    },
    {
      "step_id": "resource-paldium:003",
      "type": "craft",
      "summary": "Refine fragments from Ore",
      "detail": "Back at base, smelt spare Ore into Ingots, then crush the leftovers to convert into extra fragments.  Each smelting cycle produces 2 fragments as a by-product when using the Primitive Furnace【palwiki-paldium†L118-L140】.",
      "targets": [
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "paldium-fragment",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-paldium"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "paldium-fragment",
      "qty": 50
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": []
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "mount-foxparks-harness",
      "reason": "Paldium needed for harness crafting"
    },
    {
      "route_id": "tech-grappling-gun",
      "reason": "Supplies fragments for the tech"
    }
  ]
}
```

### Route: Honey Harvest Network

Players who want reliable Cake production need an efficient way to gather Honey. This route chains the level 18 Cinnamoth Forest loop with Mossanda Forest’s Beegarde spawn clusters and ends by wiring those Beegarde into a ranch for passive output.【pcgamesn-honey†L135-L148】【palwiki-honey†L402-L433】

```json
{
  "route_id": "resource-honey",
  "title": "Honey Harvest Network",
  "category": "resources",
  "tags": [
    "resource-farm",
    "honey",
    "breeding",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 18,
    "max": 30
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Capture honey-dropping Pals",
    "Secure a steady honey supply at your ranch"
  ],
  "estimated_time_minutes": {
    "solo": 18,
    "coop": 12
  },
  "estimated_xp_gain": {
    "min": 220,
    "max": 420
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Respawn runs from Mossanda Forest take several minutes if you faint.",
    "hardcore": "Level 30 patrols around Mossanda Forest can one-shot undergeared players."
  },
  "adaptive_guidance": {
    "underleveled": "Stay near Cinnamoth Forest (-74,-279) and net 6+ honey from level 18 Cinnamoth before approaching Mossanda Forest Pals.【pcgamesn-honey†L135-L144】",
    "overleveled": "Chain Cinnamoth and Mossanda loops without fast travel to restock 20+ honey in a single outing.【pcgamesn-honey†L135-L145】",
    "resource_shortages": [
      {
        "item_id": "pal-sphere",
        "solution": "Craft extra Pal Spheres at base before hunting to avoid running dry mid-loop."
      }
    ],
    "time_limited": "Clear only the Cinnamoth loop (step :001) for a quick honey top-up, then assign your best Beegarde at base.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split roles—one player kites and weakens targets while the other nets captures and hauls honey.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-honey:001",
          "resource-honey:002"
        ]
      },
      {
        "signal": "resource_gap:honey_high",
        "condition": "resource_gaps contains honey >= 25",
        "adjustment": "Capture two extra Beegarde in step :002 and immediately assign them to a spare ranch slot to double passive output.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-honey:002",
          "resource-honey:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-honey:checkpoint-cinnamoth",
      "summary": "Cinnamoth loop cleared",
      "related_steps": [
        "resource-honey:001"
      ],
      "benefits": [
        "Initial honey stock",
        "Mid-tier bug pals captured"
      ]
    },
    {
      "id": "resource-honey:checkpoint-ranch",
      "summary": "Ranch assignment complete",
      "related_steps": [
        "resource-honey:003"
      ],
      "benefits": [
        "Passive honey income",
        "Cake crafting ready"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "starter-base-capture"
    ],
    "optional": [
      "resource-leather-early"
    ]
  },
  "failure_recovery": {
    "normal": "Fast travel back to Mossanda Forest, retrieve your pouch, and resume from the last cleared spawn loop.",
    "hardcore": "If a death drops gear in Mossanda Forest, regroup at base, craft heat/cold protection, and recover with a co-op buddy if possible."
  },
  "steps": [
    {
      "step_id": "resource-honey:001",
      "type": "capture",
      "summary": "Capture Cinnamoth near Cinnamoth Forest",
      "detail": "Teleport to Cinnamoth Forest (-74,-279) north of the Bridge of the Twin Knights. The level ~18 Cinnamoth here drop Honey when captured or defeated, letting you stock 6–8 units quickly.【pcgamesn-honey†L135-L144】",
      "targets": [
        {
          "kind": "item",
          "id": "honey",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "sea-breeze-archipelago",
          "coords": [
            -74,
            -279
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use ranged attacks to whittle Cinnamoth before capture and dodge their powder gusts.",
          "safety_buffer_items": [
            {
              "item_id": "medicine",
              "qty": 2
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "honey",
            "qty": 6
          }
        ],
        "pals": [
          "cinnamoth"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-honey"
      ]
    },
    {
      "step_id": "resource-honey:002",
      "type": "capture",
      "summary": "Hunt Beegarde in Mossanda Forest",
      "detail": "Travel to Mossanda Forest (234,-118). Level 20–30 Beegarde spawn in groups and reliably drop Honey; capture two or three to staff your ranch and stock additional drops.【pcgamesn-honey†L135-L145】",
      "targets": [
        {
          "kind": "pal",
          "id": "beegarde",
          "qty": 2
        },
        {
          "kind": "item",
          "id": "honey",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "forest-of-oblivion",
          "coords": [
            234,
            -118
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "controller",
              "tasks": "Pull individual Beegarde and keep aggro"
            },
            {
              "role": "catcher",
              "tasks": "Secure captures and collect Honey"
            }
          ],
          "loot_rules": "Prioritise Honey for breeding stock"
        }
      },
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "honey",
            "qty": 12
          }
        ],
        "pals": [
          "beegarde"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-honey"
      ]
    },
    {
      "step_id": "resource-honey:003",
      "type": "base",
      "summary": "Assign Beegarde to your ranch",
      "detail": "Back at base, assign captured Beegarde to a Ranch. They will periodically produce Honey without further intervention, keeping your cake pipeline stocked.【pcgamesn-honey†L146-L148】【palwiki-honey†L402-L433】",
      "targets": [
        {
          "kind": "item",
          "id": "honey",
          "qty": 20
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "beegarde"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "honey",
            "qty": 20
          }
        ],
        "pals": [],
        "unlocks": {
          "stations": [
            "ranch"
          ]
        }
      },
      "branching": [],
      "citations": [
        "pcgamesn-honey",
        "palwiki-honey"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "honey",
      "qty": 20
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "honey-farm"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Honey enables cake production for mid-game breeding and automation."
    },
    {
      "route_id": "tower-pal-genetics",
      "reason": "Stockpiled honey feeds breeding loops needed before confronting Pal Genetics."
    }
  ]
}
```

### Route: Coal Vein Circuit

Coal unlocks Refined Ingot fuel for improved furnaces and automation upgrades. The loop starts in the Hillside Cavern near the Windswept Hills statue, then graduates to the Desiccated Desert ridgeline and Astral Mountain veins once you can survive the heat and enemy levels.【pcgamesn-coal†L135-L138】【palwiki-coal†L388-L430】

```json
{
  "route_id": "resource-coal",
  "title": "Coal Vein Circuit",
  "category": "resources",
  "tags": [
    "resource-farm",
    "coal",
    "refined-ingot",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 20,
    "max": 35
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Mine early Coal deposits safely",
    "Unlock higher-yield Coal veins for Refined Ingots"
  ],
  "estimated_time_minutes": {
    "solo": 22,
    "coop": 15
  },
  "estimated_xp_gain": {
    "min": 260,
    "max": 480
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Encumbrance slows escape from dungeon mobs; expect a long jog if you overfill your pouch.",
    "hardcore": "Heat and high-level enemies in late-game regions can wipe an unprepared team, costing gear."
  },
  "adaptive_guidance": {
    "underleveled": "Loop the Hillside Cavern entrance nodes and reset rather than diving deep until you reach level 25.【pcgamesn-coal†L135-L138】",
    "overleveled": "Add the Desiccated Desert ridge and Astral Mountain outcrops to clear 60+ Coal per circuit.【pcgamesn-coal†L135-L138】",
    "resource_shortages": [
      {
        "item_id": "metal-pickaxe",
        "solution": "Upgrade to a Metal Pickaxe before leaving base so Coal rocks break quickly."
      }
    ],
    "time_limited": "Run only step :001 and leave once your carry weight hits 70% to avoid slowing down.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to mine while the partner ferries ore to a chest outside the dungeon, keeping spawns cycling.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-coal:001",
          "resource-coal:002"
        ]
      },
      {
        "signal": "resource_gap:coal_high",
        "condition": "resource_gaps contains coal >= 80",
        "adjustment": "Queue Crusher batches in :003 so spare Stone converts to Coal Fragments while you mine fresh nodes.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-coal:002",
          "resource-coal:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-coal:checkpoint-hillside",
      "summary": "Hillside Cavern cleared",
      "related_steps": [
        "resource-coal:001"
      ],
      "benefits": [
        "20+ Coal mined",
        "Respawn statue unlocked"
      ]
    },
    {
      "id": "resource-coal:checkpoint-smelter",
      "summary": "Refined output queued",
      "related_steps": [
        "resource-coal:003"
      ],
      "benefits": [
        "Refined Ingot fuel ready",
        "Passive Coal from Crusher"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-paldium"
    ],
    "optional": []
  },
  "failure_recovery": {
    "normal": "Drop excess Stone to regain stamina and kite remaining mobs back toward the entrance.",
    "hardcore": "If you fall in late-game zones, retreat until you craft Heat Resistant gear before attempting recovery."
  },
  "steps": [
    {
      "step_id": "resource-coal:001",
      "type": "gather",
      "summary": "Mine Hillside Cavern nodes",
      "detail": "Enter Hillside Cavern at 147,-397 northeast of Rayne Syndicate Tower. Clear the Coal, Sulfur, and Ore clusters with a Metal Pickaxe, exiting before weight caps you.【pcgamesn-coal†L135-L138】",
      "targets": [
        {
          "kind": "item",
          "id": "coal",
          "qty": 24
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            147,
            -397
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use torches to reveal ambushes and pull ranged mobs back toward the entrance hallway.",
          "safety_buffer_items": [
            {
              "item_id": "medicine",
              "qty": 2
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 210
      },
      "outputs": {
        "items": [
          {
            "item_id": "coal",
            "qty": 24
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-coal"
      ]
    },
    {
      "step_id": "resource-coal:002",
      "type": "gather",
      "summary": "Survey high-yield ridges",
      "detail": "Once geared, push into the Desiccated Desert ridgeline (~340,-120) and Astral Mountain foothills (~40, 320) where Coal veins respawn quickly but enemies hit much harder.【pcgamesn-coal†L135-L138】",
      "targets": [
        {
          "kind": "item",
          "id": "coal",
          "qty": 36
        }
      ],
      "locations": [
        {
          "region_id": "desiccated-desert",
          "coords": [
            340,
            -120
          ],
          "time": "day",
          "weather": "clear"
        },
        {
          "region_id": "astral-mountain",
          "coords": [
            40,
            320
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break Coal veins"
            },
            {
              "role": "lookout",
              "tasks": "Ping elite patrols and escort hauls"
            }
          ],
          "loot_rules": "Bank Coal in shared chests before fast travelling home"
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 190,
        "max": 240
      },
      "outputs": {
        "items": [
          {
            "item_id": "coal",
            "qty": 36
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-coal"
      ]
    },
    {
      "step_id": "resource-coal:003",
      "type": "craft",
      "summary": "Process Coal for Refined Ingots",
      "detail": "Back at base, feed Coal and Ore into the Improved Furnace to create Refined Ingots, or run Stone through the Crusher for extra Coal fragments.【palwiki-coal†L388-L430】",
      "targets": [
        {
          "kind": "item",
          "id": "refined-ingot",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 160
      },
      "outputs": {
        "items": [
          {
            "item_id": "refined-ingot",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {
          "stations": [
            "improved-furnace"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-coal"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "coal",
      "qty": 60
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "refined-ingot-fuel"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Refined Ingots power the automation upgrades in the mid-game arc."
    },
    {
      "route_id": "tower-brothers-eternal-pyre",
      "reason": "Coal stockpiles support fire-resistant gear before tackling the Eternal Pyre."
    }
  ]
}
```

### Route: Wool Ranch Loop

Cloth upgrades and tailoring requests strain early-game bases. This loop corrals Lamball herds in Windswept Hills and Sea Breeze Archipelago, then parks captured Lamball on a ranch so Wool production continues while colonists craft and haul.【palwiki-lamball†L433-L623】

```json
{
  "route_id": "resource-wool",
  "title": "Wool Ranch Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "wool",
    "early-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 4,
    "max": 18
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Sweep Windswept Hills Lamball herds",
    "Tag Sea Breeze Archipelago backups",
    "Assign ranch hands and spool cloth"
  ],
  "estimated_time_minutes": {
    "solo": 18,
    "coop": 12
  },
  "estimated_xp_gain": {
    "min": 300,
    "max": 520
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Losing the herd only costs a few Pal Spheres and a short jog.",
    "hardcore": "Hardcore runs risk sacrificing early ranch workers; keep stamina high when kiting hostile patrols."
  },
  "adaptive_guidance": {
    "underleveled": "Stick to the Windswept Hills meadows and capture docile Lamball pairs until you can safely travel to Sea Breeze.【palwiki-lamball†L620-L623】【goleap-region-levels†L131-L147】",
    "overleveled": "Chain both regions in a single loop, hauling 25+ Wool before returning to base for tailoring queues.【palwiki-lamball†L620-L623】",
    "resource_shortages": [
      {
        "item_id": "pal-sphere",
        "solution": "Craft extra Pal Spheres at the Primitive Workbench before leaving; you will need at least six to refresh ranch slots."
      }
    ],
    "time_limited": "Complete step :001 only, then assign one Lamball to the ranch for passive Wool until you can finish the loop.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties—one player lassos Lamball while the other clears respawn timers and escorts captives back to base.",
        "priority": 3,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-wool:001",
          "resource-wool:002"
        ]
      },
      {
        "signal": "resource_gap:wool_high",
        "condition": "resource_gaps contains wool >= 30",
        "adjustment": "Assign two Lamball to separate ranch slots after step :003 to double passive production and queue cloth crafting immediately.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-wool:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-wool:checkpoint-herd",
      "summary": "Herd secured",
      "benefits": [
        "Stable Wool income",
        "Extra Handiwork pals"
      ],
      "related_steps": [
        "resource-wool:001",
        "resource-wool:002"
      ]
    },
    {
      "id": "resource-wool:checkpoint-ranch",
      "summary": "Ranch staffed",
      "benefits": [
        "Passive Wool production",
        "Cloth queue primed"
      ],
      "related_steps": [
        "resource-wool:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "starter-base-capture"
    ],
    "optional": [
      "resource-honey"
    ]
  },
  "failure_recovery": {
    "normal": "If Lamball faint en route, fast travel back to the Windswept Hills statue and repeat step :001 with fresh Pal Spheres.",
    "hardcore": "Drop excess cargo before kiting hostile patrols; sprinting empty-handed keeps Hardcore characters safer while escorting Lamball."
  },
  "steps": [
    {
      "step_id": "resource-wool:001",
      "type": "capture",
      "summary": "Net Lamball herds in Windswept Hills",
      "detail": "Teleport to the Windswept Hills statue and sweep the meadows south of the plateau. Lamball spawn here in friendly pairs and drop 1–3 Wool per capture, letting you recruit three ranch hands quickly.【palwiki-lamball†L575-L623】【goleap-region-levels†L131-L147】",
      "targets": [
        {
          "kind": "pal",
          "id": "lamball",
          "qty": 3
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -58,
            -470
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Keep distance from Syndicate patrols and use ranged damage to soften Lamball before throwing Pal Spheres.",
          "safety_buffer_items": [
            {
              "item_id": "berry",
              "qty": 5
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "wrangler",
              "tasks": "Aggro and weaken Lamball"
            },
            {
              "role": "catcher",
              "tasks": "Throw Pal Spheres and haul captures"
            }
          ],
          "loot_rules": "Share Wool evenly to keep tailoring supplied"
        }
      },
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 170
      },
      "outputs": {
        "items": [
          {
            "item_id": "wool",
            "qty": 8
          }
        ],
        "pals": [
          "lamball"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-lamball",
        "goleap-region-levels"
      ]
    },
    {
      "step_id": "resource-wool:002",
      "type": "capture",
      "summary": "Rotate through Sea Breeze Archipelago pastures",
      "detail": "Sail or glide to the Sea Breeze Archipelago and loop the coastal fields north of the Church. Lamball spawn here at similar levels, ensuring replacement workers and extra Wool for crafting stock.【palwiki-lamball†L620-L623】",
      "targets": [
        {
          "kind": "item",
          "id": "wool",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "sea-breeze-archipelago",
          "coords": [
            148,
            -508
          ],
          "time": "day",
          "weather": "clear"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 130,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "wool",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-lamball"
      ]
    },
    {
      "step_id": "resource-wool:003",
      "type": "base",
      "summary": "Staff the ranch and weave cloth",
      "detail": "Back at base, assign two Lamball to the Ranch so they passively generate Wool, then queue Cloth recipes at the workbench for early armor upgrades.【palwiki-lamball†L433-L623】",
      "targets": [
        {
          "kind": "item",
          "id": "cloth",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lamball"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "wool",
            "qty": 20
          }
        ],
        "pals": [],
        "unlocks": {
          "stations": [
            "ranch"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-lamball"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "wool",
      "qty": 30
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "cloth-crafting"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Cloth and Wool keep the mid-game expansion upgrades rolling."
    },
    {
      "route_id": "resource-honey",
      "reason": "Cake production needs steady Wool alongside Honey and Eggs."
    }
  ]
}
```

### Route: Egg Clutch Run

Efficient Cake production hinges on a dependable stockpile of Eggs. This loop sweeps Windswept Hills for docile Chikipi, stations them on your ranch, and backtracks through the meadow to scoop stray ground eggs while timers reset.【palwiki-chikipi†L1850-L1859】【palwiki-chikipi†L1667-L1692】

```json
{
  "route_id": "resource-egg",
  "title": "Egg Clutch Run",
  "category": "resources",
  "tags": [
    "resource-farm",
    "egg",
    "breeding"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 3,
    "max": 12
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Capture a clutch of Chikipi",
    "Assign layers to the ranch",
    "Sweep the meadow for loose eggs"
  ],
  "estimated_time_minutes": {
    "solo": 15,
    "coop": 10
  },
  "estimated_xp_gain": {
    "min": 260,
    "max": 420
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Minimal—Chikipi flee rather than fight, so only time is lost.",
    "hardcore": "Hardcore runs risk a stray patrol near the fields; keep distance if undergeared."
  },
  "adaptive_guidance": {
    "underleveled": "Stay near the Palbox outskirts and capture one Chikipi at a time to avoid chain aggro.【palwiki-chikipi†L1850-L1857】",
    "overleveled": "Run the route twice per outing, filling both ranch slots and stockpiling 15+ Eggs for breeding queues.【palwiki-chikipi†L1667-L1693】",
    "resource_shortages": [
      {
        "item_id": "pal-sphere",
        "solution": "Bring at least five Pal Spheres so you can secure a full ranch roster without returning mid-loop."
      }
    ],
    "time_limited": "Catch two Chikipi in step :001, assign them during :002, and let passive production cover the deficit until you revisit.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:egg_high",
        "condition": "resource_gaps contains egg >= 12",
        "adjustment": "Hold an extra Chikipi in your party after step :002 so you can rotate fresh layers into the ranch as timers cool down.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-egg:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-egg:checkpoint-capture",
      "summary": "Chikipi captured",
      "benefits": [
        "Ranch-ready workers"
      ],
      "related_steps": [
        "resource-egg:001"
      ]
    },
    {
      "id": "resource-egg:checkpoint-ranch",
      "summary": "Egg production online",
      "benefits": [
        "Passive egg income",
        "Cake pipeline primed"
      ],
      "related_steps": [
        "resource-egg:002"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-honey"
    ],
    "optional": [
      "resource-wool"
    ]
  },
  "failure_recovery": {
    "normal": "If a Chikipi faints, fast travel back to the Hills statue and repeat step :001—respawns are fast.",
    "hardcore": "Avoid combat entirely; sprint away from patrols rather than risking a Hardcore wipe for a single egg."
  },
  "steps": [
    {
      "step_id": "resource-egg:001",
      "type": "capture",
      "summary": "Gather Chikipi in Windswept Hills",
      "detail": "Circle the grassy flats below the Palbox. Chikipi roam here constantly, lay eggs on the ground, and rarely fight back, so you can secure four layers quickly.【palwiki-chikipi†L1850-L1859】",
      "targets": [
        {
          "kind": "pal",
          "id": "chikipi",
          "qty": 4
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -42,
            -498
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "wrangler",
              "tasks": "Tag and weaken Chikipi"
            },
            {
              "role": "collector",
              "tasks": "Grab ground eggs and throw Pal Spheres"
            }
          ],
          "loot_rules": "Split eggs evenly for breeding"
        }
      },
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "egg",
            "qty": 6
          }
        ],
        "pals": [
          "chikipi"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-chikipi"
      ]
    },
    {
      "step_id": "resource-egg:002",
      "type": "base",
      "summary": "Assign layers to the ranch",
      "detail": "Place two captured Chikipi on the Ranch. Their Egg Layer partner skill produces eggs over time, so stagger assignments to keep timers rolling.【palwiki-chikipi†L1667-L1693】",
      "targets": [
        {
          "kind": "item",
          "id": "egg",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "chikipi"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "egg",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {
          "stations": [
            "ranch"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-chikipi"
      ]
    },
    {
      "step_id": "resource-egg:003",
      "type": "gather",
      "summary": "Scoop loose eggs while timers reset",
      "detail": "Jog a perimeter lap through the same fields, collecting freshly laid eggs and watching for respawned Chikipi to top off your ranch roster.【palwiki-chikipi†L1850-L1859】",
      "targets": [
        {
          "kind": "item",
          "id": "egg",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -35,
            -520
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 80
      },
      "outputs": {
        "items": [
          {
            "item_id": "egg",
            "qty": 8
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-chikipi"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "egg",
      "qty": 18
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "cake-baking"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-honey",
      "reason": "Pair eggs with Honey to bake Cake for breeding."
    }
  ]
}
```

### Route: Berry Seed Supply Loop

Berry Seed Supply Loop stitches Windswept Hills foraging with settlement merchant rotations so plantations stay seeded for early food chains.【palwiki-berry-seeds-raw†L1-L18】【palwiki-wandering-merchant-raw†L197-L252】【palwiki-small-settlement-raw†L1-L11】【palwiki-duneshelter-raw†L1-L7】

```json
{
  "route_id": "resource-berry-seeds",
  "title": "Berry Seed Supply Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "berry-seeds",
    "agriculture",
    "starter"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 1,
    "max": 18
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "berry-plantation"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Harvest Red Berry bushes around the Small Settlement",
    "Purchase Berry Seeds from settlement merchants",
    "Build and automate a Berry Plantation"
  ],
  "estimated_time_minutes": {
    "solo": 24,
    "coop": 18
  },
  "estimated_xp_gain": {
    "min": 100,
    "max": 160
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Getting downed near the berry patches only costs a short jog back to the Small Settlement.",
    "hardcore": "Drawing PIDF aggro at Duneshelter can snowball into squad wipes and merchant lockouts."
  },
  "adaptive_guidance": {
    "underleveled": "Stick to the Small Settlement loop until you have spare seeds and tech unlocked before pushing into the desert merchants.【palwiki-berry-seeds-raw†L1-L18】【palwiki-small-settlement-raw†L1-L11】",
    "overleveled": "Run the full Small Settlement to Duneshelter rotation to overstock seeds for multiple plantations.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-duneshelter-raw†L1-L7】",
    "resource_shortages": [
      {
        "item_id": "berry-seeds",
        "solution": "Alternate between harvesting local berry bushes and buying merchant stock each respawn to keep 30+ seeds banked.【palwiki-berry-seeds-raw†L1-L18】【palwiki-wandering-merchant-raw†L197-L252】【palwiki-small-settlement-raw†L1-L11】"
      }
    ],
    "time_limited": "Sweep merchants for quick seed purchases, drop them into base storage, and let the plantation churn while you work on other goals.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-berry-plantation-raw†L1-L34】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one partner to forage bushes while the other handles merchant runs and base deliveries each cycle.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-berry-seeds:001",
          "resource-berry-seeds:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-berry-seeds:checkpoint-forage",
      "summary": "Berry bush circuit mapped",
      "benefits": [
        "Seed drip unlocked",
        "Starter XP gathered"
      ],
      "related_steps": [
        "resource-berry-seeds:001"
      ]
    },
    {
      "id": "resource-berry-seeds:checkpoint-merchant",
      "summary": "Merchant stock secured",
      "benefits": [
        "Bulk seed reserve",
        "Gold conversion planned"
      ],
      "related_steps": [
        "resource-berry-seeds:002"
      ]
    },
    {
      "id": "resource-berry-seeds:checkpoint-plantation",
      "summary": "Plantation online",
      "benefits": [
        "Automated berry supply",
        "Base labor assigned"
      ],
      "related_steps": [
        "resource-berry-seeds:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "starter-base-capture"
    ],
    "optional": [
      "resource-chikipi-poultry"
    ]
  },
  "failure_recovery": {
    "normal": "Revisit nearby bushes or the Small Settlement vendor to restock seeds if a death drops your stash.",
    "hardcore": "Stash surplus seeds in base chests before traveling to Duneshelter so a wipe doesn't halt automation."
  },
  "steps": [
    {
      "step_id": "resource-berry-seeds:001",
      "type": "gather",
      "summary": "Harvest wild berry bushes",
      "detail": "Fast travel to the Small Settlement (~75,-479) and loop the surrounding berry patches, interacting with Red Berry bushes for free seed drops while clearing low-level mobs for XP.【palwiki-berry-seeds-raw†L1-L18】【palwiki-small-settlement-raw†L1-L11】",
      "targets": [
        {
          "kind": "item",
          "id": "berry-seeds",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            75,
            -479
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lamball"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 50
      },
      "outputs": {
        "items": [
          {
            "item_id": "berry-seeds",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-berry-seeds-raw",
        "palwiki-small-settlement-raw"
      ]
    },
    {
      "step_id": "resource-berry-seeds:002",
      "type": "trade",
      "summary": "Buy out settlement merchants",
      "detail": "Rotate between the Small Settlement and Duneshelter merchants, buying Berry Seeds for 50 gold each whenever they restock so plantations never stall.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-small-settlement-raw†L1-L11】【palwiki-duneshelter-raw†L1-L7】",
      "targets": [
        {
          "kind": "item",
          "id": "berry-seeds",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "duneshelter",
          "coords": [
            357,
            347
          ],
          "time": "any",
          "weather": "clear"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "buyer",
              "tasks": "Handle trades and ferry seeds home"
            },
            {
              "role": "scout",
              "tasks": "Watch for PIDF patrols and escort cargo"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "stone-spear"
        ],
        "pals": [
          "chikipi"
        ],
        "consumables": [
          "gold-coin"
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "berry-seeds",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-wandering-merchant-raw",
        "palwiki-small-settlement-raw",
        "palwiki-duneshelter-raw"
      ]
    },
    {
      "step_id": "resource-berry-seeds:003",
      "type": "build",
      "summary": "Construct and staff a Berry Plantation",
      "detail": "Spend 3 Berry Seeds, 20 Wood, and 20 Stone to place a Berry Plantation, then assign Planting, Watering, and Gathering pals so berries flow automatically.【palwiki-berry-plantation-raw†L1-L34】",
      "targets": [
        {
          "kind": "station",
          "id": "berry-plantation"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place the plantation and restock building materials"
            },
            {
              "role": "foreman",
              "tasks": "Assign planters and monitor berry output"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "wooden-hammer"
        ],
        "pals": [
          "lamball",
          "pengullet"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 80
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "berry-plantation"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-berry-plantation-raw"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "berry-seeds",
      "qty": 18
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "berry-plantation-automation"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-wheat-seeds",
      "reason": "Wheat fields rely on a steady berry economy to cover ranch food and base diets."
    },
    {
      "route_id": "resource-tomato-seeds",
      "reason": "Greenhouse rotations scale smoothly once berry plantations keep stamina food stocked."
    }
  ]
}
```


### Route: Pal Fluid Condenser

Water-tech automation leans on Pal Fluids. This circuit corrals Pengullet along the Windswept Hills coastline, scoops Fuack from inland ponds, and pipelines the extras into your factories and cooking queues.【palwiki-pengullet-fandom†L1868-L1872】【palwiki-pengullet†L575-L619】【palwiki-fuack†L1853-L1859】【palwiki-fuack†L1667-L1667】

```json
{
  "route_id": "resource-pal-fluids",
  "title": "Pal Fluid Condenser",
  "category": "resources",
  "tags": [
    "resource-farm",
    "pal-fluids",
    "automation"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 5,
    "max": 20
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Capture coastal Pengullet",
    "Sweep inland ponds for Fuack",
    "Assign fluid workers or cull for stock"
  ],
  "estimated_time_minutes": {
    "solo": 16,
    "coop": 11
  },
  "estimated_xp_gain": {
    "min": 320,
    "max": 500
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Aggressive patrols near the shoreline can down you; respawning costs travel time.",
    "hardcore": "Hardcore runs should avoid cliff combat—fall damage while hauling fluids can be lethal."
  },
  "adaptive_guidance": {
    "underleveled": "Capture only Pengullet during daylight and avoid the deeper coves where Syndicate scouts roam.【palwiki-pengullet-fandom†L1868-L1872】",
    "overleveled": "Chain Pengullet and Fuack loops without returning to base, filling storage with 30+ Pal Fluids per run.【palwiki-pengullet†L575-L619】【palwiki-fuack†L1667-L1667】",
    "resource_shortages": [
      {
        "item_id": "pal-sphere",
        "solution": "Craft surplus Pal Spheres so you can safely capture both species without crafting breaks."
      }
    ],
    "time_limited": "Complete step :001 only for a quick 10 Pal Fluid top-up, then let ranch assignments produce more while you log off.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player capture while the other ferries extras back to base to keep spawn timers rolling.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-pal-fluids:001",
          "resource-pal-fluids:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-pal-fluids:checkpoint-coast",
      "summary": "Coastline cleared",
      "benefits": [
        "Initial Pal Fluids",
        "Watering pals captured"
      ],
      "related_steps": [
        "resource-pal-fluids:001"
      ]
    },
    {
      "id": "resource-pal-fluids:checkpoint-base",
      "summary": "Fluid production online",
      "benefits": [
        "Factory feedstock",
        "Water chores staffed"
      ],
      "related_steps": [
        "resource-pal-fluids:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-coal"
    ],
    "optional": [
      "resource-wool"
    ]
  },
  "failure_recovery": {
    "normal": "If you fall or faint on the cliffs, fast travel back to the coastline statue and resume from the last cleared cove.",
    "hardcore": "Retreat before nightfall; Hardcore players should avoid fighting Penking patrols until geared."
  },
  "steps": [
    {
      "step_id": "resource-pal-fluids:001",
      "type": "capture",
      "summary": "Sweep the Windswept shoreline for Pengullet",
      "detail": "Follow the beach east of the Windswept Hills fast travel point. Pengullet congregate along the water, drop Pal Fluids on capture, and offer Watering utility for your base.【palwiki-pengullet-fandom†L1868-L1872】【palwiki-pengullet†L575-L619】",
      "targets": [
        {
          "kind": "item",
          "id": "pal-fluids",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -120,
            -560
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use ranged attacks from the cliffs to soften Pengullet before throwing spheres to avoid retaliation.",
          "safety_buffer_items": [
            {
              "item_id": "medicine",
              "qty": 2
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 210
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-fluids",
            "qty": 10
          }
        ],
        "pals": [
          "pengullet"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-pengullet-fandom",
        "palwiki-pengullet"
      ]
    },
    {
      "step_id": "resource-pal-fluids:002",
      "type": "capture",
      "summary": "Tag Fuack around inland ponds",
      "detail": "Cut inland to the freshwater pools west of the plateau. Fuack roam around water sources, drop Pal Fluids alongside Leather, and bolster your Watering roster.【palwiki-fuack†L1853-L1859】【palwiki-fuack†L1667-L1667】",
      "targets": [
        {
          "kind": "item",
          "id": "pal-fluids",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -30,
            -440
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-fluids",
            "qty": 12
          }
        ],
        "pals": [
          "fuack"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-fuack"
      ]
    },
    {
      "step_id": "resource-pal-fluids:003",
      "type": "base",
      "summary": "Assign fluid workers or bottle extras",
      "detail": "Back at base, station Pengullet or Fuack on Watering posts or cooking stations, then butcher surplus captures for additional Pal Fluids to feed polymer and medicine recipes.【palwiki-pengullet†L575-L619】【palwiki-fuack†L1667-L1667】",
      "targets": [
        {
          "kind": "item",
          "id": "pal-fluids",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "pengullet",
          "fuack"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-fluids",
            "qty": 15
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-pengullet",
        "palwiki-fuack"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "pal-fluids",
      "qty": 30
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "polymer-crafting"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Pal Fluids feed polymer and circuit recipes in the mid-game expansion arc."
    }
  ]
}
```


### Route: Sulfur Flow Loop

Sulfur powers gunpowder and every ballistic upgrade, so this loop opens with the Mossanda Forest lava ravine before graduating to Mount Obsidian chest staging to sustain ammunition stockpiles.【pcgamesn-sulfur†L11-L20】【palwiki-sulfur†L5-L8】

```json
{
  "route_id": "resource-sulfur",
  "title": "Sulfur Flow Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "sulfur",
    "gunpowder",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 18,
    "max": 34
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [
      "heat-resistant-armor"
    ],
    "pals": []
  },
  "objectives": [
    "Unlock safe Sulfur nodes near Mossanda Forest",
    "Establish a Mount Obsidian mining circuit",
    "Convert Sulfur into Gunpowder stock"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 20
  },
  "estimated_xp_gain": {
    "min": 340,
    "max": 520
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Heat damage and elite patrols can break gear and force long corpse runs if you overstay in lava zones.",
    "hardcore": "Volcanic DoTs stack quickly; a wipe at Mount Obsidian risks permanent loss of high-tier tools and Pals."
  },
  "adaptive_guidance": {
    "underleveled": "Loop the Mossanda Forest ravine deposits until you can survive lava enemies deeper in Mount Obsidian.【pcgamesn-sulfur†L11-L19】",
    "overleveled": "Base out of the Eternal Pyre entrance and rotate chest drops between runs to keep Sulfur flowing for munitions.【pcgamesn-sulfur†L15-L20】",
    "resource_shortages": [
      {
        "item_id": "gunpowder",
        "solution": "Run step :003 immediately after mining so Sulfur converts into ammunition stock instead of sitting unused.【pcgamesn-sulfur†L11-L15】"
      }
    ],
    "time_limited": "Hit step :001 for a 10-minute top-up, then fast travel home before heat attrition sets in.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:gunpowder_high",
        "condition": "resource_gaps contains gunpowder >= 60",
        "adjustment": "Queue two Gunpowder batches during :003 and skip optional ore hauling so ammunition deficits clear first.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-sulfur:003"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to mine while the partner ferries ore and Sulfur back to the chest outside the Eternal Pyre entrance to keep nodes respawning.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-sulfur:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-sulfur:checkpoint-ravine",
      "summary": "Mossanda ravine cleared",
      "related_steps": [
        "resource-sulfur:001"
      ],
      "benefits": [
        "10+ Sulfur mined",
        "Fast travel statue proximity unlocked"
      ]
    },
    {
      "id": "resource-sulfur:checkpoint-volcano",
      "summary": "Volcanic chest stocked",
      "related_steps": [
        "resource-sulfur:002"
      ],
      "benefits": [
        "30+ Sulfur banked",
        "Chest staging at Eternal Pyre"
      ]
    },
    {
      "id": "resource-sulfur:checkpoint-ammo",
      "summary": "Gunpowder queue started",
      "related_steps": [
        "resource-sulfur:003"
      ],
      "benefits": [
        "Ammunition craft enabled",
        "Sulfur stock stabilized"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-coal"
    ],
    "optional": [
      "resource-pal-fluids"
    ]
  },
  "failure_recovery": {
    "normal": "Retreat to the ravine loop, repair gear, and rebuild Sulfur stock before another Mount Obsidian push.",
    "hardcore": "If a Hardcore run fails, reset heat gear, recruit fresh carrying Pals, and re-enter during night when patrols thin."
  },
  "steps": [
    {
      "step_id": "resource-sulfur:001",
      "type": "gather",
      "summary": "Mine the Mossanda lava ravine",
      "detail": "Head northeast of the Mossanda Forest fast travel statue (234,-118) to a lava ravine with early Sulfur nodes; clear the small clusters quickly before heat and encumbrance stack up.【pcgamesn-sulfur†L13-L19】",
      "targets": [
        {
          "kind": "item",
          "id": "sulfur",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            234,
            -118
          ],
          "time": "day",
          "weather": "clear"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "sulfur",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-sulfur"
      ]
    },
    {
      "step_id": "resource-sulfur:002",
      "type": "gather",
      "summary": "Loop Mount Obsidian deposits",
      "detail": "Fast travel to the Brothers of the Eternal Pyre Tower (-588,-518), stage a chest outside, then sweep the surrounding lava flows while a Cattiva hauls ore and Sulfur back between passes.【pcgamesn-sulfur†L15-L20】【pcgamesn-bosses†L7-L9】【palwiki-sulfur†L5-L8】",
      "targets": [
        {
          "kind": "item",
          "id": "sulfur",
          "qty": 36
        }
      ],
      "locations": [
        {
          "region_id": "mount-obsidian",
          "coords": [
            -588,
            -518
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break Sulfur nodes"
            },
            {
              "role": "runner",
              "tasks": "Ferry loads to the chest and reset spawns"
            }
          ],
          "loot_rules": "Deposit Sulfur in the shared chest each lap"
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe",
          "heat-resistant-armor"
        ],
        "pals": [
          "cattiva"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 240
      },
      "outputs": {
        "items": [
          {
            "item_id": "sulfur",
            "qty": 36
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-sulfur",
        "pcgamesn-bosses",
        "palwiki-sulfur"
      ]
    },
    {
      "step_id": "resource-sulfur:003",
      "type": "craft",
      "summary": "Refine Sulfur into Gunpowder",
      "detail": "Back at base, combine Sulfur with Coal at the High Quality Workbench to craft Gunpowder so ammunition production keeps pace with weapon demand.【pcgamesn-sulfur†L11-L15】【palwiki-sulfur†L5-L8】",
      "targets": [
        {
          "kind": "item",
          "id": "gunpowder",
          "qty": 30
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "cattiva"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 160
      },
      "outputs": {
        "items": [
          {
            "item_id": "gunpowder",
            "qty": 30
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-sulfur",
        "palwiki-sulfur"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "sulfur",
      "qty": 48
    },
    {
      "type": "have-item",
      "item_id": "gunpowder",
      "qty": 30
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "gunpowder-stock"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-pure-quartz",
      "reason": "Pure Quartz runs pair with Sulfur to advance late-game electronics."
    },
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Gunpowder reserves accelerate weapon crafting during the mid-game expansion."
    }
  ]
}
```

### Route: Astral Quartz Expedition

Circuit boards and late-game electronics hinge on Pure Quartz. This expedition secures the PAL Research Tower fast travel, mines the Astral Mountain ridges, and anchors a base so mining Pals keep the ore flowing.【pcgamesn-pure-quartz†L15-L23】【palwiki-pure-quartz†L1-L3】

```json
{
  "route_id": "resource-pure-quartz",
  "title": "Astral Quartz Expedition",
  "category": "resources",
  "tags": [
    "resource-farm",
    "pure-quartz",
    "electronics",
    "late-mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 32,
    "max": 46
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-sulfur"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock Astral Mountain fast travel",
    "Mine high-grade Pure Quartz clusters",
    "Stage a passive extraction base for circuit crafting"
  ],
  "estimated_time_minutes": {
    "solo": 38,
    "coop": 26
  },
  "estimated_xp_gain": {
    "min": 420,
    "max": 640
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Cold damage and high-level patrols can break tools and force long retreats from Astral Mountain.",
    "hardcore": "Falls or freezes near Astral Mountain wipe end-game kits; regroup with spare cold gear before returning."
  },
  "adaptive_guidance": {
    "underleveled": "Unlock the PAL Research Tower statue first, then run short mining bursts before elites converge.【pcgamesn-pure-quartz†L15-L20】【pcgamesn-bosses†L11-L13】",
    "overleveled": "Claim a ridge base inside Astral Mountain so mining Pals harvest Pure Quartz passively between manual runs.【pcgamesn-pure-quartz†L19-L23】",
    "resource_shortages": [
      {
        "item_id": "circuit-board",
        "solution": "Feed Pure Quartz into step :003 immediately so circuit production stays ahead of polymer demand.【pcgamesn-pure-quartz†L21-L23】"
      }
    ],
    "time_limited": "Fast travel in, grab two node clusters near the tower, then recall home before respawns escalate.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:circuit-board_high",
        "condition": "resource_gaps contains circuit-board >= 20",
        "adjustment": "Run step :003 twice and prioritize manual mining in :002 over expansion tasks until the gap clears.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-pure-quartz:002",
          "resource-pure-quartz:003"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "One player scouts and kites patrols while the miner works nodes; swap roles every cycle to manage cold meters.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-pure-quartz:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-pure-quartz:checkpoint-statue",
      "summary": "Astral access unlocked",
      "related_steps": [
        "resource-pure-quartz:001"
      ],
      "benefits": [
        "PAL Research Tower statue activated",
        "Cold travel route established"
      ]
    },
    {
      "id": "resource-pure-quartz:checkpoint-quarry",
      "summary": "Quartz cache secured",
      "related_steps": [
        "resource-pure-quartz:002"
      ],
      "benefits": [
        "40+ Pure Quartz hauled",
        "Safe retreat path mapped"
      ]
    },
    {
      "id": "resource-pure-quartz:checkpoint-automation",
      "summary": "Passive mining online",
      "related_steps": [
        "resource-pure-quartz:003"
      ],
      "benefits": [
        "Astral base anchored",
        "Circuit production primed"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-pal-fluids"
    ],
    "optional": [
      "resource-sulfur"
    ]
  },
  "failure_recovery": {
    "normal": "Return during daylight with fresh cold gear and mine lighter loads until confidence returns.",
    "hardcore": "If you lose gear, restock polymer and cold armor at home before risking another Astral run."
  },
  "steps": [
    {
      "step_id": "resource-pure-quartz:001",
      "type": "travel",
      "summary": "Unlock PAL Research Tower access",
      "detail": "Climb to the PAL Research Tower statue at roughly (-149,445) so you can fast travel straight onto the snowy slopes leading into Astral Mountain’s Pure Quartz zone.【pcgamesn-bosses†L11-L13】【pcgamesn-pure-quartz†L15-L20】",
      "targets": [],
      "locations": [
        {
          "region_id": "ice-wind-island",
          "coords": [
            -149,
            445
          ],
          "time": "day",
          "weather": "clear"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 90,
        "max": 130
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "travel": [
            "pal-research-tower"
          ]
        }
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses",
        "pcgamesn-pure-quartz"
      ]
    },
    {
      "step_id": "resource-pure-quartz:002",
      "type": "gather",
      "summary": "Mine Astral Mountain ridges",
      "detail": "From the tower, sweep the Astral Mountain ridges for dark grey nodes with silver veins—these are Pure Quartz deposits that require durable pickaxes to break efficiently.【pcgamesn-pure-quartz†L15-L19】【palwiki-pure-quartz†L1-L3】",
      "targets": [
        {
          "kind": "item",
          "id": "pure-quartz",
          "qty": 40
        }
      ],
      "locations": [
        {
          "region_id": "astral-mountain",
          "coords": [
            -149,
            445
          ],
          "time": "day",
          "weather": "snow"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break Pure Quartz nodes"
            },
            {
              "role": "lookout",
              "tasks": "Ping elite patrols and pull aggro away"
            }
          ],
          "loot_rules": "Share Quartz stacks evenly for upcoming crafts"
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 220,
        "max": 300
      },
      "outputs": {
        "items": [
          {
            "item_id": "pure-quartz",
            "qty": 40
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-pure-quartz",
        "palwiki-pure-quartz"
      ]
    },
    {
      "step_id": "resource-pure-quartz:003",
      "type": "base",
      "summary": "Anchor an Astral mining outpost",
      "detail": "Claim a base spot that includes Pure Quartz nodes and assign mining and transport Pals so the deposits respawn into storage while you craft circuit boards on-site.【pcgamesn-pure-quartz†L17-L23】",
      "targets": [
        {
          "kind": "item",
          "id": "pure-quartz",
          "qty": 60
        }
      ],
      "locations": [
        {
          "region_id": "astral-mountain",
          "coords": [
            -149,
            445
          ],
          "time": "any",
          "weather": "snow"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 200,
        "max": 240
      },
      "outputs": {
        "items": [
          {
            "item_id": "pure-quartz",
            "qty": 60
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-pure-quartz"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "pure-quartz",
      "qty": 80
    }
  ],
  "yields": {
    "levels_estimate": "+1",
    "key_unlocks": [
      "circuit-board-production"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-polymer",
      "reason": "Polymer crafting consumes Pure Quartz via Circuit Boards and benefits from the Astral outpost."
    }
  ]
}
```

### Route: Polymer Assembly Workflow

Polymer production ties together high-level tech: unlock the assembly line, farm High Quality Pal Oil from ranch Pals or merchants, then craft batches that feed weapons and circuit chains.【pcgamesn-polymer†L9-L16】【palwiki-polymer†L5-L11】【palwiki-high-quality-pal-oil†L1-L8】

```json
{
  "route_id": "resource-polymer",
  "title": "Polymer Assembly Workflow",
  "category": "resources",
  "tags": [
    "resource-farm",
    "polymer",
    "advanced-crafting",
    "late-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 35,
    "max": 50
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-pure-quartz"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock polymer production tech",
    "Secure a renewable High Quality Pal Oil supply",
    "Craft Polymer batches for weapons and circuits"
  ],
  "estimated_time_minutes": {
    "solo": 28,
    "coop": 18
  },
  "estimated_xp_gain": {
    "min": 360,
    "max": 520
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Wasted oil and tech points slow weapon upgrades if the assembly line idles.",
    "hardcore": "Losing the assembly crew in raids delays late-game gear since polymer feeds every advanced recipe."
  },
  "adaptive_guidance": {
    "underleveled": "Unlock the Production Assembly Line at tech level 33, then run small polymer batches until you stockpile better gear.【pcgamesn-polymer†L9-L13】",
    "overleveled": "Queue long polymer runs overnight with multiple handiwork Pals so weapons and circuit boards never bottleneck.【pcgamesn-polymer†L9-L16】",
    "resource_shortages": [
      {
        "item_id": "high-quality-pal-oil",
        "solution": "Assign Dumud to a Ranch and buy extra oil from merchants before starting long assembly queues.【palwiki-high-quality-pal-oil†L1-L8】"
      }
    ],
    "time_limited": "Craft two quick batches in step :003, then shut down the line to avoid burning precious oil.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:polymer_high",
        "condition": "resource_gaps contains polymer >= 30",
        "adjustment": "Increase batch size in :003 to 6 polymer per queue and reassign an extra handiwork Pal until the gap closes.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-polymer:003"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player wrangle oil deliveries while the other cycles the assembly line UI for nonstop output.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-polymer:002",
          "resource-polymer:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-polymer:checkpoint-tech",
      "summary": "Assembly line unlocked",
      "related_steps": [
        "resource-polymer:001"
      ],
      "benefits": [
        "Production Assembly Line built",
        "Polymer recipe learned"
      ]
    },
    {
      "id": "resource-polymer:checkpoint-oil",
      "summary": "Oil supply secured",
      "related_steps": [
        "resource-polymer:002"
      ],
      "benefits": [
        "Ranch output established",
        "Merchant backup stock"
      ]
    },
    {
      "id": "resource-polymer:checkpoint-batch",
      "summary": "Polymer batch completed",
      "related_steps": [
        "resource-polymer:003"
      ],
      "benefits": [
        "10+ Polymer crafted",
        "Weapons and circuits unblocked"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-pal-fluids"
    ],
    "optional": [
      "resource-sulfur"
    ]
  },
  "failure_recovery": {
    "normal": "Pause the line, restock oil via merchants or ranch, and resume smaller batches until supply stabilises.",
    "hardcore": "Rebuild the assembly line with spare materials and rotate fresh handiwork Pals to avoid chain deaths."
  },
  "steps": [
    {
      "step_id": "resource-polymer:001",
      "type": "build",
      "summary": "Unlock production assembly",
      "detail": "Spend tech points at level 33 to unlock the Production Assembly Line and the Polymer recipe, then place the machine at base with power access.【pcgamesn-polymer†L9-L13】",
      "targets": [
        {
          "kind": "tech",
          "id": "production-assembly-line"
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 110
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "production-assembly-line",
            "polymer-recipe"
          ]
        }
      },
      "branching": [],
      "citations": [
        "pcgamesn-polymer"
      ]
    },
    {
      "step_id": "resource-polymer:002",
      "type": "farm",
      "summary": "Farm High Quality Pal Oil",
      "detail": "Capture Dumud or other listed Pals and station them at a Ranch to generate High Quality Pal Oil, supplementing with merchant purchases as needed.【palwiki-high-quality-pal-oil†L1-L8】",
      "targets": [
        {
          "kind": "item",
          "id": "high-quality-pal-oil",
          "qty": 20
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "rancher",
              "tasks": "Keep Dumud fed and happy"
            },
            {
              "role": "buyer",
              "tasks": "Cycle merchants for extra oil"
            }
          ],
          "loot_rules": "Split oil stacks evenly before crafting"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "dumud"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "high-quality-pal-oil",
            "qty": 20
          }
        ],
        "pals": [
          "dumud"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-high-quality-pal-oil"
      ]
    },
    {
      "step_id": "resource-polymer:003",
      "type": "craft",
      "summary": "Run Polymer batches",
      "detail": "Load the Production Assembly Line with 2 High Quality Pal Oil per craft and assign handiwork Pals to turn the stock into Polymer for weapons and circuit boards.【pcgamesn-polymer†L9-L16】【palwiki-polymer†L5-L11】",
      "targets": [
        {
          "kind": "item",
          "id": "polymer",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 230
      },
      "outputs": {
        "items": [
          {
            "item_id": "polymer",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-polymer",
        "palwiki-polymer"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "polymer",
      "qty": 24
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "polymer-supply"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-late-expansion",
      "reason": "Late-game expansion arcs consume Polymer for weapons and automation upgrades."
    }
  ]
}
```


### Route: Gunpowder Arsenal Chain

Gunpowder keeps firearms running by blending Sulfur from the Mossanda lava ravine with Charcoal burned in your furnaces, then batching everything at the High Quality Workbench so ammunition crafts stay ahead of raids.【pcgamesn-sulfur†L11-L20】【palwiki-charcoal†L1-L7】【palwiki-gunpowder†L1-L1】

```json
{
  "route_id": "resource-gunpowder",
  "title": "Gunpowder Arsenal Chain",
  "category": "resources",
  "tags": [
    "resource-farm",
    "gunpowder",
    "ammo",
    "crafting"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 24,
    "max": 38
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-sulfur",
      "resource-coal"
    ],
    "tech": [
      "high-quality-workbench"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Secure Sulfur and Charcoal inputs",
    "Staff furnaces for Charcoal production",
    "Craft Gunpowder batches for ammo stockpiles"
  ],
  "estimated_time_minutes": {
    "solo": 24,
    "coop": 16
  },
  "estimated_xp_gain": {
    "min": 260,
    "max": 360
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "If Sulfur sits idle you stall ammo queues and waste furnace uptime.",
    "hardcore": "Letting raids hit without gunpowder can cost top-tier weapons and pals."
  },
  "adaptive_guidance": {
    "underleveled": "Loop the Mossanda ravine deposits and Hillside Cavern entrance until you can survive level 30 patrols before pushing deeper.【pcgamesn-sulfur†L11-L19】【pcgamesn-coal†L135-L138】",
    "overleveled": "Stage chests at the Eternal Pyre entrance and Astral ridges so mining pals ferry Sulfur and Coal while you queue gunpowder overnight.【pcgamesn-sulfur†L15-L20】【pcgamesn-coal†L135-L138】",
    "resource_shortages": [
      {
        "item_id": "charcoal",
        "solution": "Feed furnaces with Wood stacks (2 per Charcoal) and keep a Kindling pal assigned so burners never stall.【palwiki-charcoal†L1-L7】"
      }
    ],
    "time_limited": "Skip manual mining and craft from stored Sulfur and Charcoal for a quick 10-minute ammo top-up.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:gunpowder_high",
        "condition": "resource_gaps contains gunpowder >= 60",
        "adjustment": "Queue two batches in step :003 back-to-back and pause new weapon crafts until the deficit clears.【palwiki-gunpowder†L1-L1】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-gunpowder:003"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "One player runs the Sulfur loop while the other tends furnaces and workbench queues, swapping each cycle to manage stamina.【pcgamesn-sulfur†L13-L19】【pcgamesn-coal†L135-L138】",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-gunpowder:001",
          "resource-gunpowder:002",
          "resource-gunpowder:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-gunpowder:checkpoint-stock",
      "summary": "Sulfur and Coal restocked",
      "related_steps": [
        "resource-gunpowder:001"
      ],
      "benefits": [
        "30+ Sulfur banked",
        "Coal piles staged for burning"
      ]
    },
    {
      "id": "resource-gunpowder:checkpoint-burners",
      "summary": "Charcoal burners staffed",
      "related_steps": [
        "resource-gunpowder:002"
      ],
      "benefits": [
        "Continuous Charcoal output",
        "Kindling pals assigned"
      ]
    },
    {
      "id": "resource-gunpowder:checkpoint-queue",
      "summary": "Gunpowder batches queued",
      "related_steps": [
        "resource-gunpowder:003"
      ],
      "benefits": [
        "Ammunition crafting active",
        "Sulfur and Charcoal converted"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-sulfur",
      "resource-coal"
    ],
    "optional": []
  },
  "failure_recovery": {
    "normal": "If stockpiles dip, rerun step :001 and rebuild coal and sulfur caches before restarting production.",
    "hardcore": "Rearm after wipes by restocking inputs first; only resume raids once gunpowder queues are stable."
  },
  "steps": [
    {
      "step_id": "resource-gunpowder:001",
      "type": "gather",
      "summary": "Run Sulfur and Coal loops",
      "detail": "Teleport to Mossanda Forest (234,-118) for Sulfur, then sweep Hillside Cavern at 147,-397 to refill Coal before recalling home; drop overflow in a chest outside the Eternal Pyre entrance.【pcgamesn-sulfur†L13-L19】【pcgamesn-coal†L135-L138】",
      "targets": [
        {
          "kind": "item",
          "id": "sulfur",
          "qty": 30
        },
        {
          "kind": "item",
          "id": "coal",
          "qty": 40
        }
      ],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            234,
            -118
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "windswept-hills",
          "coords": [
            147,
            -397
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break nodes and kite patrols"
            },
            {
              "role": "hauler",
              "tasks": "Collect ore and reset chest staging"
            }
          ],
          "loot_rules": "Divide Sulfur and Coal evenly before leaving the field"
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe",
          "heat-resistant-armor"
        ],
        "pals": [
          "cattiva"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 220
      },
      "outputs": {
        "items": [
          {
            "item_id": "sulfur",
            "qty": 30
          },
          {
            "item_id": "coal",
            "qty": 40
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks sulfur >= 30",
          "action": "include_subroute",
          "subroute_ref": "resource-sulfur"
        },
        {
          "condition": "player lacks coal >= 40",
          "action": "include_subroute",
          "subroute_ref": "resource-coal"
        }
      ],
      "citations": [
        "pcgamesn-sulfur",
        "pcgamesn-coal"
      ]
    },
    {
      "step_id": "resource-gunpowder:002",
      "type": "craft",
      "summary": "Burn Wood into Charcoal",
      "detail": "At base, load any furnace with Wood (2 per Charcoal) and assign a Kindling pal so the burn runs while you haul Sulfur in.【palwiki-charcoal†L1-L7】",
      "targets": [
        {
          "kind": "item",
          "id": "charcoal",
          "qty": 40
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "tender",
              "tasks": "Keep furnaces fed and Kindling pals happy"
            },
            {
              "role": "runner",
              "tasks": "Shuttle Wood and Sulfur from storage"
            }
          ],
          "loot_rules": "Stack Charcoal near the High Quality Workbench"
        }
      },
      "recommended_loadout": {
        "gear": [
          "campfire"
        ],
        "pals": [
          "foxparks"
        ],
        "consumables": [
          "wood"
        ]
      },
      "xp_award_estimate": {
        "min": 70,
        "max": 100
      },
      "outputs": {
        "items": [
          {
            "item_id": "charcoal",
            "qty": 40
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-charcoal"
      ]
    },
    {
      "step_id": "resource-gunpowder:003",
      "type": "craft",
      "summary": "Batch Gunpowder",
      "detail": "Use the High Quality Workbench (or better) to combine 2 Charcoal with 1 Sulfur per craft, queuing 60 units so ammo benches never sit idle.【palwiki-gunpowder†L1-L1】",
      "targets": [
        {
          "kind": "item",
          "id": "gunpowder",
          "qty": 60
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "crafter",
              "tasks": "Maintain workbench queues"
            },
            {
              "role": "supplier",
              "tasks": "Top off Sulfur and Charcoal bins"
            }
          ],
          "loot_rules": "Distribute gunpowder evenly before loading ammo benches"
        }
      },
      "recommended_loadout": {
        "gear": [
          "high-quality-workbench"
        ],
        "pals": [
          "anubis"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 90,
        "max": 140
      },
      "outputs": {
        "items": [
          {
            "item_id": "gunpowder",
            "qty": 60
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-gunpowder"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "gunpowder",
      "qty": 60
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "ammo-stockpile"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Mid-game expansion arcs chew through gunpowder for rifles and launchers."
    }
  ]
}
```

### Route: Sanctuary Bloom Sweep

Wildlife sanctuaries hide the only reliable wild sources of Beautiful Flowers, but trespassing summons PIDF patrols up to level 50, so this route teaches safe landings, Petallia capture chains, and late-game rotations to keep Strange Juice inputs stocked.【fe9924†L1-L20】【f574c5†L5-L24】【ba24e5†L18-L37】

```json
{
  "route_id": "resource-beautiful-flower",
  "title": "Sanctuary Bloom Sweep",
  "category": "resources",
  "tags": [
    "resource-farm",
    "beautiful-flower",
    "wildlife-sanctuary",
    "late-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 30,
    "max": 55
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Secure a safe landing on Wildlife Sanctuary No. 1",
    "Capture Petallia and other flower-dropping Pals",
    "Rotate higher-tier sanctuaries for sustained Beautiful Flower income"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 30
  },
  "estimated_xp_gain": {
    "min": 480,
    "max": 720
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Trespassing alerts trigger PIDF reinforcements that can down you and confiscate loot if you wipe.",
    "hardcore": "Hardcore deaths on sanctuaries mean permanent loss of captured rare Pals and any carried flowers."
  },
  "adaptive_guidance": {
    "underleveled": "Stay near the coastline of No. 1 Sanctuary until you can comfortably handle level-25 patrols before pushing deeper inland.",
    "overleveled": "Once you shrug off level-50 threats, rotate Sanctuaries No. 2 and No. 3 to chain guaranteed Petallia and Lyleen drops.",
    "resource_shortages": [
      {
        "item_id": "beautiful-flower",
        "solution": "Lean on step :002 captures—Petallia guarantees 2-3 Beautiful Flowers per defeat, stabilising stock quickly."
      }
    ],
    "time_limited": "Run the shore perimeter of Sanctuary No. 1, netting Petallia spawns nearest the landing before PIDF heat builds.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to kite PIDF patrols while the other captures Petallia and Ribbuny to keep the drop chain flowing.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-beautiful-flower:002"
        ]
      },
      {
        "signal": "resource_gap:strange-juice_high",
        "condition": "resource_gaps['strange-juice'] >= 10",
        "adjustment": "Queue an extra Sanctuary No. 3 sweep in step :003 so Beautiful Flower stock supports upcoming Strange Juice batches.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-beautiful-flower:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-beautiful-flower:checkpoint-landing",
      "summary": "Sanctuary No. 1 landing secure",
      "benefits": [
        "Coastline safehouse established",
        "PIDF alert window monitored"
      ],
      "related_steps": [
        "resource-beautiful-flower:001"
      ]
    },
    {
      "id": "resource-beautiful-flower:checkpoint-petallia",
      "summary": "Petallia captured",
      "benefits": [
        "Guaranteed flower drops",
        "Grass utility Pal recruited"
      ],
      "related_steps": [
        "resource-beautiful-flower:002"
      ]
    },
    {
      "id": "resource-beautiful-flower:checkpoint-rotation",
      "summary": "Sanctuary rotation online",
      "benefits": [
        "High-tier flower farm unlocked",
        "Level 50 routes vetted"
      ],
      "related_steps": [
        "resource-beautiful-flower:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-pal-fluids"
    ],
    "optional": [
      "resource-honey"
    ]
  },
  "failure_recovery": {
    "normal": "Retreat to the landing chest, clear your wanted level, and restart from step :001 once patrols reset.",
    "hardcore": "Extract immediately when reinforcements arrive; resume with throwaway gear until you rebuild a Petallia roster."
  },
  "steps": [
    {
      "step_id": "resource-beautiful-flower:001",
      "type": "travel",
      "summary": "Approach No. 1 Wildlife Sanctuary",
      "detail": "Glide or sail south to the No. 1 Wildlife Sanctuary (90,-735) and set a shoreline camp. Trespassing warnings summon PIDF forces, so keep encumbrance light for fast extractions.【fe9924†L1-L18】【f574c5†L5-L24】",
      "targets": [],
      "locations": [
        {
          "region_id": "wildlife-sanctuary-1",
          "coords": [
            90,
            -735
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "heat-resistant-armor",
          "cold-resistant-armor"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 160
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-wildlife-sanctuary-1",
        "palwiki-wildlife-sanctuary"
      ]
    },
    {
      "step_id": "resource-beautiful-flower:002",
      "type": "capture",
      "summary": "Farm Petallia and Ribbuny spawns",
      "detail": "Sweep the inner gardens for Petallia and Ribbuny. Petallia always drops 2-3 Beautiful Flowers, while Ribbuny has a 5% flower drop chance—bring fire or dark attackers like Blazehowl or Katress to accelerate clears.【ba24e5†L18-L37】【9be50c†L31-L59】【9f35a4†L31-L56】",
      "targets": [
        {
          "kind": "item",
          "id": "beautiful-flower",
          "qty": 15
        }
      ],
      "locations": [
        {
          "region_id": "wildlife-sanctuary-1",
          "coords": [
            110,
            -720
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "crowd-control",
              "tasks": "Draw PIDF patrols away from capture targets"
            },
            {
              "role": "tamer",
              "tasks": "Capture Petallia/Ribbuny and collect drops"
            }
          ],
          "loot_rules": "Deposit flowers in the shoreline chest between sweeps"
        }
      },
      "recommended_loadout": {
        "gear": [
          "legendary-sphere"
        ],
        "pals": [
          "blazehowl",
          "katress"
        ],
        "consumables": [
          "smoked-meat"
        ]
      },
      "xp_award_estimate": {
        "min": 240,
        "max": 320
      },
      "outputs": {
        "items": [
          {
            "item_id": "beautiful-flower",
            "qty": 15
          }
        ],
        "pals": [
          "petallia"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-beautiful-flower",
        "palwiki-ribbuny",
        "palwiki-petallia"
      ]
    },
    {
      "step_id": "resource-beautiful-flower:003",
      "type": "gather",
      "summary": "Rotate Sanctuaries No. 2 and No. 3",
      "detail": "Graduate to Sanctuary No. 2 (-675,-113) and No. 3 (669,640) for Wumpo Botan and Lyleen runs—level 50 patrols drop guaranteed flowers quickly, so plan fast extractions after each sweep.【ba24e5†L24-L33】【15adf0†L1-L24】【c5acbe†L1-L18】【f574c5†L13-L20】",
      "targets": [
        {
          "kind": "item",
          "id": "beautiful-flower",
          "qty": 25
        }
      ],
      "locations": [
        {
          "region_id": "wildlife-sanctuary-2",
          "coords": [
            -675,
            -113
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "wildlife-sanctuary-3",
          "coords": [
            669,
            640
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "legendary-sphere",
          "heat-resistant-armor"
        ],
        "pals": [
          "faleris"
        ],
        "consumables": [
          "mega-glide-feather"
        ]
      },
      "xp_award_estimate": {
        "min": 320,
        "max": 400
      },
      "outputs": {
        "items": [
          {
            "item_id": "beautiful-flower",
            "qty": 25
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-beautiful-flower",
        "palwiki-wildlife-sanctuary-2",
        "palwiki-wildlife-sanctuary-3",
        "palwiki-wildlife-sanctuary"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "beautiful-flower",
      "qty": 30
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "flower-apothecary"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Beautiful Flowers feed Strange Juice morale buffs for extended automation sessions."
    }
  ]
}
```


### Route: High Quality Pal Oil Hunts

High Quality Pal Oil fuels muskets, polymer, and other mid-game weaponry, so this route secures the Mossanda lava ravine, merchant restocks, and Dumud ranching to keep polymer queues flowing.【9cc14d†L17-L24】【9e983e†L1-L26】

```json
{
  "route_id": "resource-high-quality-pal-oil",
  "title": "High Quality Pal Oil Hunts",
  "category": "resources",
  "tags": [
    "resource-farm",
    "high-quality-pal-oil",
    "mid-game",
    "combat-farm"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 21,
    "max": 35
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "musket"
    ],
    "items": [
      "heat-resistant-armor"
    ],
    "pals": []
  },
  "objectives": [
    "Establish a safe camp at the Mossanda Forest lava ravine",
    "Chain Flambelle clears for High Quality Pal Oil drops",
    "Supplement drops with merchant buys and Dumud ranching"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 30
  },
  "estimated_xp_gain": {
    "min": 260,
    "max": 380
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Heat damage and level 30 patrols near Mossanda Forest can down you, wasting oil runs.",
    "hardcore": "Hardcore wipes in the lava ravine risk permanent loss of Water counters and Polymer fuel stock."
  },
  "adaptive_guidance": {
    "underleveled": "Stay near the statue-side ridge and kite level 10 Flambelle with Water pals until you can push deeper into the ravine.【9cc14d†L17-L21】",
    "overleveled": "Add Woolipop rotations east of Rayne Syndicate Tower between runs to keep oil income ahead of Polymer demand.【9cc14d†L21-L24】【c81b10†L13-L41】",
    "resource_shortages": [
      {
        "item_id": "high-quality-pal-oil",
        "solution": "Alternate Flambelle clears with merchant purchases before starting Polymer batches so stock never bottoms out.【9cc14d†L17-L24】"
      }
    ],
    "time_limited": "Hit the lava ravine for a single ten-minute sweep, bank the drops, then fast travel home before heat attrition stacks.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a vanguard to clear Flambelle while a runner ferries oil to the chest at the statue between pulls.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-high-quality-pal-oil:001",
          "resource-high-quality-pal-oil:002"
        ]
      },
      {
        "signal": "resource_gap:polymer_high",
        "condition": "resource_gaps['polymer'] >= 10",
        "adjustment": "Route oil immediately into Polymer queues once stock exceeds 10 to keep late-game weapons online.【efa13d†L1-L16】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-high-quality-pal-oil:004"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-high-quality-pal-oil:checkpoint-ravine",
      "summary": "Lava ravine staging secured",
      "benefits": [
        "Fast travel anchor established",
        "Heat mitigation checked"
      ],
      "related_steps": [
        "resource-high-quality-pal-oil:001"
      ]
    },
    {
      "id": "resource-high-quality-pal-oil:checkpoint-flambelle",
      "summary": "Flambelle loop profitable",
      "benefits": [
        "High Quality Pal Oil banked",
        "Water pal rotation tuned"
      ],
      "related_steps": [
        "resource-high-quality-pal-oil:002"
      ]
    },
    {
      "id": "resource-high-quality-pal-oil:checkpoint-supply",
      "summary": "Supplemental supply online",
      "benefits": [
        "Merchant restock secured",
        "Dumud ranch producing"
      ],
      "related_steps": [
        "resource-high-quality-pal-oil:003",
        "resource-high-quality-pal-oil:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-polymer"
    ],
    "optional": [
      "resource-sulfur"
    ]
  },
  "failure_recovery": {
    "normal": "Fast travel back to Mossanda Forest, restock Water pals, and rebuild drops before another push.",
    "hardcore": "Withdraw once patrol timers overlap; swap in expendable pals until you re-stabilise oil reserves."
  },
  "steps": [
    {
      "step_id": "resource-high-quality-pal-oil:001",
      "type": "travel",
      "summary": "Scout the Mossanda lava ravine",
      "detail": "Glide from the Mossanda Forest statue to the lava ravine at (231,-119), clear stray patrols, and stage storage near the cliff edge to minimise heat exposure.【9cc14d†L17-L21】",
      "targets": [],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            231,
            -119
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "heat-resistant-armor",
          "water-grenade"
        ],
        "pals": [
          "pengullet"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 180
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-high-quality-pal-oil"
      ]
    },
    {
      "step_id": "resource-high-quality-pal-oil:002",
      "type": "combat",
      "summary": "Farm Flambelle packs",
      "detail": "Pull level 10 Flambelle into the cliff bowl, burst them with Water damage, and scoop guaranteed oil drops before respawns tick back in.【9cc14d†L17-L21】【c3b8c9†L23-L37】",
      "targets": [
        {
          "kind": "item",
          "id": "high-quality-pal-oil",
          "qty": 8
        }
      ],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            231,
            -119
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "vanguard",
              "tasks": "Tank patrols and mark spawn cycles"
            },
            {
              "role": "collector",
              "tasks": "Finish Flambelle with Water skills and loot oil"
            }
          ],
          "loot_rules": "Evenly split oil before leaving the ravine so Polymer queues stay balanced."
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-spear"
        ],
        "pals": [
          "fuack",
          "surfent"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ]
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 220
      },
      "outputs": {
        "items": [
          {
            "item_id": "high-quality-pal-oil",
            "qty": 8
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-high-quality-pal-oil",
        "palwiki-flambelle"
      ]
    },
    {
      "step_id": "resource-high-quality-pal-oil:003",
      "type": "trade",
      "summary": "Restock from merchants",
      "detail": "Fast travel to the Small Settlement (75,-479) and buy spare oil from the Wandering Merchant whenever stock appears to cover polymer spikes.【9cc14d†L19-L24】【165dd8†L71-L90】",
      "targets": [
        {
          "kind": "item",
          "id": "high-quality-pal-oil",
          "qty": 4
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "gold-coin",
            "qty": 600
          }
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "high-quality-pal-oil",
            "qty": 4
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "capture-base-merchant"
        }
      ],
      "citations": [
        "pcgamesn-high-quality-pal-oil",
        "palwiki-small-settlement"
      ]
    },
    {
      "step_id": "resource-high-quality-pal-oil:004",
      "type": "assign",
      "summary": "Ranch Dumud for passive oil",
      "detail": "Capture or breed a Dumud and assign it to your ranch so it produces High Quality Pal Oil while you craft and explore.【9e983e†L1-L26】",
      "targets": [
        {
          "kind": "pal",
          "id": "dumud",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "dumud"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [
          {
            "item_id": "high-quality-pal-oil",
            "qty": 2
          }
        ],
        "pals": [
          "dumud"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-high-quality-pal-oil"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "high-quality-pal-oil",
      "qty": 16
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "polymer-crafting"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-polymer",
      "reason": "Polymer consumes High Quality Pal Oil, so stabilising oil feeds advanced weapon crafting."
    },
    {
      "route_id": "resource-carbon-fiber",
      "reason": "Carbon Fiber runs share assembly infrastructure; pairing them keeps late-game armor rolling."
    }
  ]
}
```

### Route: High Quality Cloth Loom Circuit

High Quality Cloth Loom Circuit clears the Sealed Realm of the Pristine for Sibelyx ranch drops, then spins surplus wool into level-36 cloth batches at the High Quality Workbench to feed late-game armor queues.【palwiki-sibelyx†L1-L64】【palwiki-high-quality-cloth†L1-L26】

```json
{
  "route_id": "resource-high-quality-cloth",
  "title": "High Quality Cloth Loom Circuit",
  "category": "resources",
  "tags": [
    "resource-farm",
    "high-quality-cloth",
    "late-game",
    "armor"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 36,
    "max": 50
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-wool"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock high-tier weaving and stockpile wool",
    "Defeat Sibelyx in the Sealed Realm of the Pristine",
    "Automate High Quality Cloth output via ranching and batch crafts"
  ],
  "estimated_time_minutes": {
    "solo": 48,
    "coop": 32
  },
  "estimated_xp_gain": {
    "min": 620,
    "max": 980
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Wiping in the sealed realm burns spheres and repair kits while you wait on the respawn timer.",
    "hardcore": "Hardcore failure despawns Sibelyx permanently and deletes late-game gear—withdraw if shields break."
  },
  "adaptive_guidance": {
    "underleveled": "Bring fire or electric pals that counter ice to stagger Sibelyx and avoid Blizzard Spike one-shots while you kite its frontal cone.【palwiki-sibelyx†L1-L62】",
    "overleveled": "After unlocking the recipe, convert spare wool piles into cloth between realm rotations so your tailors never idle.【palwiki-high-quality-cloth†L1-L26】",
    "resource_shortages": [
      {
        "item_id": "wool",
        "solution": "Run the resource-wool route again to refill bales before queueing 10-wool crafts for each cloth batch.【palwiki-high-quality-cloth†L17-L24】"
      },
      {
        "item_id": "high-quality-cloth",
        "solution": "Assign Sibelyx to a ranch so its Silk Maker passive produces cloth while workshops finish the remaining workload.【palwiki-sibelyx†L1-L64】"
      }
    ],
    "time_limited": "Skip optional wool crafts and just clear the Sealed Realm once; Sibelyx drops cloth on capture so you can deliver the minimum quota quickly.【palwiki-sibelyx†L1-L62】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player kite Sibelyx around the arena while the partner focuses on breaking its guard and setting up the capture window, then split ranch and crafting duties back at base.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-high-quality-cloth:002",
          "resource-high-quality-cloth:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-high-quality-cloth:checkpoint-blueprint",
      "label": "Weaving tech unlocked",
      "includes": [
        "resource-high-quality-cloth:001"
      ]
    },
    {
      "id": "resource-high-quality-cloth:checkpoint-sibelyx",
      "label": "Sibelyx secured",
      "includes": [
        "resource-high-quality-cloth:002"
      ]
    },
    {
      "id": "resource-high-quality-cloth:checkpoint-loom",
      "label": "Cloth automation online",
      "includes": [
        "resource-high-quality-cloth:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-wool"
    ],
    "optional": [
      "resource-carbon-fiber"
    ]
  },
  "failure_recovery": {
    "normal": "Restock spheres and food, then re-enter once the realm resets; Sibelyx respawns on the next day cycle.",
    "hardcore": "If Hardcore wipes the attempt, pivot to merchant purchases or trade partners while waiting for a friend to host the realm."
  },
  "steps": [
    {
      "step_id": "resource-high-quality-cloth:001",
      "type": "build",
      "summary": "Unlock High Quality Cloth tech",
      "detail": "Spend two technology points at level 36 to unlock High Quality Cloth, place a High Quality Workbench, and queue wool shipments so tailors can work between boss runs.【palwiki-high-quality-cloth†L1-L26】",
      "targets": [
        {
          "kind": "tech",
          "id": "high-quality-cloth"
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "high-quality-workbench"
        ],
        "pals": [],
        "consumables": [
          {
            "item_id": "wool",
            "qty": 50
          }
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "high-quality-cloth"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-high-quality-cloth"
      ]
    },
    {
      "step_id": "resource-high-quality-cloth:002",
      "type": "combat",
      "summary": "Clear Sealed Realm of the Pristine",
      "detail": "Travel to the Sealed Realm of the Pristine (250,70), break Sibelyx’s shield, and capture it for guaranteed cloth drops and the Silk Maker ranch passive.【palwiki-sealed-realms†L44-L48】【palwiki-sibelyx†L1-L64】",
      "targets": [
        {
          "kind": "pal",
          "id": "sibelyx",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "sealed-realm-of-the-pristine",
          "coords": [
            250,
            70
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "vanguard",
              "tasks": "Bait Blizzard Spike and stun Sibelyx with electric or fire skills."
            },
            {
              "role": "controller",
              "tasks": "Heal, reset traps, and secure the capture throw."
            }
          ],
          "loot_rules": "Split cloth drops before leaving the arena."
        }
      },
      "recommended_loadout": {
        "gear": [
          "legendary-sphere",
          "heat-resistant-armor"
        ],
        "pals": [
          "jormuntide-ignis",
          "kitsun"
        ],
        "consumables": [
          {
            "item_id": "repair-kit",
            "qty": 3
          }
        ]
      },
      "xp_award_estimate": {
        "min": 320,
        "max": 520
      },
      "outputs": {
        "items": [
          {
            "item_id": "high-quality-cloth",
            "qty": 1
          }
        ],
        "pals": [
          "sibelyx"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-sealed-realms",
        "palwiki-sibelyx"
      ]
    },
    {
      "step_id": "resource-high-quality-cloth:003",
      "type": "base",
      "summary": "Automate cloth output",
      "detail": "Assign Sibelyx to a Ranch so it periodically produces High Quality Cloth, then craft additional cloth in 10-wool batches at the High Quality Workbench to sustain legendary armor builds.【palwiki-sibelyx†L1-L64】【palwiki-high-quality-cloth†L17-L24】",
      "targets": [
        {
          "kind": "item",
          "id": "high-quality-cloth",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "high-quality-workbench"
        ],
        "pals": [
          "sibelyx",
          "lamball"
        ],
        "consumables": [
          {
            "item_id": "wool",
            "qty": 100
          }
        ]
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 280
      },
      "outputs": {
        "items": [
          {
            "item_id": "high-quality-cloth",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks high-quality-cloth >= 20",
          "action": "repeat"
        }
      ],
      "citations": [
        "palwiki-sibelyx",
        "palwiki-high-quality-cloth"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "high-quality-cloth",
      "qty": 20
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "tailor-upgrades"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-carbon-fiber",
      "reason": "Carbon Fiber and High Quality Cloth combine for legendary armor sets—keep both queues supplied."
    },
    {
      "route_id": "resource-ice-organ",
      "reason": "Sibelyx also drops Ice Organs, so stabilising reagent stock lets you pivot into refrigerator and ammo builds."
    }
  ]
}
```

### Route: Mozzarina Dairy Loop

Milk powers cakes, hot drinks, and early-game sanity food, so this loop builds a Ranch, corrals Mozzarina near the Swordmaster sealed realm, and uses the Small Settlement merchant to keep bottles topped off.【63794d†L1-L14】【69a959†L1-L6】

```json
{
  "route_id": "resource-milk",
  "title": "Mozzarina Dairy Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "milk",
    "ranch",
    "merchant"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 18,
    "max": 32
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "ranch"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock and place a Ranch near storage",
    "Capture Mozzarina grazing by the Swordmaster sealed realm",
    "Automate milk bottles via ranching and merchant restocks"
  ],
  "estimated_time_minutes": {
    "solo": 32,
    "coop": 24
  },
  "estimated_xp_gain": {
    "min": 280,
    "max": 460
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "If patrols down you in Bamboo Groves, Mozzarina despawn and you'll lose gathered milk.",
    "hardcore": "Hardcore wipes in the grove mean permanent gear loss and Mozzarina replacements, so retreat if overwhelmed."
  },
  "adaptive_guidance": {
    "underleveled": "Clear step :002 at dawn when Bamboo Groves spawns are calmer, then leave the Mozzarina grazing until you're strong enough to defend raids.",
    "overleveled": "Bring a capture squad and net two Mozzarina so a spare can rotate in while the first rests at base.",
    "resource_shortages": [
      {
        "item_id": "milk",
        "solution": "Run step :004 merchant purchases between ranch harvests to smooth cake production cycles."
      }
    ],
    "time_limited": "Skip merchant travel and focus on step :003 ranch drops; empty the collection chest every Pal daytime to avoid overflow.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player keep patrols busy in the grove while the partner chains captures and hauls Mozzarina home.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-milk:002"
        ]
      },
      {
        "signal": "resource_gap:honey_high",
        "condition": "resource_gaps['honey'] >= 10",
        "adjustment": "Queue resource-honey once milk stabilises so cake assembly lines don't bottleneck on sweeteners.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-milk:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-milk:checkpoint-ranch",
      "summary": "Ranch foundation placed",
      "benefits": [
        "Milk drop-off area ready",
        "Collection chest staged"
      ],
      "related_steps": [
        "resource-milk:001"
      ]
    },
    {
      "id": "resource-milk:checkpoint-mozzarina",
      "summary": "Mozzarina captured",
      "benefits": [
        "Guaranteed milk producer",
        "Farming work suitability unlocked"
      ],
      "related_steps": [
        "resource-milk:002"
      ]
    },
    {
      "id": "resource-milk:checkpoint-stockpile",
      "summary": "Milk crates filled",
      "benefits": [
        "Cake and hot drink backlog secured",
        "Merchant loop scheduled"
      ],
      "related_steps": [
        "resource-milk:003",
        "resource-milk:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-base-merchant"
    ],
    "optional": [
      "resource-honey"
    ]
  },
  "failure_recovery": {
    "normal": "If the herd flees, rest at a nearby fast travel and return after five minutes; Mozzarina respawn near the Swordmaster arena.",
    "hardcore": "Extract the captured Mozzarina immediately and store them before returning for another try—don't risk chain deaths."
  },
  "steps": [
    {
      "step_id": "resource-milk:001",
      "type": "build",
      "summary": "Unlock and place the Ranch",
      "detail": "Spend 2 technology points at level 5 to unlock the Ranch, then craft it with 50 Wood, 20 Stone, and 30 Fiber next to food storage so milk drops land by your collection chest.【1a1614†L1-L16】",
      "targets": [
        {
          "kind": "tech",
          "id": "ranch"
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Places the Ranch and walls"
            },
            {
              "role": "logistics",
              "tasks": "Feeds wood, stone, and fiber to the builder"
            }
          ],
          "loot_rules": "Deposit spare fiber in the shared chest for future repairs"
        }
      },
      "recommended_loadout": {
        "gear": [
          "stone-axe"
        ],
        "pals": [
          "lamball"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 90,
        "max": 140
      },
      "outputs": {
        "items": [
          {
            "item_id": "ranch",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-ranch"
      ]
    },
    {
      "step_id": "resource-milk:002",
      "type": "capture",
      "summary": "Capture Mozzarina north of the Swordmaster arena",
      "detail": "Glide into the Bamboo Groves herd just north of the Sealed Realm of the Swordmaster (−117, −490). Dark pals burst the neutral mobs quickly while you toss Mega Spheres at two Mozzarina before patrols rotate in from the Ravine Entrance teleport.【69a959†L1-L6】【124c92†L57-L61】",
      "targets": [
        {
          "kind": "pal",
          "id": "mozzarina",
          "qty": 2
        }
      ],
      "locations": [
        {
          "region_id": "bamboo-groves",
          "coords": [
            -117,
            -490
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "crowd-control",
              "tasks": "Kite patrols and clear hostile pals"
            },
            {
              "role": "tamer",
              "tasks": "Stun Mozzarina and throw spheres"
            }
          ],
          "loot_rules": "Store extra Mozzarina meat in the shared pack"
        }
      },
      "recommended_loadout": {
        "gear": [
          "mega-pal-sphere",
          "grappling-gun"
        ],
        "pals": [
          "katress",
          "blazehowl"
        ],
        "consumables": [
          "smoked-meat"
        ]
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 210
      },
      "outputs": {
        "items": [
          {
            "item_id": "mozzarina-meat",
            "qty": 4
          }
        ],
        "pals": [
          "mozzarina"
        ],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks mega-pal-sphere >= 4",
          "action": "include_subroute",
          "subroute_ref": "resource-paldium"
        }
      ],
      "citations": [
        "segmentnext-mozzarina",
        "palwiki-sealed-realms"
      ]
    },
    {
      "step_id": "resource-milk:003",
      "type": "assign",
      "summary": "Staff the Ranch and harvest milk",
      "detail": "Drop one Mozzarina into the Ranch and let it graze—Milk Maker guarantees a bottle every production cycle, and alpha variants keep 100% drop rates as well.【a877d4†L10-L35】",
      "targets": [
        {
          "kind": "item",
          "id": "milk",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "handler",
              "tasks": "Keeps Mozzarina happy and rested"
            },
            {
              "role": "runner",
              "tasks": "Collects bottles and restocks feed"
            }
          ],
          "loot_rules": "Split milk by crafting queue needs"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "mozzarina"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [
          {
            "item_id": "milk",
            "qty": 12
          }
        ],
        "pals": [
          "mozzarina"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-mozzarina"
      ]
    },
    {
      "step_id": "resource-milk:004",
      "type": "trade",
      "summary": "Top up from the Small Settlement merchant",
      "detail": "Ride to the Small Settlement (~75, −479) and buy extra bottles for 100 gold when ranch output lags; consider capturing the merchant later for permanent base access.【63794d†L8-L14】【165dd8†L71-L90】",
      "targets": [
        {
          "kind": "item",
          "id": "milk",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "swift-flyer"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "milk",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-milk",
        "palwiki-small-settlement"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "milk",
      "qty": 24
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "milk-stockpile"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-honey",
      "reason": "Honey pairs with milk for cakes and pastries, so stabilising both keeps cooking queues flowing."
    }
  ]
}
```

### Route: Chikipi Poultry Harvest Loop

Chikipi Poultry Harvest Loop corrals the starter meadow flocks, adds a Meat Cleaver station for humane culling, and keeps a chilled pantry stocked for early cooking chains.【palwiki-chikipi†L9-L13】【palwiki-meat-cleaver†L20-L39】

```json
{
  "route_id": "resource-chikipi-poultry",
  "title": "Chikipi Poultry Harvest Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "chikipi-poultry",
    "cooking",
    "early-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 12,
    "max": 22
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-egg"
    ],
    "tech": [
      "primitive-workbench"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Capture Chikipi near the starter Palbox",
    "Craft a Meat Cleaver and butcher excess birds for poultry",
    "Stage ranch rotations and cold storage to keep poultry flowing"
  ],
  "estimated_time_minutes": {
    "solo": 26,
    "coop": 18
  },
  "estimated_xp_gain": {
    "min": 150,
    "max": 240
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Culling the wrong Pal wastes partner passives and delays poultry restocks until respawns catch up.",
    "hardcore": "Misusing the cleaver can trigger base morale loss and raids, costing you captured layers."
  },
  "adaptive_guidance": {
    "underleveled": "Work within sight of the Palbox so aggroed flocks leash and you can reset without burning spheres.【palwiki-chikipi†L29-L35】",
    "overleveled": "Alternate meadow sweeps with butcher sessions to bank a stack of poultry before raids escalate.【palwiki-chikipi†L29-L35】【palwiki-meat-cleaver†L20-L39】",
    "resource_shortages": [
      {
        "item_id": "chikipi-poultry",
        "solution": "Cull one captured pair per loop after eggs hatch, then let timers refill ranch slots before the next hunt.【palwiki-chikipi†L63-L72】【palwiki-meat-cleaver†L20-L39】"
      }
    ],
    "time_limited": "Do a quick meadow sweep, butcher the surplus, then refrigerate the cuts so cooking can resume later.【palwiki-chikipi†L63-L72】【palwiki-meat-cleaver†L37-L41】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a wrangler to kite flocks into bolas while the butcher keeps the cleaver station clear and stocks the fridge.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-chikipi-poultry:001",
          "resource-chikipi-poultry:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-chikipi-poultry:checkpoint-pen",
      "label": "Capture Pen Stocked",
      "includes": [
        "resource-chikipi-poultry:001"
      ]
    },
    {
      "id": "resource-chikipi-poultry:checkpoint-cleaver",
      "label": "Cleaver Station Online",
      "includes": [
        "resource-chikipi-poultry:002"
      ]
    },
    {
      "id": "resource-chikipi-poultry:checkpoint-pantry",
      "label": "Poultry Pantry Filled",
      "includes": [
        "resource-chikipi-poultry:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-chikipi-poultry:001",
      "type": "capture",
      "summary": "Sweep Palbox meadow for Chikipi",
      "detail": "Teleport to the Windswept Hills statue (~-42,-498) and loop the grass flats, bolaing docile Chikipi before they flock. Scoop ground eggs while you net four prime layers for the ranch.【palwiki-chikipi†L29-L35】",
      "targets": [
        {
          "kind": "pal",
          "id": "chikipi",
          "qty": 4
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            -42,
            -498
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use bolas or Frost Grenades so incidental damage doesn’t snowball into flock aggro.",
          "mode_scope": [
            "hardcore"
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "wrangler",
              "tasks": "Tag birds and keep them corralled near the Palbox"
            },
            {
              "role": "collector",
              "tasks": "Throw Pal Spheres, gather eggs, and rotate catches to base"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "bola"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 110,
        "max": 170
      },
      "outputs": {
        "items": [
          {
            "item_id": "egg",
            "qty": 4
          }
        ],
        "pals": [
          "chikipi"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-chikipi"
      ]
    },
    {
      "step_id": "resource-chikipi-poultry:002",
      "type": "craft",
      "summary": "Forge the Meat Cleaver and butcher extras",
      "detail": "Craft the Meat Cleaver at the Primitive Workbench (5 Ingots, 20 Wood, 5 Stone), then use the Pet command wheel to butcher surplus Chikipi. Each culled bird yields guaranteed poultry for stews—stagger culls to avoid wiping the ranch.【palwiki-meat-cleaver†L20-L39】【palwiki-meat-cleaver†L25-L34】【palwiki-chikipi†L69-L76】",
      "targets": [
        {
          "kind": "item",
          "id": "chikipi-poultry",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Back up save birds with Pal Spheres before butchering so a misclick doesn’t delete your only egg layers.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "meat-cleaver"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 40
      },
      "outputs": {
        "items": [
          {
            "item_id": "chikipi-poultry",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-meat-cleaver",
        "palwiki-chikipi"
      ]
    },
    {
      "step_id": "resource-chikipi-poultry:003",
      "type": "base",
      "summary": "Balance ranch timers and cold storage",
      "detail": "Assign two Chikipi to the ranch for steady eggs, chill butchered poultry in a Cooler Box, and rotate captures each loop so new birds replace those culled for meat.【palwiki-chikipi†L63-L72】",
      "targets": [
        {
          "kind": "item",
          "id": "chikipi-poultry",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "chikipi"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 10,
        "max": 30
      },
      "outputs": {
        "items": [
          {
            "item_id": "chikipi-poultry",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-chikipi"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "chikipi-poultry",
      "qty": 18
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "poultry-stockpile"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-cake",
      "reason": "Cake production relies on poultry for high-quality cooking buffs."
    }
  ]
}
```

### Route: Ore Mining Grid

Ore underpins early metal gear, so this grid stakes the Fort Ruins ridge, anchors a Small Settlement cliff mining base, and keeps Ingots smelting out of automated hauls.【40f7a9†L1-L80】【047054†L18-L24】【951c6f†L6-L16】

```json
{
  "route_id": "resource-ore",
  "title": "Ore Mining Grid",
  "category": "resources",
  "tags": [
    "resource-farm",
    "ore",
    "early-game",
    "mining"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 10,
    "max": 25
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "primitive-furnace"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Secure Fort Ruins ore nodes for manual hauls",
    "Establish a Small Settlement cliff mining base",
    "Deploy mining pals to automate ore income",
    "Smelt ore into Ingots to feed metal crafting"
  ],
  "estimated_time_minutes": {
    "solo": 40,
    "coop": 28
  },
  "estimated_xp_gain": {
    "min": 320,
    "max": 500
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Over-encumbrance makes escape slow; stash ore between nodes to avoid wipes.",
    "hardcore": "Falling while overweight or losing automation pals off the cliff can stall production for days."
  },
  "adaptive_guidance": {
    "underleveled": "Loop the Fort Ruins ridge (155,-394) for four quick nodes before committing to a remote base build.【40f7a9†L1-L36】",
    "overleveled": "Push straight to the Small Settlement cliff (11,-523) and run eight-node automation laps once your pals can tank patrols.【40f7a9†L36-L72】",
    "resource_shortages": [
      {
        "item_id": "ingot",
        "solution": "Run step :004 every haul so mined ore turns into Ingots before weapon upgrades drain stock.【951c6f†L6-L16】"
      }
    ],
    "time_limited": "Mine Fort Ruins once, drop ore in the staging chest, and fast travel home before nodes respawn.【40f7a9†L1-L36】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a miner to break nodes while a hauler ferries loads to the cliff chest so respawns stay on cadence.【40f7a9†L36-L72】",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-ore:001",
          "resource-ore:003"
        ]
      },
      {
        "signal": "resource_gap:ingot_high",
        "condition": "resource_gaps['ingot'] >= 20",
        "adjustment": "Repeat step :004 immediately after each haul until the furnace backlog clears and Ingots hit target.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-ore:004"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-ore:checkpoint-fort",
      "summary": "Fort Ruins ridge cleared",
      "benefits": [
        "Initial ore stock banked",
        "Fast travel anchor confirmed"
      ],
      "related_steps": [
        "resource-ore:001"
      ]
    },
    {
      "id": "resource-ore:checkpoint-base",
      "summary": "Cliff base anchored",
      "benefits": [
        "Palbox and chest staged",
        "Automation pathing stabilised"
      ],
      "related_steps": [
        "resource-ore:002",
        "resource-ore:003"
      ]
    },
    {
      "id": "resource-ore:checkpoint-smelt",
      "summary": "Ingots queued",
      "benefits": [
        "Primitive Furnace active",
        "Ingot reserves replenished"
      ],
      "related_steps": [
        "resource-ore:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-base-merchant"
    ],
    "optional": [
      "resource-coal"
    ]
  },
  "failure_recovery": {
    "normal": "If tools break or packs overflow, store ore at the cliff chest and fast travel home to repair before resuming.",
    "hardcore": "Rotate mining pals out when raids spawn and keep weight under 85% to avoid lethal falls."
  },
  "steps": [
    {
      "step_id": "resource-ore:001",
      "type": "gather",
      "summary": "Mine Fort Ruins ridge",
      "detail": "Fast travel to Fort Ruins (155,-394) and clear the four grey-and-red ore rocks west of the statue, stashing loads in a drop chest to prevent encumbrance.【40f7a9†L1-L36】【047054†L18-L24】",
      "targets": [
        {
          "kind": "item",
          "id": "ore",
          "qty": 20
        }
      ],
      "locations": [
        {
          "region_id": "fort-ruins",
          "coords": [
            155,
            -394
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "stone-pickaxe"
        ],
        "pals": [
          "cattiva"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 170
      },
      "outputs": {
        "items": [
          {
            "item_id": "ore",
            "qty": 20
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-ore-farming",
        "palwiki-ore"
      ]
    },
    {
      "step_id": "resource-ore:002",
      "type": "build",
      "summary": "Anchor the cliff mining base",
      "detail": "Place a Palbox and Wooden Chest on the cliff west of the Small Settlement (11,-523) so every haul drops straight into storage without long walks.【40f7a9†L36-L60】",
      "targets": [
        {
          "kind": "structure",
          "id": "palbox",
          "qty": 1
        },
        {
          "kind": "structure",
          "id": "wooden-chest",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            11,
            -523
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "cattiva"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 110
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "palbox",
            "wooden-chest"
          ]
        }
      },
      "branching": [],
      "citations": [
        "game8-ore-farming"
      ]
    },
    {
      "step_id": "resource-ore:003",
      "type": "assign",
      "summary": "Deploy mining pals and clear pathing",
      "detail": "Bring Digtoise or other Mining level 2 pals, lay foundations over trees, and keep haulers cycling ore into the chest so automation never stalls.【d070f4†L1-L24】",
      "targets": [
        {
          "kind": "pal",
          "id": "digtoise",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            11,
            -523
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break nodes and reset respawns"
            },
            {
              "role": "runner",
              "tasks": "Collect ore and restock the chest"
            }
          ],
          "loot_rules": "Deposit ore evenly before leaving the base"
        }
      },
      "recommended_loadout": {
        "gear": [
          "stone-pickaxe"
        ],
        "pals": [
          "digtoise",
          "cattiva"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "ore",
            "qty": 40
          }
        ],
        "pals": [
          "digtoise"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-ore-farming"
      ]
    },
    {
      "step_id": "resource-ore:004",
      "type": "craft",
      "summary": "Smelt ore into Ingots",
      "detail": "At base, feed ore into the Primitive Furnace—each batch converts two ore into an Ingot that fuels mid-game weapons and armor.【951c6f†L6-L16】",
      "targets": [
        {
          "kind": "item",
          "id": "ingot",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 160
      },
      "outputs": {
        "items": [
          {
            "item_id": "ingot",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-coal"
        }
      ],
      "citations": [
        "palwiki-ingot"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "ore",
      "qty": 60
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "ingot-stockpile"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-carbon-fiber",
      "reason": "Carbon Fiber crafting consumes large Ingot reserves, so stabilising ore keeps armor upgrades rolling."
    }
  ]
}
```

### Route: Flour Milling Network

Flour Milling Network turns the Small Settlement merchant's grain stock into automated Wheat Plantations and a Mill, keeping flour flowing for bakeries and late-game cooking queues.【c6adb4†L34-L114】【af5fcd†L1-L12】【ecbbdd†L1-L16】【bfc9eb†L1-L17】

```json
{
  "route_id": "resource-flour",
  "title": "Flour Milling Network",
  "category": "resources",
  "tags": [
    "resource-farm",
    "flour",
    "agriculture",
    "cooking"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 15,
    "max": 24
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-berry-seeds"
    ],
    "tech": [
      "wheat-plantation",
      "mill"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Purchase Wheat Seeds and starter grain from the Small Settlement merchant",
    "Construct Wheat Plantations and assign planters and waterers",
    "Build a Mill with a Watering Pal to automate grinding",
    "Process harvested wheat into flour reserves"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 22
  },
  "estimated_xp_gain": {
    "min": 180,
    "max": 260
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Losing seed stock delays plantation cycles until merchants restock.",
    "hardcore": "Death in Windswept Hills risks seed stacks; stash extras at base before traveling."
  },
  "adaptive_guidance": {
    "underleveled": "Stick to day runs around Small Settlement to avoid Syndicate patrols while you buy seeds and wood.\u3010c6adb4\u2020L70-L87\u3011\u301014a18a\u2020L6-L13\u3011",
    "overleveled": "Expand to two Wheat Plantations and assign higher-tier planters to keep the mill busy between combat outings.\u3010af5fcd\u2020L1-L12\u3011",
    "resource_shortages": [
      {
        "item_id": "wheat-seeds",
        "solution": "Trigger the resource-berry-seeds subroute or re-buy Wheat Seeds from the Small Settlement merchant when the stock refreshes every day.\u3010c6adb4\u2020L70-L85\u3011",
        "subroute_ref": "resource-berry-seeds"
      },
      {
        "item_id": "flour",
        "solution": "Run step :004 twice before leaving base to keep 40+ flour queued for bakeries.\u3010bfc9eb\u2020L1-L17\u3011"
      }
    ],
    "time_limited": "Buy seeds and wood in one trip, queue a single plantation harvest, and mill only enough flour for the immediate recipe."
  },
  "checkpoints": [
    {
      "id": "resource-flour:checkpoint-merchant",
      "summary": "Seed stock purchased",
      "benefits": [
        "Seeds secured",
        "Merchant route unlocked"
      ],
      "related_steps": [
        "resource-flour:001"
      ]
    },
    {
      "id": "resource-flour:checkpoint-mill",
      "summary": "Mill producing flour",
      "benefits": [
        "Automation running",
        "Flour cached"
      ],
      "related_steps": [
        "resource-flour:003",
        "resource-flour:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-berry-seeds"
    ],
    "optional": [
      "resource-honey"
    ]
  },
  "failure_recovery": {
    "normal": "Revisit the merchant rotation or capture Bristla near Verdant Brook to restock Wheat Seeds if crops die off.",
    "hardcore": "Keep one stack of seeds in a cooled chest so a wipe en route to the Small Settlement doesn't reset progress."
  },
  "steps": [
    {
      "step_id": "resource-flour:001",
      "type": "travel",
      "summary": "Buy Wheat Seeds from the Small Settlement",
      "detail": "Fast travel to the Small Settlement (75,-479), trade with the Wandering Merchant for Wheat Seeds, Wheat, and spare berries so plantations can cycle immediately.\u3010c6adb4\u2020L70-L87\u3011\u301014a18a\u2020L6-L13\u3011",
      "targets": [
        {
          "kind": "item",
          "id": "wheat-seeds",
          "qty": 9
        },
        {
          "kind": "item",
          "id": "wheat",
          "qty": 30
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "buyer",
              "tasks": "Handle trades and ferry seeds"
            },
            {
              "role": "escort",
              "tasks": "Screen Syndicate patrols and haul lumber"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "pal-sphere"
        ],
        "pals": [
          "lamball"
        ],
        "consumables": [
          "gold-coin"
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "wheat-seeds",
            "qty": 9
          },
          {
            "item_id": "wheat",
            "qty": 30
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-berry-seeds"
        }
      ],
      "citations": [
        "palwiki-wandering-merchant",
        "palwiki-small-settlement"
      ]
    },
    {
      "step_id": "resource-flour:002",
      "type": "build",
      "summary": "Raise Wheat Plantations",
      "detail": "Spend 3 Wheat Seeds, 35 Wood, and 35 Stone per plot to build Wheat Plantations, then assign planters, waterers, and gatherers so grain cycles without supervision.\u3010af5fcd\u2020L1-L12\u3011",
      "targets": [
        {
          "kind": "structure",
          "id": "wheat-plantation",
          "qty": 2
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "adjustment": "Assign at least one Watering level 2 Pal so harvests finish before nightly raids.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "bristla",
          "fuack"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [
          {
            "item_id": "wheat",
            "qty": 60
          }
        ],
        "pals": [],
        "unlocks": {
          "structures": [
            "wheat-plantation"
          ]
        }
      },
      "branching": [
        {
          "condition": "player lacks wheat-seeds >= 3",
          "action": "repeat",
          "subroute_ref": "resource-berry-seeds"
        }
      ],
      "citations": [
        "palwiki-wheat-plantation",
        "palwiki-wheat-seeds"
      ]
    },
    {
      "step_id": "resource-flour:003",
      "type": "build",
      "summary": "Construct the Mill",
      "detail": "Unlock the Mill at technology level 15, spend 50 Wood and 40 Stone, and assign a Watering-suited Pal to spin the wheel.\u3010ecbbdd\u2020L1-L16\u3011",
      "targets": [
        {
          "kind": "structure",
          "id": "mill",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "pengullet"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "mill"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-mill"
      ]
    },
    {
      "step_id": "resource-flour:004",
      "type": "craft",
      "summary": "Grind wheat into flour",
      "detail": "Feed harvested Wheat into the Mill in batches of three to produce Flour, then store finished sacks in cooled storage to avoid spoilage.\u3010bfc9eb\u2020L1-L17\u3011\u301015b61b\u2020L1-L11\u3011",
      "targets": [
        {
          "kind": "item",
          "id": "flour",
          "qty": 24
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "fuack"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 100
      },
      "outputs": {
        "items": [
          {
            "item_id": "flour",
            "qty": 24
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-flour",
        "palwiki-wheat"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "flour",
      "qty": 24
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "bakery-supplies"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-cake",
      "reason": "Cake consumes Flour alongside milk, eggs, and honey for breeding."
    },
    {
      "route_id": "resource-bread",
      "reason": "Bread batches stabilize expedition food once flour output is reliable."
    }
  ]
}
```

### Route: Cake Assembly Line

Cake Assembly Line coordinates plantations, ranch automation, and the Cooking Pot so breeding farms always have cakes on hand.【60f5d7†L1-L20】【8f2b7b†L1-L11】【af5fcd†L1-L12】【f8b394†L1-L12】

```json
{
  "route_id": "resource-cake",
  "title": "Cake Assembly Line",
  "category": "resources",
  "tags": [
    "resource-farm",
    "cake",
    "breeding",
    "cooking"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 24,
    "max": 35
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-flour",
      "resource-milk",
      "resource-egg",
      "resource-honey"
    ],
    "tech": [
      "cooking-pot",
      "wheat-plantation",
      "berry-plantation"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Stage plantations and ranchers for cake ingredients",
    "Stabilize honey, milk, egg, and flour throughput",
    "Cook cakes at the Cooking Pot and stock the breeding farm"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 30
  },
  "estimated_xp_gain": {
    "min": 260,
    "max": 360
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Running out of cake slows breeding progress until bakeries restock.",
    "hardcore": "Ingredient deaths in raids can wipe automation; keep backup pals condensed."
  },
  "adaptive_guidance": {
    "underleveled": "Prioritize automation first: set ranchers and plantations before pushing tower fights so breeding never stalls.",
    "overleveled": "Expand to multiple plantations and mills so every breeding cycle consumes from overflow instead of active time.\u3010af5fcd\u2020L1-L12\u3011\u30108f2b7b\u2020L1-L11\u3011",
    "resource_shortages": [
      {
        "item_id": "honey",
        "solution": "Trigger resource-honey to refill Beegarde ranch output."
      },
      {
        "item_id": "milk",
        "solution": "Run resource-milk to restock Mozzarina bottles."
      },
      {
        "item_id": "egg",
        "solution": "Loop resource-egg to refresh ranch production."
      },
      {
        "item_id": "flour",
        "solution": "Re-run resource-flour and keep cooled storage near the Cooking Pot."
      }
    ],
    "time_limited": "Queue one plantation harvest, raid nearby hives for honey, then cook cakes in a single batch before logging off."
  },
  "checkpoints": [
    {
      "id": "resource-cake:checkpoint-farms",
      "summary": "Plantations online",
      "benefits": [
        "Ingredients cycling",
        "Planters assigned"
      ],
      "related_steps": [
        "resource-cake:001"
      ]
    },
    {
      "id": "resource-cake:checkpoint-pantry",
      "summary": "Pantry stocked",
      "benefits": [
        "Honey, milk, eggs buffered",
        "Flour milled"
      ],
      "related_steps": [
        "resource-cake:002",
        "resource-cake:003"
      ]
    },
    {
      "id": "resource-cake:checkpoint-bakery",
      "summary": "First cakes baked",
      "benefits": [
        "Breeding farm supplied",
        "Cooking Pot optimized"
      ],
      "related_steps": [
        "resource-cake:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-flour",
      "resource-milk",
      "resource-egg",
      "resource-honey"
    ],
    "optional": [
      "resource-berry-seeds",
      "resource-high-quality-pal-oil"
    ]
  },
  "failure_recovery": {
    "normal": "Farm Lovander for a slim cake drop chance while automation recovers.\u301060f5d7\u2020L10-L12\u3011",
    "hardcore": "Split ingredient herds across multiple bases so a raid can't depopulate every ranch at once."
  },
  "steps": [
    {
      "step_id": "resource-cake:001",
      "type": "build",
      "summary": "Expand plantations for berries and wheat",
      "detail": "Construct at least one Berry Plantation (3 Berry Seeds, 20 Wood, 20 Stone) and a Wheat Plantation (3 Wheat Seeds, 35 Wood, 35 Stone), then assign planters, waterers, and gatherers.\u30108f2b7b\u2020L1-L11\u3011\u3010af5fcd\u2020L1-L12\u3011",
      "targets": [
        {
          "kind": "structure",
          "id": "berry-plantation",
          "qty": 1
        },
        {
          "kind": "structure",
          "id": "wheat-plantation",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place plots and supply materials"
            },
            {
              "role": "wrangler",
              "tasks": "Assign ranchers and planters"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "bristla",
          "gumoss"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "red-berries",
            "qty": 40
          },
          {
            "item_id": "wheat",
            "qty": 30
          }
        ],
        "pals": [],
        "unlocks": {
          "structures": [
            "berry-plantation",
            "wheat-plantation"
          ]
        }
      },
      "branching": [
        {
          "subroute_ref": "resource-berry-seeds"
        }
      ],
      "citations": [
        "palwiki-berry-plantation",
        "palwiki-wheat-plantation"
      ]
    },
    {
      "step_id": "resource-cake:002",
      "type": "assign",
      "summary": "Stabilize ranch ingredient output",
      "detail": "Keep Chikipi, Mozzarina, and Beegarde assigned to ranches so eggs, milk, and honey flow while bakeries prep. Kick off the linked resource routes if any stockpile dips.\u301060f5d7\u2020L13-L20\u3011",
      "targets": [
        {
          "kind": "item",
          "id": "egg",
          "qty": 24
        },
        {
          "kind": "item",
          "id": "milk",
          "qty": 21
        },
        {
          "kind": "item",
          "id": "honey",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "chikipi",
          "mozzarina",
          "beegarde"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "egg",
            "qty": 24
          },
          {
            "item_id": "milk",
            "qty": 21
          },
          {
            "item_id": "honey",
            "qty": 6
          }
        ],
        "pals": [
          "chikipi",
          "mozzarina",
          "beegarde"
        ],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-egg"
        },
        {
          "subroute_ref": "resource-milk"
        },
        {
          "subroute_ref": "resource-honey"
        }
      ],
      "citations": [
        "palwiki-cake"
      ]
    },
    {
      "step_id": "resource-cake:003",
      "type": "craft",
      "summary": "Mill flour in advance",
      "detail": "Run the Flour Milling Network route or feed harvested wheat into your mill to maintain at least 30 flour on ice ahead of baking sessions.\u3010bfc9eb\u2020L1-L17\u3011",
      "targets": [
        {
          "kind": "item",
          "id": "flour",
          "qty": 30
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "fuack"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 100
      },
      "outputs": {
        "items": [
          {
            "item_id": "flour",
            "qty": 30
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-flour"
        }
      ],
      "citations": [
        "palwiki-flour"
      ]
    },
    {
      "step_id": "resource-cake:004",
      "type": "craft",
      "summary": "Bake cakes at the Cooking Pot",
      "detail": "Build a Cooking Pot (20 Wood, 15 Ingots, 3 Flame Organs) and craft cakes using 5 Flour, 8 Red Berries, 7 Milk, 8 Eggs, and 2 Honey per batch. Store finished cakes in the Breeding Farm chest so they never spoil.\u3010f8b394\u2020L1-L12\u3011\u301060f5d7\u2020L1-L16\u3011",
      "targets": [
        {
          "kind": "item",
          "id": "cake",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "adjustment": "Assign a Cooling Pal to the pantry and keep extra cakes in a safe chest in case of raids.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "heat-resistant-armor"
        ],
        "pals": [
          "flambelle"
        ],
        "consumables": [
          {
            "item_id": "flame-organ",
            "qty": 3
          }
        ]
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "cake",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {
          "structures": [
            "cooking-pot"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-cooking-pot",
        "palwiki-cake"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "cake",
      "qty": 6
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "breeding-efficiency"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "breeding-advanced",
      "reason": "Cakes unlock accelerated Pal breeding cycles."
    },
    {
      "route_id": "resource-carbon-fiber",
      "reason": "Breeding legendary pals benefits from weapon upgrades powered by cakes and polymer."
    }
  ]
}
```

### Route: Tomato Seed Greenhouse Circuit

Tomato Seed Greenhouse Circuit chains the Small Settlement and Duneshelter merchants with Oasis Isle Braloha sweeps, sanctuary alphas (Wumpo Botan, Vaelet), and a Tomato Plantation build so sandwich staples stay stocked.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-duneshelter†L506-L516】【palwiki-braloha-raw†L121-L125】【palwiki-tomato-seeds†L608-L826】【palwiki-vaelet-raw†L108-L116】【palwiki-wumpo-botan-raw†L109-L116】【palwiki-tomato-plantation-raw†L1-L34】

```json
{
  "route_id": "resource-tomato-seeds",
  "title": "Tomato Seed Greenhouse Circuit",
  "category": "resources",
  "tags": [
    "resource-farm",
    "tomato-seeds",
    "agriculture",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 20,
    "max": 35
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-berry-seeds"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Purchase tomato seeds from the Small Settlement and Duneshelter merchants",
    "Sweep Oasis Isle Braloha herds for supplementary drops",
    "Farm Wumpo Botan, Braloha, and Vaelet sanctuary loops for bulk seed stockpiles",
    "Build and automate a Tomato Plantation"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 30
  },
  "estimated_xp_gain": {
    "min": 240,
    "max": 380
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Losing seeds or coins to a wipe forces another merchant run before plantations recover.",
    "hardcore": "Alpha pals in the sanctuary can one-shot lightly geared hunters; retreat rather than risk permadeath."
  },
  "adaptive_guidance": {
    "underleveled": "Loop the Small Settlement and Duneshelter merchants until your squad can stomach sanctuary aggro; both vendors keep Tomato Seeds in stock for 200 gold.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-duneshelter†L506-L516】【palwiki-tomato-seeds†L552-L565】",
    "overleveled": "Once you're comfortable in sanctuaries, alternate Wumpo Botan circuits with Sealed Realm of the Guardian clears to stockpile seeds fast.【palwiki-wumpo-botan-raw†L109-L116】【palwiki-vaelet-raw†L108-L116】【palwiki-tomato-seeds†L608-L826】",
    "resource_shortages": [
      {
        "item_id": "tomato-seeds",
        "solution": "Rotate Wumpo Botan, Oasis Braloha, and the Vaelet alpha before plantations stall to refill the chest in one sweep.【palwiki-wumpo-botan-raw†L109-L116】【palwiki-braloha-raw†L121-L125】【palwiki-vaelet-raw†L108-L116】【palwiki-tomato-seeds†L608-L826】"
      },
      {
        "item_id": "gold-coin",
        "solution": "Carry at least 1,200 gold per loop so you can buy six seeds from both merchants without waiting on restocks.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-tomato-seeds†L552-L565】"
      }
    ],
    "time_limited": "Short on time? Buy a merchant stack, drop the plantation build, and let staffed pals harvest while you're away.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-tomato-plantation-raw†L1-L34】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties so one partner handles merchant runs while the other clears sanctuary targets and ferries seeds home.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-wumpo-botan-raw†L109-L116】【palwiki-vaelet-raw†L108-L116】",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-tomato-seeds:001",
          "resource-tomato-seeds:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-tomato-seeds:checkpoint-merchant",
      "label": "Secure Merchant Stock",
      "includes": [
        "resource-tomato-seeds:001"
      ]
    },
    {
      "id": "resource-tomato-seeds:checkpoint-hunt",
      "label": "Wild Seed Drops",
      "includes": [
        "resource-tomato-seeds:002"
      ]
    },
    {
      "id": "resource-tomato-seeds:checkpoint-plantation",
      "label": "Automate Tomatoes",
      "includes": [
        "resource-tomato-seeds:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-tomato-seeds:001",
      "type": "trade",
      "summary": "Buy Tomato Seeds from settlement and desert merchants",
      "detail": "Fast travel to the Small Settlement (78,-477) for the shared wandering merchant stock, then ride south to Duneshelter (357,347) and clear out the red-coat merchant's Tomato Seeds at 200 gold each before heading into the desert loops.【palwiki-wandering-merchant-raw†L197-L252】【palwiki-duneshelter†L506-L516】【palwiki-tomato-seeds†L552-L565】",
      "targets": [
        {
          "kind": "item",
          "id": "tomato-seeds",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            78,
            -477
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "buyer",
              "tasks": "Handle trades and courier seeds home"
            },
            {
              "role": "scout",
              "tasks": "Watch for patrols and stage wood and stone for builds"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "gold-coin",
            "qty": 1200
          }
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "tomato-seeds",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-wandering-merchant-raw",
        "palwiki-duneshelter",
        "palwiki-tomato-seeds"
      ]
    },
    {
      "step_id": "resource-tomato-seeds:002",
      "type": "hunt",
      "summary": "Chain Wumpo Botan, Braloha, and Vaelet drops",
      "detail": "Sail to No. 2 Wildlife Sanctuary (-675,-113) for Wumpo Botan's guaranteed tomato seed drops, glide east from Duneshelter (357,347) to Oasis Isle to cull Braloha herds at a 50% seed rate, then clear the Sealed Realm of the Guardian (113,-353) for the Vaelet alpha's sanctuary haul before rotating back to merchants.【palwiki-wumpo-botan-raw†L109-L116】【palwiki-tomato-seeds†L608-L826】【palwiki-braloha-raw†L121-L125】【palwiki-duneshelter†L506-L516】【palwiki-vaelet-raw†L108-L116】【palwiki-sealed-guardian†L631-L660】",
      "targets": [
        {
          "kind": "item",
          "id": "tomato-seeds",
          "qty": 14
        }
      ],
      "locations": [
        {
          "region_id": "wildlife-sanctuary-2",
          "coords": [
            -675,
            -113
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "twilight-dunes",
          "coords": [
            357,
            347
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "astral-mountain",
          "coords": [
            113,
            -353
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Prioritise captures to avoid prolonged brawls with sanctuary elites, using smoke or freeze pals to disengage when multiple targets converge.",
          "mode_scope": [
            "hardcore"
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "controller",
              "tasks": "Snare Wumpo Botan and Braloha while tagging Vaelet's adds"
            },
            {
              "role": "finisher",
              "tasks": "Secure captures and ferry seeds or loot back to camp"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "heat-resistant-armor",
          "grappling-gun"
        ],
        "pals": [
          "surfent",
          "kitsun"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 10
          }
        ]
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 260
      },
      "outputs": {
        "items": [
          {
            "item_id": "tomato-seeds",
            "qty": 14
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-wumpo-botan-raw",
        "palwiki-tomato-seeds",
        "palwiki-braloha-raw",
        "palwiki-duneshelter",
        "palwiki-vaelet-raw",
        "palwiki-sealed-guardian"
      ]
    },
    {
      "step_id": "resource-tomato-seeds:003",
      "type": "build",
      "summary": "Construct and staff a Tomato Plantation",
      "detail": "Spend 3 Tomato Seeds, 70 Wood, 50 Stone, and 5 Pal Fluids to place a Tomato Plantation, then assign Planting, Watering, and Gathering pals so tomatoes flow between merchant runs and sanctuary sweeps.【palwiki-tomato-plantation-raw†L1-L34】【palwiki-tomato-seeds†L847-L868】",
      "targets": [
        {
          "kind": "station",
          "id": "tomato-plantation"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place the plantation and restock building materials"
            },
            {
              "role": "quartermaster",
              "tasks": "Assign Planting and Watering pals and manage the harvest chest"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "wooden-hammer"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 100
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "tomato-plantation"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-tomato-plantation-raw",
        "palwiki-tomato-seeds"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "tomato-seeds",
      "qty": 15
    },
    {
      "type": "build-station",
      "station_id": "tomato-plantation"
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "tomato-supply"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-lettuce-seeds",
      "reason": "Pair tomato harvests with lettuce beds to cover every salad and sandwich recipe."
    }
  ]
}
```

### Route: Lettuce Seed Hydroponics

Lettuce Seed Hydroponics buys Small Settlement stock, loops Wumpo Botan sanctuaries alongside forest Bristla, and automates a Lettuce Plantation for late-tier meals.【cf6b68†L1-L4】【fb8f93†L1-L2】【ca10a8†L1-L6】【bb2b70†L1-L7】【ec48c2†L1-L5】

```json
{
  "route_id": "resource-lettuce-seeds",
  "title": "Lettuce Seed Hydroponics",
  "category": "resources",
  "tags": [
    "resource-farm",
    "lettuce-seeds",
    "agriculture",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 25,
    "max": 40
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-berry-seeds"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Purchase lettuce seeds from the Small Settlement merchant",
    "Harvest sanctuary Wumpo Botan and forest Bristla for extra seeds",
    "Build and automate a Lettuce Plantation"
  ],
  "estimated_time_minutes": {
    "solo": 40,
    "coop": 28
  },
  "estimated_xp_gain": {
    "min": 260,
    "max": 420
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Dropping seed stacks to aggressive pals wastes the 200 gold spend and resets plantation cycles.",
    "hardcore": "Sanctuary elites and alpha bosses can wipe an unprepared crew; disengage rather than risking permanent losses."
  },
  "adaptive_guidance": {
    "underleveled": "Lean on merchant purchases and pacifist Bristla forests until your team can absorb sanctuary hits.【cf6b68†L1-L4】【bb2b70†L1-L7】",
    "overleveled": "Farm No. 2 Wildlife Sanctuary on repeat; Wumpo Botan provide both Lettuce and Tomato Seeds while Dinossom Lux tops up extras.【fb8f93†L1-L2】【ca10a8†L1-L6】",
    "resource_shortages": [
      {
        "item_id": "lettuce-seeds",
        "solution": "Rotate between the sanctuary Wumpo Botan spawn and Bristla forest patrols to refill reserves before plantations stall.【ca10a8†L1-L6】【fb8f93†L1-L2】【bb2b70†L1-L7】"
      }
    ],
    "time_limited": "Grab a handful of merchant seeds and drop the plantation; you can return later for sanctuary hunting.【cf6b68†L1-L4】【ec48c2†L1-L5】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties so one player escorts seeds while the other clears sanctuary packs and keeps the boat ready for extraction.【fb8f93†L1-L2】",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-lettuce-seeds:001",
          "resource-lettuce-seeds:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-lettuce-seeds:checkpoint-merchant",
      "label": "Secure Merchant Supply",
      "includes": [
        "resource-lettuce-seeds:001"
      ]
    },
    {
      "id": "resource-lettuce-seeds:checkpoint-hunt",
      "label": "Wild Drops",
      "includes": [
        "resource-lettuce-seeds:002"
      ]
    },
    {
      "id": "resource-lettuce-seeds:checkpoint-plantation",
      "label": "Automate Lettuce",
      "includes": [
        "resource-lettuce-seeds:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-lettuce-seeds:001",
      "type": "trade",
      "summary": "Buy Lettuce Seeds from the Small Settlement merchant",
      "detail": "Visit the Small Settlement vendor to buy Lettuce Seeds for 200 gold each while restocking wood and stone for the plantation build.【cf6b68†L1-L4】【c6adb4†L34-L114】【165dd8†L71-L90】",
      "targets": [
        {
          "kind": "item",
          "id": "lettuce-seeds",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            78,
            -477
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "buyer",
              "tasks": "Handle trades and haul seeds"
            },
            {
              "role": "quartermaster",
              "tasks": "Pre-stage construction mats and ferry them home"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          "gold-coin"
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "lettuce-seeds",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-lettuce-seeds-fandom",
        "palwiki-wandering-merchant",
        "palwiki-small-settlement"
      ]
    },
    {
      "step_id": "resource-lettuce-seeds:002",
      "type": "hunt",
      "summary": "Loop sanctuary Wumpo Botan and Bristla forests",
      "detail": "Farm No. 2 Wildlife Sanctuary (-675,-113) for Wumpo Botan, then sweep Verdant Brook forests where Bristla mingle with Cinnamoth to top off Lettuce Seeds without elite pressure.【fb8f93†L1-L2】【ca10a8†L1-L6】【bb2b70†L1-L7】【15adf0†L1-L22】",
      "targets": [
        {
          "kind": "item",
          "id": "lettuce-seeds",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "wildlife-sanctuary-2",
          "coords": [
            -675,
            -113
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Capture instead of KO to avoid long fights, and evacuate if multiple sanctuary mobs converge.",
          "mode_scope": [
            "hardcore"
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "controller",
              "tasks": "Peel Wumpo Botan away from guards"
            },
            {
              "role": "runner",
              "tasks": "Deliver seed stacks to the boat and scout Bristla groves"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 230
      },
      "outputs": {
        "items": [
          {
            "item_id": "lettuce-seeds",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-wumpo-botan",
        "palwiki-wumpo-botan-habitat",
        "palwiki-lettuce-seeds-fandom",
        "palwiki-bristla",
        "palwiki-wildlife-sanctuary-2"
      ]
    },
    {
      "step_id": "resource-lettuce-seeds:003",
      "type": "build",
      "summary": "Construct and staff a Lettuce Plantation",
      "detail": "Invest 3 Lettuce Seeds, 100 Wood, 70 Stone, and 10 Pal Fluids into a Lettuce Plantation, then assign Planting, Watering, and Gathering pals to keep greens flowing.【ec48c2†L1-L5】【23bbf1†L1-L3】【fb8486†L1-L4】",
      "targets": [
        {
          "kind": "station",
          "id": "lettuce-plantation"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place the plantation and refresh inputs"
            },
            {
              "role": "quartermaster",
              "tasks": "Assign watering pals and manage produce storage"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "wooden-hammer"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 90,
        "max": 110
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "lettuce-plantation"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-lettuce-plantation",
        "palwiki-lettuce-seeds",
        "palwiki-lettuce"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "lettuce-seeds",
      "qty": 15
    },
    {
      "type": "build-station",
      "station_id": "lettuce-plantation"
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "lettuce-supply"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-milk",
      "reason": "Lettuce pairs with milk and tomatoes for salad and sandwich production once dairies are online."
    }
  ]
}
```

### Route: Bone Forager Loop

Bone Forager Loop hunts Windswept Hills Rushoar packs, spins up ranch pals, and leans on the Small Settlement merchant so cement and medicine queues never stall.【palfandom-bone†L36-L55】【palwiki-windswept-hills†L7-L22】【palwiki-small-settlement†L3-L15】

```json
{
  "route_id": "resource-bone",
  "title": "Bone Forager Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "bone",
    "crafting-material",
    "early-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 8,
    "max": 25
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Stage Windswept Hills bone hunts around the Small Settlement",
    "Capture ranch pals that produce bones automatically",
    "Use merchants to top off bone stockpiles for cement and medicine"
  ],
  "estimated_time_minutes": {
    "solo": 35,
    "coop": 25
  },
  "estimated_xp_gain": {
    "min": 200,
    "max": 320
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Death on hill patrols wastes bones and gold, forcing you to restock before cement batches resume.",
    "hardcore": "Hardcore wipes while farming Sakurajima elites cost irreplaceable ranch producers and stall medicine crafting."
  },
  "adaptive_guidance": {
    "underleveled": "Loop the Plateau of Beginnings near the Small Settlement and focus on Vixy or Rushoar pairs until you can safely branch into night hunts.【palwiki-windswept-hills†L14-L21】【palfandom-bone†L36-L55】",
    "overleveled": "Layer in Sakurajima Sootseer sweeps at night before returning to the hills so ranch automation keeps up with late-game demand.【palwiki-sootseer†L12-L16】【palwiki-sootseer†L114-L114】",
    "resource_shortages": [
      {
        "item_id": "bone",
        "solution": "Keep at least one ranch slot staffed with a bone producer before launching long expeditions.【palwiki-bone†L20-L27】"
      }
    ],
    "time_limited": "Buy merchant bones on each Small Settlement pass, then bank the haul before leaving for tower runs.【palwiki-small-settlement†L3-L15】【palwiki-bone†L22-L27】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player tag Rushoar aggro while the partner finishes captures and ferries bones to storage.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-bone:001"
        ]
      },
      {
        "signal": "resource_gap:cement_high",
        "condition": "resource_gaps['cement'] >= 5",
        "adjustment": "Push merchant buys to hit at least 30 bones before swapping back to building queues.【palwiki-bone†L20-L27】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-bone:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-bone:checkpoint-hunt",
      "summary": "Hill patrol loop established",
      "benefits": [
        "Reliable bone drops online",
        "Merchant access secured"
      ],
      "related_steps": [
        "resource-bone:001"
      ]
    },
    {
      "id": "resource-bone:checkpoint-ranch",
      "summary": "Ranch automation producing",
      "benefits": [
        "Vixy or Sootseer assigned",
        "Passive bones flowing"
      ],
      "related_steps": [
        "resource-bone:002"
      ]
    },
    {
      "id": "resource-bone:checkpoint-stockpile",
      "summary": "Stockpile topped off",
      "benefits": [
        "Merchant bones stashed",
        "Cement queue unblocked"
      ],
      "related_steps": [
        "resource-bone:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-ore"
    ],
    "optional": []
  },
  "failure_recovery": {
    "normal": "Restock healing items, revisit the Small Settlement statue, and resume short Rushoar loops before venturing farther.",
    "hardcore": "Retreat once patrol timers overlap; rely on ranch output until Hardcore-safe escorts are ready."
  },
  "steps": [
    {
      "step_id": "resource-bone:001",
      "type": "travel",
      "summary": "Stage Small Settlement bone hunts",
      "detail": "Fast travel to the Small Settlement (75,-479), clear poachers, then circle the surrounding Plateau of Beginnings to defeat or capture Rushoar and Vixy for guaranteed bones.【palwiki-small-settlement†L3-L15】【palwiki-windswept-hills†L14-L21】【palwiki-rushoar†L65-L76】【palfandom-bone†L36-L55】",
      "targets": [
        {
          "kind": "item",
          "id": "bone",
          "qty": 8
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "vanguard",
              "tasks": "Tag Rushoar packs and keep aggro off the merchant camp"
            },
            {
              "role": "collector",
              "tasks": "Capture weakened pals and ferry bones to storage"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-spear"
        ],
        "pals": [
          "lamball"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ]
      },
      "xp_award_estimate": {
        "min": 90,
        "max": 140
      },
      "outputs": {
        "items": [
          {
            "item_id": "bone",
            "qty": 8
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-ore"
        }
      ],
      "citations": [
        "palwiki-small-settlement",
        "palwiki-windswept-hills",
        "palwiki-rushoar",
        "palfandom-bone"
      ]
    },
    {
      "step_id": "resource-bone:002",
      "type": "assign",
      "summary": "Put ranch pals on bone duty",
      "detail": "Bring captured Vixy back to base so Dig Here! feeds bones and arrows, then add a Sakurajima Sootseer once you can handle night patrols for guaranteed ranch bones.【palwiki-vixy†L9-L49】【palfandom-bone†L36-L55】【palwiki-sootseer†L12-L16】【palwiki-sootseer†L114-L114】",
      "targets": [
        {
          "kind": "pal",
          "id": "vixy",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Capture rather than KO night spawns and retreat if patrol overlap stacks heat and dark damage.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "vixy"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [
          {
            "item_id": "bone",
            "qty": 4
          }
        ],
        "pals": [
          "vixy"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-vixy",
        "palfandom-bone",
        "palwiki-sootseer",
        "palwiki-bone"
      ]
    },
    {
      "step_id": "resource-bone:003",
      "type": "trade",
      "summary": "Buy out wandering merchants",
      "detail": "Spend spare gold at the Small Settlement wandering merchant for 100G bones whenever you bank a hunt, keeping cement queues topped up.【palwiki-small-settlement†L3-L15】【palwiki-bone†L20-L27】",
      "targets": [
        {
          "kind": "item",
          "id": "bone",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "quartermaster",
              "tasks": "Handle trades and refresh gold"
            },
            {
              "role": "runner",
              "tasks": "Escort merchant goods back to base"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "gold-coin",
            "qty": 600
          }
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "bone",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "capture-base-merchant"
        }
      ],
      "citations": [
        "palwiki-small-settlement",
        "palwiki-bone"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "bone",
      "qty": 30
    },
    {
      "type": "have-pal",
      "pal_id": "vixy",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "cement-batches"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-early-foundation",
      "reason": "Bones fuel Cement and medicine stockpiles that power the early base expansion chain."
    }
  ]
}
```

### Route: Nail Fabrication Chain

Nail Fabrication Chain locks in level 10 tech, smelts ore into ingots, and automates workbench plus assembly line batches so construction upgrades stay ahead of base demand.【palwiki-nail†L3-L33】【game8-nail†L102-L124】

```json
{
  "route_id": "resource-nail",
  "title": "Nail Fabrication Chain",
  "category": "resources",
  "tags": [
    "resource-farm",
    "nail",
    "construction",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 10,
    "max": 30
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-ore"
    ],
    "tech": [
      "primitive-furnace",
      "primitive-workbench"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock Nail tech at level 10 and stock an ingot backlog",
    "Craft nails at workbenches using the 1 ingot to 2 nails recipe",
    "Scale into Production Assembly Line batches for construction projects"
  ],
  "estimated_time_minutes": {
    "solo": 40,
    "coop": 28
  },
  "estimated_xp_gain": {
    "min": 180,
    "max": 260
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Losing ores or ingots slows early building unlocks until mines are restocked.",
    "hardcore": "Hardcore deaths while hauling ore can wipe tech unlock progress and stall weapon upgrades."
  },
  "adaptive_guidance": {
    "underleveled": "Prioritise the level 10 tech unlock, then smelt a starter batch of ingots before expanding the queue.【palwiki-nail†L13-L22】【game8-nail†L118-L124】",
    "overleveled": "Unlock the Production Assembly Line as soon as you have spare power cores so nail batches keep up with mid-game structures.【game8-nail†L111-L117】",
    "resource_shortages": [
      {
        "item_id": "nail",
        "solution": "Maintain a 2:1 ingot-to-nail conversion cycle so base expansions never stall.【palwiki-nail†L3-L33】"
      }
    ],
    "time_limited": "Craft nails in short workbench bursts each time you return from ore runs to avoid idle furnaces.【game8-nail†L118-L124】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split roles so one player smelts ingots while the other queues nails and delivers materials to construction sites.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-nail:001",
          "resource-nail:002"
        ]
      },
      {
        "signal": "resource_gap:ingot_low",
        "condition": "resource_gaps['ingot'] <= 10",
        "adjustment": "Pause workbench crafting until the furnace rebuilds at least 20 spare ingots for the next batch.【game8-nail†L118-L124】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-nail:001"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-nail:checkpoint-furnace",
      "summary": "Ingot backlog secured",
      "benefits": [
        "Primitive Furnace running",
        "Ore supply stabilised"
      ],
      "related_steps": [
        "resource-nail:001"
      ]
    },
    {
      "id": "resource-nail:checkpoint-workbench",
      "summary": "Workbench production online",
      "benefits": [
        "Nail batches crafted",
        "Construction queue primed"
      ],
      "related_steps": [
        "resource-nail:002"
      ]
    },
    {
      "id": "resource-nail:checkpoint-assembly",
      "summary": "Assembly line scaling",
      "benefits": [
        "Production Assembly Line placed",
        "Automation powered"
      ],
      "related_steps": [
        "resource-nail:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-ore"
    ],
    "optional": []
  },
  "failure_recovery": {
    "normal": "Run quick ore hauls and rebuild ingot stacks before queuing more nails.",
    "hardcore": "Deposit ingots between batches and rotate spare builders so Hardcore wipes do not reset progress."
  },
  "steps": [
    {
      "step_id": "resource-nail:001",
      "type": "craft",
      "summary": "Unlock Nail tech and smelt ingots",
      "detail": "Reach level 10, spend the tech point on Nail, and keep a Primitive Furnace smelting ore into ingots for upcoming batches.【palwiki-nail†L13-L22】【game8-nail†L118-L124】",
      "targets": [
        {
          "kind": "item",
          "id": "ingot",
          "qty": 20
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "smelter",
              "tasks": "Feed ore into the furnace and monitor fuel"
            },
            {
              "role": "hauler",
              "tasks": "Deliver ore from storage and bank finished ingots"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 70,
        "max": 100
      },
      "outputs": {
        "items": [
          {
            "item_id": "ingot",
            "qty": 20
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-ore"
        }
      ],
      "citations": [
        "palwiki-nail",
        "game8-nail"
      ]
    },
    {
      "step_id": "resource-nail:002",
      "type": "craft",
      "summary": "Forge nails at workbenches",
      "detail": "Queue nails at a Primitive or High Quality Workbench, converting one ingot into two nails per recipe cycle.【palwiki-nail†L3-L33】【game8-nail†L102-L124】",
      "targets": [
        {
          "kind": "item",
          "id": "nail",
          "qty": 40
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "crafter",
              "tasks": "Operate the workbench and manage tech point spend"
            },
            {
              "role": "supplier",
              "tasks": "Refill ingots and haul finished nails to storage"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 110
      },
      "outputs": {
        "items": [
          {
            "item_id": "nail",
            "qty": 40
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-nail",
        "game8-nail"
      ]
    },
    {
      "step_id": "resource-nail:003",
      "type": "build",
      "summary": "Automate nails with an assembly line",
      "detail": "Place a Production Assembly Line once unlocked so ingot deliveries turn into bulk nail batches without tying up handcrafting time.【game8-nail†L111-L117】【palwiki-nail†L3-L17】",
      "targets": [
        {
          "kind": "station",
          "id": "production-assembly-line"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place the line and power sources"
            },
            {
              "role": "engineer",
              "tasks": "Assign handiwork pals and route ingot deliveries"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "wooden-hammer"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "production-assembly-line"
          ]
        }
      },
      "branching": [],
      "citations": [
        "game8-nail",
        "palwiki-nail"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "nail",
      "qty": 80
    },
    {
      "type": "build-station",
      "station_id": "production-assembly-line"
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "base-construction"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Nail throughput feeds the mid-expansion building chain for walls, chests, and automation benches."
    }
  ]
}
```

### Route: Refined Ingot Forge Cycle

Refined Ingot Forge Cycle anchors an Improved Furnace hub on the Desiccated Desert ridge, pipelines ore and coal into double-node quarries, and keeps refined metal batches flowing for mid-game construction.【segmentnext-refined-ingot†L2-L5】

```json
{
  "route_id": "resource-refined-ingot",
  "title": "Refined Ingot Forge Cycle",
  "category": "resources",
  "tags": [
    "resource-farm",
    "refined-ingot",
    "metal",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 34,
    "max": 48
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-ore",
      "resource-coal"
    ],
    "tech": [
      "improved-furnace"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock Improved Furnace and Refined Ingot tech at level 34",
    "Stage a mining outpost at (191,-36) that feeds ore and coal simultaneously",
    "Smelt refined ingots continuously to buffer mid-game upgrades"
  ],
  "estimated_time_minutes": {
    "solo": 55,
    "coop": 38
  },
  "estimated_xp_gain": {
    "min": 280,
    "max": 380
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Letting the furnace go dark wastes mined ore and slows construction unlocks until stockpiles recover.",
    "hardcore": "Hardcore wipes in the desert ridge cost mining pals and tech progress, delaying improved furnace output."
  },
  "adaptive_guidance": {
    "underleveled": "Rush level 34, then drop your Improved Furnace on the (191,-36) ridge so you can mine coal and ore without deep desert fights.【segmentnext-refined-ingot†L2-L5】",
    "overleveled": "Chain multiple Improved Furnaces and maintain a 2:2 ore-to-coal delivery loop so refined ingot batches stay ahead of building demand.【palwiki-refined-ingot†L1-L6】【segmentnext-refined-ingot†L4-L5】",
    "resource_shortages": [
      {
        "item_id": "coal",
        "solution": "Keep a hauler rota working the ridge at (191,-36) before queueing more furnace batches.【segmentnext-refined-ingot†L5-L5】"
      },
      {
        "item_id": "refined-ingot",
        "solution": "Each refined ingot consumes 2 Ore and 2 Coal—rebuild the ratio before resuming hand-ins.【palwiki-refined-ingot†L1-L6】"
      }
    ],
    "time_limited": "Smelt in short bursts every time you return to the ridge so the furnace never idles between expeditions.【segmentnext-refined-ingot†L4-L4】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to cycle ore/coal hauls while the partner runs furnace queues and maintenance.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-refined-ingot:001",
          "resource-refined-ingot:003"
        ]
      },
      {
        "signal": "resource_gap:coal_low",
        "condition": "resource_gaps['coal'] <= 20",
        "adjustment": "Trigger the resource-coal subroute or rotate fresh mining pals before resuming furnace work.【segmentnext-refined-ingot†L5-L5】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-refined-ingot:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-refined-ingot:checkpoint-site",
      "summary": "Ridge outpost established",
      "benefits": [
        "Improved Furnace frame placed",
        "Hauler pals staged"
      ],
      "related_steps": [
        "resource-refined-ingot:001"
      ]
    },
    {
      "id": "resource-refined-ingot:checkpoint-feed",
      "summary": "Ore and coal loop stabilised",
      "benefits": [
        "Dual-node mining active",
        "Storage buffers topped"
      ],
      "related_steps": [
        "resource-refined-ingot:002"
      ]
    },
    {
      "id": "resource-refined-ingot:checkpoint-stockpile",
      "summary": "Refined ingots banked",
      "benefits": [
        "Mid-game upgrades funded",
        "Assembly inputs secured"
      ],
      "related_steps": [
        "resource-refined-ingot:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-refined-ingot:001",
      "type": "build",
      "summary": "Unlock and place an Improved Furnace",
      "detail": "Hit level 34, spend tech points on both Refined Ingot and the Improved Furnace, then blueprint the furnace on the ore/coal ridge. Bring 100 Stone, 30 Cement, and 15 Flame Organs to finish construction.【segmentnext-refined-ingot†L2-L3】",
      "targets": [
        {
          "kind": "station",
          "id": "improved-furnace"
        }
      ],
      "locations": [
        {
          "region_id": "desiccated-desert",
          "coords": [
            191,
            -36
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place the furnace frame and handle tech spend"
            },
            {
              "role": "supplier",
              "tasks": "Ferry stone, cement, and flame organs from base"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [
          "digtoise",
          "tombat"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 160
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "stations": [
            "improved-furnace"
          ]
        }
      },
      "branching": [
        {
          "subroute_ref": "resource-coal"
        }
      ],
      "citations": [
        "segmentnext-refined-ingot"
      ]
    },
    {
      "step_id": "resource-refined-ingot:002",
      "type": "gather",
      "summary": "Mine ore and coal from the ridge",
      "detail": "Cycle mining pals through the (191,-36) plateau so coal nodes and ore boulders refill storage between furnace batches.【segmentnext-refined-ingot†L5-L5】",
      "targets": [
        {
          "kind": "item",
          "id": "ore",
          "qty": 120
        },
        {
          "kind": "item",
          "id": "coal",
          "qty": 120
        }
      ],
      "locations": [
        {
          "region_id": "desiccated-desert",
          "coords": [
            191,
            -36
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Break nodes and rotate pals"
            },
            {
              "role": "hauler",
              "tasks": "Keep storage chests clear and feed the furnace"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [
          "digtoise",
          "tombat"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 130,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "ore",
            "qty": 120
          },
          {
            "item_id": "coal",
            "qty": 120
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-ore"
        },
        {
          "subroute_ref": "resource-coal"
        }
      ],
      "citations": [
        "segmentnext-refined-ingot"
      ]
    },
    {
      "step_id": "resource-refined-ingot:003",
      "type": "craft",
      "summary": "Smelt refined ingots in batches",
      "detail": "Queue refined ingots at the Improved Furnace, feeding 2 Ore and 2 Coal per bar so construction stockpiles stay ahead of blueprints.【palwiki-refined-ingot†L1-L6】【segmentnext-refined-ingot†L4-L4】",
      "targets": [
        {
          "kind": "item",
          "id": "refined-ingot",
          "qty": 60
        }
      ],
      "locations": [
        {
          "region_id": "desiccated-desert",
          "coords": [
            191,
            -36
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "stoker",
              "tasks": "Assign Kindling pals and refresh fuel"
            },
            {
              "role": "quartermaster",
              "tasks": "Balance ore and coal inputs between furnaces"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "refined-ingot",
            "qty": 60
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-refined-ingot",
        "segmentnext-refined-ingot"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-station",
      "station_id": "improved-furnace"
    },
    {
      "type": "have-item",
      "item_id": "refined-ingot",
      "qty": 60
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "refined-ingot-supply"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-late-expansion",
      "reason": "Late-expansion structures consume refined ingots in bulk for automation benches."
    },
    {
      "route_id": "resource-pal-metal-ingot",
      "reason": "Pal Metal Ingots demand refined stockpiles to build the Electric Furnace frame."
    }
  ]
}
```

### Route: Pal Metal Alloy Grid

Pal Metal Alloy Grid upgrades your forge to electric tier, loops ore and Paldium into alloy batches, and supplements production with late-game Pal drops so legendary weapon queues never stall.【palwiki-pal-metal-ingot†L1-L3】【fandom-pal-metal-ingot†L1-L4】

```json
{
  "route_id": "resource-pal-metal-ingot",
  "title": "Pal Metal Alloy Grid",
  "category": "resources",
  "tags": [
    "resource-farm",
    "pal-metal-ingot",
    "late-game",
    "metal"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 44,
    "max": 55
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-refined-ingot",
      "resource-paldium"
    ],
    "tech": [
      "electric-furnace",
      "power-generator"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Construct and power the Electric Furnace at level 44",
    "Stabilise ore and Paldium fragment supply for alloying",
    "Smelt Pal Metal Ingots and reinforce stock with elite Pal drops"
  ],
  "estimated_time_minutes": {
    "solo": 60,
    "coop": 42
  },
  "estimated_xp_gain": {
    "min": 320,
    "max": 450
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Losing alloy stockpiles forces another long Paldium and ore grind before late-game gear resumes.",
    "hardcore": "Hardcore wipes while farming Pal Metal drops risk irreplaceable high-level pals and generator repairs."
  },
  "adaptive_guidance": {
    "underleveled": "Bank refined ingots and tech points before level 44 so the Electric Furnace and generator frame go up in one trip.【palwiki-electric-furnace†L1-L5】",
    "overleveled": "Once alloy batches flow, rotate into Astegon or Necromus hunts to add guaranteed Pal Metal drops for legendary queues.【fandom-pal-metal-ingot†L1-L4】",
    "resource_shortages": [
      {
        "item_id": "paldium-fragment",
        "solution": "Trigger the resource-paldium subroute or run riverbank loops until you refill at least 80 fragments.【palwiki-paldium†L42-L71】"
      },
      {
        "item_id": "pal-metal-ingot",
        "solution": "Each bar consumes 4 Ore and 2 Paldium fragments—balance smelts with mining runs before queueing late-game gear.【palwiki-pal-metal-ingot†L1-L3】"
      }
    ],
    "time_limited": "Craft Pal Metal Ingots in bursts while the generator is fuelled to avoid power waste between batches.【palwiki-pal-metal-ingot†L1-L3】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties so one player manages generators and electricity while the other smelts and ferries alloy stock.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-pal-metal-ingot:001",
          "resource-pal-metal-ingot:003"
        ]
      },
      {
        "signal": "resource_gap:paldium-fragment_low",
        "condition": "resource_gaps['paldium-fragment'] <= 20",
        "adjustment": "Pause smelting and rerun resource-paldium to rebuild fragments before draining ore stock.【palwiki-paldium†L42-L71】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-pal-metal-ingot:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-pal-metal-ingot:checkpoint-electric",
      "summary": "Electric Furnace online",
      "benefits": [
        "Generator wired",
        "Fire pals assigned"
      ],
      "related_steps": [
        "resource-pal-metal-ingot:001"
      ]
    },
    {
      "id": "resource-pal-metal-ingot:checkpoint-alloy",
      "summary": "Alloy feed secured",
      "benefits": [
        "Ore buffer stabilised",
        "Paldium fragments stocked"
      ],
      "related_steps": [
        "resource-pal-metal-ingot:002"
      ]
    },
    {
      "id": "resource-pal-metal-ingot:checkpoint-drops",
      "summary": "Pal Metal drops unlocked",
      "benefits": [
        "Elite hunts on rotation",
        "Legendary craft queue primed"
      ],
      "related_steps": [
        "resource-pal-metal-ingot:004"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-pal-metal-ingot:001",
      "type": "build",
      "summary": "Construct and power the Electric Furnace",
      "detail": "Spend level-44 tech points on the Electric Furnace, deliver 50 Refined Ingots, 10 Circuit Boards, 20 Polymer, and 20 Carbon Fiber, then wire it into a Power Generator and assign a high-tier fire Pal to light it.【palwiki-electric-furnace†L1-L5】",
      "targets": [
        {
          "kind": "station",
          "id": "electric-furnace"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "engineer",
              "tasks": "Place the furnace, run cables, and manage generators"
            },
            {
              "role": "quartermaster",
              "tasks": "Deliver refined ingots, polymer, and boards"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "jormuntide-ignis"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 210
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "stations": [
            "electric-furnace"
          ]
        }
      },
      "branching": [
        {
          "subroute_ref": "resource-refined-ingot"
        }
      ],
      "citations": [
        "palwiki-electric-furnace"
      ]
    },
    {
      "step_id": "resource-pal-metal-ingot:002",
      "type": "gather",
      "summary": "Stockpile ore and Paldium fragments",
      "detail": "Loop the desert ridge for ore while triggering resource-paldium runs so fragment reserves stay ahead of 4 Ore + 2 Paldium alloy batches.【segmentnext-refined-ingot†L5-L5】【palwiki-paldium†L42-L71】【palwiki-pal-metal-ingot†L1-L3】",
      "targets": [
        {
          "kind": "item",
          "id": "ore",
          "qty": 160
        },
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 80
        }
      ],
      "locations": [
        {
          "region_id": "desiccated-desert",
          "coords": [
            191,
            -36
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Harvest ore and refill generators"
            },
            {
              "role": "runner",
              "tasks": "Complete Paldium fragment loops and resupply the furnace"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [
          "digtoise",
          "tombat"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "ore",
            "qty": 160
          },
          {
            "item_id": "paldium-fragment",
            "qty": 80
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-ore"
        },
        {
          "subroute_ref": "resource-paldium"
        }
      ],
      "citations": [
        "segmentnext-refined-ingot",
        "palwiki-paldium",
        "palwiki-pal-metal-ingot"
      ]
    },
    {
      "step_id": "resource-pal-metal-ingot:003",
      "type": "craft",
      "summary": "Smelt Pal Metal Ingots",
      "detail": "Feed 4 Ore and 2 Paldium Fragments into the Electric Furnace per bar, keeping generators powered so late-game armor and weapon blueprints stay supplied.【palwiki-pal-metal-ingot†L1-L3】【fandom-pal-metal-ingot†L1-L4】",
      "targets": [
        {
          "kind": "item",
          "id": "pal-metal-ingot",
          "qty": 40
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "smelter",
              "tasks": "Queue alloy batches and manage power"
            },
            {
              "role": "logistics",
              "tasks": "Refill ore, fragments, and cooling supplies"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 240
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-metal-ingot",
            "qty": 40
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-pal-metal-ingot",
        "fandom-pal-metal-ingot"
      ]
    },
    {
      "step_id": "resource-pal-metal-ingot:004",
      "type": "hunt",
      "summary": "Farm elite Pal Metal drops",
      "detail": "Rotate Astegon, Necromus, Paladius, and Shadowbeak hunts so guaranteed Pal Metal drops top off alloy storage between furnace cycles.【fandom-pal-metal-ingot†L1-L4】",
      "targets": [
        {
          "kind": "pal",
          "id": "astegon",
          "qty": 1
        },
        {
          "kind": "pal",
          "id": "necromus",
          "qty": 1
        },
        {
          "kind": "pal",
          "id": "paladius",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "astral-mountain",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Bring ranged pals and heavy shields to mitigate alpha burst damage while farming drops.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 220,
        "max": 300
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-metal-ingot",
            "qty": 20
          }
        ],
        "pals": [
          "astegon"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "fandom-pal-metal-ingot"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-station",
      "station_id": "electric-furnace"
    },
    {
      "type": "have-item",
      "item_id": "pal-metal-ingot",
      "qty": 40
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "pal-metal-stockpile"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-carbon-fiber",
      "reason": "Production Assembly Lines and carbon fiber stockpiles consume refined alloy frames."
    },
    {
      "route_id": "purposeful-arc-legendary-push",
      "reason": "Legendary push plans consume large Pal Metal batches for endgame armor and weapons."
    },
    {
      "route_id": "purposeful-arc-late-expansion",
      "reason": "Late expansion automation benches rely on Pal Metal alloys and powered factories."
    }
  ]
}
```

### Route: Carbon Fiber Filament Works

Carbon Fiber Filament Works unlocks the Production Assembly Line, pipelines coal and charcoal inputs, and keeps fiber batches rolling so late-game armor and weapon queues never stall.【palwiki-production-assembly-line†L1-L35】【palwiki-carbon-fiber†L13-L40】【palfandom-carbon-fiber†L86-L110】

```json
{
  "route_id": "resource-carbon-fiber",
  "title": "Carbon Fiber Filament Works",
  "category": "resources",
  "tags": [
    "resource-farm",
    "carbon-fiber",
    "manufacturing",
    "late-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 34,
    "max": 44
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-refined-ingot",
      "resource-coal",
      "resource-gunpowder"
    ],
    "tech": [
      "production-assembly-line"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock and build the Production Assembly Line",
    "Stabilise coal and charcoal inputs for filament batches",
    "Automate carbon fiber production and top up with legendary drops"
  ],
  "estimated_time_minutes": {
    "solo": 55,
    "coop": 38
  },
  "estimated_xp_gain": {
    "min": 280,
    "max": 420
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Letting the assembly line sit idle wastes ingots, nails, and cement that took hours to stockpile.",
    "hardcore": "Hardcore wipes during ridge mining can strand your coal haulers and stall the entire fiber supply chain."
  },
  "adaptive_guidance": {
    "underleveled": "Bank the 100 Ingots, 20 Nails, and 10 Cement before hitting level 28 so the line goes up in one construction cycle.【palwiki-production-assembly-line†L8-L45】",
    "overleveled": "Rotate Jetragon or Shadowbeak hunts between craft batches so their guaranteed drops patch any coal shortages.【palfandom-carbon-fiber†L108-L110】",
    "resource_shortages": [
      {
        "item_id": "carbon-fiber",
        "solution": "Each craft costs 2 Coal or 5 Charcoal—match queue sizes to your mining throughput before loading the hopper.【palwiki-carbon-fiber†L13-L40】【palfandom-carbon-fiber†L86-L110】"
      }
    ],
    "time_limited": "Burn through a stored Charcoal crate for a 20-piece batch when you only have minutes before a raid.【palwiki-carbon-fiber†L37-L40】【palwiki-charcoal†L22-L31】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to the Astral ridge mining loop while another staffs the assembly line and ferries wood for Charcoal.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-carbon-fiber:002",
          "resource-carbon-fiber:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-carbon-fiber:checkpoint-line",
      "label": "Assembly Line Framed",
      "includes": [
        "resource-carbon-fiber:001"
      ]
    },
    {
      "id": "resource-carbon-fiber:checkpoint-feedstock",
      "label": "Coal & Charcoal Stocked",
      "includes": [
        "resource-carbon-fiber:002"
      ]
    },
    {
      "id": "resource-carbon-fiber:checkpoint-batch",
      "label": "Fiber Batches Queued",
      "includes": [
        "resource-carbon-fiber:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-carbon-fiber:001",
      "type": "build",
      "summary": "Construct the Production Assembly Line",
      "detail": "Spend 3 tech points at level 28 to unlock the Production Assembly Line, then deliver 100 Ingots, 50 Wood, 20 Nails, and 10 Cement so three handiwork pals can staff the station without downtime.【palwiki-production-assembly-line†L8-L35】",
      "targets": [
        {
          "kind": "station",
          "id": "production-assembly-line"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "wooden-hammer"
        ],
        "pals": [
          "anubis"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "production-assembly-line"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-production-assembly-line"
      ]
    },
    {
      "step_id": "resource-carbon-fiber:002",
      "type": "gather",
      "summary": "Mine Astral ridge coal and cook backup Charcoal",
      "detail": "Set Digtoise and Tombat crews on the (191,-36) ridge so ore and coal flow together, then keep furnaces burning Wood at a 2:1 ratio for Charcoal to buffer outages.【segmentnext-refined-ingot†L2-L5】【palwiki-charcoal†L22-L31】",
      "targets": [
        {
          "kind": "item",
          "id": "coal",
          "qty": 60
        },
        {
          "kind": "item",
          "id": "charcoal",
          "qty": 40
        }
      ],
      "locations": [
        {
          "region_id": "astral-mountain",
          "coords": [
            191,
            -36
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shielded pals to soak alpha breath attacks while miners ferry loads back to base.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-pickaxe"
        ],
        "pals": [
          "digtoise",
          "tombat",
          "blazamut"
        ],
        "consumables": [
          "wood"
        ]
      },
      "xp_award_estimate": {
        "min": 200,
        "max": 260
      },
      "outputs": {
        "items": [
          {
            "item_id": "coal",
            "qty": 60
          },
          {
            "item_id": "charcoal",
            "qty": 40
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "resource-coal"
        }
      ],
      "citations": [
        "segmentnext-refined-ingot",
        "palwiki-charcoal"
      ]
    },
    {
      "step_id": "resource-carbon-fiber:003",
      "type": "craft",
      "summary": "Queue carbon fiber batches",
      "detail": "Assign handiwork pals to the Assembly Line, feed it 2 Coal or 5 Charcoal per craft, and backfill with Jetragon or Shadowbeak drops when queues spike for late-game weapons.【palwiki-carbon-fiber†L13-L40】【palfandom-carbon-fiber†L86-L110】",
      "targets": [
        {
          "kind": "item",
          "id": "carbon-fiber",
          "qty": 60
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "crafter",
              "tasks": "Manage queues and swap handiwork pals"
            },
            {
              "role": "supplier",
              "tasks": "Refuel coal crates and stage Charcoal"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "anubis",
          "grizzbolt"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 220
      },
      "outputs": {
        "items": [
          {
            "item_id": "carbon-fiber",
            "qty": 60
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "purposeful-arc-legendary-push"
        }
      ],
      "citations": [
        "palwiki-carbon-fiber",
        "palfandom-carbon-fiber"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-station",
      "station_id": "production-assembly-line"
    },
    {
      "type": "have-item",
      "item_id": "carbon-fiber",
      "qty": 60
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "carbon-fiber-stockpile"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-legendary-push",
      "reason": "Legendary weapon and armor queues consume large carbon fiber stacks."
    },
    {
      "route_id": "purposeful-arc-late-expansion",
      "reason": "Factory expansions rely on carbon fiber components once assembly lines are online."
    }
  ]
}
```

### Route: Electric Organ Relay Circuit

Electric Organ Relay Circuit strings together Rayne Syndicate Tower hunting loops and Small Settlement restocks so Sparkit and Jolthog drops never fall behind power-generation demand.【9565e9†L3-L14】【eec516†L5-L14】【9565e9†L60-L66】

```json
{
  "route_id": "resource-electric-organ",
  "title": "Electric Organ Relay Circuit",
  "category": "resources",
  "tags": [
    "resource-farm",
    "electric-organ",
    "early-game",
    "combat-farm"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 8,
    "max": 24
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Stage the Bridge of the Twin Knights hunting lane",
    "Chain Sparkit and Jolthog clears for organ drops",
    "Top up organ stock from Small Settlement merchants"
  ],
  "estimated_time_minutes": {
    "solo": 25,
    "coop": 18
  },
  "estimated_xp_gain": {
    "min": 240,
    "max": 360
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Deaths near the tower spawn you at distant statues and cost transport time and repair bills.",
    "hardcore": "Hardcore wipes drop your early electric pals and any organs you hauled back toward base."
  },
  "adaptive_guidance": {
    "underleveled": "Glide down from Rayne Syndicate Tower and kite Sparkit toward the bridge while Water pals soak their attacks before committing to longer loops.【9565e9†L11-L14】【eec516†L5-L9】",
    "overleveled": "Rotate a Twilight Dunes sweep between bridge runs so higher-level Sparkit chains keep pace with late-game conductor crafting.【eec516†L5-L7】",
    "resource_shortages": [
      {
        "item_id": "electric-organ",
        "solution": "Buy the merchant’s 200-gold stock after every hunt to buffer against unlucky Sparkit drops.【9565e9†L6-L8】【eec516†L9-L14】"
      }
    ],
    "time_limited": "Run a single bridge lap, fast travel home, and bank the organs so you always leave with net profit.【9565e9†L11-L14】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a vanguard to tag Sparkit while a collector handles finishing blows and loot ferries back to the statue chest.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-electric-organ:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-electric-organ:checkpoint-scout",
      "summary": "Bridge lane scouted",
      "benefits": [
        "Sparkit patrols marked",
        "Respawn anchor set"
      ],
      "related_steps": [
        "resource-electric-organ:001"
      ]
    },
    {
      "id": "resource-electric-organ:checkpoint-hunt",
      "summary": "Sparkit loop cleared",
      "benefits": [
        "Electric organ stack secured",
        "Jolthog route learned"
      ],
      "related_steps": [
        "resource-electric-organ:002"
      ]
    },
    {
      "id": "resource-electric-organ:checkpoint-supply",
      "summary": "Merchant restock complete",
      "benefits": [
        "Gold stock converted",
        "Base stores replenished"
      ],
      "related_steps": [
        "resource-electric-organ:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-paldium"
    ],
    "optional": [
      "capture-base-merchant"
    ]
  },
  "failure_recovery": {
    "normal": "Respawn at Rayne Tower, rehydrate, and resume bridge pulls once armor is repaired.",
    "hardcore": "Withdraw after each loop to deposit organs; don’t risk a Hardcore wipe carrying full stacks." 
  },
  "steps": [
    {
      "step_id": "resource-electric-organ:001",
      "type": "travel",
      "summary": "Stage the Rayne tower descent",
      "detail": "Fast travel to Rayne Syndicate Tower Entrance (~112,-434), glide toward Bridge of the Twin Knights, and flag Sparkit patrol nodes before the farming loop begins.【9565e9†L11-L14】【825211382965329†L103-L118】",
      "targets": [],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            112,
            -434
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "glider"
        ],
        "pals": [
          "pengullet"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-electric-organ",
        "dexerto-electric-organ",
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "resource-electric-organ:002",
      "type": "combat",
      "summary": "Loop Sparkit and Jolthog packs",
      "detail": "Work the bridge ridge, burst Sparkit and Jolthog, fast travel to reset spawns, and repeat until you bank at least a dozen electric organs from guaranteed drops.【9565e9†L11-L14】【9565e9†L60-L66】【eec516†L5-L7】",
      "targets": [
        {
          "kind": "item",
          "id": "electric-organ",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            112,
            -434
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "vanguard",
              "tasks": "Tag Sparkit and juggle aggro"
            },
            {
              "role": "collector",
              "tasks": "Finish weakened targets and loot organs"
            }
          ],
          "loot_rules": "Split organs based on polymer and generator queues"
        }
      },
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "pengullet",
          "eikthyrdeer"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ]
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 210
      },
      "outputs": {
        "items": [
          {
            "item_id": "electric-organ",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-electric-organ",
        "dexerto-electric-organ"
      ]
    },
    {
      "step_id": "resource-electric-organ:003",
      "type": "trade",
      "summary": "Buy out the Small Settlement vendor",
      "detail": "Visit the Small Settlement merchant (~73,-485) after each hunt and spend 200 gold per organ to pad reserves while wandering stock lasts.【9565e9†L6-L8】【eec516†L9-L14】",
      "targets": [
        {
          "kind": "item",
          "id": "electric-organ",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "gold-coin",
            "qty": 1200
          }
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "electric-organ",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "capture-base-merchant"
        }
      ],
      "citations": [
        "game8-electric-organ",
        "dexerto-electric-organ"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "electric-organ",
      "qty": 20
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "power-generator"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-flame-organ",
      "reason": "Fire and electric reagents pair for polymer and generator upgrades."
    }
  ]
}
```

### Route: Wheat Seed Field Logistics

Wheat Seed Field Logistics threads merchant buys with Dinossom and Flopie patrols so Wheat Plantations stay stocked for flour production.【46c54c†L9-L21】【a05a80†L1-L13】【b1cc9c†L1-L2】

```json
{
  "route_id": "resource-wheat-seeds",
  "title": "Wheat Seed Field Logistics",
  "category": "resources",
  "tags": [
    "resource-farm",
    "wheat-seeds",
    "agriculture",
    "early-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 14,
    "max": 28
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-berry-seeds"
    ],
    "tech": [
      "wheat-plantation"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Purchase Wheat Seeds from the Small Settlement merchant",
    "Farm Dinossom and Flopie near Rayne Tower for drops",
    "Build and automate a Wheat Plantation"
  ],
  "estimated_time_minutes": {
    "solo": 32,
    "coop": 24
  },
  "estimated_xp_gain": {
    "min": 180,
    "max": 300
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Dropping seed stacks to aggressive mobs forces another merchant run before plantations recover.",
    "hardcore": "Bridge-of-the-Twin-Knights patrols hit level 20+, so a wipe can cost your entire seed stock and high-level pals."
  },
  "adaptive_guidance": {
    "underleveled": "Stay on the merchant rotation until you unlock the Wheat Plantation at tech level 15, stocking seeds without provoking the level-20 bridge patrols.【46c54c†L9-L21】",
    "overleveled": "Chain Dinossom's 50% Wheat Seed drop with Flopie loops beyond the bridge to overstock plantations between tech pushes.【46c54c†L9-L17】【b1cc9c†L1-L2】",
    "resource_shortages": [
      {
        "item_id": "wheat-seeds",
        "solution": "Alternate between Small Settlement purchases and Rayne tower hunts so plantations never stall on reseed stock.【46c54c†L12-L17】【a05a80†L1-L13】"
      }
    ],
    "time_limited": "Buy a handful of seeds, drop a plantation, and let automation roll while you focus on other objectives.【46c54c†L18-L21】【54c140†L1-L9】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to escort the merchant haul while the other clears Flopie and Dinossom patrols northeast of Rayne Tower for steady drops.【46c54c†L9-L17】",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-wheat-seeds:001",
          "resource-wheat-seeds:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-wheat-seeds:checkpoint-merchant",
      "label": "Merchant Stock Secured",
      "includes": [
        "resource-wheat-seeds:001"
      ]
    },
    {
      "id": "resource-wheat-seeds:checkpoint-hunt",
      "label": "Field Drops Collected",
      "includes": [
        "resource-wheat-seeds:002"
      ]
    },
    {
      "id": "resource-wheat-seeds:checkpoint-plantation",
      "label": "Plantation Online",
      "includes": [
        "resource-wheat-seeds:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-wheat-seeds:001",
      "type": "trade",
      "summary": "Buy Wheat Seeds from the Small Settlement merchant",
      "detail": "Fast travel to the Small Settlement (~75,-479) and buy at least nine Wheat Seeds from the wandering merchant for 100 gold each whenever they appear, keeping spare stacks for reseeds.【46c54c†L12-L16】【4d9312†L12-L14】【bda51b†L1-L4】",
      "targets": [
        {
          "kind": "item",
          "id": "wheat-seeds",
          "qty": 9
        }
      ],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            75,
            -479
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "buyer",
              "tasks": "Handle trades and ferry seeds back to base"
            },
            {
              "role": "lookout",
              "tasks": "Scout for patrols and restock wood and stone"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          "gold-coin"
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [
          {
            "item_id": "wheat-seeds",
            "qty": 9
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-wheat-seeds",
        "palwiki-wandering-merchant",
        "palwiki-small-settlement"
      ]
    },
    {
      "step_id": "resource-wheat-seeds:002",
      "type": "hunt",
      "summary": "Farm Dinossom and Flopie for field drops",
      "detail": "Stage at Rayne Syndicate Tower Entrance (~112,-434), sweep the surrounding Windswept Hills for Dinossom's 50% Wheat Seed drops, then glide northeast across the Bridge of the Twin Knights to capture Flopie packs for additional seeds.【ca82d7†L1-L4】【46c54c†L9-L17】【b1cc9c†L1-L2】【a05a80†L1-L13】",
      "targets": [
        {
          "kind": "item",
          "id": "wheat-seeds",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            112,
            -434
          ],
          "time": "day",
          "weather": "any"
        },
        {
          "region_id": "verdant-brook",
          "coords": [
            140,
            -410
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Stick to captures and kite patrols toward the bridge choke point so level-20 mobs can't surround you.",
          "mode_scope": [
            "hardcore"
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "controller",
              "tasks": "Weaken Dinossom and Flopie targets and keep them snared"
            },
            {
              "role": "courier",
              "tasks": "Collect drops and reset patrol paths while monitoring weight"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "crossbow"
        ],
        "pals": [
          "gumoss",
          "fuddler"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "wheat-seeds",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses",
        "pcgamesn-wheat-seeds",
        "palwiki-dinossom",
        "palwiki-wheat-seeds"
      ]
    },
    {
      "step_id": "resource-wheat-seeds:003",
      "type": "build",
      "summary": "Construct and staff a Wheat Plantation",
      "detail": "Spend 3 Wheat Seeds, 35 Wood, and 35 Stone to place a Wheat Plantation, then assign Planting and Watering pals to keep grain flowing into mills.【46c54c†L18-L21】【54c140†L1-L9】",
      "targets": [
        {
          "kind": "station",
          "id": "wheat-plantation"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Place the plantation and restock construction materials"
            },
            {
              "role": "quartermaster",
              "tasks": "Assign planters/waterers and manage grain storage"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "wooden-hammer"
        ],
        "pals": [
          "lamball",
          "pengullet"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 110
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "structures": [
            "wheat-plantation"
          ]
        }
      },
      "branching": [],
      "citations": [
        "pcgamesn-wheat-seeds",
        "palwiki-wheat-plantation"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "wheat-seeds",
      "qty": 18
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "wheat-plantation-automation"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-flour",
      "reason": "Flour Milling Network consumes Wheat harvested here for bakery chains."
    },
    {
      "route_id": "resource-cake",
      "reason": "Cake Assembly Line requires steady Wheat and Flour stocks for breeding."
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-berry-seeds"
    ],
    "optional": [
      "resource-milk"
    ]
  },
  "failure_recovery": {
    "normal": "If seed stacks are lost, circle back to the Small Settlement vendor or sweep nearby Dinossom until you restock.",
    "hardcore": "Bank extra seeds in cold storage before crossing the bridge so a wipe doesn't reset your plantation cycle."
  }
}
```

### Route: Flame Organ Kiln Loop

Flame Organ Kiln Loop keeps Foxparks sweeps, Flambelle ranching, and merchant buys in sync so furnaces and cooking pots never stall.【cf6c22†L3-L8】【5531dc†L2-L9】【cf6c22†L56-L65】

```json
{
  "route_id": "resource-flame-organ",
  "title": "Flame Organ Kiln Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "flame-organ",
    "early-game",
    "ranch"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 10,
    "max": 28
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "ranch"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Farm Foxparks near spawn for rapid organ drops",
    "Assign Flambelle to the ranch for passive production",
    "Supplement supply by purchasing Small Settlement stock"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 22
  },
  "estimated_xp_gain": {
    "min": 220,
    "max": 340
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Being downed near Rayne Tower wastes time jogging back to the Foxparks trail.",
    "hardcore": "Hardcore wipes can cost your Flambelle rancher and reset organ automation." 
  },
  "adaptive_guidance": {
    "underleveled": "Stick to the Grassy Behemoth Hills and Rayne Tower entrance path where Foxparks are easy kills with basic bows.【5531dc†L2-L6】",
    "overleveled": "Add Mount Obsidian Flambelle sweeps to feed ranch assignments as you scale into mid-game heat tech.【5531dc†L7-L8】",
    "resource_shortages": [
      {
        "item_id": "flame-organ",
        "solution": "Cycle Foxparks runs, restock merchants, and keep a Flambelle grazing so you always have backup drops.【cf6c22†L5-L8】"
      }
    ],
    "time_limited": "Run the Foxparks ridge once, toss drops into base storage, and resume later without losing progress.【5531dc†L5-L6】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one hunter clear Foxparks while the partner ferries organs home and rotates Flambelle at the ranch.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-flame-organ:001",
          "resource-flame-organ:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-flame-organ:checkpoint-foxparks",
      "summary": "Foxparks loop mapped",
      "benefits": [
        "Spawn path memorized",
        "Early organs banked"
      ],
      "related_steps": [
        "resource-flame-organ:001"
      ]
    },
    {
      "id": "resource-flame-organ:checkpoint-ranch",
      "summary": "Flambelle ranching",
      "benefits": [
        "Passive organ output",
        "Base heat labor covered"
      ],
      "related_steps": [
        "resource-flame-organ:002"
      ]
    },
    {
      "id": "resource-flame-organ:checkpoint-merchant",
      "summary": "Merchant cleared",
      "benefits": [
        "Gold converted",
        "Emergency reserve filled"
      ],
      "related_steps": [
        "resource-flame-organ:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-coal"
    ],
    "optional": [
      "resource-cake"
    ]
  },
  "failure_recovery": {
    "normal": "Grab stored organs from base chests and rerun the spawn lap.",
    "hardcore": "Keep a spare Flambelle condensed; replace any loss immediately to keep the ranch rolling."
  },
  "steps": [
    {
      "step_id": "resource-flame-organ:001",
      "type": "travel",
      "summary": "Sweep the Foxparks ridge",
      "detail": "Warp to Grassy Behemoth Hills, sprint toward Rayne Syndicate Tower Entrance, and clear Foxparks along the ridge before fast travelling home to reset.【5531dc†L2-L6】",
      "targets": [
        {
          "kind": "item",
          "id": "flame-organ",
          "qty": 8
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "bow"
        ],
        "pals": [
          "pengullet"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 4
          }
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "flame-organ",
            "qty": 8
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "progameguides-flame-organ"
      ]
    },
    {
      "step_id": "resource-flame-organ:002",
      "type": "assign",
      "summary": "Ranch Flambelle for steady supply",
      "detail": "Capture a Flambelle at roughly (361,-48), drop it into your ranch, and let Magma Tears generate organs while you craft.【5531dc†L7-L9】【cf6c22†L8-L8】",
      "targets": [
        {
          "kind": "item",
          "id": "flame-organ",
          "qty": 4
        }
      ],
      "locations": [
        {
          "region_id": "mount-obsidian",
          "coords": [
            361,
            -48
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "heat-resistant-armor"
        ],
        "pals": [
          "flambelle"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "flame-organ",
            "qty": 4
          }
        ],
        "pals": [
          "flambelle"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "progameguides-flame-organ",
        "game8-flame-organ"
      ]
    },
    {
      "step_id": "resource-flame-organ:003",
      "type": "trade",
      "summary": "Buy 100-gold organs",
      "detail": "Swing through the Small Settlement after each run and spend 100 gold per Flame Organ to cushion crafting spikes.【cf6c22†L6-L6】",
      "targets": [
        {
          "kind": "item",
          "id": "flame-organ",
          "qty": 5
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "gold-coin",
            "qty": 500
          }
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "flame-organ",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "capture-base-merchant"
        }
      ],
      "citations": [
        "game8-flame-organ"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "flame-organ",
      "qty": 18
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "cooking-pot"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-cake",
      "reason": "Cakes and polymer both lean on steady flame organ income."
    }
  ]
}
```

### Route: Ice Organ Chill Chain

Ice Organ Chill Chain leans on the Penking alpha dungeon and Duneshelter merchants so refrigeration, ice mines, and frost saddles stay stocked.【4307f5†L3-L11】【955051†L5-L8】【4307f5†L58-L64】【0e4eda†L6-L83】

```json
{
  "route_id": "resource-ice-organ",
  "title": "Ice Organ Chill Chain",
  "category": "resources",
  "tags": [
    "resource-farm",
    "ice-organ",
    "dungeon",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 18,
    "max": 32
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock the Sealed Realm of the Frozen Wings teleport",
    "Farm Pengullet waves inside the Penking arena",
    "Buy 100-gold organs from Duneshelter merchants"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 22
  },
  "estimated_xp_gain": {
    "min": 320,
    "max": 480
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Clearing Penking ends the dungeon and forces a respawn timer, wasting the farm run.",
    "hardcore": "Hardcore wipes inside the arena delete your frost pals—leave once armor degrades." 
  },
  "adaptive_guidance": {
    "underleveled": "Enter the dungeon, clear Pengullets, and exit before touching Penking so you avoid the hour-long reset timer.【4307f5†L9-L11】",
    "overleveled": "Rotate additional Ice-type drops like Reindrix or Foxcicle between dungeon runs to accelerate legendary saddle crafting.【4307f5†L58-L64】",
    "resource_shortages": [
      {
        "item_id": "ice-organ",
        "solution": "Buy Duneshelter stock for 100 gold whenever you pass through the desert to buffer against slow dungeon respawns.【4307f5†L6-L7】【955051†L5-L8】"
      }
    ],
    "time_limited": "Run one Pengullet clear, leave the dungeon, and stash organs before the cooldown catches up.【4307f5†L9-L11】",
    "dynamic_rules": [
      {
        "signal": "resource_gap:pal-fluids_high",
        "condition": "resource_gaps['pal-fluids'] >= 10",
        "adjustment": "Stay inside for an extra Pengullet cycle—the arena doubles as a Pal Fluid farm.【4307f5†L9-L10】",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-ice-organ:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-ice-organ:checkpoint-realm",
      "summary": "Frozen Wings teleport unlocked",
      "benefits": [
        "Quick arena access",
        "Safe exit plan"
      ],
      "related_steps": [
        "resource-ice-organ:001"
      ]
    },
    {
      "id": "resource-ice-organ:checkpoint-dungeon",
      "summary": "Pengullet wave cleared",
      "benefits": [
        "Ice organs stocked",
        "Pal fluids topped"
      ],
      "related_steps": [
        "resource-ice-organ:002"
      ]
    },
    {
      "id": "resource-ice-organ:checkpoint-merchant",
      "summary": "Duneshelter inventory purchased",
      "benefits": [
        "Desert route completed",
        "Reserve organ cache"
      ],
      "related_steps": [
        "resource-ice-organ:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-pal-fluids"
    ],
    "optional": [
      "resource-electric-organ"
    ]
  },
  "failure_recovery": {
    "normal": "Reset the dungeon timer, refill potions, and re-enter once Penking respawns.",
    "hardcore": "Keep a spare cold-resist set ready; replace any fallen frost pals before the next run." 
  },
  "steps": [
    {
      "step_id": "resource-ice-organ:001",
      "type": "travel",
      "summary": "Unlock the Frozen Wings fast travel",
      "detail": "Activate the Sealed Realm of the Frozen Wings statue and set a camp outside the (113,-351) dungeon door for quick entries.【4307f5†L9-L10】",
      "targets": [],
      "locations": [
        {
          "region_id": "ice-wind-island",
          "coords": [
            113,
            -351
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "cold-resistant-armor"
        ],
        "pals": [
          "blazehowl"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-ice-organ"
      ]
    },
    {
      "step_id": "resource-ice-organ:002",
      "type": "combat",
      "summary": "Farm Pengullets in the arena",
      "detail": "Clear Pengullets supporting Penking, leave before defeating the boss, then re-enter once the cooldown lifts for another wave of organ drops.【4307f5†L9-L11】",
      "targets": [
        {
          "kind": "item",
          "id": "ice-organ",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "ice-wind-island",
          "coords": [
            113,
            -351
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "controller",
              "tasks": "Keeps Pengullets grouped"
            },
            {
              "role": "finisher",
              "tasks": "Delivers last hits and gathers loot"
            }
          ],
          "loot_rules": "Split organs evenly before leaving the dungeon"
        }
      },
      "recommended_loadout": {
        "gear": [
          "musket"
        ],
        "pals": [
          "kitsun",
          "surfent"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 200,
        "max": 300
      },
      "outputs": {
        "items": [
          {
            "item_id": "ice-organ",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-ice-organ"
      ]
    },
    {
      "step_id": "resource-ice-organ:003",
      "type": "trade",
      "summary": "Purchase Duneshelter stock",
      "detail": "Travel to Duneshelter (358,350) and buy any 100-gold ice organs from the wandering merchants stationed there.【0e4eda†L83-L83】【955051†L5-L8】",
      "targets": [
        {
          "kind": "item",
          "id": "ice-organ",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "twilight-dunes",
          "coords": [
            358,
            350
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "gold-coin",
            "qty": 600
          }
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "ice-organ",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "subroute_ref": "capture-base-merchant"
        }
      ],
      "citations": [
        "game8-ice-organ",
        "dexerto-ice-organ"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "ice-organ",
      "qty": 20
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "refrigerator"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-electric-organ",
      "reason": "Pair ice and electric reagents to finish late-game generator chains."
    }
  ]
}
```

### Route: Venom Gland Vial Chain

Harvest enough Venom Glands to sustain poison ammo, dark saddles, and antidote stocks while automating backup supply lines through merchants and ranch drops.

```json
{
  "route_id": "resource-venom-gland",
  "title": "Venom Gland Vial Chain",
  "category": "resource",
  "tags": [
    "resource",
    "poison",
    "mid-game",
    "ammo-support"
  ],
  "progression_role": "resource",
  "recommended_level": {
    "min": 14,
    "max": 32
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Stage a night-hunt camp south of the Plateau of Beginnings",
    "Cull nocturnal poison pals for an initial organ stockpile",
    "Backfill shortages through merchants and Caprity Noct ranching"
  ],
  "estimated_time_minutes": {
    "solo": 40,
    "coop": 28
  },
  "estimated_xp_gain": {
    "min": 520,
    "max": 900
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Night hunts risk wipes from clustered poison projectiles; expect armor durability loss.",
    "hardcore": "Being downed by Helzephyr barrages ends the save—kite aggressively and disengage below half HP."
  },
  "adaptive_guidance": {
    "underleveled": "If armor is below Metal tier, anchor Step :001 at coordinate cluster C for easy retreat to Plateau fast travel before sunrise.【palnerd-venom-gland†L1-L20】【progameguides-base-triangle†L1-L15】",
    "overleveled": "Players running rocket or shotgun builds can skip Step :002 after tagging 10 glands and move straight to ranch automation.",
    "resource_shortages": [
      {
        "item_id": "venom-gland",
        "solution": "Trigger Step :003 to restock from the Small Settlement merchant before repeating night loops."
      }
    ],
    "time_limited": "Complete Steps :001 and :002 only; bank 10 glands then purchase extras on the next login."
  },
  "checkpoints": [
    {
      "id": "resource-venom-gland:checkpoint-scout",
      "summary": "Camp staged south ridge",
      "benefits": [
        "Fast-travel anchor set",
        "Bed and chests placed"
      ],
      "related_steps": [
        "resource-venom-gland:001"
      ]
    },
    {
      "id": "resource-venom-gland:checkpoint-harvest",
      "summary": "Night culling complete",
      "benefits": [
        "Initial venom stockpile",
        "Poison arrow queue primed"
      ],
      "related_steps": [
        "resource-venom-gland:002"
      ]
    },
    {
      "id": "resource-venom-gland:checkpoint-automation",
      "summary": "Merchant and ranch running",
      "benefits": [
        "Emergency vendor access",
        "Caprity Noct drops cycling"
      ],
      "related_steps": [
        "resource-venom-gland:003",
        "resource-venom-gland:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-base-merchant",
      "resource-paldium"
    ],
    "optional": [
      "resource-carbon-fiber",
      "mount-foxparks-harness"
    ]
  },
  "failure_recovery": {
    "normal": "If you wipe to poison volleys, rest at the Plateau fast travel, buy five glands from the Small Settlement, and reset the hunt loop.【palnerd-venom-gland†L21-L35】【palwiki-venom-gland†L1-L18】",
    "hardcore": "Rotate night hunts with a partner in co-op so one player stays at camp to revive if the other is downed."
  },
  "steps": [
    {
      "step_id": "resource-venom-gland:001",
      "type": "travel",
      "summary": "Stage Plateau south ridge camp",
      "detail": "Fast travel to Plateau of Beginnings, glide to the southern peninsula, and drop a campfire, bed, and storage at roughly (230,-510) so you can reset night loops quickly.【progameguides-base-triangle†L1-L15】",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            230,
            -510
          ],
          "time": "evening",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "metal-armor",
          "crossbow"
        ],
        "pals": [
          "nox",
          "rushoar"
        ],
        "consumables": [
          {
            "item_id": "antidote",
            "qty": 3
          }
        ]
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "progameguides-base-triangle"
      ]
    },
    {
      "step_id": "resource-venom-gland:002",
      "type": "combat",
      "summary": "Cull Daedream and Depresso packs",
      "detail": "Hunt Daedream and Depresso along the southern plateau ridges at night; both species drop Venom Glands when defeated or captured, letting you bank 12-15 glands per cycle before dawn.【palnerd-venom-gland†L5-L23】【palwiki-venom-gland†L1-L18】",
      "targets": [
        {
          "kind": "item",
          "id": "venom-gland",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            160,
            -560
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "vanguard",
              "tasks": "Tag Daedream aggro with ranged fire and kite poison orbs."
            },
            {
              "role": "collector",
              "tasks": "Capture weakened targets with Giga Spheres and scoop drops."
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "poison-resistant-amulet"
        ],
        "pals": [
          "eikthyrdeer",
          "foxparks"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ]
      },
      "xp_award_estimate": {
        "min": 220,
        "max": 360
      },
      "outputs": {
        "items": [
          {
            "item_id": "venom-gland",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palnerd-venom-gland",
        "palwiki-venom-gland",
        "progameguides-base-triangle"
      ]
    },
    {
      "step_id": "resource-venom-gland:003",
      "type": "trade",
      "summary": "Buy out Small Settlement stock",
      "detail": "Visit the Small Settlement merchants around (100,-525) and purchase Venom Glands for 100 gold each to buffer poison ammo crafting before your next hunt cycle.【palnerd-venom-gland†L21-L35】【palwiki-venom-gland†L1-L18】【progameguides-base-triangle†L10-L15】",
      "targets": [
        {
          "kind": "item",
          "id": "venom-gland",
          "qty": 5
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            100,
            -525
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lamball"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 80
      },
      "outputs": {
        "items": [
          {
            "item_id": "venom-gland",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palnerd-venom-gland",
        "palwiki-venom-gland",
        "progameguides-base-triangle"
      ]
    },
    {
      "step_id": "resource-venom-gland:004",
      "type": "build",
      "summary": "Assign Caprity Noct to ranches",
      "detail": "Capture Caprity Noct from Feybreak spawns and station it on a Ranch so it periodically drops Venom Glands for base logistics while you craft poison arrows.【palnerd-venom-gland†L23-L35】",
      "targets": [
        {
          "kind": "pal",
          "id": "caprity-noct",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "caprity-noct"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 100
      },
      "outputs": {
        "items": [],
        "pals": [
          "caprity-noct"
        ],
        "unlocks": {
          "structures": [
            "ranch"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palnerd-venom-gland"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "venom-gland",
      "qty": 20
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "poison-arrow-crafting",
      "shadowbeak-saddle"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-katress-hair",
      "reason": "Katress hunts overlap night loops and unlock Katress Cap crafting."
    }
  ]
}
```

### Route: Katress Weaving Circuit

Secure Katress Hair for witch gear and speed remedies by chaining Moonless Shore patrols, alpha boss captures, and breeding-farm replenishment.

```json
{
  "route_id": "resource-katress-hair",
  "title": "Katress Weaving Circuit",
  "category": "resource",
  "tags": [
    "resource",
    "dark",
    "mid-game",
    "gear"
  ],
  "progression_role": "resource",
  "recommended_level": {
    "min": 23,
    "max": 38
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-venom-gland"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Night-hunt Katress patrols in Moonless Shore and Verdant Brook",
    "Defeat or capture the Sealed Realm of the Invincible alpha",
    "Breed backup Katress eggs and craft Katress Cap upgrades"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 32
  },
  "estimated_xp_gain": {
    "min": 680,
    "max": 1100
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Katress claw combos inflict heavy stagger and leather steals; expect potion spend.",
    "hardcore": "Dark spell barrages can one-shot underleveled teams—retreat if shields break."
  },
  "adaptive_guidance": {
    "underleveled": "Use dragon-type pals like Dinossom to exploit Katress weakness and disengage after two kills before dawn.【gameleap-katress†L7-L20】",
    "overleveled": "Players above 35 can farm the alpha first, then loop Moonless Shore to minimize travel time.",
    "resource_shortages": [
      {
        "item_id": "katress-hair",
        "solution": "Run Step :003 breeding while Moonless Shore respawns reset."
      }
    ],
    "time_limited": "Execute Step :001 only, banking 6-8 hair, and postpone the alpha fight until you have a longer session."
  },
  "checkpoints": [
    {
      "id": "resource-katress-hair:checkpoint-patrol",
      "summary": "Moonless patrol cleared",
      "benefits": [
        "Initial hair supply",
        "Dark drops secured"
      ],
      "related_steps": [
        "resource-katress-hair:001"
      ]
    },
    {
      "id": "resource-katress-hair:checkpoint-alpha",
      "summary": "Alpha subdued",
      "benefits": [
        "High-tier drops",
        "Fast travel anchor unlocked"
      ],
      "related_steps": [
        "resource-katress-hair:002"
      ]
    },
    {
      "id": "resource-katress-hair:checkpoint-breeding",
      "summary": "Breeding loop online",
      "benefits": [
        "Egg pipeline running",
        "Katress Cap crafted"
      ],
      "related_steps": [
        "resource-katress-hair:003",
        "resource-katress-hair:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-base-merchant",
      "resource-pure-quartz"
    ],
    "optional": [
      "mount-foxparks-harness",
      "resource-carbon-fiber"
    ]
  },
  "failure_recovery": {
    "normal": "If Katress wipes the party, fast travel back at dawn, restock healing, and resume after nightfall with dragon pals in front.",
    "hardcore": "Have one co-op player remain airborne on a flying pal to rez fallen allies if the alpha counters."
  },
  "steps": [
    {
      "step_id": "resource-katress-hair:001",
      "type": "combat",
      "summary": "Hunt Moonless Shore Katress",
      "detail": "Circle Moonless Shore and Verdant Brook after dusk; Katress only spawn at night and have about a 50% chance to drop Katress Hair alongside leather.【palnerd-katress-hair†L1-L20】【palwiki-katress-hair†L1-L10】",
      "targets": [
        {
          "kind": "item",
          "id": "katress-hair",
          "qty": 8
        }
      ],
      "locations": [
        {
          "region_id": "moonless-shore",
          "coords": [
            0,
            0
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "scout",
              "tasks": "Sweep shoreline on flying mount to tag spawns."
            },
            {
              "role": "finisher",
              "tasks": "Ground Katress with dragon skills and capture or defeat."
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-armor",
          "shotgun"
        ],
        "pals": [
          "dinossom",
          "chillet"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ]
      },
      "xp_award_estimate": {
        "min": 260,
        "max": 420
      },
      "outputs": {
        "items": [
          {
            "item_id": "katress-hair",
            "qty": 8
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palnerd-katress-hair",
        "gameleap-katress",
        "palwiki-katress-hair"
      ]
    },
    {
      "step_id": "resource-katress-hair:002",
      "type": "combat",
      "summary": "Clear Sealed Realm of the Invincible",
      "detail": "Tackle the level 23 Katress alpha at the Sealed Realm of the Invincible near (241,-330) to secure high-grade drops and a fast travel anchor.【segmentnext-katress†L7-L24】",
      "targets": [
        {
          "kind": "pal",
          "id": "katress",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "marsh-island",
          "coords": [
            241,
            -330
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "poison-resist-amulet",
          "assault-rifle"
        ],
        "pals": [
          "suzaku",
          "grizzbolt"
        ],
        "consumables": [
          {
            "item_id": "large-med-kit",
            "qty": 2
          }
        ]
      },
      "xp_award_estimate": {
        "min": 240,
        "max": 360
      },
      "outputs": {
        "items": [],
        "pals": [
          "katress"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "segmentnext-katress"
      ]
    },
    {
      "step_id": "resource-katress-hair:003",
      "type": "build",
      "summary": "Spin up Katress breeding pairs",
      "detail": "Unlock the Breeding Farm and incubate Large Dark Eggs using combos like Penking + Celaray or Direhowl + Elizabee to replenish Katress without nightly hunts.【gameleap-katress†L20-L32】",
      "targets": [
        {
          "kind": "item",
          "id": "large-dark-egg",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "penking",
          "celaray"
        ],
        "consumables": [
          {
            "item_id": "cake",
            "qty": 2
          }
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [],
        "pals": [
          "katress"
        ],
        "unlocks": {
          "structures": [
            "breeding-farm"
          ]
        }
      },
      "branching": [],
      "citations": [
        "gameleap-katress"
      ]
    },
    {
      "step_id": "resource-katress-hair:004",
      "type": "craft",
      "summary": "Craft Katress Cap and remedies",
      "detail": "Spend Katress Hair on the Katress Cap schematic from Duneshelter merchants or convert surplus into Speed Remedy batches for work-speed buffs.【palnerd-katress-hair†L20-L36】【palwiki-katress-hair†L1-L13】",
      "targets": [
        {
          "kind": "item",
          "id": "katress-cap",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "katress"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 140
      },
      "outputs": {
        "items": [
          "katress-cap"
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palnerd-katress-hair",
        "palwiki-katress-hair"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "katress-hair",
      "qty": 15
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "katress-cap",
      "speed-remedy"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 1,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-poison-arrow",
      "reason": "Hair and glands feed advanced poison ammo crafting."
    }
  ]
}
```

### Route: Medium Pal Soul Harmonization

Medium Pal Souls sit at the core of Statue of Power scaling, so this plan charts Helzephyr night sorties above the Bridge of the Twin Knights, Sakurajima Sootseer hunts, Desiccated Desert chest laps, and Crusher conversions to stabilize supply.【palwiki-helzephyr-raw†L65-L116】【palwiki-sootseer†L65-L114】【palwiki-medium-pal-soul-raw†L22-L42】【palfandom-medium-pal-soul-raw†L27-L38】

```json
{
  "route_id": "resource-medium-pal-soul",
  "title": "Medium Pal Soul Harmonization",
  "category": "resources",
  "tags": [
    "resource-farm",
    "medium-pal-soul",
    "statue-upgrades",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 35,
    "max": 48
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-bone"
    ],
    "tech": [
      "statue-of-power",
      "crusher"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Ambush Helzephyr patrols for rare Medium Pal Soul drops",
    "Clear Sakurajima Sootseer camps for guaranteed Medium Pal Souls",
    "Loot Desiccated Desert treasure chests for loose Medium Pal Souls",
    "Convert excess Small or Large souls in the Crusher to balance demand"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 32
  },
  "estimated_xp_gain": {
    "min": 480,
    "max": 720
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Falling during aerial pursuits or over-pulling Sakurajima camps can result in squad wipes and lost souls.",
    "hardcore": "Death while hauling souls deletes the stack and risks losing late-game pals needed for Crusher automation."
  },
  "adaptive_guidance": {
    "underleveled": "Stay near the Bridge of the Twin Knights waypoint and chip Helzephyr with rifles from cliffs instead of chasing into syndicate camps.【palwiki-helzephyr-raw†L68-L116】",
    "overleveled": "Rotate between Helzephyr ridges and Sakurajima camps every in-game night to keep the Crusher stocked before statue upgrades spike demand.【palwiki-helzephyr-raw†L65-L116】【palwiki-sootseer†L65-L114】",
    "resource_shortages": [
      {
        "item_id": "medium-pal-soul",
        "solution": "Run Crusher conversions each time Small Pal Souls exceed 40 so the statue never stalls.【palwiki-medium-pal-soul-raw†L31-L42】"
      }
    ],
    "time_limited": "Fast travel to Duneshelter, sweep the nearest Desiccated Desert chests, then smash spare Small Souls at the Crusher before logging off.【palwiki-medium-pal-soul-raw†L22-L36】【palfandom-medium-pal-soul-raw†L27-L38】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one hunter to kite Helzephyr while the other nets Sootseer drops, then swap roles after each night cycle to balance soul income.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-medium-pal-soul:001",
          "resource-medium-pal-soul:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-medium-pal-soul:checkpoint-helzephyr",
      "summary": "Helzephyr ridge secured",
      "benefits": [
        "Flying patrol cleared",
        "Initial Medium Pal Souls banked"
      ],
      "related_steps": [
        "resource-medium-pal-soul:001"
      ]
    },
    {
      "id": "resource-medium-pal-soul:checkpoint-sakurajima",
      "summary": "Sootseer camps rotated",
      "benefits": [
        "Guaranteed drops harvested",
        "Night raids stabilized"
      ],
      "related_steps": [
        "resource-medium-pal-soul:002"
      ]
    },
    {
      "id": "resource-medium-pal-soul:checkpoint-processor",
      "summary": "Crusher conversions online",
      "benefits": [
        "Soul stock buffered",
        "Statue queue ready"
      ],
      "related_steps": [
        "resource-medium-pal-soul:004"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-medium-pal-soul:001",
      "type": "hunt",
      "summary": "Intercept Helzephyr above the twin bridges",
      "detail": "Glide up from the Bridge of the Twin Knights waypoint (~113,-352) after dusk and tag the Helzephyr flock as it circles the northern mesas. Its Medium Pal Soul drop rate is low, so use chain bolas or rifles to secure repeated captures and harvest rare souls along with Venom Glands.【palwiki-helzephyr-raw†L65-L116】",
      "targets": [
        {
          "kind": "item",
          "id": "medium-pal-soul",
          "qty": 2
        },
        {
          "kind": "pal",
          "id": "helzephyr",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "verdant-brook",
          "coords": [
            113,
            -352
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Anchor a Grappling Gun or flying mount before engaging so a fall from the mesas doesn’t end the run.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "assault-rifle",
          "grappling-gun"
        ],
        "pals": [
          "helzephyr",
          "ragnahawk"
        ],
        "consumables": [
          "large-bandage"
        ]
      },
      "xp_award_estimate": {
        "min": 160,
        "max": 220
      },
      "outputs": {
        "items": [
          {
            "item_id": "medium-pal-soul",
            "qty": 2
          },
          {
            "item_id": "venom-gland",
            "qty": 2
          }
        ],
        "pals": [
          "helzephyr"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-helzephyr-raw"
      ]
    },
    {
      "step_id": "resource-medium-pal-soul:002",
      "type": "hunt",
      "summary": "Purge Sakurajima Sootseer camps",
      "detail": "Swoop into Sakurajima’s crater camps after midnight, luring Sootseer pairs out of the purple flame pits. Every takedown yields guaranteed Medium Pal Souls plus Bones and Crude Oil—kite them through open lava channels to avoid getting cornered.【palwiki-sootseer†L65-L114】",
      "targets": [
        {
          "kind": "item",
          "id": "medium-pal-soul",
          "qty": 4
        },
        {
          "kind": "pal",
          "id": "sootseer",
          "qty": 2
        }
      ],
      "locations": [
        {
          "region_id": "sakurajima",
          "coords": [
            450,
            -360
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "tactics": "Have one player freeze Sootseer aggro with Shock Pals while the other focuses fire to keep the lava arena manageable.",
          "mode_scope": [
            "coop"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "rocket-launcher"
        ],
        "pals": [
          "jetragon",
          "anubis"
        ],
        "consumables": [
          "fire-tonic"
        ]
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 260
      },
      "outputs": {
        "items": [
          {
            "item_id": "medium-pal-soul",
            "qty": 4
          },
          {
            "item_id": "bone",
            "qty": 4
          }
        ],
        "pals": [
          "sootseer"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-sootseer"
      ]
    },
    {
      "step_id": "resource-medium-pal-soul:003",
      "type": "explore",
      "summary": "Sweep Desiccated Desert treasure chains",
      "detail": "Teleport to Duneshelter (357,347) and circuit the nearby wrecked convoys and cliff ruins; Medium Pal Souls frequently spawn loose or in chests throughout the desert, so clear each lap before raids reset.【palwiki-medium-pal-soul-raw†L22-L29】【palfandom-medium-pal-soul-raw†L27-L30】【palwiki-duneshelter†L506-L516】",
      "targets": [
        {
          "kind": "item",
          "id": "medium-pal-soul",
          "qty": 3
        }
      ],
      "locations": [
        {
          "region_id": "desiccated-desert",
          "coords": [
            357,
            347
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "lantern"
        ],
        "pals": [
          "mammorest",
          "pyrin"
        ],
        "consumables": [
          "heat-resistant-armor"
        ]
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "medium-pal-soul",
            "qty": 3
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-medium-pal-soul-raw",
        "palfandom-medium-pal-soul-raw",
        "palwiki-duneshelter"
      ]
    },
    {
      "step_id": "resource-medium-pal-soul:004",
      "type": "craft",
      "summary": "Convert souls at the Crusher",
      "detail": "Feed surplus Small Pal Souls into the Crusher for Medium conversions and down-convert spare Large souls when raids oversupply them, keeping the statue queue flush before raid prep sessions.【palwiki-medium-pal-soul-raw†L31-L42】",
      "targets": [
        {
          "kind": "item",
          "id": "medium-pal-soul",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "anubis"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "medium-pal-soul",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {
          "statue-upgrades": true
        }
      },
      "branching": [],
      "citations": [
        "palwiki-medium-pal-soul-raw"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "medium-pal-soul",
      "qty": 20
    }
  ],
  "yields": {
    "levels_estimate": "+1 to +2",
    "key_unlocks": [
      "medium-pal-soul-buffer",
      "statue-upgrade-pipeline"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-large-pal-soul",
      "reason": "Large Pal Souls convert from Mediums and fuel the same Statue upgrades once mid-tier queues stabilize."
    }
  ]
}
```

Large Pal Souls fuel Statue of Power upgrades for late-game builds, so this circuit unlocks the statue and Crusher, loops Anubis in Twilight Dunes, and backfills demand with Crusher conversions plus sanctuary sweeps.【game8-large-pal-soul†L87-L158】【palwiki-large-pal-soul†L116-L160】

```json
{
  "route_id": "resource-large-pal-soul",
  "title": "Large Pal Soul Resonance",
  "category": "resources",
  "tags": [
    "resource-farm",
    "pal-soul",
    "statue-of-power"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 45,
    "max": 60
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "resource-ore"
    ],
    "tech": [
      "statue-of-power",
      "crusher"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Unlock and build a Statue of Power and Crusher hub",
    "Farm Anubis in Twilight Dunes for guaranteed Large Pal Souls",
    "Convert Medium and Giant Pal Souls into Large via the Crusher",
    "Sweep sanctuaries and Executioner raids for bonus Large Pal Souls"
  ],
  "estimated_time_minutes": {
    "solo": 55,
    "coop": 40
  },
  "estimated_xp_gain": {
    "min": 720,
    "max": 1180
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Being downed by level 50+ elites forces a corpse run through PIDF patrols and chews through high-tier gear durability.",
    "hardcore": "Hardcore wipes against Anubis or Executioner raids delete endgame kits—disengage if shields and potions run dry."
  },
  "adaptive_guidance": {
    "underleveled": "Rotate Step :002 at night with traps and dark pals so Anubis stays staggered while you build Crusher stockpiles before challenging Executioner raids.【game8-large-pal-soul†L113-L136】",
    "overleveled": "Chain Steps :002 and :004 in a single loop—clear Anubis, fast travel to the sanctuary, then intercept raids to bank 4+ souls per lap.【palwiki-large-pal-soul†L125-L160】",
    "resource_shortages": [
      {
        "item_id": "large-pal-soul",
        "solution": "Run Step :003 to convert two Medium Pal Souls or split one Giant Pal Soul into two Large souls whenever drops lag behind Statue demands.【game8-large-pal-soul†L117-L156】【palwiki-crusher†L159-L179】"
      }
    ],
    "time_limited": "Prioritise Steps :001 and :003 so Crusher conversions keep Statue projects moving even if you skip hunt rotations this session.【game8-large-pal-soul†L117-L156】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player kite Anubis while the partner rotates burst pals and Shock Traps to secure fast captures or kills.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-large-pal-soul:002"
        ]
      },
      {
        "signal": "resource_gap:medium-pal-soul_high",
        "condition": "resource_gaps['medium-pal-soul'] >= 5",
        "adjustment": "Queue medium soul farming before Step :003 so Crusher conversions stay positive.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "resource-large-pal-soul:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-large-pal-soul:checkpoint-base",
      "summary": "Statue and Crusher online",
      "benefits": [
        "Statue upgrades unlocked",
        "Crusher conversion hub active"
      ],
      "related_steps": [
        "resource-large-pal-soul:001"
      ]
    },
    {
      "id": "resource-large-pal-soul:checkpoint-anubis",
      "summary": "Anubis cleared",
      "benefits": [
        "Guaranteed Large Pal Soul secured",
        "Twilight Dunes fast travel refreshed"
      ],
      "related_steps": [
        "resource-large-pal-soul:002"
      ]
    },
    {
      "id": "resource-large-pal-soul:checkpoint-stockpile",
      "summary": "Soul stockpile stabilised",
      "benefits": [
        "Crusher conversion cycle running",
        "Sanctuary sweep route mapped"
      ],
      "related_steps": [
        "resource-large-pal-soul:003",
        "resource-large-pal-soul:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-carbon-fiber",
      "resource-ore"
    ],
    "optional": [
      "resource-pure-quartz"
    ]
  },
  "failure_recovery": {
    "normal": "If Anubis wipes you, rest at the Twilight Dunes statue and return with fresh traps once patrols reset—the alpha respawns at (-134,-95).【palfandom-anubis†L294-L303】",
    "hardcore": "Hardcore saves should lean on Step :003 conversions from banked Medium or Giant souls instead of repeating risky alpha fights.【game8-large-pal-soul†L117-L156】【palwiki-crusher†L159-L179】"
  },
  "steps": [
    {
      "step_id": "resource-large-pal-soul:001",
      "type": "build",
      "summary": "Install Statue of Power and Crusher",
      "detail": "Spend tech points to unlock both the Statue of Power and Crusher, then place them near storage so Large Pal Souls can immediately feed upgrades and conversions.【palwiki-statue-of-power†L160-L186】【palwiki-crusher†L159-L179】",
      "targets": [
        {
          "kind": "tech",
          "id": "statue-of-power"
        },
        {
          "kind": "tech",
          "id": "crusher"
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "builder",
              "tasks": "Places foundations and wiring"
            },
            {
              "role": "quartermaster",
              "tasks": "Delivers ingots, stone, and Paldium"
            }
          ],
          "loot_rules": "Log soul deposits in shared chests"
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-armor"
        ],
        "pals": [
          "anubis"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [
          {
            "item_id": "statue-of-power",
            "qty": 1
          },
          {
            "item_id": "crusher",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-statue-of-power",
        "palwiki-crusher"
      ]
    },
    {
      "step_id": "resource-large-pal-soul:002",
      "type": "combat",
      "summary": "Defeat Anubis in Twilight Dunes",
      "detail": "Fast travel to Twilight Dunes and clear the level 47 Anubis alpha at (-134,-95); every kill drops a Large Pal Soul alongside Bones, making it the fastest repeatable source.【palfandom-anubis†L294-L303】【game8-large-pal-soul†L113-L120】【palwiki-large-pal-soul†L125-L132】",
      "targets": [
        {
          "kind": "pal",
          "id": "anubis",
          "qty": 1
        },
        {
          "kind": "item",
          "id": "large-pal-soul",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "twilight-dunes",
          "coords": [
            -134,
            -95
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Kite Anubis and soak Ground Smash combos"
            },
            {
              "role": "burst",
              "tasks": "Drop Shock Traps and unload dark damage"
            }
          ],
          "loot_rules": "Alternate soul pickups between runs"
        }
      },
      "recommended_loadout": {
        "gear": [
          "legendary-crossbow",
          "shock-trap"
        ],
        "pals": [
          "suzaku",
          "grizzbolt"
        ],
        "consumables": [
          {
            "item_id": "large-med-kit",
            "qty": 2
          }
        ]
      },
      "xp_award_estimate": {
        "min": 260,
        "max": 420
      },
      "outputs": {
        "items": [
          {
            "item_id": "large-pal-soul",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks shock-trap",
          "action": "include_subroute",
          "subroute_ref": "resource-carbon-fiber"
        }
      ],
      "citations": [
        "palfandom-anubis",
        "game8-large-pal-soul",
        "palwiki-large-pal-soul"
      ]
    },
    {
      "step_id": "resource-large-pal-soul:003",
      "type": "craft",
      "summary": "Convert souls at the Crusher",
      "detail": "Feed two Medium Pal Souls or one Giant Pal Soul into the Crusher to mint Large Pal Souls whenever Statue projects demand more than hunts provide.【game8-large-pal-soul†L117-L156】【palwiki-crusher†L159-L179】",
      "targets": [
        {
          "kind": "item",
          "id": "large-pal-soul",
          "qty": 2
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "operator",
              "tasks": "Queues Crusher recipes"
            },
            {
              "role": "runner",
              "tasks": "Shuttles medium and giant souls from storage"
            }
          ],
          "loot_rules": "Record conversion yields in shared ledger"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "digtoise"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 150
      },
      "outputs": {
        "items": [
          {
            "item_id": "large-pal-soul",
            "qty": 2
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "game8-large-pal-soul",
        "palwiki-crusher"
      ]
    },
    {
      "step_id": "resource-large-pal-soul:004",
      "type": "gather",
      "summary": "Sweep sanctuaries and raids",
      "detail": "After each hunt, glide through No. 2 Wildlife Sanctuary (-675,-113) and intercept Pal Genetic Research Unit raids—both zones leave Large Pal Souls on the ground after skirmishes.【palwiki-large-pal-soul†L116-L160】【palwiki-wildlife-sanctuary-2†L1-L15】",
      "targets": [
        {
          "kind": "item",
          "id": "large-pal-soul",
          "qty": 2
        }
      ],
      "locations": [
        {
          "region_id": "wildlife-sanctuary-2",
          "coords": [
            -675,
            -113
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Avoid chaining kills once PIDF reinforcements spawn—grab souls and extract immediately.",
          "mode_scope": [
            "hardcore"
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "spotter",
              "tasks": "Marks loose souls and incoming raid waves"
            },
            {
              "role": "clean-up",
              "tasks": "Finishes elites and secures drops"
            }
          ],
          "loot_rules": "Alternate who claims raid soul drops"
        }
      },
      "recommended_loadout": {
        "gear": [
          "heat-resistant-armor",
          "cold-resistant-armor"
        ],
        "pals": [
          "paladius"
        ],
        "consumables": [
          {
            "item_id": "antidote",
            "qty": 2
          }
        ]
      },
      "xp_award_estimate": {
        "min": 240,
        "max": 360
      },
      "outputs": {
        "items": [
          {
            "item_id": "large-pal-soul",
            "qty": 2
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-large-pal-soul",
        "palwiki-wildlife-sanctuary-2"
      ]
    }
  ]
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
  "tags": [
    "human",
    "merchant",
    "base-support"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 10,
    "max": 18
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Craft or buy high-grade Pal Spheres for human capture",
    "Travel to the Small Settlement and separate a merchant from guards",
    "Capture the merchant and assign them to your base"
  ],
  "estimated_time_minutes": {
    "solo": 25,
    "coop": 18
  },
  "estimated_xp_gain": {
    "min": 350,
    "max": 600
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Knockouts drop your pouch and may cost gold if PIDF guards finish the fight.",
    "hardcore": "Being executed by guards permanently ends the save—retreat if health drops below 40%."
  },
  "adaptive_guidance": {
    "underleveled": "If your weapons are below Iron tier, focus on trapping single merchants at night when patrols thin out before attempting the capture.",
    "overleveled": "Players above level 18 can skip step :001 if they already stock Mega Pal Spheres and move straight to isolating the merchant.",
    "resource_shortages": [
      {
        "item_id": "paldium-fragment",
        "solution": "Trigger resource-paldium from step :001 to restock fragments for higher-grade spheres."
      }
    ],
    "time_limited": "Complete steps :001 and :002 only; mark the merchant’s position and return later with time to handle the capture.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Have one player kite PIDF guards away during step :003 while the other drops the merchant to low HP for an easy capture.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "capture-base-merchant:003"
        ],
        "follow_up_routes": []
      },
      {
        "signal": "resource_gap:pal-sphere",
        "condition": "resource_gaps contains pal-sphere >= 5",
        "adjustment": "Loop resource-paldium immediately after step :001 to craft additional high-grade spheres before confronting the merchant.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "capture-base-merchant:001"
        ],
        "follow_up_routes": [
          "resource-paldium"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "capture-base-merchant:checkpoint-scout",
      "summary": "Merchant location scouted",
      "benefits": [
        "Safe pull path identified"
      ],
      "related_steps": [
        "capture-base-merchant:002"
      ]
    },
    {
      "id": "capture-base-merchant:checkpoint-captured",
      "summary": "Merchant captured",
      "benefits": [
        "Permanent base vendor unlocked"
      ],
      "related_steps": [
        "capture-base-merchant:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-paldium"
    ],
    "optional": []
  },
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
      "targets": [
        {
          "kind": "item",
          "id": "pal-sphere",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Craft a spare stack to avoid mid-raid shortages; you cannot risk repeat crimes.",
          "safety_buffer_items": [
            {
              "item_id": "pal-sphere",
              "qty": 3
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "crafter",
              "tasks": "Queues high-grade spheres"
            },
            {
              "role": "supplier",
              "tasks": "Feeds fragments and ingots"
            }
          ],
          "loot_rules": "Split sphere stacks evenly"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ]
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks pal-sphere >= 6",
          "action": "include_subroute",
          "subroute_ref": "resource-paldium"
        }
      ],
      "citations": [
        "palwiki-humans"
      ]
    },
    {
      "step_id": "capture-base-merchant:002",
      "type": "travel",
      "summary": "Scout the Small Settlement",
      "detail": "Ride or glide to the Small Settlement at approximately (75, -479). The village hosts both a Pal Merchant and a Wandering Merchant—confirm patrol routes and identify clear back alleys for the capture attempt【165dd8†L71-L90】.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Enter from the cliffside to avoid triggering wanted status while scouting."
        },
        "coop": {
          "role_splits": [
            {
              "role": "spotter",
              "tasks": "Marks guard paths"
            },
            {
              "role": "controller",
              "tasks": "Prepares trap location"
            }
          ],
          "loot_rules": "Share any merchant stock equally"
        }
      },
      "recommended_loadout": {
        "gear": [
          "glider"
        ],
        "pals": [
          "foxparks"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 70
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-small-settlement"
      ]
    },
    {
      "step_id": "capture-base-merchant:003",
      "type": "capture",
      "summary": "Weaken and capture the merchant",
      "detail": "Aggro the merchant away from guards, chip them to low HP, then throw your high-grade Pal Spheres until the catch lands. All non-leader humans can be captured once weakened, but expect multiple throws because their catch rate is significantly lower than normal Pals【529f5c†L67-L90】.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use stun grenades or partner skills to avoid lethal retaliation—you cannot afford PIDF executions."
        },
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Holds aggro"
            },
            {
              "role": "snare",
              "tasks": "Applies slow and throws spheres"
            }
          ],
          "loot_rules": "Whoever spends the most spheres gets priority on merchant placement"
        }
      },
      "recommended_loadout": {
        "gear": [
          "pal-sphere"
        ],
        "pals": [
          "direhowl"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 6
          }
        ]
      },
      "xp_award_estimate": {
        "min": 180,
        "max": 280
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-humans"
      ]
    },
    {
      "step_id": "capture-base-merchant:004",
      "type": "deliver",
      "summary": "Assign the merchant to your base",
      "detail": "Place the captured merchant in your base party. Humans have only rank 1 work suitability and cannot run farms or wield their weapons, but merchants stationed at your base permanently open their shop so you can buy and sell without hunting for a wandering spawn【94455f†L13-L18】【529f5c†L76-L90】.",
      "targets": [],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 80
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-humans"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-base-npc",
      "npc_id": "pal-merchant"
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "base-merchant-vendor"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
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
  "tags": [
    "pal-gear",
    "fire-support",
    "early-game",
    "combat"
  ],
  "progression_role": "optional",
  "recommended_level": {
    "min": 6,
    "max": 8
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "tech-pal-gear-workbench"
    ],
    "items": [],
    "pals": [
      "foxparks"
    ]
  },
  "objectives": [
    "Unlock Foxparks Harness tech",
    "Gather Leather, Flame Organs and Paldium Fragments",
    "Craft the harness",
    "Equip and use Foxparks as a flamethrower"
  ],
  "estimated_time_minutes": {
    "solo": 20,
    "coop": 15
  },
  "estimated_xp_gain": {
    "min": 400,
    "max": 600
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Loss of materials",
    "hardcore": "Death results in loss of Pals and materials"
  },
  "adaptive_guidance": {
    "underleveled": "Focus on capturing Foxparks at night when their patrol radius shrinks, then delay crafting until level 7 for better survivability.",
    "overleveled": "Skip step :001 if your Pal roster already includes Foxparks and jump straight to unlocking and crafting.",
    "resource_shortages": [
      {
        "item_id": "leather",
        "solution": "Invoke resource-leather-early via step :003’s branching."
      },
      {
        "item_id": "flame-organ",
        "solution": "Farm Rushoar in the Sea Breeze Archipelago while Foxparks respawn."
      }
    ],
    "time_limited": "Perform steps :002 through :004 only; purchase missing Leather to finish within ten minutes.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:flame-organ",
        "condition": "resource_gaps contains flame-organ >= 5",
        "adjustment": "Loop Rushoar packs near the Sea Breeze bridge between attempts in step :003 until the flame-organ shortage clears.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-foxparks-harness:003"
        ],
        "follow_up_routes": [
          "resource-leather-early"
        ]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 15",
        "adjustment": "Skip capturing in :001, buy the remaining Leather via the merchant tip, and craft immediately after step :002.",
        "priority": 3,
        "mode_scope": [
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-foxparks-harness:002",
          "mount-foxparks-harness:004"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to gather Flame Organs while another mines Paldium in :003 to finish the material checklist in a single loop.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "mount-foxparks-harness:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "mount-foxparks-harness:checkpoint-capture",
      "summary": "Foxparks secured",
      "benefits": [
        "Unlocks partner flamethrower",
        "Qualifies for harness tech"
      ],
      "related_steps": [
        "mount-foxparks-harness:001"
      ]
    },
    {
      "id": "mount-foxparks-harness:checkpoint-crafted",
      "summary": "Harness crafted",
      "benefits": [
        "Fire damage tool ready",
        "Improves furnace automation"
      ],
      "related_steps": [
        "mount-foxparks-harness:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-leather-early"
    ],
    "optional": [
      "resource-paldium"
    ]
  },
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
      "targets": [
        {
          "kind": "pal",
          "id": "foxparks",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            189,
            -478
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "windswept-hills",
          "coords": [
            144,
            -583
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Capture from behind to avoid being burned and always carry a water Pal",
          "safety_buffer_items": [
            {
              "item_id": "pal-sphere",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "bait",
              "tasks": "Aggro Foxparks"
            },
            {
              "role": "catcher",
              "tasks": "Throw Pal Spheres"
            }
          ],
          "loot_rules": "Whoever catches it keeps it"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 3
          }
        ]
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 100
      },
      "outputs": {
        "items": [],
        "pals": [
          "foxparks"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "thegamer-foxparks-spawn"
      ]
    },
    {
      "step_id": "mount-foxparks-harness:002",
      "type": "unlock-tech",
      "summary": "Unlock the Foxparks Harness",
      "detail": "Open the Technology menu at level 6 and spend 1 tech point to unlock the Foxparks Harness【353245298505537†L150-L180】.  This requires that you have already built a Pal Gear Workbench.",
      "targets": [
        {
          "kind": "tech",
          "id": "tech-foxparks-harness"
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 10,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "tech-foxparks-harness"
          ]
        }
      },
      "branching": [],
      "citations": [
        "gameclubz-foxparks-harness"
      ]
    },
    {
      "step_id": "mount-foxparks-harness:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 3 Leather, 5 Flame Organs and 5 Paldium Fragments.  Hunt Foxparks and Rushoars for Leather and Flame Organs, or branch to the leather farm route if you lack Leather.  Mine blue ore nodes for Paldium Fragments.",
      "targets": [
        {
          "kind": "item",
          "id": "leather",
          "qty": 3
        },
        {
          "kind": "item",
          "id": "flame-organ",
          "qty": 5
        },
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 5
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            189,
            -478
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "sea-breeze-archipelago",
          "coords": [
            -650,
            -650
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Farm extra Leather (5 instead of 3) to allow for gear repairs",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "farmer",
              "tasks": "Hunt Foxparks and collect Flame Organs"
            },
            {
              "role": "miner",
              "tasks": "Mine Paldium nodes"
            }
          ],
          "loot_rules": "Pool resources then split evenly"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 200
      },
      "outputs": {
        "items": [
          {
            "item_id": "leather",
            "qty": 3
          },
          {
            "item_id": "flame-organ",
            "qty": 5
          },
          {
            "item_id": "paldium-fragment",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks leather >= 3",
          "action": "include_subroute",
          "subroute_ref": "resource-leather-early"
        }
      ],
      "citations": [
        "gameclubz-foxparks-harness",
        "shockbyte-leather-sources"
      ]
    },
    {
      "step_id": "mount-foxparks-harness:004",
      "type": "craft",
      "summary": "Craft the harness",
      "detail": "At your Pal Gear Workbench, craft the Foxparks Harness using the collected materials【353245298505537†L150-L180】.  The process takes about one minute.",
      "targets": [
        {
          "kind": "item",
          "id": "foxparks-harness",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 80
      },
      "outputs": {
        "items": [
          {
            "item_id": "foxparks-harness",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "gameclubz-foxparks-harness"
      ]
    },
    {
      "step_id": "mount-foxparks-harness:005",
      "type": "explore",
      "summary": "Equip the harness and use Foxparks",
      "detail": "Equip the harness on Foxparks via the Pal menu.  Summon Foxparks, then hold the attack button to spray fire like a flamethrower【513843636763139†L117-L170】.  This tool is excellent for clearing early dungeons and lighting furnaces.",
      "targets": [
        {
          "kind": "item",
          "id": "foxparks-harness",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "foxparks-harness"
        ],
        "pals": [
          "foxparks"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 50
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "paldb-foxparks-partner"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "foxparks-harness",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+1",
    "key_unlocks": []
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "mount-eikthyrdeer-saddle",
      "reason": "Progress to a ridable mount after unlocking saddle tech"
    },
    {
      "route_id": "mount-direhowl-harness",
      "reason": "Alternative ground mount path"
    }
  ]
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
  "tags": [
    "mount",
    "mobility",
    "mid-game",
    "logging"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 12,
    "max": 15
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "tech-pal-gear-workbench"
    ],
    "items": [],
    "pals": [
      "eikthyrdeer"
    ]
  },
  "objectives": [
    "Capture an Eikthyrdeer",
    "Unlock the Eikthyrdeer Saddle tech",
    "Gather Leather, Fiber, Ingots, Horns and Paldium",
    "Craft the saddle",
    "Ride the mount"
  ],
  "estimated_time_minutes": {
    "solo": 40,
    "coop": 30
  },
  "estimated_xp_gain": {
    "min": 800,
    "max": 1200
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Loss of materials",
    "hardcore": "Death may delete your character and Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Farm Leather and Fiber before attempting the capture; Eikthyrdeer hits hard at level 10 and below.",
    "overleveled": "Skip step :001 if you already captured multiple Eikthyrdeer and proceed to crafting for a quick unlock.",
    "resource_shortages": [
      {
        "item_id": "ingot",
        "solution": "Smelt Ore at a Primitive Furnace before starting step :003."
      },
      {
        "item_id": "horn",
        "solution": "Hunt extra Eikthyrdeer or trade with co-op partners who have surplus."
      }
    ],
    "time_limited": "Complete steps :002 through :004 now and return for the capture later; the saddle can be pre-crafted once resources are stockpiled.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:ingot",
        "condition": "resource_gaps contains ingot >= 10",
        "adjustment": "Insert a furnace run before step :003—queue 5 ore batches to cover the ingot deficit while other materials are gathered.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-eikthyrdeer-saddle:003"
        ]
      },
      {
        "signal": "level_gap:under",
        "condition": "player.estimated_level < recommended_level.min",
        "adjustment": "Delay the capture in :001 and loop resource-leather-early plus tower-free XP farms until level 12.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-eikthyrdeer-saddle:001"
        ],
        "follow_up_routes": [
          "resource-leather-early",
          "resource-paldium"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign the highest damage player to secure the capture in :001 while teammates pre-farm Fiber and Paldium for :003, reducing downtime.",
        "priority": 3,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "mount-eikthyrdeer-saddle:001",
          "mount-eikthyrdeer-saddle:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "mount-eikthyrdeer-saddle:checkpoint-capture",
      "summary": "Eikthyrdeer captured",
      "benefits": [
        "Unlocks Guardian of the Forest partner skill"
      ],
      "related_steps": [
        "mount-eikthyrdeer-saddle:001"
      ]
    },
    {
      "id": "mount-eikthyrdeer-saddle:checkpoint-craft",
      "summary": "Saddle assembled",
      "benefits": [
        "Enables riding",
        "Improves logging throughput"
      ],
      "related_steps": [
        "mount-eikthyrdeer-saddle:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-leather-early",
      "resource-paldium"
    ],
    "optional": [
      "mount-foxparks-harness"
    ]
  },
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
      "targets": [
        {
          "kind": "pal",
          "id": "eikthyrdeer",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            300,
            100
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Approach slowly and aim for a back attack; avoid the Tower’s aggro range",
          "safety_buffer_items": [
            {
              "item_id": "pal-sphere",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Hold aggro"
            },
            {
              "role": "catcher",
              "tasks": "Throw spheres"
            }
          ],
          "loot_rules": "First catch wins"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "foxparks"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ]
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 150
      },
      "outputs": {
        "items": [],
        "pals": [
          "eikthyrdeer"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "gameclubz-eikthyrdeer-saddle"
      ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:002",
      "type": "unlock-tech",
      "summary": "Unlock the saddle tech",
      "detail": "At level 12, spend 2 tech points to unlock the Eikthyrdeer Saddle【963225160620124†L160-L167】.",
      "targets": [
        {
          "kind": "tech",
          "id": "tech-eikthyrdeer-saddle"
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 10,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "tech-eikthyrdeer-saddle"
          ]
        }
      },
      "branching": [],
      "citations": [
        "gameclubz-eikthyrdeer-saddle"
      ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 5 Leather, 20 Fiber, 10 Ingots, 3 Horns and 15 Paldium Fragments【963225160620124†L160-L167】.  Leather can be farmed using the leather subroute.  Fiber is harvested from bushes; Ingots require smelting ore.  Horns drop from Eikthyrdeer; if you only have one, defeat additional Eikthyrdeers.  Paldium comes from ore nodes.",
      "targets": [
        {
          "kind": "item",
          "id": "leather",
          "qty": 5
        },
        {
          "kind": "item",
          "id": "fiber",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "ingot",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "horn",
          "qty": 3
        },
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 15
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            189,
            -478
          ],
          "time": "any",
          "weather": "any"
        },
        {
          "region_id": "bamboo-groves",
          "coords": [
            300,
            300
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Gather a 20 % buffer (6 Leather, 24 Fiber) to account for mistakes",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "hunter",
              "tasks": "Farm Leather and Horns"
            },
            {
              "role": "miner",
              "tasks": "Mine ore and smelt Ingots"
            },
            {
              "role": "gatherer",
              "tasks": "Collect Fiber and Paldium"
            }
          ],
          "loot_rules": "Pool resources and split after crafting"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 300,
        "max": 500
      },
      "outputs": {
        "items": [
          {
            "item_id": "leather",
            "qty": 5
          },
          {
            "item_id": "fiber",
            "qty": 20
          },
          {
            "item_id": "ingot",
            "qty": 10
          },
          {
            "item_id": "horn",
            "qty": 3
          },
          {
            "item_id": "paldium-fragment",
            "qty": 15
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks leather >= 5",
          "action": "include_subroute",
          "subroute_ref": "resource-leather-early"
        }
      ],
      "citations": [
        "gameclubz-eikthyrdeer-saddle",
        "eikthyrdeer-drops"
      ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:004",
      "type": "craft",
      "summary": "Craft the saddle",
      "detail": "Use the Pal Gear Workbench to craft the Eikthyrdeer Saddle【963225160620124†L160-L167】.  The process takes around 90 seconds.",
      "targets": [
        {
          "kind": "item",
          "id": "eikthyrdeer-saddle",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 150
      },
      "outputs": {
        "items": [
          {
            "item_id": "eikthyrdeer-saddle",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "gameclubz-eikthyrdeer-saddle"
      ]
    },
    {
      "step_id": "mount-eikthyrdeer-saddle:005",
      "type": "explore",
      "summary": "Equip and ride your mount",
      "detail": "Equip the saddle on Eikthyrdeer via the Pal menu and summon it.  Press LB to call the Pal and X to mount.  Enjoy increased movement speed, a double jump and improved logging efficiency【142053078936299†L123-L142】.",
      "targets": [
        {
          "kind": "pal",
          "id": "eikthyrdeer",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "eikthyrdeer-saddle"
        ],
        "pals": [
          "eikthyrdeer"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 70
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "gameclubz-eikthyrdeer-saddle",
        "eikthyrdeer-partner-skill"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "eikthyrdeer-saddle",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+2 to +3",
    "key_unlocks": [
      "tech-eikthyrdeer-saddle"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "mount-nitewing-saddle",
      "reason": "Progress to a flying mount"
    },
    {
      "route_id": "tower-rayne-syndicate",
      "reason": "Now strong enough to challenge a tower"
    }
  ]
}
```

### Route: Craft Direhowl Harness (Ground Mount)

Direhowl provides a faster ground mount than Eikthyrdeer but lacks logging bonuses.  This route covers capturing Direhowl and crafting its harness.

```json
{
  "route_id": "mount-direhowl-harness",
  "title": "Craft Direhowl Harness",
  "category": "mounts",
  "tags": [
    "mount",
    "speed",
    "mid-game",
    "night-hunt"
  ],
  "progression_role": "optional",
  "recommended_level": {
    "min": 9,
    "max": 12
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "tech-pal-gear-workbench"
    ],
    "items": [],
    "pals": [
      "direhowl"
    ]
  },
  "objectives": [
    "Capture a Direhowl",
    "Unlock the Direhowl Harness",
    "Gather Leather, Wood, Fiber and Paldium",
    "Craft the harness",
    "Ride the mount"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 20
  },
  "estimated_xp_gain": {
    "min": 500,
    "max": 800
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Loss of materials",
    "hardcore": "Death may delete character and Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Hunt Direhowl during dawn when fewer spawn together, and bring a tanky Pal to soak hits.",
    "overleveled": "Use tranquilizer bolts to speed up captures; Direhowl’s HP melts under high-tier gear.",
    "resource_shortages": [
      {
        "item_id": "wood",
        "solution": "Assign work Pals to logging while you hunt; deposit extras before step :003."
      },
      {
        "item_id": "leather",
        "solution": "Loop the leather subroute or trade with co-op allies."
      }
    ],
    "time_limited": "Skip step :001 if Direhowl is already caught and fast travel to your base to craft immediately.",
    "dynamic_rules": [
      {
        "signal": "mode:hardcore",
        "condition": "mode.hardcore === true",
        "adjustment": "Use the Moonless Shore spawn where cliffs provide cover; retreat after each pull to avoid overlapping packs during step :001.",
        "priority": 1,
        "mode_scope": [
          "hardcore"
        ],
        "related_steps": [
          "mount-direhowl-harness:001"
        ]
      },
      {
        "signal": "resource_gap:wood",
        "condition": "resource_gaps contains wood >= 20",
        "adjustment": "Queue base logging jobs before leaving or bring a logging Pal like Eikthyrdeer so step :003 completes in a single loop.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-direhowl-harness:003"
        ]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 20",
        "adjustment": "Craft immediately if Direhowl is already owned; otherwise capture once and postpone any optional repeat farming to a later session.",
        "priority": 3,
        "mode_scope": [
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-direhowl-harness:001",
          "mount-direhowl-harness:004"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "mount-direhowl-harness:checkpoint-capture",
      "summary": "Direhowl captured",
      "benefits": [
        "Unlocks sprinting partner skill"
      ],
      "related_steps": [
        "mount-direhowl-harness:001"
      ]
    },
    {
      "id": "mount-direhowl-harness:checkpoint-crafted",
      "summary": "Harness ready",
      "benefits": [
        "Fastest ground mount unlocked"
      ],
      "related_steps": [
        "mount-direhowl-harness:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-leather-early"
    ],
    "optional": [
      "resource-paldium"
    ]
  },
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
      "targets": [
        {
          "kind": "pal",
          "id": "direhowl",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "moonless-shore",
          "coords": [
            600,
            -350
          ],
          "time": "night",
          "weather": "any"
        },
        {
          "region_id": "twilight-dunes",
          "coords": [
            700,
            -100
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Bring a Pal with healing skills and avoid multiple Direhowls",
          "safety_buffer_items": [
            {
              "item_id": "pal-sphere",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Take aggro"
            },
            {
              "role": "catcher",
              "tasks": "Throw spheres"
            }
          ],
          "loot_rules": "First catch keeps it"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "eikthyrdeer"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ]
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [],
        "pals": [
          "direhowl"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-direhowl-recipe"
      ]
    },
    {
      "step_id": "mount-direhowl-harness:002",
      "type": "unlock-tech",
      "summary": "Unlock Direhowl Harness tech",
      "detail": "At level 9, spend 1 tech point to unlock the Direhowl Harness【197143349627535†L151-L156】.",
      "targets": [
        {
          "kind": "tech",
          "id": "tech-direhowl-harness"
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 10,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "tech-direhowl-harness"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-direhowl-recipe"
      ]
    },
    {
      "step_id": "mount-direhowl-harness:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 10 Leather, 20 Wood, 15 Fiber and 10 Paldium Fragments【197143349627535†L151-L156】.  Use the leather farming route if necessary.  Wood and Fiber can be collected around the Windswept Hills; Paldium from blue ore nodes.",
      "targets": [
        {
          "kind": "item",
          "id": "leather",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "wood",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "fiber",
          "qty": 15
        },
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 10
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Gather a 10 % buffer",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "farmer",
              "tasks": "Collect Leather"
            },
            {
              "role": "logger",
              "tasks": "Gather Wood and Fiber"
            },
            {
              "role": "miner",
              "tasks": "Mine Paldium"
            }
          ],
          "loot_rules": "Pool then split"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 200,
        "max": 350
      },
      "outputs": {
        "items": [
          {
            "item_id": "leather",
            "qty": 10
          },
          {
            "item_id": "wood",
            "qty": 20
          },
          {
            "item_id": "fiber",
            "qty": 15
          },
          {
            "item_id": "paldium-fragment",
            "qty": 10
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks leather >= 10",
          "action": "include_subroute",
          "subroute_ref": "resource-leather-early"
        }
      ],
      "citations": [
        "palwiki-direhowl-recipe",
        "shockbyte-leather-sources"
      ]
    },
    {
      "step_id": "mount-direhowl-harness:004",
      "type": "craft",
      "summary": "Craft the harness",
      "detail": "Use the Pal Gear Workbench to craft the Direhowl Harness with the collected materials【197143349627535†L151-L156】.",
      "targets": [
        {
          "kind": "item",
          "id": "direhowl-harness",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 100
      },
      "outputs": {
        "items": [
          {
            "item_id": "direhowl-harness",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-direhowl-recipe"
      ]
    },
    {
      "step_id": "mount-direhowl-harness:005",
      "type": "explore",
      "summary": "Equip and ride",
      "detail": "Equip the harness on Direhowl and ride your new mount.  It offers greater sprint speed than Eikthyrdeer but lacks double jump and logging bonuses.",
      "targets": [
        {
          "kind": "pal",
          "id": "direhowl",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "direhowl-harness"
        ],
        "pals": [
          "direhowl"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 50
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-direhowl-recipe"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "direhowl-harness",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+1 to +2",
    "key_unlocks": [
      "tech-direhowl-harness"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "mount-eikthyrdeer-saddle",
      "reason": "Alternate mount path"
    },
    {
      "route_id": "tower-rayne-syndicate",
      "reason": "Ready to tackle a boss"
    }
  ]
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
  "tags": [
    "mount",
    "flight",
    "mid-game",
    "exploration"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 15,
    "max": 20
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "mount-eikthyrdeer-saddle"
    ],
    "tech": [
      "tech-pal-gear-workbench"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Capture a Nitewing",
    "Unlock the Nitewing Saddle tech",
    "Gather materials: 20 Leather, 10 Cloth, 15 Ingots, 20 Fiber, 20 Paldium",
    "Craft the saddle",
    "Ride a flying mount"
  ],
  "estimated_time_minutes": {
    "solo": 45,
    "coop": 35
  },
  "estimated_xp_gain": {
    "min": 900,
    "max": 1400
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Loss of materials",
    "hardcore": "Death may delete character and Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Farm Leather and Cloth before travelling; Ice Wind Island’s level 18 mobs overwhelm players below 14.",
    "overleveled": "Capture Nitewing using Ultra Spheres for a near-guaranteed catch, then finish crafting in one trip.",
    "resource_shortages": [
      {
        "item_id": "cloth",
        "solution": "Queue extra Cloth at the Workbench before leaving for Ice Wind Island."
      },
      {
        "item_id": "paldium-fragment",
        "solution": "Mine volcanic nodes while mounted on Eikthyrdeer."
      }
    ],
    "time_limited": "Skip step :001 if you already own Nitewing and focus on crafting to unlock flight quickly.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:cloth",
        "condition": "resource_gaps contains cloth >= 10",
        "adjustment": "Batch-craft Cloth before departure so step :003 doesn’t require a return trip mid-route.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-nitewing-saddle:003"
        ]
      },
      {
        "signal": "time_budget_short",
        "condition": "available_time_minutes && available_time_minutes < 30",
        "adjustment": "Defer the Ice Wind Island capture to a future session; instead, craft outstanding materials in :003 and unlock the tech in :002 now.",
        "priority": 2,
        "mode_scope": [
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-nitewing-saddle:002",
          "mount-nitewing-saddle:003"
        ]
      },
      {
        "signal": "goal:exploration",
        "condition": "goals includes exploration",
        "adjustment": "Prioritise finishing all steps in one run to unlock aerial scouting; queue this route to the top of recommendations when exploration is requested.",
        "priority": 3,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "mount-nitewing-saddle:004",
          "mount-nitewing-saddle:005"
        ],
        "follow_up_routes": [
          "tech-grappling-gun",
          "tower-rayne-syndicate"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "mount-nitewing-saddle:checkpoint-capture",
      "summary": "Nitewing captured",
      "benefits": [
        "Access to flight-ready Pal"
      ],
      "related_steps": [
        "mount-nitewing-saddle:001"
      ]
    },
    {
      "id": "mount-nitewing-saddle:checkpoint-crafted",
      "summary": "Saddle complete",
      "benefits": [
        "Unlocks full aerial traversal",
        "Opens late-game farming spots"
      ],
      "related_steps": [
        "mount-nitewing-saddle:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-leather-early",
      "resource-paldium"
    ],
    "optional": [
      "mount-foxparks-harness"
    ]
  },
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
      "targets": [
        {
          "kind": "pal",
          "id": "nitewing",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "ice-wind-island",
          "coords": [
            -800,
            450
          ],
          "time": "day",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Approach from behind to avoid Nitewing’s dive attacks and bring healing supplies",
          "safety_buffer_items": [
            {
              "item_id": "pal-sphere",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "bait",
              "tasks": "Aggro Nitewing and dodge"
            },
            {
              "role": "catcher",
              "tasks": "Throw Pal Spheres"
            }
          ],
          "loot_rules": "First capture keeps it"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "eikthyrdeer"
        ],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [],
        "pals": [
          "nitewing"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "mount-nitewing-saddle:002",
      "type": "unlock-tech",
      "summary": "Unlock Nitewing Saddle tech",
      "detail": "At level 15, spend 2 tech points to unlock the Nitewing saddle【524512399342633†L151-L156】.",
      "targets": [
        {
          "kind": "tech",
          "id": "tech-nitewing-saddle"
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 40
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "tech-nitewing-saddle"
          ]
        }
      },
      "branching": [],
      "citations": [
        "palwiki-nitewing-saddle"
      ]
    },
    {
      "step_id": "mount-nitewing-saddle:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 20 Leather, 10 Cloth, 15 Ingots, 20 Fiber and 20 Paldium Fragments.  Hunt leather‑dropping Pals or branch to the leather loop if needed.  Cloth is crafted from fiber at a Primitive Workbench.  Ingots require smelting ore.",
      "targets": [
        {
          "kind": "item",
          "id": "leather",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "cloth",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "ingot",
          "qty": 15
        },
        {
          "kind": "item",
          "id": "fiber",
          "qty": 20
        },
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 20
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Collect a 20 % buffer of each material to account for failures",
          "safety_buffer_items": [
            {
              "item_id": "leather",
              "qty": 4
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "farmer",
              "tasks": "Gather Leather and Fiber"
            },
            {
              "role": "crafter",
              "tasks": "Craft Cloth and smelt Ingots"
            },
            {
              "role": "miner",
              "tasks": "Mine Paldium"
            }
          ],
          "loot_rules": "Pool resources and share after crafting"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 300,
        "max": 500
      },
      "outputs": {
        "items": [
          {
            "item_id": "leather",
            "qty": 20
          },
          {
            "item_id": "cloth",
            "qty": 10
          },
          {
            "item_id": "ingot",
            "qty": 15
          },
          {
            "item_id": "fiber",
            "qty": 20
          },
          {
            "item_id": "paldium-fragment",
            "qty": 20
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks leather >= 20",
          "action": "include_subroute",
          "subroute_ref": "resource-leather-early"
        }
      ],
      "citations": [
        "palwiki-nitewing-saddle",
        "shockbyte-leather-sources"
      ]
    },
    {
      "step_id": "mount-nitewing-saddle:004",
      "type": "craft",
      "summary": "Craft the Nitewing Saddle",
      "detail": "At your Pal Gear Workbench, craft the Nitewing Saddle using the collected materials【524512399342633†L151-L156】.  The process takes about two minutes.",
      "targets": [
        {
          "kind": "item",
          "id": "nitewing-saddle",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 150
      },
      "outputs": {
        "items": [
          {
            "item_id": "nitewing-saddle",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-nitewing-saddle"
      ]
    },
    {
      "step_id": "mount-nitewing-saddle:005",
      "type": "explore",
      "summary": "Equip and fly",
      "detail": "Equip the saddle on Nitewing via the Pal menu and summon it.  Use the mount to fly across the map at high speed, unlocking new exploration possibilities.",
      "targets": [
        {
          "kind": "pal",
          "id": "nitewing",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "nitewing-saddle"
        ],
        "pals": [
          "nitewing"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 70
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-nitewing-saddle"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "nitewing-saddle",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+2 to +3",
    "key_unlocks": [
      "tech-nitewing-saddle"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "tech-grappling-gun",
      "reason": "Use flying mobility to gather materials for advanced tools"
    },
    {
      "route_id": "tower-rayne-syndicate",
      "reason": "Now capable of taking on tower bosses"
    }
  ]
}
```

### Route: Craft Grappling Gun

The Grappling Gun allows players to traverse cliffs and gaps quickly.  Unlocking it requires an Ancient Technology Point obtained from a tower boss.  The crafting recipe calls for Paldium, Ingots, Fiber and an Ancient Civilization Part【312162085103617†L180-L205】.

```json
{
  "route_id": "tech-grappling-gun",
  "title": "Craft Grappling Gun",
  "category": "tech",
  "tags": [
    "mobility",
    "tool",
    "mid-game",
    "tech"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 12,
    "max": 16
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [],
    "tech": [
      "tech-grappling-gun"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Obtain an Ancient Technology Point",
    "Unlock Grappling Gun tech",
    "Gather crafting materials",
    "Craft the Grappling Gun",
    "Use the tool"
  ],
  "estimated_time_minutes": {
    "solo": 30,
    "coop": 25
  },
  "estimated_xp_gain": {
    "min": 500,
    "max": 800
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Loss of materials",
    "hardcore": "Death may result in permanent character loss"
  },
  "adaptive_guidance": {
    "underleveled": "Secure the Ancient Technology Point via the tower route with a coop partner if you are below level 14.",
    "overleveled": "Speedrun the tower fight and craft immediately to unlock traversal shortcuts for late-game farming.",
    "resource_shortages": [
      {
        "item_id": "ancient-civilization-part",
        "solution": "Run Ruin dungeons or reuse spare parts from tower caches."
      },
      {
        "item_id": "fiber",
        "solution": "Assign work Pals to logging stations to auto-gather while you clear the tower."
      }
    ],
    "time_limited": "Borrow an Ancient Technology Point from stored inventory and postpone dungeon farming for later.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:ancient-civilization-part",
        "condition": "resource_gaps contains ancient-civilization-part >= 1",
        "adjustment": "Schedule a dungeon run immediately after step :001 so the Ancient Part is secured before crafting begins.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tech-grappling-gun:003"
        ],
        "follow_up_routes": [
          "tower-rayne-syndicate"
        ]
      },
      {
        "signal": "goal:mobility",
        "condition": "goals includes mobility",
        "adjustment": "Prioritise this route once the Ancient Point is banked; the recommender boosts its score when mobility is requested.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tech-grappling-gun:004",
          "tech-grappling-gun:005"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties—two players clear the tower while the others farm fiber and ingots—so crafting can start immediately after the point is earned.",
        "priority": 3,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "tech-grappling-gun:001",
          "tech-grappling-gun:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tech-grappling-gun:checkpoint-point",
      "summary": "Ancient Technology Point acquired",
      "benefits": [
        "Unlocks advanced tech tier"
      ],
      "related_steps": [
        "tech-grappling-gun:001"
      ]
    },
    {
      "id": "tech-grappling-gun:checkpoint-craft",
      "summary": "Grappling Gun crafted",
      "benefits": [
        "Enables rapid traversal"
      ],
      "related_steps": [
        "tech-grappling-gun:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "tower-rayne-syndicate",
      "mount-nitewing-saddle"
    ],
    "optional": [
      "resource-paldium"
    ]
  },
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
      "targets": [
        {
          "kind": "item",
          "id": "ancient-technology-point",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 500,
        "max": 700
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks ancient-technology-point >= 1",
          "action": "include_subroute",
          "subroute_ref": "tower-rayne-syndicate"
        }
      ],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tech-grappling-gun:002",
      "type": "unlock-tech",
      "summary": "Unlock Grappling Gun tech",
      "detail": "Spend 1 Ancient Technology Point at level 12 to unlock the Grappling Gun【312162085103617†L180-L205】.",
      "targets": [
        {
          "kind": "tech",
          "id": "tech-grappling-gun"
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 10,
        "max": 20
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {
          "tech": [
            "tech-grappling-gun"
          ]
        }
      },
      "branching": [],
      "citations": [
        "pcgamer-grappling-gun"
      ]
    },
    {
      "step_id": "tech-grappling-gun:003",
      "type": "gather",
      "summary": "Collect materials",
      "detail": "Gather 10 Paldium Fragments, 10 Ingots, 30 Fiber and 1 Ancient Civilization Part【312162085103617†L180-L205】.  Ancient Civilization Parts drop from tower bosses and dungeons.",
      "targets": [
        {
          "kind": "item",
          "id": "paldium-fragment",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "ingot",
          "qty": 10
        },
        {
          "kind": "item",
          "id": "fiber",
          "qty": 30
        },
        {
          "kind": "item",
          "id": "ancient-civilization-part",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Gather a 10 % buffer of each resource",
          "safety_buffer_items": [
            {
              "item_id": "paldium-fragment",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "miner",
              "tasks": "Mine Paldium"
            },
            {
              "role": "smelter",
              "tasks": "Craft Ingots"
            },
            {
              "role": "gatherer",
              "tasks": "Harvest Fiber"
            },
            {
              "role": "raider",
              "tasks": "Farm Ancient Parts from dungeons"
            }
          ],
          "loot_rules": "Pool resources and share"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 250
      },
      "outputs": {
        "items": [
          {
            "item_id": "paldium-fragment",
            "qty": 10
          },
          {
            "item_id": "ingot",
            "qty": 10
          },
          {
            "item_id": "fiber",
            "qty": 30
          },
          {
            "item_id": "ancient-civilization-part",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamer-grappling-gun"
      ]
    },
    {
      "step_id": "tech-grappling-gun:004",
      "type": "craft",
      "summary": "Craft the Grappling Gun",
      "detail": "At your Primitive Workbench or Weapon Workbench, craft the Grappling Gun using the collected materials【312162085103617†L180-L205】.",
      "targets": [
        {
          "kind": "item",
          "id": "grappling-gun",
          "qty": 1
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 80,
        "max": 120
      },
      "outputs": {
        "items": [
          {
            "item_id": "grappling-gun",
            "qty": 1
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamer-grappling-gun"
      ]
    },
    {
      "step_id": "tech-grappling-gun:005",
      "type": "explore",
      "summary": "Use the Grappling Gun",
      "detail": "Equip the Grappling Gun and test it on nearby cliffs.  Aim at a surface and fire to pull yourself toward it.  This tool greatly improves exploration and mobility.",
      "targets": [
        {
          "kind": "item",
          "id": "grappling-gun",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "grappling-gun"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 20,
        "max": 30
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamer-grappling-gun"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "grappling-gun",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+1",
    "key_unlocks": [
      "tech-grappling-gun"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "capture-jetragon",
      "reason": "Use advanced mobility to tackle a legendary Pal"
    }
  ]
}
```

### Route: Rayne Syndicate Tower (Zoe & Grizzbolt)

The first tower challenge pits you against Zoe and her electric Pal Grizzbolt.  You must deal 30 000 damage within ten minutes【825211382965329†L103-L118】.  Completing this fight awards several Ancient Technology Points and unlocks higher‑tier tech.

```json
{
  "route_id": "tower-rayne-syndicate",
  "title": "Rayne Syndicate Tower: Zoe & Grizzbolt",
  "category": "bosses",
  "tags": [
    "tower",
    "boss",
    "ancient-points",
    "combat"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 15,
    "max": 18
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "mount-eikthyrdeer-saddle"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Travel to the Rayne Syndicate Tower",
    "Prepare with Ground‑type Pals and gear",
    "Defeat Zoe & Grizzbolt within the time limit",
    "Claim Ancient Technology Points"
  ],
  "estimated_time_minutes": {
    "solo": 15,
    "coop": 10
  },
  "estimated_xp_gain": {
    "min": 1500,
    "max": 2500
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of consumables and time",
    "hardcore": "Death results in character deletion and loss of Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Delay the attempt until level 15+ or bring a co-op partner to split aggro.",
    "overleveled": "Focus on phase DPS; you can burst the boss quickly with upgraded rifles and fire pals.",
    "resource_shortages": [
      {
        "item_id": "healing-potion",
        "solution": "Craft Large Berries at camp before entry."
      },
      {
        "item_id": "shield",
        "solution": "Forge spares at the Weapon Workbench in case of durability loss."
      }
    ],
    "time_limited": "If pressed for time, skip optional mobs and sprint straight to the arena; the boss instance starts instantly.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:healing-potion",
        "condition": "resource_gaps contains healing-potion >= 3",
        "adjustment": "Queue a berry crafting batch before travelling so each player carries at least three heals into step :003.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-rayne-syndicate:002",
          "tower-rayne-syndicate:003"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a dedicated healer who rotates shields while the DPS focuses on Grizzbolt; swap roles after each phase to manage stamina.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "tower-rayne-syndicate:003"
        ]
      },
      {
        "signal": "goal:ancient-points",
        "condition": "goals includes ancient-points",
        "adjustment": "Push this tower to the top of recommendations until its Ancient Technology Points are secured, then immediately surface tech-grappling-gun as the follow-up.",
        "priority": 3,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-rayne-syndicate:003"
        ],
        "follow_up_routes": [
          "tech-grappling-gun"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tower-rayne-syndicate:checkpoint-arrival",
      "summary": "Tower entrance reached",
      "benefits": [
        "Unlocks fast travel statue"
      ],
      "related_steps": [
        "tower-rayne-syndicate:001"
      ]
    },
    {
      "id": "tower-rayne-syndicate:checkpoint-victory",
      "summary": "Zoe & Grizzbolt defeated",
      "benefits": [
        "Awards Ancient Technology Points",
        "Unlocks Grappling Gun tech"
      ],
      "related_steps": [
        "tower-rayne-syndicate:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "mount-eikthyrdeer-saddle",
      "mount-nitewing-saddle"
    ],
    "optional": [
      "tech-grappling-gun"
    ]
  },
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
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            112,
            -434
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "eikthyrdeer-saddle"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 70
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-rayne-syndicate:002",
      "type": "prepare",
      "summary": "Prepare for battle",
      "detail": "Equip Ground or Grass Pals such as Gumoss and Fuddler to counter Grizzbolt’s Electric attacks【825211382965329†L103-L118】.  Carry healing items and equip decent armor.  In Hardcore, craft an extra shield.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Bring two Ground Pals and keep distance when Grizzbolt powers up",
          "safety_buffer_items": [
            {
              "item_id": "paldium-fragment",
              "qty": 5
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Hold boss aggro"
            },
            {
              "role": "dps",
              "tasks": "Deal damage from range"
            }
          ],
          "loot_rules": "Ancient Technology Points are shared"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "foxparks",
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 100,
        "max": 200
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-rayne-syndicate:003",
      "type": "fight",
      "summary": "Defeat Zoe & Grizzbolt",
      "detail": "Engage Zoe and her Pal Grizzbolt.  Deal at least 30K damage within ten minutes【825211382965329†L103-L118】.  Use Ground or Water attacks, dodge electric beams and avoid the arena edges.",
      "targets": [
        {
          "kind": "boss",
          "id": "rayne-syndicate-tower",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Stay mobile, use ranged attacks and always maintain a safe distance",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "healer",
              "tasks": "Heal allies"
            },
            {
              "role": "damage",
              "tasks": "Focus on Grizzbolt"
            }
          ],
          "loot_rules": "Share Ancient Technology Points equally"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "lifmunk"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 1200,
        "max": 2000
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-rayne-syndicate:004",
      "type": "quest",
      "summary": "Log the Rayne Syndicate defeat with the guild investigators",
      "detail": "After the tower clears, interact with any Investigator board to record Zoe & Grizzbolt's defeat. This advances the main story requests and unlocks fresh bounties.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 250,
        "max": 400
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "boss-cleared",
      "boss_id": "rayne-syndicate-tower"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +4",
    "key_unlocks": [
      "ancient-technology-points"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "tech-grappling-gun",
      "reason": "Rewards provide the point needed to unlock this tech"
    },
    {
      "route_id": "capture-jetragon",
      "reason": "Gives experience and resources to attempt the legendary Pal"
    },
    {
      "route_id": "tower-free-pal-alliance",
      "reason": "Next tower in the Investigator storyline"
    }
  ]
}
```

### Route: Capture Jetragon (Legendary Dragon)

This advanced route details how to capture Jetragon, a level 50 legendary Pal found at Mount Obsidian【825211382965329†L337-L339】.  It requires high‑level gear, heat resistance and strong Pals.  Capturing Jetragon provides one of the fastest flying mounts in Palworld.

```json
{
  "route_id": "capture-jetragon",
  "title": "Capture Jetragon",
  "category": "capture-index",
  "tags": [
    "legendary",
    "capture",
    "late-game",
    "flying"
  ],
  "progression_role": "optional",
  "recommended_level": {
    "min": 50,
    "max": 60
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-rayne-syndicate",
      "mount-nitewing-saddle"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Prepare high‑level gear and Pals",
    "Travel to Mount Obsidian",
    "Weaken Jetragon",
    "Capture it"
  ],
  "estimated_time_minutes": {
    "solo": 60,
    "coop": 45
  },
  "estimated_xp_gain": {
    "min": 2500,
    "max": 4000
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of valuable Pal Spheres and gear",
    "hardcore": "Death may result in permanent loss of character and Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Run tower and dungeon loops until at least level 48; bring Heat Resistant armor before attempting the volcano.",
    "overleveled": "Use Legendary Spheres and heavy weapons to shorten the fight; Jetragon can be bursted down quickly at high gear scores.",
    "resource_shortages": [
      {
        "item_id": "heat-resistant-armor",
        "solution": "Craft at a Production Assembly Line using Fire Organs and Ingot stock."
      },
      {
        "item_id": "ultra-pal-sphere",
        "solution": "Farm Ancient Parts and craft extras before travelling."
      }
    ],
    "time_limited": "Skip optional prep by borrowing Ultra Spheres from teammates and focusing on the capture attempt.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:heat-resistant-armor",
        "condition": "resource_gaps contains heat-resistant-armor >= 1",
        "adjustment": "Queue armor crafting before departure to prevent heat damage from ending the run early; do not proceed to step :002 without it.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "capture-jetragon:001"
        ]
      },
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Designate a loot master to track Ultra Sphere usage so the team can rotate capture attempts without wasting consumables.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "capture-jetragon:003",
          "capture-jetragon:004"
        ]
      },
      {
        "signal": "goal:legendary",
        "condition": "goals includes legendary",
        "adjustment": "Surface this route immediately after prerequisites clear and highlight the need for Ultra Spheres plus Grappling Gun mobility in the recommendation copy.",
        "priority": 3,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "capture-jetragon:001",
          "capture-jetragon:004"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "capture-jetragon:checkpoint-prep",
      "summary": "Heat gear and spheres ready",
      "benefits": [
        "Ensures survival in Mount Obsidian"
      ],
      "related_steps": [
        "capture-jetragon:001"
      ]
    },
    {
      "id": "capture-jetragon:checkpoint-engage",
      "summary": "Jetragon weakened",
      "benefits": [
        "Capture threshold reached"
      ],
      "related_steps": [
        "capture-jetragon:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "tech-grappling-gun",
      "mount-nitewing-saddle"
    ],
    "optional": [
      "tower-rayne-syndicate"
    ]
  },
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
        "hardcore": {
          "tactics": "Ensure all gear is upgraded and carry backup mounts",
          "safety_buffer_items": [
            {
              "item_id": "paldium-fragment",
              "qty": 10
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "tank",
              "tasks": "Take aggro and soak damage"
            },
            {
              "role": "damage",
              "tasks": "Deal sustained damage"
            },
            {
              "role": "support",
              "tasks": "Heal and provide buffs"
            }
          ],
          "loot_rules": "The player who throws the final sphere keeps Jetragon"
        }
      },
      "recommended_loadout": {
        "gear": [
          "grappling-gun"
        ],
        "pals": [
          "nitewing"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 300,
        "max": 400
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses",
        "pcgamer-grappling-gun"
      ]
    },
    {
      "step_id": "capture-jetragon:002",
      "type": "travel",
      "summary": "Reach Mount Obsidian",
      "detail": "Fly to Mount Obsidian in the volcanic region.  Use your Nitewing or Eikthyrdeer to reach the foot of the volcano without taking lava damage.",
      "targets": [],
      "locations": [
        {
          "region_id": "mount-obsidian",
          "coords": [
            850,
            -500
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "eikthyrdeer-saddle",
          "nitewing-saddle"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 80
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-jetragon"
      ]
    },
    {
      "step_id": "capture-jetragon:003",
      "type": "fight",
      "summary": "Weaken Jetragon",
      "detail": "Engage Jetragon cautiously.  Use Ice or Dragon attacks to exploit its weaknesses.  Dodge its fire breath and meteor strikes.  Reduce its HP to the capture threshold.",
      "targets": [
        {
          "kind": "pal",
          "id": "jetragon",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Maintain maximum distance and use hit‑and‑run tactics",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "kiter",
              "tasks": "Lead Jetragon around obstacles"
            },
            {
              "role": "sniper",
              "tasks": "Deal high damage with rockets"
            },
            {
              "role": "catcher",
              "tasks": "Prepare Pal Spheres"
            }
          ],
          "loot_rules": "Discuss who will claim the capture"
        }
      },
      "recommended_loadout": {
        "gear": [
          "grappling-gun"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 2000,
        "max": 3000
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-jetragon"
      ]
    },
    {
      "step_id": "capture-jetragon:004",
      "type": "capture",
      "summary": "Capture Jetragon",
      "detail": "When Jetragon’s health is low, throw Ultra Pal Spheres until you succeed.  It may take several attempts.  Once captured, Jetragon becomes a powerful flying mount with unmatched speed and combat abilities.",
      "targets": [
        {
          "kind": "pal",
          "id": "jetragon",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": [
          {
            "item_id": "pal-sphere",
            "qty": 5
          }
        ]
      },
      "xp_award_estimate": {
        "min": 200,
        "max": 300
      },
      "outputs": {
        "items": [],
        "pals": [
          "jetragon"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-jetragon"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "jetragon",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+5 to +6",
    "key_unlocks": [
      "pal-jetragon"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 0
  },
  "next_routes": []
}
```

### Route: Purposeful Arc — Early Foundation

Players who prefer a guided progression can follow this purposeful arc to
chain the early-game routes automatically.  It bundles the starter base
plan, resource farming and first mount unlocks so Palmate can recommend the
entire flow as a single experience.

```json
{
  "route_id": "purposeful-arc-early-foundation",
  "title": "Purposeful Arc — Early Foundation",
  "category": "campaign",
  "tags": [
    "purposeful",
    "campaign",
    "early-game",
    "base-building",
    "mounts"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 1,
    "max": 12
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Complete the starter playlist that unlocks automation and key work pals",
    "Craft Foxparks and Eikthyrdeer gear to add furnace automation and traversal"
  ],
  "estimated_time_minutes": {
    "solo": 110,
    "coop": 80
  },
  "estimated_xp_gain": {
    "min": 1400,
    "max": 2300
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Failed captures cost spheres and time",
    "hardcore": "Deaths during mount hunts jeopardise the save"
  },
  "adaptive_guidance": {
    "underleveled": "If you are level 3 or lower, run Starter Base and Capture twice before moving on to the mount steps.",
    "overleveled": "Players above level 12 can move straight from Foxparks harness into the Eikthyrdeer saddle without repeating the leather loop.",
    "resource_shortages": [
      {
        "item_id": "leather",
        "solution": "Repeat the leather loop in step :002 until at least 20 Leather are banked."
      },
      {
        "item_id": "paldium-fragment",
        "solution": "Trigger the resource-paldium subroute between steps :002 and :003 if you drop below 15 fragments."
      }
    ],
    "time_limited": "When you have under an hour, complete steps :001 and :003, then bookmark the saddle run in :004 for another session.",
    "dynamic_rules": [
      {
        "signal": "goal:automation",
        "condition": "goals includes automation",
        "adjustment": "Prioritise the Foxparks harness immediately after the starter base route to ignite furnaces and campfires without manual tending.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "purposeful-arc-early-foundation:003"
        ],
        "follow_up_routes": [
          "mount-foxparks-harness"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "purposeful-early:checkpoint-base",
      "summary": "Starter base secured",
      "benefits": [
        "Workbench unlocked",
        "Pal automation online"
      ],
      "related_steps": [
        "purposeful-arc-early-foundation:001"
      ]
    },
    {
      "id": "purposeful-early:checkpoint-mounts",
      "summary": "Foxparks and Eikthyrdeer saddles crafted",
      "benefits": [
        "Rapid travel",
        "Automated smelting"
      ],
      "related_steps": [
        "purposeful-arc-early-foundation:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-leather-early",
      "resource-paldium"
    ],
    "optional": [
      "capture-base-merchant"
    ]
  },
  "failure_recovery": {
    "normal": "Recraft Pal Spheres and repeat failed captures; regroup at your base to restock.",
    "hardcore": "Abort the hunt if HP drops below 40%—Hardcore saves should never risk a wipe over a mount."
  },
  "steps": [
    {
      "step_id": "purposeful-arc-early-foundation:001",
      "type": "plan",
      "summary": "Run Starter Base and Capture",
      "detail": "Queue the Starter Base and Capture route to gather tools, craft Pal Spheres and recruit Lamball-class workers. The remaining steps assume those outputs are ready.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 300,
        "max": 600
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "starter-base-capture"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-early-foundation:002",
      "type": "plan",
      "summary": "Stockpile Leather",
      "detail": "Follow the Leather Farming Loop to harvest enough hides for both upcoming harnesses before you begin crafting.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 250,
        "max": 450
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "resource-leather-early"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-early-foundation:003",
      "type": "plan",
      "summary": "Unlock Foxparks harness",
      "detail": "Execute the Foxparks harness route to light furnaces automatically and add early combat firepower.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 400,
        "max": 600
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "mount-foxparks-harness"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-early-foundation:004",
      "type": "plan",
      "summary": "Secure an Eikthyrdeer saddle",
      "detail": "Finish the Eikthyrdeer saddle route to add double-jump traversal and heavy logging support.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 450,
        "max": 650
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "mount-eikthyrdeer-saddle"
        }
      ],
      "citations": []
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "foxparks-harness",
      "qty": 1
    },
    {
      "type": "have-item",
      "item_id": "eikthyrdeer-saddle",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+2 to +4",
    "key_unlocks": [
      "tech-foxparks-harness",
      "tech-eikthyrdeer-saddle"
    ]
  },
  "metrics": {
    "progress_segments": 8,
    "boss_targets": 0,
    "quest_nodes": 2
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-mid-expansion",
      "reason": "Continue the purposeful campaign into mounts, merchants and the first tower"
    }
  ]
}
```

### Route: Purposeful Arc — Mid Expansion

This arc transitions players into mid-game systems.  It bundles the base
merchant capture, faster mounts, a flying saddle, the first tower boss and
the Grappling Gun tech so the recommender can surface them together when a
player asks for a directed progression path.

```json
{
  "route_id": "purposeful-arc-mid-expansion",
  "title": "Purposeful Arc — Mid Expansion",
  "category": "campaign",
  "tags": [
    "purposeful",
    "campaign",
    "mid-game",
    "merchant",
    "mounts"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 12,
    "max": 28
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "purposeful-arc-early-foundation"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Bring a merchant home, then upgrade to Direhowl and Nitewing mobility",
    "Defeat Zoe & Grizzbolt and invest the Ancient Technology Point in the Grappling Gun"
  ],
  "estimated_time_minutes": {
    "solo": 150,
    "coop": 110
  },
  "estimated_xp_gain": {
    "min": 2200,
    "max": 3400
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Tower wipes and failed captures cost valuable gear",
    "hardcore": "Tower defeats delete the run"
  },
  "adaptive_guidance": {
    "underleveled": "If you enter below level 15, capture Direhowl before attempting the tower to boost combat stats.",
    "overleveled": "Players above level 25 can swap steps :002 and :004 to unlock the tower first, then finish Direhowl on the way out.",
    "resource_shortages": [
      {
        "item_id": "pal-sphere",
        "solution": "Craft Great Spheres between steps :001 and :002 so human captures do not deplete your supply."
      },
      {
        "item_id": "cloth",
        "solution": "Queue cloth crafting before the flying saddle in step :003."
      }
    ],
    "time_limited": "With limited time, focus on the merchant capture and Nitewing saddle; bookmark the tower run for later.",
    "dynamic_rules": [
      {
        "signal": "goal:boss",
        "condition": "goals includes boss",
        "adjustment": "Move the tower encounter to the top of the list so you secure Ancient Technology Points before other errands.",
        "priority": 3,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "purposeful-arc-mid-expansion:004"
        ],
        "follow_up_routes": [
          "tower-rayne-syndicate"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "purposeful-mid:checkpoint-merchant",
      "summary": "Base merchant recruited",
      "benefits": [
        "Permanent vendor access"
      ],
      "related_steps": [
        "purposeful-arc-mid-expansion:001"
      ]
    },
    {
      "id": "purposeful-mid:checkpoint-tower",
      "summary": "Zoe & Grizzbolt defeated",
      "benefits": [
        "Ancient Technology Point",
        "Tower fast travel"
      ],
      "related_steps": [
        "purposeful-arc-mid-expansion:004"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-paldium",
      "resource-leather-early"
    ],
    "optional": [
      "mount-eikthyrdeer-saddle"
    ]
  },
  "failure_recovery": {
    "normal": "Restock spheres and medicine after each major attempt; re-run leather or paldium farms if supplies run low.",
    "hardcore": "Bail from tower fights when shields break—preserving the save is more important than the Ancient Point."
  },
  "steps": [
    {
      "step_id": "purposeful-arc-mid-expansion:001",
      "type": "plan",
      "summary": "Capture a merchant for your base",
      "detail": "Run the base merchant capture route so you can trade from home between the remaining steps.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 350,
        "max": 550
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "capture-base-merchant"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-mid-expansion:002",
      "type": "plan",
      "summary": "Unlock Direhowl mobility",
      "detail": "Complete the Direhowl harness route to gain a sprinting mount for desert travel and raids.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 450,
        "max": 650
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "mount-direhowl-harness"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-mid-expansion:003",
      "type": "plan",
      "summary": "Earn the Nitewing saddle",
      "detail": "Follow the Nitewing saddle guide to secure flying travel for tower assaults and long-range exploration.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 500,
        "max": 700
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "mount-nitewing-saddle"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-mid-expansion:004",
      "type": "plan",
      "summary": "Defeat Zoe & Grizzbolt",
      "detail": "Run the Rayne Syndicate tower route to earn Ancient Technology Points and unlock late-game tech.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 600,
        "max": 900
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "tower-rayne-syndicate"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-mid-expansion:005",
      "type": "plan",
      "summary": "Craft the Grappling Gun",
      "detail": "Spend the Ancient Technology Point from the tower on the Grappling Gun route to finish your mobility toolkit.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 300,
        "max": 600
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "tech-grappling-gun"
        }
      ],
      "citations": []
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "nitewing-saddle",
      "qty": 1
    },
    {
      "type": "have-tech",
      "tech_id": "tech-grappling-gun"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +5",
    "key_unlocks": [
      "tech-grappling-gun",
      "base-merchant-vendor"
    ]
  },
  "metrics": {
    "progress_segments": 8,
    "boss_targets": 1,
    "quest_nodes": 2
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-legendary-push",
      "reason": "Cap the purposeful run with a legendary capture"
    }
  ]
}
```

### Route: Purposeful Arc — Legendary Push

The final purposeful arc pairs Grappling Gun mobility with the legendary
Jetragon capture.  Queue it when you want a single campaign task that
carries you from late-game prep into the flagship legendary mount.

```json
{
  "route_id": "purposeful-arc-legendary-push",
  "title": "Purposeful Arc — Legendary Push",
  "category": "campaign",
  "tags": [
    "purposeful",
    "campaign",
    "late-game",
    "legendary",
    "raid-prep"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 35,
    "max": 50
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "purposeful-arc-mid-expansion"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Refresh Grappling Gun supplies and craft endgame gear",
    "Capture the legendary Jetragon to finish the purposeful campaign"
  ],
  "estimated_time_minutes": {
    "solo": 120,
    "coop": 95
  },
  "estimated_xp_gain": {
    "min": 2600,
    "max": 4200
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Legendary attempts consume expensive spheres",
    "hardcore": "Heat damage and boss wipes can end the save"
  },
  "adaptive_guidance": {
    "underleveled": "If you are under level 40, loop tower and dungeon routes for XP before tackling Jetragon.",
    "overleveled": "Players with legendary gear can skip the Grappling Gun refresh and go straight to the capture attempt.",
    "resource_shortages": [
      {
        "item_id": "ultra-pal-sphere",
        "solution": "Farm Ancient Parts via tower re-clears before committing to the capture."
      }
    ],
    "time_limited": "With limited time, scout Mount Obsidian and craft Ultra Spheres now, then schedule the capture for later.",
    "dynamic_rules": [
      {
        "signal": "goal:legendary",
        "condition": "goals includes legendary",
        "adjustment": "Surface the Jetragon capture immediately and keep it pinned in the active queue until it is completed.",
        "priority": 3,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "purposeful-arc-legendary-push:002"
        ],
        "follow_up_routes": [
          "capture-jetragon"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "purposeful-legendary:checkpoint-prep",
      "summary": "Grappling Gun refitted",
      "benefits": [
        "Mobility confirmed"
      ],
      "related_steps": [
        "purposeful-arc-legendary-push:001"
      ]
    },
    {
      "id": "purposeful-legendary:checkpoint-capture",
      "summary": "Jetragon secured",
      "benefits": [
        "Legendary flying mount unlocked"
      ],
      "related_steps": [
        "purposeful-arc-legendary-push:002"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "tower-rayne-syndicate",
      "tech-grappling-gun"
    ],
    "optional": [
      "resource-leather-early"
    ]
  },
  "failure_recovery": {
    "normal": "Refill Ultra Spheres and cooling gear after a failed attempt before re-engaging.",
    "hardcore": "Exit the volcano if armour drops into the red; Hardcore survival outweighs the legendary reward."
  },
  "steps": [
    {
      "step_id": "purposeful-arc-legendary-push:001",
      "type": "plan",
      "summary": "Refresh Grappling Gun logistics",
      "detail": "Re-run the Grappling Gun route if you still need Ancient Parts or crafted charges before travelling to Mount Obsidian.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 400,
        "max": 600
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "tech-grappling-gun"
        }
      ],
      "citations": []
    },
    {
      "step_id": "purposeful-arc-legendary-push:002",
      "type": "plan",
      "summary": "Capture Jetragon",
      "detail": "Execute the Jetragon capture route to claim the fastest legendary mount and finish the purposeful campaign.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 2200,
        "max": 3600
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "always",
          "action": "include_subroute",
          "subroute_ref": "capture-jetragon"
        }
      ],
      "citations": []
    }
  ],
  "completion_criteria": [
    {
      "type": "have-pal",
      "pal_id": "jetragon",
      "qty": 1
    }
  ],
  "yields": {
    "levels_estimate": "+4 to +6",
    "key_unlocks": [
      "pal-jetragon"
    ]
  },
  "metrics": {
    "progress_segments": 10,
    "boss_targets": 2,
    "quest_nodes": 3
  },
  "next_routes": []
}
```
### Route: PIDF Tower: Axel & Orserk

```json
{
  "route_id": "tower-pidf-axel-orserk",
  "title": "PIDF Tower: Axel & Orserk",
  "category": "bosses",
  "tags": [
    "tower",
    "boss",
    "ancient-points",
    "combat"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 34,
    "max": 42
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-free-pal-alliance",
      "tech-grappling-gun"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Enter the PIDF desert headquarters",
    "Prepare a counter team",
    "Defeat Axel & Orserk",
    "Report the victory to the Investigator board"
  ],
  "estimated_time_minutes": {
    "solo": 17,
    "coop": 13
  },
  "estimated_xp_gain": {
    "min": 2600,
    "max": 3400
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of consumables and time",
    "hardcore": "Death results in character deletion and loss of Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Run additional base defense missions or craft higher-tier rifles before challenging Axel.",
    "overleveled": "Lean on burst Dragon damage to end Orserk quickly and skip the longer beam patterns.",
    "resource_shortages": [
      {
        "item_id": "heat-resistant-undershirt",
        "solution": "Craft heat gear at base to avoid attrition in the PIDF desert approach."
      }
    ],
    "time_limited": "Sprint past patrols and head straight to the lift; the tower queue is short once inside.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:heat-resistant-undershirt",
        "condition": "resource_gaps includes heat-resistant-undershirt",
        "adjustment": "Queue a quick heat gear craft before :001 so the desert march does not chip away your HP.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-pidf-axel-orserk:001",
          "tower-pidf-axel-orserk:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tower-pidf-axel-orserk:checkpoint-arrival",
      "summary": "PIDF gate breached",
      "benefits": [
        "Unlocks PIDF fast travel"
      ],
      "related_steps": [
        "tower-pidf-axel-orserk:001"
      ]
    },
    {
      "id": "tower-pidf-axel-orserk:checkpoint-victory",
      "summary": "Axel & Orserk defeated",
      "benefits": [
        "Grants Ancient Technology Points",
        "Opens desert mission board upgrades"
      ],
      "related_steps": [
        "tower-pidf-axel-orserk:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "tech-grappling-gun",
      "mount-direhowl-harness"
    ],
    "optional": [
      "resource-paldium"
    ]
  },
  "failure_recovery": {
    "normal": "If you fail the timer, exit to restock consumables and re-enter; progress resets but no loot is lost.",
    "hardcore": "Abort the attempt if armor durability reaches red; Hardcore characters should prioritise survival over DPS."
  },
  "steps": [
    {
      "step_id": "tower-pidf-axel-orserk:001",
      "type": "travel",
      "summary": "Enter the PIDF desert headquarters",
      "detail": "Glide into the PIDF headquarters courtyard at (350, -200). Bring heat protection; the desert sun and lasers hit hard.",
      "targets": [],
      "locations": [
        {
          "region_id": "pidf-hq",
          "coords": [
            350,
            -200
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-pidf-axel-orserk:002",
      "type": "prepare",
      "summary": "Prepare a counter team",
      "detail": "Prioritise high-mobility Electric or Dragon pals like Astegon, Rayhound, or Beakon to interrupt Orserk. Pack both heat and cold resistance for Axel's elemental swaps.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry extra shields and keep distance to avoid burst phases.",
          "safety_buffer_items": [
            {
              "item_id": "large-med-kit",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "support",
              "tasks": "Keep heals and revives ready"
            },
            {
              "role": "damage",
              "tasks": "Maintain boss aggro and burst windows"
            }
          ],
          "loot_rules": "Share Ancient Technology Points equally"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "astegon",
          "rayhound",
          "beakon"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 260
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-pidf-axel-orserk:003",
      "type": "fight",
      "summary": "Defeat Axel & Orserk",
      "detail": "Axel deploys Orserk's lightning charges. Time dodges between beam sweeps and punish after slam combos. Keep stamina for sudden teleports.",
      "targets": [
        {
          "kind": "boss",
          "id": "tower-pidf-axel-orserk",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shields and disengage during enraged phases to avoid permadeath wipes.",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "breaker",
              "tasks": "Stagger the boss with elemental counters"
            },
            {
              "role": "finisher",
              "tasks": "Push damage once shields fall"
            }
          ],
          "loot_rules": "Ensure everyone tags the boss before the final blow"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "astegon",
          "rayhound"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 2000,
        "max": 3000
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-pidf-axel-orserk:004",
      "type": "quest",
      "summary": "Report the victory",
      "detail": "File the PIDF takedown at an Investigator board to unlock the next chain of priority alerts.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 280,
        "max": 420
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "boss-cleared",
      "boss_id": "tower-pidf-axel-orserk"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +4",
    "key_unlocks": [
      "ancient-technology-points"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "tower-brothers-eternal-pyre",
      "reason": "Carry momentum into the Mount Obsidian assault"
    }
  ]
}
```

### Route: Brothers of the Eternal Pyre Tower: Marcus & Faleris

```json
{
  "route_id": "tower-brothers-eternal-pyre",
  "title": "Brothers of the Eternal Pyre Tower: Marcus & Faleris",
  "category": "bosses",
  "tags": [
    "tower",
    "boss",
    "ancient-points",
    "combat"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 40,
    "max": 48
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-pidf-axel-orserk"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Scale Mount Obsidian to the Eternal Pyre",
    "Prepare a counter team",
    "Defeat Marcus & Faleris",
    "Report the victory to the Investigator board"
  ],
  "estimated_time_minutes": {
    "solo": 19,
    "coop": 14
  },
  "estimated_xp_gain": {
    "min": 3000,
    "max": 3800
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of consumables and time",
    "hardcore": "Death results in character deletion and loss of Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Farm volcanic alpha pals or clear high-tier raids to hit level 40 before challenging Marcus.",
    "overleveled": "Use Water turrets or dual Surfents to stagger Faleris and shorten the encounter.",
    "resource_shortages": [
      {
        "item_id": "cooler-box",
        "solution": "Build a Cooler Box and craft heat-resistant meals before entering the lava zone."
      }
    ],
    "time_limited": "Teleport directly to the Mount Obsidian statue and race up the cliff, ignoring side fights.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:cooler-box",
        "condition": "resource_gaps includes cooler-box",
        "adjustment": "Add a quick cooler-box craft to keep heat buffs ready for :001.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-brothers-eternal-pyre:001",
          "tower-brothers-eternal-pyre:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tower-brothers-eternal-pyre:checkpoint-arrival",
      "summary": "Volcano ascent complete",
      "benefits": [
        "Unlocks Mount Obsidian fast travel"
      ],
      "related_steps": [
        "tower-brothers-eternal-pyre:001"
      ]
    },
    {
      "id": "tower-brothers-eternal-pyre:checkpoint-victory",
      "summary": "Marcus & Faleris defeated",
      "benefits": [
        "Awards Ancient Technology Points",
        "Unlocks late-game heat gear"
      ],
      "related_steps": [
        "tower-brothers-eternal-pyre:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-jetragon",
      "tech-grappling-gun"
    ],
    "optional": [
      "mount-direhowl-harness"
    ]
  },
  "failure_recovery": {
    "normal": "If you fail the timer, exit to restock consumables and re-enter; progress resets but no loot is lost.",
    "hardcore": "Abort the attempt if armor durability reaches red; Hardcore characters should prioritise survival over DPS."
  },
  "steps": [
    {
      "step_id": "tower-brothers-eternal-pyre:001",
      "type": "travel",
      "summary": "Scale Mount Obsidian to the Eternal Pyre",
      "detail": "Climb the lava plateau on Mount Obsidian to reach the Brothers of the Eternal Pyre tower at (-560, -518).",
      "targets": [],
      "locations": [
        {
          "region_id": "mount-obsidian",
          "coords": [
            -560,
            -518
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-brothers-eternal-pyre:002",
      "type": "prepare",
      "summary": "Prepare a counter team",
      "detail": "Assemble Water and Ice pals like Surfent, Suzaku Aqua, or Jolthog Cryst to douse Faleris. Pack cooling drinks and heatproof armor.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry extra shields and keep distance to avoid burst phases.",
          "safety_buffer_items": [
            {
              "item_id": "large-med-kit",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "support",
              "tasks": "Keep heals and revives ready"
            },
            {
              "role": "damage",
              "tasks": "Maintain boss aggro and burst windows"
            }
          ],
          "loot_rules": "Share Ancient Technology Points equally"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "surfent",
          "suzaku-aqua",
          "jolthog-cryst"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 260
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-brothers-eternal-pyre:003",
      "type": "fight",
      "summary": "Defeat Marcus & Faleris",
      "detail": "Marcus fights alongside Faleris' firestorms. Quench flame orbs, avoid lava pools, and punish when Faleris dives.",
      "targets": [
        {
          "kind": "boss",
          "id": "tower-brothers-eternal-pyre",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shields and disengage during enraged phases to avoid permadeath wipes.",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "breaker",
              "tasks": "Stagger the boss with elemental counters"
            },
            {
              "role": "finisher",
              "tasks": "Push damage once shields fall"
            }
          ],
          "loot_rules": "Ensure everyone tags the boss before the final blow"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "surfent",
          "suzaku-aqua"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 2400,
        "max": 3400
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 5
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-brothers-eternal-pyre:004",
      "type": "quest",
      "summary": "Report the victory",
      "detail": "Log the Eternal Pyre clear with the Investigator board to unlock the high-heat emergency quests.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 280,
        "max": 420
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "boss-cleared",
      "boss_id": "tower-brothers-eternal-pyre"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +4",
    "key_unlocks": [
      "ancient-technology-points"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "tower-pal-genetics",
      "reason": "Advance to the PAL Genetic Research Unit finale"
    }
  ]
}
```

### Route: PAL Genetic Research Unit: Victor & Shadowbeak

```json
{
  "route_id": "tower-pal-genetics",
  "title": "PAL Genetic Research Unit: Victor & Shadowbeak",
  "category": "bosses",
  "tags": [
    "tower",
    "boss",
    "ancient-points",
    "combat"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 46,
    "max": 54
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-brothers-eternal-pyre",
      "capture-jetragon"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Storm the PAL Genetic Research Unit",
    "Prepare a counter team",
    "Defeat Victor & Shadowbeak",
    "Report the victory to the Investigator board"
  ],
  "estimated_time_minutes": {
    "solo": 20,
    "coop": 15
  },
  "estimated_xp_gain": {
    "min": 3600,
    "max": 4400
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of consumables and time",
    "hardcore": "Death results in character deletion and loss of Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Complete legendary capture routes or high-tier raids to gear up before fighting Victor.",
    "overleveled": "Chain Dragon burst windows to phase Shadowbeak quickly and skip the late enrage.",
    "resource_shortages": [
      {
        "item_id": "ancient-technology-point",
        "solution": "Farm earlier towers or raids to stock Ancient Technology Points for emergency revives."
      }
    ],
    "time_limited": "Rush the lab lobby and ignore optional console rooms; the arena is near the entrance elevator.",
    "dynamic_rules": [
      {
        "signal": "goal:legendary-captures",
        "condition": "goals includes legendary-captures",
        "adjustment": "Surface capture-jetragon immediately after Victor falls to capitalise on the unlocked skies.",
        "priority": 2,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-pal-genetics:003"
        ],
        "follow_up_routes": [
          "capture-jetragon"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tower-pal-genetics:checkpoint-arrival",
      "summary": "Research unit breached",
      "benefits": [
        "Unlocks PAL Genetic fast travel"
      ],
      "related_steps": [
        "tower-pal-genetics:001"
      ]
    },
    {
      "id": "tower-pal-genetics:checkpoint-victory",
      "summary": "Victor & Shadowbeak defeated",
      "benefits": [
        "Awards Ancient Technology Points",
        "Opens late-game raid rotation"
      ],
      "related_steps": [
        "tower-pal-genetics:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-jetragon",
      "purposeful-arc-legendary-push"
    ],
    "optional": [
      "tech-grappling-gun"
    ]
  },
  "failure_recovery": {
    "normal": "If you fail the timer, exit to restock consumables and re-enter; progress resets but no loot is lost.",
    "hardcore": "Abort the attempt if armor durability reaches red; Hardcore characters should prioritise survival over DPS."
  },
  "steps": [
    {
      "step_id": "tower-pal-genetics:001",
      "type": "travel",
      "summary": "Storm the PAL Genetic Research Unit",
      "detail": "Fly to the snowbound PAL Genetic Research Unit around (558, 340). Expect elite automatons on the approach.",
      "targets": [],
      "locations": [
        {
          "region_id": "pal-genetic-research-unit",
          "coords": [
            558,
            340
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-pal-genetics:002",
      "type": "prepare",
      "summary": "Prepare a counter team",
      "detail": "Bring legendary Dragons such as Jetragon, Frostallion, or Shadowbeak Noct to counter Victor. Carry plenty of shields for the beam spam.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry extra shields and keep distance to avoid burst phases.",
          "safety_buffer_items": [
            {
              "item_id": "large-med-kit",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "support",
              "tasks": "Keep heals and revives ready"
            },
            {
              "role": "damage",
              "tasks": "Maintain boss aggro and burst windows"
            }
          ],
          "loot_rules": "Share Ancient Technology Points equally"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "jetragon",
          "frostallion",
          "shadowbeak"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 260
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-pal-genetics:003",
      "type": "fight",
      "summary": "Defeat Victor & Shadowbeak",
      "detail": "Victor summons Shadowbeak's void beams. Circle the arena, burst during cooldown windows, and avoid stacked lasers.",
      "targets": [
        {
          "kind": "boss",
          "id": "tower-pal-genetics",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shields and disengage during enraged phases to avoid permadeath wipes.",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "breaker",
              "tasks": "Stagger the boss with elemental counters"
            },
            {
              "role": "finisher",
              "tasks": "Push damage once shields fall"
            }
          ],
          "loot_rules": "Ensure everyone tags the boss before the final blow"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "jetragon",
          "frostallion"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 3000,
        "max": 4000
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-pal-genetics:004",
      "type": "quest",
      "summary": "Report the victory",
      "detail": "Submit the PAL Genetic Research Unit defeat to the Investigator board to unlock endgame raids and Sakurajima intel.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 280,
        "max": 420
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "boss-cleared",
      "boss_id": "tower-pal-genetics"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +4",
    "key_unlocks": [
      "ancient-technology-points"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "tower-sakurajima",
      "reason": "Travel to Sakurajima for the Moonflower offensive"
    },
    {
      "route_id": "purposeful-arc-legendary-push",
      "reason": "Leverage new tech and raids unlocked by Victor's defeat"
    }
  ]
}
```

### Route: Moonflower Tower: Saya & Selyne

```json
{
  "route_id": "tower-sakurajima",
  "title": "Moonflower Tower: Saya & Selyne",
  "category": "bosses",
  "tags": [
    "tower",
    "boss",
    "ancient-points",
    "combat"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 50,
    "max": 58
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-pal-genetics"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Sail to Sakurajima and reach Moonflower Tower",
    "Prepare a counter team",
    "Defeat Saya & Selyne",
    "Report the victory to the Investigator board"
  ],
  "estimated_time_minutes": {
    "solo": 21,
    "coop": 16
  },
  "estimated_xp_gain": {
    "min": 3800,
    "max": 4700
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of consumables and time",
    "hardcore": "Death results in character deletion and loss of Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Complete Sakurajima world quests and raid bosses to push into the low 50s before challenging Saya.",
    "overleveled": "Leverage dual Fire legendary pals to collapse Selyne's shield phases rapidly.",
    "resource_shortages": [
      {
        "item_id": "antidote",
        "solution": "Craft Antidotes and anti-toxin meals to survive Selyne's poison mist."
      }
    ],
    "time_limited": "Teleport to the island statue and head straight to the blossom platform without clearing optional camps.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:antidote",
        "condition": "resource_gaps includes antidote",
        "adjustment": "Queue a quick antidote craft before :002 so you can cleanse Selyne's poison mist.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-sakurajima:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tower-sakurajima:checkpoint-arrival",
      "summary": "Moonflower Tower reached",
      "benefits": [
        "Unlocks Sakurajima fast travel"
      ],
      "related_steps": [
        "tower-sakurajima:001"
      ]
    },
    {
      "id": "tower-sakurajima:checkpoint-victory",
      "summary": "Saya & Selyne defeated",
      "benefits": [
        "Awards Ancient Technology Points",
        "Unlocks Feybreak chain"
      ],
      "related_steps": [
        "tower-sakurajima:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "capture-jetragon",
      "purposeful-arc-legendary-push"
    ],
    "optional": [
      "mount-nitewing-saddle"
    ]
  },
  "failure_recovery": {
    "normal": "If you fail the timer, exit to restock consumables and re-enter; progress resets but no loot is lost.",
    "hardcore": "Abort the attempt if armor durability reaches red; Hardcore characters should prioritise survival over DPS."
  },
  "steps": [
    {
      "step_id": "tower-sakurajima:001",
      "type": "travel",
      "summary": "Sail to Sakurajima and reach Moonflower Tower",
      "detail": "Glide onto the blossom platform at (640, 120) on Sakurajima Island to enter Moonflower Tower.",
      "targets": [],
      "locations": [
        {
          "region_id": "sakurajima-island",
          "coords": [
            640,
            120
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-sakurajima:002",
      "type": "prepare",
      "summary": "Prepare a counter team",
      "detail": "Mix Fire and Dark pals such as Faleris, Blazamut Ryu, or Helzephyr to counter Selyne's Ice and Toxic phases. Carry antidotes for poison fog.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry extra shields and keep distance to avoid burst phases.",
          "safety_buffer_items": [
            {
              "item_id": "large-med-kit",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "support",
              "tasks": "Keep heals and revives ready"
            },
            {
              "role": "damage",
              "tasks": "Maintain boss aggro and burst windows"
            }
          ],
          "loot_rules": "Share Ancient Technology Points equally"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "faleris",
          "blazamut-ryu",
          "helzephyr"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 260
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-sakurajima:003",
      "type": "fight",
      "summary": "Defeat Saya & Selyne",
      "detail": "Saya & Selyne rotate toxic storms and Ice barrages. Cleanse poison quickly, dodge crescent slashes, and retaliate with Fire bursts.",
      "targets": [
        {
          "kind": "boss",
          "id": "tower-sakurajima",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shields and disengage during enraged phases to avoid permadeath wipes.",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "breaker",
              "tasks": "Stagger the boss with elemental counters"
            },
            {
              "role": "finisher",
              "tasks": "Push damage once shields fall"
            }
          ],
          "loot_rules": "Ensure everyone tags the boss before the final blow"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "faleris",
          "blazamut-ryu"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 3200,
        "max": 4300
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-sakurajima:004",
      "type": "quest",
      "summary": "Report the victory",
      "detail": "Report the Moonflower victory to queue Feybreak missions on the Investigator board.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 280,
        "max": 420
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "boss-cleared",
      "boss_id": "tower-sakurajima"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +4",
    "key_unlocks": [
      "ancient-technology-points"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "tower-feybreak",
      "reason": "Advance to the Feybreak finale"
    }
  ]
}
```

### Route: Feybreak Tower: Bjorn & Bastigor

```json
{
  "route_id": "tower-feybreak",
  "title": "Feybreak Tower: Bjorn & Bastigor",
  "category": "bosses",
  "tags": [
    "tower",
    "boss",
    "ancient-points",
    "combat"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 54,
    "max": 60
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-sakurajima"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Fly to the Feybreak Tower summit",
    "Prepare a counter team",
    "Defeat Bjorn & Bastigor",
    "Report the victory to the Investigator board"
  ],
  "estimated_time_minutes": {
    "solo": 22,
    "coop": 17
  },
  "estimated_xp_gain": {
    "min": 4200,
    "max": 5200
  },
  "risk_profile": "high",
  "failure_penalties": {
    "normal": "Loss of consumables and time",
    "hardcore": "Death results in character deletion and loss of Pals"
  },
  "adaptive_guidance": {
    "underleveled": "Complete Sakurajima dungeons and late-game raids to polish gear before fighting Bjorn.",
    "overleveled": "Use legendary Fire pal synergy to burst Bastigor before the heavy enrage.",
    "resource_shortages": [
      {
        "item_id": "hot-curry",
        "solution": "Cook heat buffs before the flight so the cold winds do not drain stamina."
      }
    ],
    "time_limited": "Teleport to Feybreak Outpost and ride a flyer straight to the summit, ignoring chilling patrols.",
    "dynamic_rules": [
      {
        "signal": "resource_gap:hot-curry",
        "condition": "resource_gaps includes hot-curry",
        "adjustment": "Queue warming meals before :001 to resist Feybreak chill.",
        "priority": 1,
        "mode_scope": [
          "normal",
          "hardcore",
          "solo",
          "coop"
        ],
        "related_steps": [
          "tower-feybreak:001"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "tower-feybreak:checkpoint-arrival",
      "summary": "Feybreak summit secured",
      "benefits": [
        "Unlocks Feybreak fast travel"
      ],
      "related_steps": [
        "tower-feybreak:001"
      ]
    },
    {
      "id": "tower-feybreak:checkpoint-victory",
      "summary": "Bjorn & Bastigor defeated",
      "benefits": [
        "Awards Ancient Technology Points",
        "Completes Investigator storyline"
      ],
      "related_steps": [
        "tower-feybreak:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "purposeful-arc-legendary-push",
      "capture-jetragon"
    ],
    "optional": [
      "tech-grappling-gun"
    ]
  },
  "failure_recovery": {
    "normal": "If you fail the timer, exit to restock consumables and re-enter; progress resets but no loot is lost.",
    "hardcore": "Abort the attempt if armor durability reaches red; Hardcore characters should prioritise survival over DPS."
  },
  "steps": [
    {
      "step_id": "tower-feybreak:001",
      "type": "travel",
      "summary": "Fly to the Feybreak Tower summit",
      "detail": "Soar to the peak of Feybreak Island at (512, -662). Strong winds and ice bombardments guard the tower entrance.",
      "targets": [],
      "locations": [
        {
          "region_id": "feybreak-island",
          "coords": [
            512,
            -662
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-feybreak:002",
      "type": "prepare",
      "summary": "Prepare a counter team",
      "detail": "Deploy elite Fire and Dragon pals such as Blazamut, Jetragon, or Ignis Ravager to crack Bastigor's armor. Stockpile warming meals.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Carry extra shields and keep distance to avoid burst phases.",
          "safety_buffer_items": [
            {
              "item_id": "large-med-kit",
              "qty": 2
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "support",
              "tasks": "Keep heals and revives ready"
            },
            {
              "role": "damage",
              "tasks": "Maintain boss aggro and burst windows"
            }
          ],
          "loot_rules": "Share Ancient Technology Points equally"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "blazamut",
          "jetragon",
          "ignis-ravager"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 150,
        "max": 260
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-feybreak:003",
      "type": "fight",
      "summary": "Defeat Bjorn & Bastigor",
      "detail": "Bjorn commands Bastigor's crushing strikes. Watch for icy ground spikes, maintain fire damage uptime, and save stamina for aerial dives.",
      "targets": [
        {
          "kind": "boss",
          "id": "tower-feybreak",
          "qty": 1
        }
      ],
      "locations": [],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Rotate shields and disengage during enraged phases to avoid permadeath wipes.",
          "safety_buffer_items": [
            {
              "item_id": "ancient-technology-point",
              "qty": 1
            }
          ]
        },
        "coop": {
          "role_splits": [
            {
              "role": "breaker",
              "tasks": "Stagger the boss with elemental counters"
            },
            {
              "role": "finisher",
              "tasks": "Push damage once shields fall"
            }
          ],
          "loot_rules": "Ensure everyone tags the boss before the final blow"
        }
      },
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "blazamut",
          "jetragon"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 3600,
        "max": 4800
      },
      "outputs": {
        "items": [
          {
            "item_id": "ancient-technology-point",
            "qty": 8
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "tower-feybreak:004",
      "type": "quest",
      "summary": "Report the victory",
      "detail": "Turn the Feybreak victory into the Investigator board to complete the adaptive story arc and unlock the final question set.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 280,
        "max": 420
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "boss-cleared",
      "boss_id": "tower-feybreak"
    }
  ],
  "yields": {
    "levels_estimate": "+3 to +4",
    "key_unlocks": [
      "ancient-technology-points"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 1,
    "quest_nodes": 1
  },
  "next_routes": [
    {
      "route_id": "quest-main-story",
      "reason": "Wrap the Investigator campaign and review completed questions"
    }
  ]
}
```

### Route: Investigator Main Story Wrap-Up

```json
{
  "route_id": "quest-main-story",
  "title": "Investigator Main Story Wrap-Up",
  "category": "progression",
  "tags": [
    "story",
    "quest",
    "boss"
  ],
  "progression_role": "core",
  "recommended_level": {
    "min": 1,
    "max": 60
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "tower-feybreak"
    ],
    "tech": [],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Check off every Investigator board request",
    "Track tower victories and update the adaptive question set",
    "Celebrate finishing the campaign with bonus quests"
  ],
  "estimated_time_minutes": {
    "solo": 60,
    "coop": 45
  },
  "estimated_xp_gain": {
    "min": 2000,
    "max": 3500
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Missing a board hand-in only costs time; re-open the log to resubmit.",
    "hardcore": "Hardcore players should turn in quests before logging off to avoid progress loss."
  },
  "adaptive_guidance": {
    "underleveled": "If the final requests feel rough, re-run earlier towers or legendary captures for XP boosts.",
    "overleveled": "Speed through the board and mop up any missed optional questions to unlock cosmetics.",
    "resource_shortages": [
      {
        "item_id": "ancient-technology-point",
        "solution": "Re-clear earlier towers or raid bosses to refill Ancient Technology Points before answering the final prompts."
      }
    ],
    "time_limited": "Focus on the mandatory board turn-ins first; optional question prompts can wait for a longer session.",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split the board checklist between players so everyone hands in different regions simultaneously.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "quest-main-story:002",
          "quest-main-story:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "quest-main-story:checkpoint-first",
      "summary": "Investigator board synced",
      "benefits": [
        "Displays completed question sets"
      ],
      "related_steps": [
        "quest-main-story:001"
      ]
    },
    {
      "id": "quest-main-story:checkpoint-final",
      "summary": "Campaign epilogue viewed",
      "benefits": [
        "Unlocks repeatable expert questions"
      ],
      "related_steps": [
        "quest-main-story:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "purposeful-arc-legendary-push",
      "tower-feybreak"
    ],
    "optional": [
      "capture-jetragon"
    ]
  },
  "failure_recovery": {
    "normal": "Reopen the Investigator board to re-accept any missed requests; progress is saved per question.",
    "hardcore": "Log board completions immediately to avoid losing them to Hardcore wipes."
  },
  "steps": [
    {
      "step_id": "quest-main-story:001",
      "type": "quest",
      "summary": "Sync with the Investigator board",
      "detail": "Open an Investigator board and review completed tower records. Accept any lingering story requests tied to previous bosses.",
      "targets": [],
      "locations": [
        {
          "region_id": "small-settlement",
          "coords": [
            116,
            -398
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 300,
        "max": 420
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "quest-main-story:002",
      "type": "quest",
      "summary": "Hand in tower clear evidence",
      "detail": "Submit proof of each tower victory (Rayne, Free Pal, PIDF, Eternal Pyre, PAL Genetic, Moonflower, Feybreak) to finish the Investigator campaign log.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 600,
        "max": 900
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "pcgamesn-bosses"
      ]
    },
    {
      "step_id": "quest-main-story:003",
      "type": "quest",
      "summary": "Complete the adaptive question set",
      "detail": "Answer every remaining Investigator question to unlock the adaptive guide epilogue and celebratory cosmetics.",
      "targets": [],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 700,
        "max": 1100
      },
      "outputs": {
        "items": [],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": []
    }
  ],
  "completion_criteria": [
    {
      "type": "quest-chain",
      "quest_id": "investigator-mainline"
    }
  ],
  "yields": {
    "levels_estimate": "+2 to +3",
    "key_unlocks": [
      "investigator-epilogue"
    ]
  },
  "metrics": {
    "progress_segments": 6,
    "boss_targets": 0,
    "quest_nodes": 8
  },
  "next_routes": [
    {
      "route_id": "purposeful-arc-legendary-push",
      "reason": "Replay legendary hunts with full adaptive context"
    }
  ]
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
      "gather": {
        "min": 10,
        "max": 40
      },
      "build": {
        "min": 30,
        "max": 50
      },
      "craft": {
        "min": 50,
        "max": 80
      },
      "capture": {
        "min": 60,
        "max": 200
      },
      "farm": {
        "min": 150,
        "max": 300
      },
      "unlock-tech": {
        "min": 10,
        "max": 20
      },
      "travel": {
        "min": 5,
        "max": 15
      },
      "fight": {
        "min": 100,
        "max": 500
      },
      "explore": {
        "min": 30,
        "max": 70
      },
      "quest": {
        "min": 150,
        "max": 400
      }
    },
    "metric_usage": {
      "progress_segment_value": 40,
      "boss_clear_value": 520,
      "quest_node_value": 320,
      "description": "Route-level metrics reflect adaptive momentum: progress segments reward checklist depth, boss clears add large boosts, and quest nodes track story completions."
    },
    "estimation_method": "\n1. For each completed step, take the median of its XP estimate range (or the per-step range if no estimate is provided).  Sum these medians to compute the base XP.\n2. Add adaptive bonuses: progress_segments × progress_segment_value, boss_targets × boss_clear_value, and quest_nodes × quest_node_value.\n3. Add +500 XP for each boss clear marked directly on a step and +10% for finishing the route deathless in Hardcore.  In Co-Op, divide XP evenly among players.\n4. Convert cumulative XP to a player level by finding the highest level where cumulative_xp ≤ total XP in the xp_thresholds array.\n5. Compute confidence as the fraction of steps with explicit XP estimates plus 0.1 if route metrics are provided (cap at 1.0).",
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
      "mode": {
        "hardcore": "bool",
        "coop": "bool"
      },
      "completed_routes": [
        "route-id"
      ],
      "goals": [
        "tag"
      ],
      "available_time_minutes": "int|null",
      "resource_gaps": [
        {
          "item_id": "string",
          "qty": "int"
        }
      ]
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
      "progress_segments": {
        "target": 4,
        "score_per_sigma": 1.2
      },
      "boss_targets": {
        "target": 1,
        "score_per_sigma": 1.5
      },
      "quest_nodes": {
        "target": 1,
        "score_per_sigma": 1.1
      }
    },
    "decision_flow": [
      "Filter out routes with unmet prerequisites or missing adaptive_guidance entries for requested goals",
      "Boost support routes when resource_gaps overlap with their outputs",
      "Prefer routes whose metrics meet or exceed normalization targets when available_time_minutes is low",
      "Award dynamic_alignment when player context satisfies a route’s adaptive_guidance.dynamic_rules"
    ],
    "tie_breakers": [
      "lowest_consumable_cost",
      "shortest_time",
      "highest_unlock_value",
      "alphabetical"
    ],
    "explanation_templates": {
      "prerequisites_met": "You meet all prerequisites for this route.",
      "level_fit": "Your estimated level of {level} fits the recommended range ({min}-{max}).",
      "unlock_value": "Completing this route unlocks {unlocks}.",
      "resource_need": "You need {item} for upcoming routes.",
      "progression_role": "This is a {role} route that keeps your progression on track.",
      "metric_efficiency": "Covers {progress_segments} major steps with {boss_targets} boss clear(s) and {quest_nodes} story objective(s) tracked.",
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

### Route: Gold Coin Treasury Circuit

Gold Coin Treasury Circuit chains Mau night raids, Vixy ranch digs, and settlement sell runs so your economy keeps pace with merchant schematics and tech unlocks.【palwiki-mau-raw†L11-L115】【palwiki-vixy†L118-L176】【palwiki-gold-coin-raw†L20-L28】【palwiki-wandering-merchant-raw†L1-L119】

```json
{
  "route_id": "resource-gold-coin",
  "title": "Gold Coin Treasury Circuit",
  "category": "resources",
  "tags": [
    "resource-farm",
    "gold-coin",
    "currency",
    "economy"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 12,
    "max": 30
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture"
    ],
    "tech": [
      "ranch"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Hunt Windswept Hills camps for Mau captures and coin drops",
    "Assign Mau and Vixy to ranch slots for passive coin income",
    "Sell surplus loot to settlement merchants and sweep chests between payouts"
  ],
  "estimated_time_minutes": {
    "solo": 38,
    "coop": 26
  },
  "estimated_xp_gain": {
    "min": 220,
    "max": 340
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Getting downed by faction patrols drops coin hauls and consumables needed for later merchant buys.",
    "hardcore": "Hardcore wipes while escorting merchants can delete Mau/Vixy producers and stall your entire economy for hours."
  },
  "adaptive_guidance": {
    "underleveled": "Stage near the Small Settlement statue and focus on Vixy captures before pushing into night camps for Mau coins.【palwiki-small-settlement†L1-L9】【palwiki-vixy†L118-L176】",
    "overleveled": "Chain dungeon clears with settlement sell runs so every patrol and chest becomes coin yield, not wasted time.【palwiki-mau-raw†L109-L114】【palwiki-gold-coin-raw†L20-L28】",
    "resource_shortages": [
      {
        "item_id": "gold-coin",
        "solution": "Rotate Mau and Vixy through the ranch before departing so Gold Digger and Dig Here! keep banking coins between raids.【palwiki-mau-raw†L11-L115】【palwiki-vixy†L118-L176】"
      }
    ],
    "time_limited": "Sell high-value drops at the Small Settlement merchant each pass, then sprint back to base before raids hit.【palwiki-wandering-merchant-raw†L24-L119】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign one player to escort merchants while the partner clears patrols and ferries loot to storage.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-gold-coin:003",
          "resource-gold-coin:004"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-gold-coin:checkpoint-captures",
      "label": "Mau Captured and Routed",
      "includes": [
        "resource-gold-coin:001"
      ]
    },
    {
      "id": "resource-gold-coin:checkpoint-ranch",
      "label": "Ranch Automation Paying Out",
      "includes": [
        "resource-gold-coin:002"
      ]
    },
    {
      "id": "resource-gold-coin:checkpoint-ledger",
      "label": "Merchant Sales Loop",
      "includes": [
        "resource-gold-coin:003",
        "resource-gold-coin:004"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-gold-coin:001",
      "type": "capture",
      "summary": "Sweep Windswept Hills nights for Mau",
      "detail": "Teleport to the Small Settlement (75,-479), clear nearby faction camps, and dive Windswept Hills dungeons at night to capture at least two Mau for coin production and drops.【palwiki-small-settlement†L1-L9】【palwiki-mau-raw†L11-L115】",
      "targets": [
        {
          "kind": "pal",
          "id": "mau",
          "qty": 2
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "night",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Use higher-tier spheres and disengage if multiple patrol waves stack to avoid losing coin drops.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "mega-sphere"
        ],
        "pals": [
          "rushoar"
        ],
        "consumables": [
          "paldium-fragment"
        ]
      },
      "xp_award_estimate": {
        "min": 140,
        "max": 210
      },
      "outputs": {
        "items": [
          {
            "item_id": "gold-coin",
            "qty": 200
          }
        ],
        "pals": [
          "mau"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-small-settlement",
        "palwiki-mau-raw"
      ]
    },
    {
      "step_id": "resource-gold-coin:002",
      "type": "assign",
      "summary": "Automate Mau and Vixy at the ranch",
      "detail": "Assign Mau and Vixy to ranch slots so Gold Digger and Dig Here! continuously dig coins, spheres, and arrows between field runs.【palwiki-mau-raw†L11-L115】【palwiki-vixy†L118-L176】【palwiki-gold-coin-raw†L20-L27】",
      "targets": [
        {
          "kind": "item",
          "id": "gold-coin",
          "qty": 120
        }
      ],
      "locations": [
        {
          "region_id": "base",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [],
        "pals": [
          "mau",
          "vixy"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 50,
        "max": 80
      },
      "outputs": {
        "items": [
          {
            "item_id": "gold-coin",
            "qty": 120
          }
        ],
        "pals": [
          "mau",
          "vixy"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-mau-raw",
        "palwiki-vixy",
        "palwiki-gold-coin-raw"
      ]
    },
    {
      "step_id": "resource-gold-coin:003",
      "type": "trade",
      "summary": "Sell loot to settlement merchants",
      "detail": "Haul crafted goods, spare bones, and excess pals to the Small Settlement merchants to convert inventory into gold coins before the next hunt.【palwiki-gold-coin-raw†L20-L28】【palwiki-gold-coin†L28-L44】【palwiki-wandering-merchant-raw†L1-L119】",
      "targets": [
        {
          "kind": "item",
          "id": "gold-coin",
          "qty": 300
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "coop": {
          "role_splits": [
            {
              "role": "quartermaster",
              "tasks": "Handle trades and track merchant inventory"
            },
            {
              "role": "runner",
              "tasks": "Escort goods and restock ranch pals"
            }
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "inventory-pouch"
        ],
        "pals": [
          "mau"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "gold-coin",
            "qty": 300
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-gold-coin-raw",
        "palwiki-gold-coin",
        "palwiki-wandering-merchant-raw"
      ]
    },
    {
      "step_id": "resource-gold-coin:004",
      "type": "combat",
      "summary": "Clear patrols and open chests along the circuit",
      "detail": "Sweep the crossroads between merchant stops, eliminate Syndicate patrols, and crack open treasure chests to top off coins between ranch payouts.【palwiki-gold-coin-raw†L20-L28】【palwiki-wandering-merchant-raw†L12-L18】",
      "targets": [
        {
          "kind": "item",
          "id": "gold-coin",
          "qty": 80
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            60,
            -440
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Break line of sight after each incident to avoid overlapping patrol aggro before regrouping.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "metal-spear"
        ],
        "pals": [
          "anubis"
        ],
        "consumables": [
          "medical-supplies"
        ]
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 90
      },
      "outputs": {
        "items": [
          {
            "item_id": "gold-coin",
            "qty": 80
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-gold-coin-raw",
        "palwiki-wandering-merchant-raw"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "gold-coin",
      "qty": 500
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "merchant-funding"
    ]
  },
  "metrics": {
    "progress_segments": 4,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-refined-ingot",
      "reason": "Refined ingot upgrades demand heavy merchant spending, so a coin surplus keeps furnaces online."
    },
    {
      "route_id": "resource-milk",
      "reason": "Milk and bakery chains buy daily from settlement merchants; bank coins to keep dairies stocked."
    }
  ]
}
```

### Route: Lamball Butchery Circuit

Lamball Butchery Circuit corrals Windswept Hills Lamball, unlocks the Meat Cleaver, and turns the flock into reliable Lamball Mutton for early cooking and merchant trades.【palfandom-lamball†L17-L75】【palwiki-meat-cleaver†L2-L38】【palwiki-lamball-mutton-raw†L1-L27】

```json
{
  "route_id": "resource-lamball-mutton",
  "title": "Lamball Butchery Circuit",
  "category": "resources",
  "tags": [
    "resource-farm",
    "lamball-mutton",
    "cooking",
    "early-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 6,
    "max": 18
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-wool"
    ],
    "tech": [
      "primitive-workbench",
      "meat-cleaver"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Capture Lamball near the Small Settlement statue",
    "Unlock the Meat Cleaver and butcher surplus stock for mutton",
    "Cook or trade finished cuts to keep the pantry supplied"
  ],
  "estimated_time_minutes": {
    "solo": 24,
    "coop": 16
  },
  "estimated_xp_gain": {
    "min": 160,
    "max": 240
  },
  "risk_profile": "low",
  "failure_penalties": {
    "normal": "Butchering the wrong Lamball removes wool producers and delays restocks until respawns arrive.",
    "hardcore": "Losing breeders in Hardcore forces risky replacement hunts through raider patrols."
  },
  "adaptive_guidance": {
    "underleveled": "Hunt within Palbox range so skittish Lamball leash home if poachers interfere, keeping the capture loop safe.【palfandom-lamball†L28-L33】",
    "overleveled": "Rotate extra captures through the ranch before culling them so each sweep yields wool and guaranteed mutton.【palfandom-lamball†L10-L12】【palfandom-lamball†L67-L75】",
    "resource_shortages": [
      {
        "item_id": "lamball-mutton",
        "solution": "Keep two Lamball assigned to the ranch for wool, then butcher the spares for meat to cover both pantry needs.【palfandom-lamball†L10-L12】【palfandom-lamball†L67-L75】"
      }
    ],
    "time_limited": "Cull two Lamball, cook the cuts at a nearby camp kitchen, and store meals before sprinting back to other objectives.【palwiki-lamball-mutton-raw†L1-L27】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Split duties so one player kites and captures Lamball while the partner handles cleaver work and meal prep between raids.",
        "priority": 2,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-lamball-mutton:001",
          "resource-lamball-mutton:002",
          "resource-lamball-mutton:003"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-lamball-mutton:checkpoint-corral",
      "label": "Breeder Pen Secured",
      "includes": [
        "resource-lamball-mutton:001"
      ]
    },
    {
      "id": "resource-lamball-mutton:checkpoint-cleaver",
      "label": "Cleaver Rotation Online",
      "includes": [
        "resource-lamball-mutton:002"
      ]
    },
    {
      "id": "resource-lamball-mutton:checkpoint-pantry",
      "label": "Mutton Pantry Stocked",
      "includes": [
        "resource-lamball-mutton:003"
      ]
    }
  ],
  "steps": [
    {
      "step_id": "resource-lamball-mutton:001",
      "type": "capture",
      "summary": "Net docile Lamball near the Small Settlement",
      "detail": "Teleport to the Small Settlement (75,-479) in the Windswept Hills and sweep the surrounding meadow for Lamball packs. Net four breeders before raids roll through so you can separate wool stock from butcher fodder back at base.【palwiki-small-settlement†L1-L8】【palfandom-lamball†L17-L76】",
      "targets": [
        {
          "kind": "pal",
          "id": "lamball",
          "qty": 4
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            75,
            -479
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Drag Lamball away from Syndicate patrols before throwing spheres so stray shots don’t delete your breeders.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "bola"
        ],
        "pals": [
          "lifmunk"
        ],
        "consumables": [
          "pal-sphere"
        ]
      },
      "xp_award_estimate": {
        "min": 120,
        "max": 180
      },
      "outputs": {
        "items": [],
        "pals": [
          "lamball"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-small-settlement",
        "palfandom-lamball"
      ]
    },
    {
      "step_id": "resource-lamball-mutton:002",
      "type": "craft",
      "summary": "Unlock the Meat Cleaver and butcher surplus Lamball",
      "detail": "Spend 2 Technology Points at level 12 to unlock the Meat Cleaver, craft it at the Primitive Workbench (5 Ingots, 20 Wood, 5 Stone), then butcher extra Lamball to harvest guaranteed mutton while keeping a breeding pair alive.【palwiki-meat-cleaver†L2-L38】【palfandom-lamball†L67-L75】",
      "targets": [
        {
          "kind": "item",
          "id": "lamball-mutton",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Capture backup Lamball before carving so accidents don’t strand you without wool or mutton income.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "meat-cleaver"
        ],
        "pals": [],
        "consumables": [
          "ingot"
        ]
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "lamball-mutton",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-meat-cleaver",
        "palfandom-lamball"
      ]
    },
    {
      "step_id": "resource-lamball-mutton:003",
      "type": "base",
      "summary": "Cook, trade, or store the fresh mutton",
      "detail": "Cook Lamball Mutton at a Campfire, Cooking Pot, or Electric Kitchen to stretch its hunger value, and buy or sell extra cuts through Wandering Merchants for 100/10 gold when you need to balance stockpiles.【palwiki-lamball-mutton-raw†L1-L27】",
      "targets": [
        {
          "kind": "item",
          "id": "lamball-mutton",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "campfire"
        ],
        "pals": [],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 30,
        "max": 40
      },
      "outputs": {
        "items": [
          {
            "item_id": "lamball-mutton",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-lamball-mutton-raw"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "lamball-mutton",
      "qty": 12
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "pantry-stock"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-chikipi-poultry",
      "reason": "Pair poultry and mutton harvests so hearty meal recipes stay stocked."
    },
    {
      "route_id": "resource-flour",
      "reason": "Bakery prep benefits from surplus cooked meals to keep workers fed."
    }
  ]
}
```

### Route: Mozzarina Meat Packing Loop

Mozzarina Meat Packing Loop pivots the Swordmaster pasture captures into a cleaver-and-cooler chain that harvests 2–3 Mozzarina Meat per cull while leaving ranchers on dairy duty.【segmentnext-mozzarina†L3-L8】【palwiki-mozzarina-raw†L65-L93】

```json
{
  "route_id": "resource-mozzarina-meat",
  "title": "Mozzarina Meat Packing Loop",
  "category": "resources",
  "tags": [
    "resource-farm",
    "mozzarina-meat",
    "cooking",
    "mid-game"
  ],
  "progression_role": "support",
  "recommended_level": {
    "min": 20,
    "max": 34
  },
  "modes": {
    "normal": true,
    "hardcore": true,
    "solo": true,
    "coop": true
  },
  "prerequisites": {
    "routes": [
      "starter-base-capture",
      "resource-milk"
    ],
    "tech": [
      "meat-cleaver",
      "cooler-box"
    ],
    "items": [],
    "pals": []
  },
  "objectives": [
    "Reinforce the Mozzarina pasture north of the Swordmaster sealed realm",
    "Unlock the Meat Cleaver and Cooler Box to process and chill prime cuts",
    "Cull surplus Mozzarina for guaranteed meat while preserving dairy producers"
  ],
  "estimated_time_minutes": {
    "solo": 36,
    "coop": 26
  },
  "estimated_xp_gain": {
    "min": 320,
    "max": 520
  },
  "risk_profile": "medium",
  "failure_penalties": {
    "normal": "Wiping in Bamboo Groves despawns the herd and wastes cleaver cooldowns until respawns reset.",
    "hardcore": "Hardcore deaths strand captured Mozzarina and delete crafted cleavers, so retreat if patrols swarm."
  },
  "adaptive_guidance": {
    "underleveled": "Sweep the grove at dawn, use Dark pals to stagger the herd, and pick off sleepy Mozzarina in small pulls.【segmentnext-mozzarina†L4-L7】【segmentnext-mozzarina†L21-L24】",
    "overleveled": "Rotate hunts day and night—herds respawn in pairs so you can chain captures into a cull cycle.【segmentnext-mozzarina†L4-L8】",
    "resource_shortages": [
      {
        "item_id": "mozzarina-meat",
        "solution": "Cull two Mozzarina per loop with the cleaver; each yields 2–3 meat at a 100% rate so chill the cuts immediately.【palwiki-mozzarina-raw†L65-L93】【palwiki-cooler-box-raw†L1-L27】"
      }
    ],
    "time_limited": "Butcher two captives, stash the meat in a Cooler Box, then let ranchers refill stocks between raids.【palwiki-cooler-box-raw†L1-L24】【palwiki-mozzarina-raw†L65-L93】",
    "dynamic_rules": [
      {
        "signal": "mode:coop",
        "condition": "mode.coop === true",
        "adjustment": "Assign a wrangler to kite patrols while the butcher chains cleaver swings and rotates chilled storage.",
        "priority": 1,
        "mode_scope": [
          "coop"
        ],
        "related_steps": [
          "resource-mozzarina-meat:001",
          "resource-mozzarina-meat:002"
        ]
      }
    ]
  },
  "checkpoints": [
    {
      "id": "resource-mozzarina-meat:checkpoint-herd",
      "label": "Mozzarina Herd Secured",
      "includes": [
        "resource-mozzarina-meat:001"
      ]
    },
    {
      "id": "resource-mozzarina-meat:checkpoint-cleaver",
      "label": "Cleaver & Cooler Online",
      "includes": [
        "resource-mozzarina-meat:002"
      ]
    },
    {
      "id": "resource-mozzarina-meat:checkpoint-pantry",
      "label": "Meat Pantry Stocked",
      "includes": [
        "resource-mozzarina-meat:003"
      ]
    }
  ],
  "supporting_routes": {
    "recommended": [
      "resource-milk"
    ],
    "optional": [
      "resource-ice-organ"
    ]
  },
  "failure_recovery": {
    "normal": "Fast travel to Ravine Entrance, rest five minutes, then recapture the herd once patrols rotate away.【segmentnext-mozzarina†L4-L8】",
    "hardcore": "Extract captured Mozzarina immediately and restock ice organs before another butchering run to avoid compounding losses.【segmentnext-mozzarina†L7-L8】【palwiki-cooler-box-raw†L17-L24】"
  },
  "steps": [
    {
      "step_id": "resource-mozzarina-meat:001",
      "type": "capture",
      "summary": "Reinforce the Swordmaster pasture",
      "detail": "Glide to the Sealed Realm of the Swordmaster (−117, −490) and sweep the southern Bamboo Groves. Mozzarina spawn in peaceful pairs all day, so use Dark pals to stagger them and throw Mega Spheres before Syndicate patrols rotate in.【segmentnext-mozzarina†L3-L8】【segmentnext-mozzarina†L21-L24】【124c92†L57-L61】",
      "targets": [
        {
          "kind": "pal",
          "id": "mozzarina",
          "qty": 4
        }
      ],
      "locations": [
        {
          "region_id": "bamboo-groves",
          "coords": [
            -117,
            -490
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Tag one Mozzarina at a time and drag it toward Ravine Entrance before culling so backup patrols don't collapse on you.【segmentnext-mozzarina†L4-L8】",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "mega-pal-sphere",
          "grappling-gun"
        ],
        "pals": [
          "blazehowl"
        ],
        "consumables": [
          "smoked-meat"
        ]
      },
      "xp_award_estimate": {
        "min": 200,
        "max": 320
      },
      "outputs": {
        "items": [
          {
            "item_id": "milk",
            "qty": 2
          }
        ],
        "pals": [
          "mozzarina"
        ],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "segmentnext-mozzarina",
        "palwiki-sealed-realms"
      ]
    },
    {
      "step_id": "resource-mozzarina-meat:002",
      "type": "craft",
      "summary": "Unlock cleaver and chill storage",
      "detail": "Spend 2 tech points at level 12 to unlock the Meat Cleaver, craft it at the Primitive Workbench (5 Ingots, 20 Wood, 5 Stone), then unlock the Cooler Box at level 13 so chilled storage keeps cuts fresh when tended by a Cooling Pal.【palwiki-meat-cleaver†L20-L39】【palwiki-cooler-box-raw†L1-L24】",
      "targets": [
        {
          "kind": "item",
          "id": "mozzarina-meat",
          "qty": 6
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {
        "hardcore": {
          "tactics": "Capture an extra Mozzarina before butchering so a cleaver misclick doesn't exhaust your dairy line.",
          "mode_scope": [
            "hardcore"
          ]
        }
      },
      "recommended_loadout": {
        "gear": [
          "meat-cleaver",
          "cooler-box"
        ],
        "pals": [
          "penking"
        ],
        "consumables": [
          "ice-organ"
        ]
      },
      "xp_award_estimate": {
        "min": 60,
        "max": 80
      },
      "outputs": {
        "items": [
          {
            "item_id": "mozzarina-meat",
            "qty": 6
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [
        {
          "condition": "player lacks ice-organ >= 5",
          "action": "include_subroute",
          "subroute_ref": "resource-ice-organ"
        }
      ],
      "citations": [
        "palwiki-meat-cleaver",
        "palwiki-cooler-box-raw"
      ]
    },
    {
      "step_id": "resource-mozzarina-meat:003",
      "type": "base",
      "summary": "Balance dairy and butcher rotations",
      "detail": "Keep two Mozzarina assigned to the ranch for milk while cycling the extras through the cleaver. Each cull yields 2–3 Mozzarina Meat at 100%, so stage Cooler Box slots or cook high-SAN meals as needed.【palwiki-mozzarina-raw†L65-L121】【segmentnext-mozzarina†L28-L30】",
      "targets": [
        {
          "kind": "item",
          "id": "mozzarina-meat",
          "qty": 12
        }
      ],
      "locations": [
        {
          "region_id": "windswept-hills",
          "coords": [
            0,
            0
          ],
          "time": "any",
          "weather": "any"
        }
      ],
      "mode_adjustments": {},
      "recommended_loadout": {
        "gear": [
          "cooler-box",
          "campfire"
        ],
        "pals": [
          "penking"
        ],
        "consumables": []
      },
      "xp_award_estimate": {
        "min": 40,
        "max": 60
      },
      "outputs": {
        "items": [
          {
            "item_id": "mozzarina-meat",
            "qty": 12
          }
        ],
        "pals": [],
        "unlocks": {}
      },
      "branching": [],
      "citations": [
        "palwiki-mozzarina-raw",
        "segmentnext-mozzarina"
      ]
    }
  ],
  "completion_criteria": [
    {
      "type": "have-item",
      "item_id": "mozzarina-meat",
      "qty": 12
    }
  ],
  "yields": {
    "levels_estimate": "+0 to +1",
    "key_unlocks": [
      "prime-protein"
    ]
  },
  "metrics": {
    "progress_segments": 3,
    "boss_targets": 0,
    "quest_nodes": 0
  },
  "next_routes": [
    {
      "route_id": "resource-cake",
      "reason": "Cakes and other luxury meals scale with Mozzarina dairy and meat reserves."
    },
    {
      "route_id": "resource-ice-organ",
      "reason": "Cooler Boxes demand a steady Ice Organ supply to keep meat preserved."
    }
  ]
}
```

## Source Registry

The source registry maps the short citation keys used throughout this file
to full references.  Include the title, URL and access date.  When
updating guides, refresh these entries with new dates and pages.

```json
{
  "sources": {
    "paldb-primitive-workbench": {
      "title": "Primitive Workbench \u2013 PalDB",
      "url": "https://paldb.cc/station/primitive-workbench",
      "access_date": "2025-09-30",
      "notes": "Shows that the Primitive Workbench requires 2 Wood to build\u3010907636800064548\u2020screenshot\u3011."
    },
    "thegamer-foxparks-spawn": {
      "title": "Palworld: How To Find And Capture Foxparks",
      "url": "https://www.thegamer.com/palworld-foxparks-location-guide/",
      "access_date": "2025-09-30",
      "notes": "Provides spawn coordinates for Foxparks and notes they are kindling Pals\u3010956200907149478\u2020L146-L169\u3011."
    },
    "namehero-xp-capture": {
      "title": "Palworld Leveling Guide",
      "url": "https://www.namehero.com/game-guides/palworld-leveling-guide/",
      "access_date": "2025-09-30",
      "notes": "Highlights that capturing Pals yields more XP than defeating them\u3010116860197722081\u2020L96-L128\u3011."
    },
    "shockbyte-leather-sources": {
      "title": "Palworld: How To Get Leather",
      "url": "https://shockbyte.com/blog/how-to-get-leather-in-palworld",
      "access_date": "2025-09-30",
      "notes": "Lists Pals that drop Leather and notes the Sea\u00a0Breeze Archipelago Church and Bridge of the Twin Knights as farming locations\u3010840767909995613\u2020L78-L100\u3011\u3010840767909995613\u2020L106-L135\u3011."
    },
    "shockbyte-leather-merchant": {
      "title": "Palworld: How To Get Leather",
      "url": "https://shockbyte.com/blog/how-to-get-leather-in-palworld",
      "access_date": "2025-09-30",
      "notes": "Notes that Wandering Merchants sell Leather for about 150\u00a0gold each\u3010840767909995613\u2020L78-L100\u3011."
    },
    "gameclubz-foxparks-harness": {
      "title": "Palworld \u2013 How to Unlock and Use Foxparks Harness",
      "url": "https://gameclubz.com/palworld/foxparks-harness-guide",
      "access_date": "2025-09-30",
      "notes": "Provides the Foxparks Harness recipe (3\u00a0Leather, 5\u00a0Flame Organs, 5\u00a0Paldium Fragments) and explains unlocking at level\u00a06 after catching Foxparks\u3010353245298505537\u2020L150-L180\u3011."
    },
    "gameclubz-eikthyrdeer-saddle": {
      "title": "Palworld \u2013 Eikthyrdeer Saddle Guide",
      "url": "https://gameclubz.com/palworld/eikthyrdeer-saddle-guide",
      "access_date": "2025-09-30",
      "notes": "States that the Eikthyrdeer Saddle unlocks at level\u00a012 with 2\u00a0tech points and lists required materials (5\u00a0Leather, 20\u00a0Fiber, 10\u00a0Ingots, 3\u00a0Horns, 15\u00a0Paldium Fragments)\u3010963225160620124\u2020L160-L167\u3011."
    },
    "eikthyrdeer-drops": {
      "title": "Eikthyrdeer \u2013 Palworld Wiki",
      "url": "https://palworld.fandom.com/wiki/Eikthyrdeer",
      "access_date": "2025-09-30",
      "notes": "Lists Eikthyrdeer drops: 2\u00a0Venison, 2\u20133\u00a0Leather and 2\u00a0Horns at 100\u00a0% drop rate\u3010142053078936299\u2020L295-L311\u3011."
    },
    "eikthyrdeer-partner-skill": {
      "title": "Eikthyrdeer \u2013 Palworld Wiki",
      "url": "https://palworld.fandom.com/wiki/Eikthyrdeer",
      "access_date": "2025-09-30",
      "notes": "Describes the partner skill \u2018Guardian of the Forest\u2019 \u2013 the Pal can be ridden, enables double jump and increases tree\u2011cutting efficiency\u3010142053078936299\u2020L123-L142\u3011."
    },
    "paldb-foxparks-partner": {
      "title": "Foxparks \u2013 PalDB",
      "url": "https://paldb.cc/pal/foxparks",
      "access_date": "2025-09-30",
      "notes": "Mentions the partner skill \u2018Huggy Fire\u2019 which equips Foxparks as a flamethrower and its work suitability (Kindling Lv1)\u3010513843636763139\u2020L117-L170\u3011."
    },
    "palwiki-direhowl-recipe": {
      "title": "Direhowl Saddled Harness \u2013 Palworld Wiki",
      "url": "https://palworld.fandom.com/wiki/Direhowl_Saddled_Harness",
      "access_date": "2025-09-30",
      "notes": "Provides the Direhowl harness recipe (10\u00a0Leather, 20\u00a0Wood, 15\u00a0Fiber, 10\u00a0Paldium Fragments) and states it unlocks at level\u00a09 with 1\u00a0tech point\u3010197143349627535\u2020L151-L156\u3011."
    },
    "palwiki-nitewing-saddle": {
      "title": "Nitewing Saddled Harness \u2013 Palworld Wiki",
      "url": "https://palworld.fandom.com/wiki/Nitewing_Saddle",
      "access_date": "2025-09-30",
      "notes": "Lists the Nitewing saddle recipe (20\u00a0Leather, 10\u00a0Cloth, 15\u00a0Ingots, 20\u00a0Fiber, 20\u00a0Paldium Fragments) and level requirements\u3010524512399342633\u2020L151-L156\u3011."
    },
    "updatecrazy-patch-067": {
      "title": "Palworld Update v0.6.7 Patch Notes",
      "url": "https://updatecrazy.com/palworld-update-v0-6-7-patch-notes",
      "access_date": "2025-09-30",
      "notes": "Confirms game version 1.079.736 released on Sept\u00a029\u00a02025 and fixes relating to dungeon crashes\u3010353708512100491\u2020L31-L56\u3011."
    },
    "goleap-region-levels": {
      "title": "Palworld Map Level Zones",
      "url": "https://www.gameleap.com/palworld-map-level-zones",
      "access_date": "2025-09-30",
      "notes": "Provides level ranges for each region (e.g. Windswept Hills 1\u201315, Sea\u00a0Breeze Archipelago 1\u201310)\u3010950757978743332\u2020L131-L147\u3011."
    },
    "gosunoob-vixy-breeding": {
      "title": "Palworld \u2013 Vixy Breeding Combinations",
      "url": "https://www.gosunoob.com/palworld/vixy-breeding/",
      "access_date": "2025-09-30",
      "notes": "Lists combos that produce Vixy and notes its work suitability and drops\u3010506019502892519\u2020screenshot\u3011\u3010761280216223901\u2020screenshot\u3011."
    },
    "pcgamesn-wheat-seeds": {
      "title": "Where to find Wheat Seeds in Palworld",
      "url": "https://www.pcgamesn.com/palworld/wheat-seeds",
      "access_date": "2025-10-16",
      "notes": "Explains that Dinossum drops Wheat Seeds, wandering merchants sell them for 100 gold, and Flopie spawns beyond the Bridge of the Twin Knights northeast of Rayne Syndicate Tower Entrance.【46c54c†L9-L17】"
    },
    "pcgamesn-bosses": {
      "title": "All Palworld bosses in order and how to beat them",
      "url": "https://www.pcgamesn.com/palworld/bosses",
      "access_date": "2025-09-30",
      "notes": "Provides details on tower bosses including Zoe & Grizzbolt, coordinates (112,\u00a0-434), challenge damage (30K), recommended ground Pals and tactics\u3010825211382965329\u2020L103-L118\u3011; also lists Nitewing as an Alpha Pal at Ice Wind Island (level\u00a018)\u3010825211382965329\u2020L294-L302\u3011 and Jetragon at Mount Obsidian (level\u00a050)\u3010825211382965329\u2020L337-L339\u3011."
    },
    "pcgamer-grappling-gun": {
      "title": "Palworld grappling gun guide",
      "url": "https://www.pcgamer.com/palworld-grappling-gun-crafting/",
      "access_date": "2025-09-30",
      "notes": "Explains that the Grappling Gun unlocks at level\u00a012 and costs 1\u00a0Ancient Technology Point; crafting requires 10\u00a0Paldium Fragments, 10\u00a0Ingots, 30\u00a0Fiber and 1\u00a0Ancient Civilization Part\u3010312162085103617\u2020L180-L205\u3011."
    },
    "pcgamesn-jetragon": {
      "title": "All Palworld bosses in order and how to beat them \u2013 Jetragon entry",
      "url": "https://www.pcgamesn.com/palworld/bosses",
      "access_date": "2025-09-30",
      "notes": "States that Jetragon is a level\u00a050 Legendary Celestial Dragon found at Mount Obsidian\u3010825211382965329\u2020L337-L339\u3011."
    },
    "palwiki-humans": {
      "title": "Humans \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Humans",
      "access_date": "2025-09-30",
      "notes": "Explains that non-leader humans can be captured with Pal Spheres, have lower catch rates needing higher-grade spheres, cannot use their weapons, and merchants stationed at bases provide permanent shop access despite only rank\u00a01 work suitability.\u3010529f5c\u2020L67-L90\u3011\u301094455f\u2020L13-L18\u3011"
    },
    "palwiki-small-settlement": {
      "title": "Small Settlement \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Small_Settlement",
      "access_date": "2025-10-18",
      "notes": "Provides the Small Settlement coordinates (75,-479) and lists resident merchants for early-game trade routes.【palwiki-small-settlement†L3-L15】"
    },
    "palwiki-paldium": {
      "title": "Paldium Fragment \u2013 Palworld Wiki",
      "url": "https://palworld.fandom.com/wiki/Paldium_Fragment",
      "access_date": "2025-09-30",
      "notes": "Lists river, cliff and smelting sources for Paldium Fragments including respawn timers and conversion tips\u3010palwiki-paldium\u2020L42-L71\u3011\u3010palwiki-paldium\u2020L86-L115\u3011\u3010palwiki-paldium\u2020L118-L140\u3011."
    },
    "palwiki-lamball": {
      "title": "Lamball \u2013 The Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Lamball",
      "access_date": "2025-10-01",
      "notes": "Details Lamball drops, ranch production, and spawn regions in Windswept Hills and Sea Breeze Archipelago.\u30101e15ae\u2020L1-L6\u3011\u30109dc91d\u2020L1-L5\u3011\u3010ca929c\u2020L1-L7\u3011\u30100fa8e2\u2020L1-L4\u3011"
    },
    "palfandom-lamball": {
      "title": "Lamball \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Lamball",
      "access_date": "2025-10-23",
      "notes": "Lists Windswept Hills Lamball spawns, ranch wool production, and guaranteed Lamball Mutton drops for each cull.【palfandom-lamball†L17-L75】"
    },
    "palwiki-lamball-mutton-raw": {
      "title": "Lamball Mutton \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Lamball_Mutton&action=raw",
      "access_date": "2025-10-23",
      "notes": "Shows Lamball Mutton as an ingredient sold by Wandering Merchants for 100 gold, selling for 10, and cooked at camp kitchens to restore hunger.【palwiki-lamball-mutton-raw†L1-L27】"
    },
    "palwiki-chikipi": {
      "title": "Chikipi \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Chikipi",
      "access_date": "2025-10-01",
      "notes": "States that Chikipi roam the Windswept Hills, lay eggs on the ground, and their Egg Layer partner skill produces eggs at the ranch.\u30107b6ddf\u2020L1-L27\u3011\u3010c48565\u2020L1-L10\u3011\u3010cca570\u2020L1-L2\u3011"
    },
    "palwiki-pengullet": {
      "title": "Pengullet \u2013 The Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Pengullet",
      "access_date": "2025-10-01",
      "notes": "Confirms Pengullet drop Pal Fluids and describes their coastal behaviour and utility.\u301075c8b4\u2020L10-L45\u3011"
    },
    "palwiki-pengullet-fandom": {
      "title": "Pengullet \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Pengullet",
      "access_date": "2025-10-01",
      "notes": "Lists Windswept Hills as a wild spawn region for Pengullet along with dungeon appearances.\u30107e854f\u2020L1-L9\u3011"
    },
    "palwiki-fuack": {
      "title": "Fuack \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Fuack",
      "access_date": "2025-10-01",
      "notes": "Notes Fuack roam bodies of water in the Windswept Hills and drop both Leather and Pal Fluids when defeated.\u3010edfa41\u2020L1-L12\u3011\u3010904908\u2020L1-L10\u3011"
    },
    "pcgamesn-sulfur": {
      "title": "Where to get Palworld Sulfur",
      "url": "https://www.pcgamesn.com/palworld/sulfur",
      "access_date": "2025-10-05",
      "notes": "Describes sulfur spawns at the Mossanda Forest ravine (234,-118), Mount Obsidian volcanic loops, and chest staging near the Eternal Pyre Tower Entrance.\u3010951f6a\u2020L9-L20\u3011"
    },
    "palwiki-sulfur": {
      "title": "Sulfur \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Sulfur",
      "access_date": "2025-10-05",
      "notes": "States sulfur can be mined from volcanic rocks and the dedicated Sulfur Mine.\u3010449b54\u2020L5-L8\u3011"
    },
    "pcgamesn-pure-quartz": {
      "title": "Where to get Palworld Pure Quartz",
      "url": "https://www.pcgamesn.com/palworld/pure-quartz",
      "access_date": "2025-10-05",
      "notes": "Locates Pure Quartz in the Astral Mountain snowy biome, recommends high-durability pickaxes, and suggests building an Astral base for passive mining.\u3010def911\u2020L13-L23\u3011"
    },
    "palwiki-pure-quartz": {
      "title": "Pure Quartz \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Pure_Quartz",
      "access_date": "2025-10-05",
      "notes": "Explains Pure Quartz rocks populate the Astral Mountain snowy fields and benefit from mining helpers like Xenogard.\u3010eeb471\u2020L1-L3\u3011"
    },
    "pcgamesn-polymer": {
      "title": "Palworld Polymer crafting guide",
      "url": "https://www.pcgamesn.com/palworld/polymer",
      "access_date": "2025-10-05",
      "notes": "Shows that Polymer unlocks at Technology level 33 on the Production Assembly Line and requires High Quality Pal Oil plus handiwork Pals to automate output.\u3010efa13d\u2020L1-L16\u3011"
    },
    "palwiki-polymer": {
      "title": "Polymer \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Polymer",
      "access_date": "2025-10-05",
      "notes": "Lists Polymer as crafted from 2 High Quality Pal Oil, weighs 0.5, and unlocks via the Technology branch.\u301099ff2c\u2020L5-L11\u3011"
    },
    "palwiki-high-quality-pal-oil": {
      "title": "High Quality Pal Oil \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/High_Quality_Pal_Oil",
      "access_date": "2025-10-05",
      "notes": "Catalogs High Quality Pal Oil sources including merchants, Dumud ranching, and high-tier Pals like Quivern and Relaxaurus.\u3010969e9d\u2020L1-L8\u3011"
    },
    "palwiki-charcoal": {
      "title": "Charcoal \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Charcoal",
      "access_date": "2025-10-05",
      "notes": "States charcoal is crafted at any furnace, weighs 2, and costs 2 Wood per batch for gunpowder prep.\u301018fa49\u2020L1-L1\u3011\u3010ac044b\u2020L1-L7\u3011"
    },
    "palwiki-gunpowder": {
      "title": "Gunpowder \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Gunpowder",
      "access_date": "2025-10-05",
      "notes": "Confirms gunpowder is a tier 21 tech crafted at a High Quality Workbench or better using 2 Charcoal and 1 Sulfur for ammunition.\u301031b0ff\u2020L1-L1\u3011\u30104c6362\u2020L1-L1\u3011"
    },
    "pcgamesn-beautiful-flower": {
      "title": "Palworld beautiful flower locations",
      "url": "https://www.pcgamesn.com/palworld/beautiful-flower",
      "access_date": "2025-10-07",
      "notes": "Lists Ribbunny, Petallia, Wumpo, and Lyleen as flower drops and explains Strange Juice crafting at the Medieval Medicine Workbench.\u3010ba24e5\u2020L18-L37\u3011\u30100ed4ae\u2020L1-L12\u3011"
    },
    "palwiki-wildlife-sanctuary": {
      "title": "Wildlife Sanctuary \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Wildlife_Sanctuary",
      "access_date": "2025-10-07",
      "notes": "Explains trespassing penalties and that Sanctuary No.1 hosts level 20-25 pals while No.2 and No.3 feature level 50 threats.\u3010f574c5\u2020L5-L24\u3011"
    },
    "palwiki-wildlife-sanctuary-1": {
      "title": "No. 1 Wildlife Sanctuary \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/No._1_Wildlife_Sanctuary",
      "access_date": "2025-10-07",
      "notes": "Gives the island\u2019s coordinates (90,-735), highlights resident pals, and confirms Beautiful Flower harvesting there.\u3010fe9924\u2020L1-L20\u3011"
    },
    "palwiki-wildlife-sanctuary-2": {
      "title": "No. 2 Wildlife Sanctuary \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/No._2_Wildlife_Sanctuary",
      "access_date": "2025-10-07",
      "notes": "Provides coordinates (-675,-113) and lists late-game pals plus Beautiful Flower, Sulfur, and Ore spawns.\u301015adf0\u2020L1-L22\u3011"
    },
    "palwiki-wildlife-sanctuary-3": {
      "title": "No. 3 Wildlife Sanctuary \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/No._3_Wildlife_Sanctuary",
      "access_date": "2025-10-07",
      "notes": "Locates the island at (669,640) and details Lyleen, Shadowbeak, and other high-level pals alongside Beautiful Flowers.\u3010c5acbe\u2020L1-L19\u3011"
    },
    "palwiki-ribbuny": {
      "title": "Ribbuny \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Ribbuny",
      "access_date": "2025-10-07",
      "notes": "Drop table shows Beautiful Flower as a rare drop alongside Leather and Ribbuny Ribbon while outlining work skills.\u30109be50c\u2020L31-L59\u3011"
    },
    "palwiki-petallia": {
      "title": "Petallia \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Petallia",
      "access_date": "2025-10-07",
      "notes": "Confirms Petallia guarantees 2-3 Beautiful Flowers per defeat and only appears in Sanctuary No.1 with healing partner skills.\u30109f35a4\u2020L31-L52\u3011"
    },
    "palwiki-beautiful-flower": {
      "title": "Beautiful Flower \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Beautiful_Flower",
      "access_date": "2025-10-07",
      "notes": "States the ingredient is harvested in every Wildlife Sanctuary and fuels Strange Juice recipes.\u301021cd8a\u2020L1-L28\u3011"
    },
    "pcgamesn-carbon-fiber": {
      "title": "How to get Palworld Carbon Fiber",
      "url": "https://www.pcgamesn.com/palworld/carbon-fiber",
      "access_date": "2025-10-07",
      "notes": "Explains unlocking the Production Assembly Line at level 28, the 2 Coal/5 Charcoal crafting inputs, and legendary drop alternatives from Jetragon or Shadowbeak.\u30102b82ab\u2020L138-L145\u3011"
    },
    "palwiki-carbon-fiber": {
      "title": "Carbon Fiber \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Carbon_Fiber",
      "access_date": "2025-10-07",
      "notes": "Lists Production Assembly Line recipes converting Coal or Charcoal into Carbon Fiber and documents unlock requirements.\u3010f7ee05\u2020L1-L28\u3011"
    },
    "palwiki-berry-plantation-raw": {
      "title": "Berry Plantation \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Berry_Plantation&action=raw",
      "access_date": "2025-10-29",
      "notes": "Raw wikitext lists the Berry Plantation cost of 3 Berry Seeds, 20 Wood, and 20 Stone and confirms it unlocks at technology level 5.【palwiki-berry-plantation-raw†L1-L37】"
    },
    "palwiki-berry-seeds-raw": {
      "title": "Berry Seeds \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Berry_Seeds&action=raw",
      "access_date": "2025-10-29",
      "notes": "States that Berry Seeds drop when harvesting berry bushes and are used to build Berry Plantations.【palwiki-berry-seeds-raw†L3-L24】"
    },
    "palwiki-small-settlement-raw": {
      "title": "Small Settlement \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Small_Settlement&action=raw",
      "access_date": "2025-10-29",
      "notes": "Confirms the Small Settlement sits at approximately (75,-479) in Windswept Hills and hosts both Pal and Wandering Merchants.【palwiki-small-settlement-raw†L3-L16】"
    },
    "palwiki-duneshelter-raw": {
      "title": "Duneshelter \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Duneshelter&action=raw",
      "access_date": "2025-10-29",
      "notes": "Notes Duneshelter sits at (357,347) in the desert and includes two Wandering Merchants and a Pal Merchant inside the palace ruins.【palwiki-duneshelter-raw†L1-L7】"
    },
    "palwiki-production-assembly-line": {
      "title": "Production Assembly Line \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Production_Assembly_Line",
      "access_date": "2025-10-07",
      "notes": "Details the station\u2019s level 28 unlock, material costs (100 Ingots, 50 Wood, 20 Nails, 10 Cement), and need for handiwork pals plus power.\u30105d3253\u2020L1-L35\u3011"
    },
    "palwiki-jetragon": {
      "title": "Jetragon \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Jetragon",
      "access_date": "2025-10-07",
      "notes": "Drop table shows Carbon Fiber, Polymer, and Pure Quartz rewards from the legendary Mount Obsidian dragon.\u3010278868\u2020L31-L60\u3011"
    },
    "palwiki-shadowbeak": {
      "title": "Shadowbeak \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Shadowbeak",
      "access_date": "2025-10-07",
      "notes": "Lists Carbon Fiber and Pal Metal Ingot drops plus its Sanctuary No.3 habitat and combat profile.\u3010eac1d9\u2020L33-L62\u3011"
    },
    "palwiki-berry-seeds": {
      "title": "Berry Seeds \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Berry_Seeds",
      "access_date": "2025-10-09",
      "notes": "Explains Berry Seeds drop from berry bushes and certain Pals and that Berry Plantations cost 3 seeds, 20 Wood, and 20 Stone.\u3010bcbe7f\u2020L1-L8\u3011"
    },
    "zilliongamer-berry-seeds": {
      "title": "Palworld | Berry Seeds Location & Crafting Recipe",
      "url": "https://zilliongamer.com/palworld/c/materials/berry-seeds-palworld",
      "access_date": "2025-10-09",
      "notes": "States Lifmunk and Gumoss guarantee Berry Seed drops, picking berries yields seeds, and plantations convert seeds into berry farms.\u301074f880\u2020L1-L45\u3011"
    },
    "gamesfuze-lifmunk": {
      "title": "Where to Find and Catch Lifmunk in Palworld",
      "url": "https://gamesfuze.com/guides/where-to-find-and-catch-lifmunk-in-palworld/",
      "access_date": "2025-10-09",
      "notes": "Pins Lifmunk north of Rayne Syndicate Tower at (117,-405), notes Berry Seed drops, and recommends fire-element allies for captures.\u3010b765fb\u2020L6-L17\u3011"
    },
    "dexerto-gumoss": {
      "title": "Where to find and catch Gumoss in Palworld",
      "url": "https://www.dexerto.com/palworld/where-to-find-and-catch-gumoss-in-palworld-2498063/",
      "access_date": "2025-10-09",
      "notes": "Highlights Gumoss habitats including Small Settlement and Investigator's Fork with best coordinates 208,-476 and 198,-482.\u30107da1bf\u2020L8-L18\u3011"
    },
    "palwiki-lifmunk": {
      "title": "Lifmunk \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Lifmunk",
      "access_date": "2025-10-09",
      "notes": "Lists Berry Seeds as a drop, outlines Lifmunk work skills, and confirms Windswept Hills habitat.\u3010a54223\u2020L1-L24\u3011"
    },
    "palwiki-mozzarina": {
      "title": "Mozzarina \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Mozzarina",
      "access_date": "2025-10-11",
      "notes": "Documents Milk Maker\u2019s ranch production and that Mozzarina drop milk at 100% in both normal and alpha variants.\u3010a877d4\u2020L10-L35\u3011"
    },
    "palwiki-mozzarina-raw": {
      "title": "Mozzarina \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Mozzarina&action=raw",
      "access_date": "2025-10-27",
      "notes": "Shows Mozzarina Meat dropping in 2\u20133 piece bundles at 100% alongside guaranteed milk for both normal and alpha variants.\u3010palwiki-mozzarina-raw\u2020L65-L105\u3011"
    },
    "palwiki-gumoss": {
      "title": "Gumoss \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Gumoss",
      "access_date": "2025-10-09",
      "notes": "Confirms Gumoss drops Berry Seeds and Gumoss Leaf and describes the special flower variant.\u30101e725f\u2020L1-L8\u3011"
    },
    "palwiki-ranch": {
      "title": "Ranch \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Ranch",
      "access_date": "2025-10-11",
      "notes": "Shows Ranch unlock requirements (level 5, two tech points) and build costs of 50 Wood, 20 Stone, and 30 Fiber.\u30101a1614\u2020L1-L16\u3011"
    },
    "palwiki-cooler-box-raw": {
      "title": "Cooler Box \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Cooler_Box&action=raw",
      "access_date": "2025-10-27",
      "notes": "Explains the Cooler Box unlock at technology level 13, its 20 Ingot/20 Stone/5 Ice Organ recipe, and that Cooling pals prevent stored food from spoiling.\u3010palwiki-cooler-box-raw\u2020L1-L24\u3011"
    },
    "palwiki-sealed-realms": {
      "title": "Sealed Realms \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Sealed_Realms",
      "access_date": "2025-10-11",
      "notes": "Lists every sealed realm with coordinates, including Sealed Realm of the Swordmaster at (-117,-490).\u3010124c92\u2020L57-L61\u3011"
    },
    "pcgamesn-high-quality-pal-oil": {
      "title": "Where to find Palworld High Quality Pal Oil",
      "url": "https://www.pcgamesn.com/palworld/high-quality-pal-oil",
      "access_date": "2025-10-10",
      "notes": "Calls out the Mossanda Forest lava ravine at (231,-119), merchant restocks, and Woolipop rotations for High Quality Pal Oil farming.\u30109cc14d\u2020L17-L24\u3011"
    },
    "pcgamesn-milk": {
      "title": "Where to get Palworld milk",
      "url": "https://www.pcgamesn.com/palworld/milk",
      "access_date": "2025-10-11",
      "notes": "Explains you can ranch Mozzarina for guaranteed milk and buy extra bottles from the Small Settlement merchant for 100 gold.\u301063794d\u2020L1-L14\u3011"
    },
    "palwiki-flambelle": {
      "title": "Flambelle \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Flambelle",
      "access_date": "2025-10-10",
      "notes": "Lists Flambelle\u2019s guaranteed drops, including 1 High Quality Pal Oil per defeat.\u3010c3b8c9\u2020L23-L37\u3011"
    },
    "palwiki-woolipop": {
      "title": "Woolipop \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Woolipop",
      "access_date": "2025-10-10",
      "notes": "Shows Woolipop drops 1 High Quality Pal Oil alongside Cotton Candy and documents its ranch output.\u3010c81b10\u2020L13-L41\u3011"
    },
    "palwiki-meat-cleaver": {
      "title": "Meat Cleaver \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Meat_Cleaver",
      "access_date": "2025-10-21",
      "notes": "Confirms the Meat Cleaver unlocks at level 12, costs 5 Ingots, 20 Wood, and 5 Stone to craft, and that equipping it replaces the Pet command with Butcher for harvesting Pal drops.\u3010palwiki-meat-cleaver\u2020L20-L39\u3011"
    },
    "segmentnext-mozzarina": {
      "title": "Palworld: Mozzarina Location (& Best Breeding Combos)",
      "url": "https://segmentnext.com/palworld-mozzarina/",
      "access_date": "2025-10-11",
      "notes": "Highlights Mozzarina herds grazing in the southern Bamboo Groves just north of the Sealed Realm of the Swordmaster and between nearby fast travel points.\u301069a959\u2020L1-L6\u3011"
    },
    "palwiki-wandering-merchant": {
      "title": "Wandering Merchant \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Wandering_Merchant",
      "access_date": "2025-10-12",
      "notes": "Lists merchant inventory including Berry Seeds, Wheat Seeds, Wheat, and more with shared spawn coordinates like the Small Settlement vendor (78,-477).\u3010c6adb4\u2020L34-L114\u3011"
    },
    "palwiki-dinossom": {
      "title": "Dinossom \u2013 The Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Dinossom",
      "access_date": "2025-10-16",
      "notes": "Lists Dinossom's regular drops as 1-2 Wheat Seeds at a 50% rate.【b1cc9c†L1-L2】"
    },
    "palwiki-wheat-seeds": {
      "title": "Wheat Seeds \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Wheat_Seeds",
      "access_date": "2025-10-16",
      "notes": "Explains Wheat Seeds drop sources (Bristla, Dinossom, Robinquill, etc.) and that wandering merchants sell seeds for 100 gold.\u3010a05a80\u2020L1-L13\u3011"
    },
    "palwiki-wheat-plantation": {
      "title": "Wheat Plantation \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Wheat_Plantation",
      "access_date": "2025-10-12",
      "notes": "Details build costs (3 Wheat Seeds, 35 Wood, 35 Stone), tier 15 unlock, and automation tips for growing Wheat.\u3010af5fcd\u2020L1-L12\u3011"
    },
    "palwiki-mill": {
      "title": "Mill \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Mill",
      "access_date": "2025-10-12",
      "notes": "States the Mill unlocks at technology tier 15 for 2 points, costs 50 Wood and 40 Stone, and requires a Watering Pal to grind Wheat into Flour.\u3010ecbbdd\u2020L1-L16\u3011"
    },
    "palwiki-ore": {
      "title": "Ore \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Ore",
      "access_date": "2025-10-15",
      "notes": "Explains ore nodes are gray with red streaks, cites Ore Mining Site variants, and lists mining pal drop tables for ore.\u3010047054\u2020L18-L24\u3011"
    },
    "palwiki-flour": {
      "title": "Flour \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Flour",
      "access_date": "2025-10-12",
      "notes": "Covers the 3 Wheat to 1 Flour conversion, Mill requirement, and storage recommendations for preventing spoilage.\u3010bfc9eb\u2020L1-L17\u3011"
    },
    "palwiki-wheat": {
      "title": "Wheat \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Wheat",
      "access_date": "2025-10-12",
      "notes": "Notes Wheat can be purchased from merchants or grown via Wheat Plantations before milling into Flour.\u301015b61b\u2020L1-L11\u3011"
    },
    "palwiki-ingot": {
      "title": "Ingot \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Ingot",
      "access_date": "2025-10-15",
      "notes": "Describes crafting Ingots by smelting two ore in a Primitive Furnace and highlights their role in mid-game equipment.【951c6f†L6-L16】"
    },
    "palwiki-cake": {
      "title": "Cake \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Cake",
      "access_date": "2025-10-12",
      "notes": "Lists the Cake recipe (5 Flour, 8 Red Berries, 7 Milk, 8 Eggs, 2 Honey) and outlines the ranching infrastructure needed for steady production.\u301060f5d7\u2020L1-L20\u3011"
    },
    "palwiki-berry-plantation": {
      "title": "Berry Plantation \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Berry_Plantation",
      "access_date": "2025-10-12",
      "notes": "Provides costs (3 Berry Seeds, 20 Wood, 20 Stone) and automation notes for farming Red Berries.\u30108f2b7b\u2020L1-L11\u3011"
    },
    "palwiki-cooking-pot": {
      "title": "Cooking Pot \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Cooking_Pot",
      "access_date": "2025-10-12",
      "notes": "Explains the tier 17 unlock, 20 Wood/15 Ingot/3 Flame Organ build cost, and lists Cake among Cooking Pot recipes.\u3010f8b394\u2020L1-L12\u3011"
    },
    "game8-electric-organ": {
      "title": "How to Get Electric Organs | Palworld\u3010Game8\u3011",
      "url": "https://game8.co/games/Palworld/archives/440188",
      "access_date": "2025-10-13",
      "notes": "Details Bridge of the Twin Knights Sparkit routes, merchant pricing at Small Settlement (73,-485), and the list of Electric-type pals that drop organs.\u30109565e9\u2020L3-L14\u3011\u30109565e9\u2020L60-L66\u3011"
    },
    "dexerto-electric-organ": {
      "title": "How to farm Electric Organs in Palworld",
      "url": "https://www.dexerto.com/palworld/how-to-get-farm-electric-organ-in-palworld-2489235/",
      "access_date": "2025-10-13",
      "notes": "Recommends Sparkit loops west of Rayne Tower, outlines Wandering Merchant purchases for 200 gold, and summarizes core organ crafting uses.\u3010eec516\u2020L5-L15\u3011"
    },
    "game8-flame-organ": {
      "title": "How to Get Flame Organs | Palworld\u3010Game8\u3011",
      "url": "https://game8.co/games/Palworld/archives/440175",
      "access_date": "2025-10-13",
      "notes": "Lists Flame Organ droppers, confirms 100 gold merchant pricing, and notes Flambelle ranch production via Magma Tears.\u3010cf6c22\u2020L3-L8\u3011\u3010cf6c22\u2020L56-L65\u3011"
    },
    "progameguides-flame-organ": {
      "title": "Best Flame Organ farm in Palworld",
      "url": "https://progameguides.com/palworld/best-flame-organ-farm-in-palworld-where-to-farm-fire-pals/",
      "access_date": "2025-10-13",
      "notes": "Highlights Foxparks loops from Grassy Behemoth Hills and Flambelle ranch automation at (361,-48) for sustained Flame Organ income.\u30105531dc\u2020L2-L9\u3011"
    },
    "game8-ice-organ": {
      "title": "How to Get Ice Organs | Palworld\u3010Game8\u3011",
      "url": "https://game8.co/games/Palworld/archives/440190",
      "access_date": "2025-10-13",
      "notes": "Covers Pengullet farming inside the Penking arena at (113,-351), Duneshelter merchant stock, and cautions against killing the boss during loops.\u30104307f5\u2020L3-L11\u3011\u30100e4eda\u2020L6-L83\u3011"
    },
    "game8-ore-farming": {
      "title": "How to Farm Ore and Best Locations | Palworld\u3010Game8\u3011",
      "url": "https://game8.co/games/Palworld/archives/440245",
      "access_date": "2025-10-15",
      "notes": "Lists Fort Ruins, Desolate Church, Small Settlement, and Icy Weasel Hill ore coordinates with base layout and automation guidance for mining pals.\u301040f7a9\u2020L1-L80\u3011\u3010d070f4\u2020L1-L24\u3011"
    },
    "dexerto-ice-organ": {
      "title": "How to get & farm Ice Organs in Palworld",
      "url": "https://www.dexerto.com/palworld/how-to-get-farm-ice-organs-in-palworld-2507616/",
      "access_date": "2025-10-13",
      "notes": "Adds Duneshelter purchase advice and penguin spawn descriptions for reliable Ice Organ hunting.\u3010955051\u2020L5-L9\u3011"
    },
    "palnerd-venom-gland": {
      "title": "Palworld Venom Gland Farm & Its Uses in Palworld - PalNerd",
      "url": "https://palnerd.com/palworld-venom-gland-farm/",
      "access_date": "2025-10-14",
      "notes": "Details Daedream/Depresso night hunts, Small Settlement merchant pricing, and Caprity Noct ranch drops for Venom Glands.\u3010118080\u2020L1-L36\u3011"
    },
    "palwiki-venom-gland": {
      "title": "Venom Gland \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Venom_Gland",
      "access_date": "2025-10-14",
      "notes": "Lists merchant pricing and poison Pal drop sources for Venom Glands.\u3010f93012\u2020L1-L28\u3011"
    },
    "progameguides-base-triangle": {
      "title": "Best starting base locations in Palworld \u2013 Pro Game Guides",
      "url": "https://progameguides.com/palworld/best-starting-base-locations-in-palworld/",
      "access_date": "2025-10-14",
      "notes": "Provides Plateau of Beginnings southern peninsula coordinates (230,-510 / 160,-560 / 100,-525) used for staging camps and merchant runs.\u3010c3e4e9\u2020L1-L15\u3011"
    },
    "palnerd-katress-hair": {
      "title": "Palworld Katress Hair (How to Get, Location & Uses) - PalNerd",
      "url": "https://palnerd.com/how-to-get-katress-hair-palworld/",
      "access_date": "2025-10-14",
      "notes": "Covers Katress night spawns, drop rates, and Katress Cap crafting with Speed Remedy usage.\u3010bd4bea\u2020L1-L36\u3011"
    },
    "palwiki-katress-hair": {
      "title": "Katress Hair \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Katress_Hair",
      "access_date": "2025-10-14",
      "notes": "Confirms Katress and Katress Ignis as sources and notes Katress Cap schematic vendor.\u30101a1e89\u2020L1-L18\u3011"
    },
    "segmentnext-katress": {
      "title": "Palworld: Katress Location (& Best Breeding Combos) \u2013 SegmentNext",
      "url": "https://segmentnext.com/palworld-katress/",
      "access_date": "2025-10-14",
      "notes": "Maps Moonless Shore/Verdant Brook patrols, Sealed Realm of the Invincible (241,-330) alpha, and merchant/breeding options for Katress.\u3010c322c9\u2020L1-L24\u3011"
    },
    "gameleap-katress": {
      "title": "How to Get Katress in Palworld: Location, Drops & Breeding Combos \u2013 GameLeap",
      "url": "https://www.gameleap.com/articles/how-to-get-katress-in-palworld-location-drops-breeding-combos",
      "access_date": "2025-10-14",
      "notes": "Highlights Moonless Shore and Verdant Brook night hunts plus recommended breeding pairs for Katress eggs.\u3010725fb4\u2020L1-L24\u3011"
    },
    "game8-large-pal-soul": {
      "title": "How to Get Large Pal Soul: All Recipes and Effects  | Palworld\u3010Game8\u3011",
      "url": "https://game8.co/games/Palworld/archives/440127",
      "access_date": "2025-10-17",
      "notes": "Lists Large Pal Soul drop sources (Anubis, Frostallion Noct, Necromus) and shows Crusher conversions between Medium, Large, and Giant souls plus Statue usage.\u3010game8-large-pal-soul\u2020L113-L158\u3011"
    },
    "palwiki-large-pal-soul": {
      "title": "Large Pal Soul \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Large_Pal_Soul",
      "access_date": "2025-10-17",
      "notes": "Confirms Large Pal Souls spawn on the ground and drop from Anubis, Frostallion Noct, Necromus, Neptilius, and Pal Genetic Research Unit Executioners.\u3010palwiki-large-pal-soul\u2020L116-L160\u3011"
    },
    "palwiki-statue-of-power": {
      "title": "Statue of Power \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Statue_of_Power",
      "access_date": "2025-10-17",
      "notes": "Explains Statue of Power interaction flow and that Pal enhancement consumes Small, Medium, Large, and Giant Pal Souls.\u3010palwiki-statue-of-power\u2020L160-L186\u3011"
    },
    "palwiki-crusher": {
      "title": "Crusher \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Crusher",
      "access_date": "2025-10-17",
      "notes": "Lists Crusher recipes converting Small to Medium, Medium to Large, and Giant to Large Pal Souls.\u3010palwiki-crusher\u2020L159-L179\u3011"
    },
    "palwiki-wandering-merchant-raw": {
      "title": "Wandering Merchant \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Wandering_Merchant&printable=yes&action=raw",
      "access_date": "2025-10-17",
      "notes": "Raw inventory table listing the Small Settlement (78,-477) and Duneshelter (357,347) merchants selling Tomato Seeds for 200 gold.【palwiki-wandering-merchant-raw†L197-L252】"
    },
    "palwiki-duneshelter": {
      "title": "Duneshelter \u2013 Palworld Wiki (printable)",
      "url": "https://palworld.wiki.gg/index.php?title=Duneshelter&printable=yes",
      "access_date": "2025-10-17",
      "notes": "Identifies Duneshelter at (357,347) with resident wandering merchants for desert trade routes.【palwiki-duneshelter†L506-L516】"
    },
    "palwiki-braloha-raw": {
      "title": "Braloha \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Braloha&action=raw",
      "access_date": "2025-10-17",
      "notes": "States Braloha spawns exclusively on Oasis Isle east of the Desiccated Desert peninsula.【palwiki-braloha-raw†L121-L125】"
    },
    "palwiki-wumpo-botan-raw": {
      "title": "Wumpo Botan \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Wumpo_Botan&action=raw",
      "access_date": "2025-10-17",
      "notes": "Confirms Wumpo Botan resides in No. 2 Wildlife Sanctuary and as an alpha on Eastern Wild Island.【palwiki-wumpo-botan-raw†L109-L116】"
    },
    "palwiki-vaelet-raw": {
      "title": "Vaelet \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Vaelet&action=raw",
      "access_date": "2025-10-17",
      "notes": "Notes Vaelet patrols No. 1 Wildlife Sanctuary and appears as an alpha at the Sealed Realm of the Guardian.【palwiki-vaelet-raw†L108-L116】"
    },
    "palwiki-sealed-guardian": {
      "title": "Sealed Realm of the Guardian \u2013 Palworld Wiki (printable)",
      "url": "https://palworld.wiki.gg/index.php?title=Sealed_Realm_of_the_Guardian&printable=yes",
      "access_date": "2025-10-17",
      "notes": "Lists Sealed Realm coordinates including the Guardian portal at (113,-353).【palwiki-sealed-guardian†L631-L660】"
    },
    "palwiki-tomato-seeds": {
      "title": "Tomato Seeds \u2013 Palworld Wiki (printable)",
      "url": "https://palworld.wiki.gg/index.php?title=Tomato_Seeds&printable=yes",
      "access_date": "2025-10-17",
      "notes": "Details merchant pricing (200 gold) and drop rates for Braloha, Vaelet, and Wumpo Botan tomato seeds plus plantation material costs.【palwiki-tomato-seeds†L552-L868】"
    },
    "palwiki-tomato-plantation-raw": {
      "title": "Tomato Plantation \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Tomato_Plantation&action=raw",
      "access_date": "2025-10-17",
      "notes": "Raw build data listing the 3 Tomato Seeds, 70 Wood, 50 Stone, and 5 Pal Fluids cost along with required work suitabilities.【palwiki-tomato-plantation-raw†L1-L34】"
    },
    "palfandom-anubis": {
      "title": "Anubis \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Anubis",
      "access_date": "2025-10-17",
      "notes": "States Anubis spawns as an Alpha at Twilight Dunes (-134,-95).\u3010palfandom-anubis\u2020L300-L303\u3011"
    },
    "palwiki-bone": {
      "title": "Bone \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Bone",
      "access_date": "2025-10-18",
      "notes": "Lists Wandering Merchant pricing, notes Sootseer and Vixy produce bones at the ranch, and summarizes bone crafting uses.【palwiki-bone†L1-L37】"
    },
    "palfandom-bone": {
      "title": "Bone \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Bone",
      "access_date": "2025-10-18",
      "notes": "Provides the full drop list, confirms ranch production from Sootseer and Vixy, and reiterates the 100G merchant price.【palfandom-bone†L1-L55】"
    },
    "palwiki-sootseer": {
      "title": "Sootseer \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Sootseer",
      "access_date": "2025-10-18",
      "notes": "Documents the Grave Robber partner skill digging bones at the ranch, guaranteed bone drops, and night spawns across Sakurajima.【palwiki-sootseer†L12-L116】"
    },
    "palwiki-rushoar": {
      "title": "Rushoar \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Rushoar",
      "access_date": "2025-10-18",
      "notes": "Confirms Rushoar drops Bone alongside Pork and Leather and describes its aggressive hill patrol behaviour.【palwiki-rushoar†L65-L116】"
    },
    "palwiki-windswept-hills": {
      "title": "Windswept Hills \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Windswept_Hills",
      "access_date": "2025-10-18",
      "notes": "Explains the region is the starting zone with low-level pals and lists the Small Settlement as a key point of interest.【palwiki-windswept-hills†L7-L22】"
    },
    "palwiki-vixy": {
      "title": "Vixy \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Vixy",
      "access_date": "2025-10-18",
      "notes": "Shows Dig Here! produces items at the ranch and that Vixy drops Bone and Leather at 100% rates.【palwiki-vixy†L9-L49】"
    },
    "palwiki-mau-raw": {
      "title": "Mau – Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Mau",
      "access_date": "2025-10-21",
      "notes": "Confirms Mau’s Gold Digger partner skill digs coins, lists coin drop amounts, and notes it spawns in Windswept Hills dungeons or faction camps.【palwiki-mau-raw†L11-L115】"
    },
    "palwiki-gold-coin-raw": {
      "title": "Gold Coin – Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Gold_Coin",
      "access_date": "2025-10-21",
      "notes": "States Gold Coins are traded currency and can be earned by selling items or pals, defeating human mobs, opening chests, or ranching Mau, Mau Cryst, and Vixy.【palwiki-gold-coin-raw†L3-L28】"
    },
    "palwiki-gold-coin": {
      "title": "Gold Coin – Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Gold_Coin",
      "access_date": "2025-10-21",
      "notes": "Lists merchant sales, Syndicate drops, and ranch producers (Mau, Mau Cryst, Vixy) for Gold Coins.【palwiki-gold-coin†L28-L44】"
    },
    "palwiki-nail": {
      "title": "Nail \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Nail",
      "access_date": "2025-10-18",
      "notes": "Details the level 10 tech unlock, Primitive Workbench crafting requirement, and 1 Ingot to 2 Nail recipe.【palwiki-nail†L3-L33】"
    },
    "game8-nail": {
      "title": "How to Get Nail: All Recipes and Effects  | Palworld\u3010Game8\u3011",
      "url": "https://game8.co/games/Palworld/archives/440158",
      "access_date": "2025-10-18",
      "notes": "Explains reaching level 10 to unlock Nail tech, crafting nails from ingots at workbenches and assembly lines, and the need for a Primitive Furnace to feed the recipe.【game8-nail†L100-L124】"
    },
    "palwiki-refined-ingot": {
      "title": "Refined Ingot \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Refined_Ingot",
      "access_date": "2025-10-20",
      "notes": "Confirms refined ingots are crafted from 2 Ore and 2 Coal at an Improved Furnace unlocked at tech level 34.【palwiki-refined-ingot†L1-L5】"
    },
    "segmentnext-refined-ingot": {
      "title": "How To Get Refined Ingots In Palworld",
      "url": "https://segmentnext.com/palworld-refined-ingot/",
      "access_date": "2025-10-20",
      "notes": "Describes unlocking refined ingots and the Improved Furnace at level 34, notes each bar costs Ore \u00d72 and Coal \u00d72, and recommends the (191,-36) mining outpost with Digtoise/Tombat automation.【segmentnext-refined-ingot†L1-L5】"
    },
    "palwiki-electric-furnace": {
      "title": "Electric Furnace \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Electric_Furnace",
      "access_date": "2025-10-20",
      "notes": "Shows the Electric Furnace unlocks at level 44, costs 50 Refined Ingots, 10 Circuit Boards, 20 Polymer, 20 Carbon Fiber, and still needs electricity plus a fire Pal to operate.【palwiki-electric-furnace†L1-L4】"
    },
    "palwiki-helzephyr-raw": {
      "title": "Helzephyr \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Helzephyr&action=raw",
      "access_date": "2025-10-24",
      "notes": "Lists Helzephyr Medium Pal Soul drop chances and describes its nocturnal patrols north of the Bridge of the Twin Knights and Islandhopper Coast waypoints.【palwiki-helzephyr-raw†L65-L116】"
    },
    "palwiki-medium-pal-soul-raw": {
      "title": "Medium Pal Soul \u2013 Palworld Wiki (raw)",
      "url": "https://palworld.wiki.gg/index.php?title=Medium_Pal_Soul&action=raw",
      "access_date": "2025-10-24",
      "notes": "Explains Medium Pal Soul uses, desert chest spawns, and Crusher recipes converting Small and Large souls.【palwiki-medium-pal-soul-raw†L22-L42】"
    },
    "palwiki-pal-metal-ingot": {
      "title": "Pal Metal Ingot \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Pal_Metal_Ingot",
      "access_date": "2025-10-20",
      "notes": "States Pal Metal Ingots are crafted at the Electric Furnace with a 4 Ore + 2 Paldium Fragment recipe and notes their late-game usage and drops.【palwiki-pal-metal-ingot†L1-L3】"
    },
    "palwiki-high-quality-cloth": {
      "title": "High Quality Cloth \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/High_Quality_Cloth",
      "access_date": "2025-10-26",
      "notes": "Shows the level 36 unlock, High Quality Workbench crafting recipe (10 Wool per cloth), and Sibelyx ranch production for High Quality Cloth.【palwiki-high-quality-cloth†L3-L36】"
    },
    "palwiki-sibelyx": {
      "title": "Sibelyx \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Sibelyx",
      "access_date": "2025-10-26",
      "notes": "Lists the Silk Maker passive, guaranteed cloth drops, and confirms Sibelyx resides in the Sealed Realm of the Pristine.【palwiki-sibelyx†L11-L122】"
    },
    "palwiki-sealed-realms": {
      "title": "Sealed Realms \u2013 Palworld Wiki",
      "url": "https://palworld.wiki.gg/wiki/Sealed_Realms",
      "access_date": "2025-10-26",
      "notes": "Provides the Sealed Realm of the Pristine entry with Sibelyx, recommended level 40, and coordinates (250,70).【palwiki-sealed-realms†L44-L47】"
    },
    "fandom-pal-metal-ingot": {
      "title": "Pal Metal Ingot \u2013 Palworld Wiki (Fandom)",
      "url": "https://palworld.fandom.com/wiki/Pal_Metal_Ingot",
      "access_date": "2025-10-20",
      "notes": "Provides the Electric Furnace recipe, reiterates 4 Ore + 2 Paldium Fragment cost, and lists Astegon, Necromus, Paladius, and Shadowbeak as drop sources.【fandom-pal-metal-ingot†L1-L4】"
    },
    "palfandom-medium-pal-soul-raw": {
      "title": "Medium Pal Soul \u2013 Palworld Wiki (Fandom, raw)",
      "url": "https://palworld.fandom.com/wiki/Medium_Pal_Soul?action=raw",
      "access_date": "2025-10-24",
      "notes": "Confirms guaranteed Sootseer drops, Helzephyr sources, and Desiccated Desert treasure chest spawns for Medium Pal Souls.【palfandom-medium-pal-soul-raw†L12-L38】"
    }
  }
}
```
