# Palmate Project Overview

**Palworld** is a survival and creature‑collection game where players capture and befriend Pals, build bases, craft technology, and explore a large open world.  **Palmate** is an adaptive route‑guide system designed to help players navigate Palworld’s complex progression.  It analyses the player’s estimated level, declared difficulty (Normal or Hardcore), party mode (Solo or Co‑Op) and completed routes to recommend the next best guides.  This repository contains the data and logic that power Palmate.

## Adaptive Routes

Palmate’s guides are organised into **routes**.  Each route is a high‑level objective broken down into actionable steps.  Routes include metadata such as recommended level ranges, prerequisites, estimated completion time and XP gain, risk profile, failure penalties, and a full list of steps with targets, locations and mode‑specific adjustments.  When the player completes a route, Palmate uses the XP earned in each step to estimate the player’s level and uses this estimate, along with declared difficulty and party mode, to recommend the next routes.

Routes are adaptive in three ways:

1. **Difficulty and party adjustments** – Every step can include modifications for Hardcore and Co‑Op.  For example, a Hardcore variant may recommend additional safety gear or higher‑level pals, while Co‑Op steps split roles between group members (e.g. “puller” and “farmer”).
2. **Resource dependencies** – When a route requires materials (e.g. a saddle needing Leather), it either contains steps to gather those materials or branches to a **resource subroute**.  The amount of material required is calculated from the current recipe (plus a buffer for Hardcore).  This ensures players never get stuck because they are missing ingredients.
3. **Dynamic rules** – Each route now ships with machine-readable triggers (level gaps, time budgets, resource shortages, party composition, player goals) that tell the recommender how to pivot the route.  When the player’s context matches a rule, Palmate explains the adjustment (e.g. “Skip the capture step and craft now”) and boosts that route’s score.

## Guide Suite

| File | Audience | Purpose |
| --- | --- | --- |
| `guides.md` | Palmate runtime & integrators | Master data file with schema, ontologies, XP tables and machine-readable routes. |
| `palworld_complete_guide.md` | Researchers, tool builders | Encyclopedic catalogue of every quick guide plus detailed step-by-step instructions, now aligned with the other documents. |
| `palworld_purposeful_guides.md` | Players seeking a directed campaign | Goal-driven progression playbooks that link out to the relevant quick guides and missions. |
| `palworld_full_route_normal_coop_optional.md` | Families and co-op duos on Normal | Checkbox-focused story route covering all towers with optional co-op chores and kid-friendly wording. |

## Data Layout

All game data lives in **guides.md**.  The file is organised into human‑readable sections followed by machine‑readable JSON blocks.  The main sections are:

1. **Global metadata** – Schema version, game version, verification timestamp, coordinate system, and available difficulty/party modes.
2. **XP & level tables** – A cumulative XP table up to the current level cap and a map of XP awards for common actions (e.g. capturing a Pal, defeating a boss, crafting items).  These values are approximate; update them as more accurate data becomes available.
3. **Ontologies** – Dictionaries for pals, items, recipes, tech tree, crafting stations, regions, resource nodes, bosses and dungeons, and breeding combinations.  IDs are stable slugs (kebab‑case).  Only a subset of Pals and items necessary for the provided routes are included here.
4. **Route schema** – A JSON block that defines the shape of each route.  Clients use this to validate and parse route data.
5. **Route library** – The actual guides.  Each route contains metadata, prerequisites, objectives, estimated time/XP, risk profiles, step lists (with mode adjustments and branching), completion criteria, yields, and pointers to next routes.  Steps reference the ontologies using their IDs.  The library spans early progression, resource loops, mount acquisition, tower and boss fights, and—new in this release—the full main and side mission quest chains.
6. **Level estimator** – A block describing how the client estimates player level from completed steps.  It references the XP table and describes an algorithm for summing XP, adding bonuses, converting to a level, and computing a confidence score.
7. **Recommender** – A block defining how the home page recommends routes.  It takes the player’s declared and estimated level, difficulty/party modes, completed routes and optional goals, scores candidate routes using weighted signals, and explains why each route is recommended.
8. **Source registry** – A JSON map that links short citation keys used throughout `guides.md` to full references, with titles and access dates.  When the underlying web pages update, these references should be refreshed.

### Example Route Block

Below is a simplified example of how a route is represented in `guides.md` (the actual guides are far more detailed):

```json
{
  "route_id": "early-capture-basics",
  "title": "Early Capture Basics",
  "category": "progression",
  "recommended_level": { "min": 1, "max": 5 },
  "modes": { "normal": true, "hardcore": true, "solo": true, "coop": true },
  "prerequisites": { "routes": [], "tech": [], "items": [], "pals": [] },
  "objectives": ["Unlock Pal Spheres", "Capture 3 different pals"],
  "estimated_time_minutes": { "solo": 20, "coop": 15 },
  "estimated_xp_gain": { "min": 300, "max": 600 },
  "risk_profile": "low",
  "failure_penalties": { "normal": "loss of items used", "hardcore": "permadeath on party wipe" },
  "steps": [
    {
      "step_id": "early-capture-basics:001",
      "type": "gather",
      "summary": "Collect Wood and Stone",
      "detail": "Harvest 10 Wood from nearby trees and 5 Stone from loose rocks.",
      "targets": [],
      "locations": [{ "region_id": "windswept-hills", "coords": [0, 0], "time": "day", "weather": "any" }],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 20, "max": 30 },
      "outputs": { "items": [{ "item_id": "wood", "qty": 10 }, { "item_id": "stone", "qty": 5 }], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": []
    },
    {
      "step_id": "early-capture-basics:002",
      "type": "craft",
      "summary": "Craft Pal Spheres",
      "detail": "Use a Primitive Workbench to craft at least 5 Pal Spheres.",
      "targets": [{ "kind": "item", "id": "pal-sphere", "qty": 5 }],
      "locations": [],
      "mode_adjustments": {},
      "recommended_loadout": { "gear": [], "pals": [], "consumables": [] },
      "xp_award_estimate": { "min": 50, "max": 70 },
      "outputs": { "items": [{ "item_id": "pal-sphere", "qty": 5 }], "pals": [], "unlocks": {} },
      "branching": [],
      "citations": []
    }
  ],
  "completion_criteria": [
    { "type": "have-item", "item_id": "pal-sphere", "qty": 5 }
  ],
  "yields": { "levels_estimate": "+1 to +2", "key_unlocks": ["workbench", "capture-bonus"] },
  "next_routes": [{ "route_id": "early-base-setup", "reason": "next logical progression" }]
}
```

### Recommendation Engine Example

Suppose a player has completed the early capture route above and is now level 4.  They declared **Normal** difficulty and **Solo** play.  Palmate examines available routes and scores them based on prerequisites, level fit, time‑to‑power ratio and novelty.  It then recommends, for example, `early-base-setup` (build a base and unlock crafting stations) because it unlocks critical tech and fits their level.  If the player declares they are level 10, the system may skip ahead to a mount acquisition route (e.g. `mount-eikthyrdeer`) because the prerequisites (capturing Eikthyrdeer and unlocking the saddle) are now met.

## Contribution Guide

Contributions are welcome!  To add or update a route:

1. **Follow the schema** – Each route must match the `route_schema` defined in `guides.md`.  Validate JSON before committing.
2. **Use stable IDs** – IDs must be lowercase kebab‑case and remain stable.  Do not rename IDs of existing routes or entities; instead, deprecate old IDs and add new ones.
3. **Citations** – Provide inline citations for any non‑obvious fact (spawn locations, drop rates, recipe costs, etc.).  Use the short keys defined in the source registry and ensure they map to actual URLs with dates.
4. **Sane level ranges** – Choose recommended level ranges that match the difficulty of the content.  Ensure Hardcore adjustments are present for dangerous encounters and that Co‑Op steps divide roles logically.
5. **Update metadata** – If a new patch changes game mechanics (e.g. recipe ingredients), update the global metadata and affected routes.  Note the new game version and update `verified_at_utc`.

## Versioning and Changelog

The `schema_version` in `guides.md` increments whenever the route schema changes in a way that would break existing clients.  The `game_version` tracks the latest verified Palworld build (current: **v0.6.7**, patch `1.079.736` released September 29 2025【353245298505537†L150-L168】).  See the `CHANGELOG` file for a history of updates.

## License and Attribution

All original content in this repository is released under the MIT License.  External data from the Palworld Wiki and other sources is provided under their respective licenses; see the source registry in `guides.md` for full citations.  Portions of this guide incorporate data from the Palworld Wiki (CC‑BY‑SA 4.0)【142053078936299†L300-L321】 and community guides.  Please respect the terms of those licenses when redistributing.