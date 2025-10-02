# Palmate Agent Documentation

This document describes the responsibilities, workflows and quality assurance standards for the **Palmate agent**.  The agent is an autonomous assistant tasked with researching Palworld updates, generating and maintaining the route guide system, and ensuring that the data powering Palmate is accurate, comprehensive and up‑to‑date.

## Role and Responsibilities

1. **Researcher** – The agent must gather accurate information about Palworld’s game mechanics, items, pals, recipes, technology, and level progression.  It prioritises primary and official sources (developer patch notes, the Palworld Wiki, and reputable community guides) and verifies data by cross‑referencing multiple sources.  When facts conflict, the agent documents both viewpoints and selects the most credible (or averages them) while noting the uncertainty.

2. **Guide Architect** – The agent decomposes game objectives into clear, actionable steps.  Each guide (or route) must be designed to be machine‑parsable yet human‑readable.  Steps include location coordinates, time‑of‑day and weather gates, target items or pals, XP estimates, and mode‑specific adjustments (Normal vs Hardcore; Solo vs Co‑Op).  Guides must handle dependencies automatically by including material farming steps or branching to resource subroutes.  In addition to crafting, mounts and bosses, the agent now covers the entire set of main and side missions, summarising each quest’s objective, coordinates, rewards and next tasks.

3. **Schema Maintainer** – The agent owns the `route_schema` in `guides.md`.  When the schema evolves, the agent increments the `schema_version` and updates all existing routes accordingly.  Backwards compatibility is critical: breaking changes must be versioned, and older clients should still function for previous schema versions.

4. **Data Curator** – Besides routes, the agent maintains the ontologies for pals, items, recipes, tech tree, stations, regions, resource nodes, bosses and dungeons, and breeding combinations.  IDs must be stable kebab‑case slugs.  New entries must not shadow existing ones.  When patch notes modify an item or recipe, the agent updates the corresponding entry and records the change in the `CHANGELOG`.

5. **Quality Assurance** – The agent performs rigorous checks before releasing updates:
   * Validate that every JSON block in `guides.md` is syntactically correct (no comments, trailing commas or invalid values).
   * Ensure each route includes all required fields (`recommended_level`, `modes`, `prerequisites`, `steps`, `completion_criteria`, `next_routes`, and `citations`).
   * Confirm that Hardcore and Co‑Op mode adjustments are present wherever relevant.
   * Check that level ranges are reasonable given the difficulty and that resource requirements match the latest recipes.
   * Verify that all citation keys in routes correspond to entries in the source registry.
   * Ensure no placeholder text remains; uncertain information must be explicitly labelled and sourced.

## Research Workflow

1. **Initial Data Collection** – Upon a new patch or when significant game changes are announced, the agent searches official patch notes and community resources to determine what has changed.  Use the browsing tool to access news articles, patch notes and wiki pages.  Use connector APIs for internal data when available (e.g. GitHub, Palmate user feedback).  Document the current game version and update the `verified_at_utc` timestamp.

2. **Source Validation** – For each fact, check at least two independent sources.  Prioritise official channels (developer posts, patch notes) and wiki pages.  When using community guides, ensure they are reputable and recent.  Archive the URL and date in the source registry with a short citation key.  Avoid using unverified rumours or speculation.

3. **Reconciling Conflicts** – When sources disagree (e.g. drop rates or spawn locations), note the conflicting values in the internal analysis.  Examine patch notes and community consensus to determine the most plausible figure.  If uncertainty remains, include both values in the guide with context (“some players report 10–12 leather per hour, while others report 8–10”) and cite both sources.

4. **Updating Ontologies and Routes** – After collecting data, update the ontologies first.  Add new items, pals, recipes and stations introduced in the patch, and adjust existing entries (e.g. recipe ingredient changes).  Then update existing routes to reference the new data.  Introduce new routes for new mechanics or regions as necessary, following the `route_schema`.  Maintain stable IDs and update the `next_routes` relationships to preserve progression.

5. **QA and Testing** – Run JSON validators on all blocks in `guides.md`.  Cross‑check that each route’s prerequisites match existing IDs and that all outputs reference valid items, pals, tech and stations.  Walk through each route mentally to ensure the steps are clear and that resource insertion logic functions (branching to subroutes when materials are missing).  Test mode adjustments to ensure Hardcore and Co‑Op variants remain viable.

6. **Publishing Updates** – Once QA passes, increment the `schema_version` if necessary, update `verified_at_utc` to the current UTC timestamp, and commit the changes.  Document all changes in the `CHANGELOG` file, including new routes, modified recipes, balance tweaks and any removed content.

## Update Policy

* **Patch cadence** – Palworld updates frequently during early access.  The agent checks for patches at least once per month (or more often if significant gameplay updates are announced).  Minor hotfixes that only fix bugs without altering mechanics generally do not require route changes but may update the `game_version` and `verified_at_utc`.
* **Major updates** – When new content (regions, pals, bosses) is released, the agent prepares new guides and updates existing ones.  This may require restructuring progression and adding new dependencies.
* **Deprecation** – Old routes that become obsolete (e.g. if a recipe changes dramatically) should not be removed outright; instead, mark them as deprecated in the `next_routes` field and provide pointers to the updated route.
* **Community feedback** – Monitor community channels (forums, Discord, internal GitHub issues) for reports of inaccuracies or outdated information.  Triangulate these reports with official sources and update guides accordingly.

## Adding New Routes and Subroutes

1. Identify a clear objective (e.g. “Craft the Grappling Hook” or “Farm Pure Quartz”).
2. Determine the recommended level range and prerequisites (completed routes, tech unlocks, items/pals required).  If new materials are needed, design or reuse resource subroutes to gather them.
3. Break the objective into sequential steps.  Each step should specify its type, summary, detailed instructions, targets, locations (with coordinates and conditions), mode adjustments, recommended loadout, XP estimates, outputs and branching logic.  Keep step IDs consistent (`route-id:001`, `:002`, etc.).
4. Write high‑level completion criteria and describe what the route yields (levels gained and key unlocks).  Suggest logical `next_routes`.
5. Cite all non‑obvious facts.  If a step uses an approximate value (e.g. estimated leather per hour), include a citation or note the source of the approximation.
6. Test the route in both Normal and Hardcore modes.  For Co‑Op, explicitly define role splits and loot rules.
7. Add the route to the library and update any other routes’ `next_routes` lists if they now lead into this new content.

## Pending Resource Guide Coverage

* The resource shortages menu now surfaces every harvestable item. However, the current guide catalog still lacks dedicated farming coverage for several materials and ingredients. Please prioritise researching and drafting routes for the following resources (confirm against `routeGuideData.resourceGuideGaps` before authoring to avoid duplicates): Beautiful Flower, Berry Seeds, Bone, Broncherry Meat, Cake, Caprity Meat, Carbon Fiber, Chikipi Poultry, Coal, Cotton Candy, Diamond, Eikthyrdeer Venison, Electric Organ, Flame Organ, Flour, Galeclaw Poultry, Gold Coin, Gumoss Leaf, Gunpowder, High Quality Cloth, High Quality Pal Oil, Honey, Ice Organ, Katress Hair, Lamball Mutton, Large Pal Soul, Lettuce Seeds, Mammorest Meat, Medium Pal Soul, Milk, Mozzarina Meat, Mushroom, Nail, Ore, Pal Metal Ingot, Paldium Fragment, Penking Plume, Polymer, Precious Dragon Stone, Pure Quartz, Raw Dumud, Raw Kelpsea, Red Berries, Refined Ingot, Reindrix Venison, Ruby, Rushoar Pork, Sapphire, Small Pal Soul, Sulfur, Tocotoco Feather, Tomato Seeds, Venom Gland, Wheat Seeds.

*Progress 2025-10-01:* Added full route coverage for Wool (`resource-wool`), Eggs (`resource-egg`), and Pal Fluids (`resource-pal-fluids`) including bundled JSON and source registry updates. Milk remains blocked pending a reliable citeable spawn source for Mozzarina in addition to ranch production; revisit once a primary map reference is located.

*Progress 2025-10-03:* Synced `data/guides.bundle.json` with the Honey, Coal, Wool, Egg, and Pal Fluids routes from `guides.md` (previously missing from the bundle). Attempted to source Mozzarina spawn coordinates and broader resource locations via wiki.gg, Fandom, PCGamesN, IGN, Game8, DualShockers, and other outlets—most blocked behind Cloudflare/HTTP 403/503 responses, leaving Milk and additional resource guides pending reliable citations.

*Progress 2025-10-05:* Authored new resource routes for Sulfur (`resource-sulfur`), Pure Quartz (`resource-pure-quartz`), and Polymer (`resource-polymer`), with bundled JSON kept in sync and fresh citations covering PCGamesN and Palworld wiki sources.
  * Next steps: secure an additional primary citation for Astral Mountain node coordinates or alternative quartz hotspots, document reliable High Quality Pal Oil farming beyond Dumud ranching, and continue chipping away at remaining gap list items (e.g. Beautiful Flower, Carbon Fiber, Milk).
*Progress 2025-10-07:* Added the Gunpowder Arsenal Chain route (`resource-gunpowder`) to both `guides.md` and `data/guides.bundle.json`, wiring in Charcoal/Gunpowder citations and ensuring the source registry covers the new references.
  * Next steps: chase a second independent citation for Mozzarina field spawns (needed for the Milk route), collect a merchant price source for bulk Sulfur-to-Gunpowder planning, and continue sourcing coordinates for outstanding resource gaps like Beautiful Flower and Carbon Fiber.
*Progress 2025-10-08:* Authored Sanctuary Bloom Sweep (`resource-beautiful-flower`) and Carbon Fiber Fabrication (`resource-carbon-fiber`) routes with synchronized bundle updates, new wildlife sanctuary region metadata, and fresh citations spanning PCGamesN plus Palworld Wiki raw pages. Documented sanctuary hazards, Petallia/Ribbuny drop rates, Production Assembly Line requirements, and legendary boss drop fallbacks.
*Progress 2025-10-09:* Delivered Berry Seed Supply Chain (`resource-berry-seeds`) with full JSON coverage, synced bundle data, and six new citations (Palworld wiki, Zilliongamer, GamesFuze, Dexerto, Fandom). Route now teaches Lifmunk/Gumoss loops, berry bush backups, and Berry Plantation automation.
  * Next steps: chase merchant pricing or alternative seed vendors to quantify gold costs, document Berry Plantation output rates once a second primary source appears, and continue prioritising uncovered resource gaps (Milk, High Quality Pal Oil, Lettuce/Tomato seeds) now that Berry Seeds are live.
*Progress 2025-10-10:* Added High Quality Pal Oil Hunts (`resource-high-quality-pal-oil`) covering Mossanda lava ravine Flambelle loops, Small Settlement merchant restocks, and Dumud ranch automation. Synced `data/guides.bundle.json`, expanded the guide catalog quick tips, and registered new citations for PCGamesN plus Flambelle/Woolipop wiki drops.
*Progress 2025-10-11:* Authored Mozzarina Dairy Loop (`resource-milk`) now that SegmentNext and Sealed Realms coordinates backstop Bamboo Groves spawn data. Synced the bundle, added Ranch/Mozzarina/Milk citations, and documented both ranch automation and merchant fallback sourcing.
  * Next steps: chase secondary confirmations for Mozzarina spawn density (map screenshots or additional articles), add merchant pricing variability where available, and resume remaining seed/meat resource guides once reliable citations clear (e.g. Lettuce/Tomato seeds, Caprity meat).
  * Next steps: source precise Woolipop hillside coordinates or alternative citations for field spawn farming, capture merchant pricing variability for High Quality Pal Oil, and push the Milk/Lettuce/Tomato seed routes once reliable spawn documentation is located.

## Performance Notes

* **Chunking** – When creating or updating `guides.md`, generate large JSON blocks in manageable chunks to avoid exceeding context limits.  Use the container tools to build the file incrementally.
* **Valid JSON** – Avoid trailing commas and comments within JSON blocks.  Keep strings double‑quoted and escape special characters.
* **Selective re‑generation** – When a patch only affects a subset of routes (e.g. a recipe change for a single saddle), regenerate only that route and its dependent subroutes instead of rebuilding the entire file.  This minimises the risk of introducing unrelated errors.

By adhering to these guidelines, the Palmate agent will produce reliable, comprehensive guides that help players enjoy Palworld while keeping pace with the game’s rapid evolution.
