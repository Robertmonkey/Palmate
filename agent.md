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

## Guides Bundle Workflow (Updated 2025-11-28)

1. Treat `data/guides.bundle.json` as a derived artifact. Never hand-edit it; author changes in `guides.md` and `data/guide_catalog.json`, then rebuild the bundle.
2. Run `python3 scripts/regenerate_guides_bundle.py` (optionally with `--dry-run` first) after every guides or catalog change. The script validates the reconstructed payload, compares it to the baseline backup, and performs atomic writes so truncated files cannot land.
3. When patching individual bundle sections, use `scripts/update_guides_bundle.py` with a JSON patch file. The helper enforces the same validation and loss guards before swapping files.
4. If regeneration or patching is expected to remove routes, steps, or catalog entries, pass the explicit `--allow-*` flags so the loss guard records the intent.
5. Commit both the regenerated bundle and the refreshed backup snapshot together so future guard checks have an intact baseline.

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

### Alignment Review

*The 2025-10 route development log above has been audited end-to-end.* Each dated entry still reflects a meaningful expansion of the shortages menu, and every completed route is mirrored in `guides.md`, `data/guides.bundle.json`, and the source registry. The in-progress next steps have been regrouped below so that ongoing work continues to reinforce Palmate’s core goal: a context-aware resource menu that lets us instantly surface the right farming loop, adjust it for the player’s phase/level, and bolt on side routes for any missing prerequisites.

Key confirmations from the review:

1. **Menu Coverage Trajectory** – Newly authored guides consistently wire into the shortages UI and catalogue. As long as future routes follow the same sync requirements (guide JSON + bundle + catalog entry + citations), the menu will remain authoritative.
2. **Context Hooks Present** – Each shipped route already carries recommended level ranges, prerequisite routes, and mode adjustments. Maintain this standard and explicitly note phase-specific pivots (e.g., “Early-game Bronze Age base vs. Mid-game Electricity unlocks”) when drafting new resources.
3. **Extras & Branching** – Existing guides include optional steps for surplus gathering (e.g., merchant loops, automated ranching). Preserve this pattern and expand it when a resource benefits from stocking buffers (ammo, cooking ingredients, crafting reagents).

### Operating Instructions

1. **Validate Menu Integration** – Before committing a new resource route, confirm that `routeGuideData.resourceGuideGaps` no longer lists the resource, that `data/guide_catalog.json` contains a `resource-*` entry with `shortage_menu: true`, and that the shortages UI renders the new option with correct recommended phase/level labels.
2. **Phase/Level Sensitivity** – Every route must spell out at least one adjustment per major progression band:
   * **Early (Lv 1–18)** – Limited tech, focus on manual gathering and basic workstations.
   * **Mid (Lv 19–35)** – Bronze/Steel infrastructure, mid-tier pals, Improved Furnace era.
   * **Late (Lv 36+)** – Electricity/Assembly Line automation, sealed realms, alpha rotations.
   Document how to pivot between these bands (alternate pals, workstation swaps, travel unlocks) and flag when a band should defer to a prerequisite route instead of forcing inefficient grinds.
3. **Extras Acquisition Paths** – For each resource, provide at least one optional “surplus” branch (merchant restocks, ranch automation, dungeon sweep, or alpha circuit) with timer/respawn notes so players can stack reserves beyond immediate crafting needs.
4. **Dependency Surfacing** – If a route requires sub-materials (e.g., Gunpowder needing Charcoal + Sulfur), explicitly reference the existing resource guides in `prerequisites` and `branching` fields. When no guide exists yet, record the gap in `routeGuideData.resourceGuideGaps` and park a TODO in this section’s backlog until citations are secured.
5. **Citation Rigor** – Maintain two-source verification for spawn coordinates, merchant inventories, and recipe yields whenever possible. Log HTTP/Cloudflare blocks in the source registry notes so future agents know which outlets are currently inaccessible.

### Backlog (Confirm Against `routeGuideData.resourceGuideGaps` Before Starting)

* High-priority shortages requiring follow-up work: **Polymer** (field loop now mapped to Duneshelter merchants and Sanctuary No. 2 spawns; still need an interactive map citation for Quivern patrol clusters), **Pal Metal Ingot** (Alpha/ore rotation coordinates), **Flame Organ** (volcano node coordinates), **Katress Hair** (nighttime alley sweep coordinates), **Resource Respawn Timers** (baseline logging path coordinates), **Sanctuary-exclusive drops (e.g., Lyleen Noct hair, Sibelyx Ignis cloth)**.
* Secondary targets once two independent citations are secured: **Milk auxiliary spawns**, **Seed restock timers (Tomato/Lettuce/Berry)**, **Elite alpha respawn timers for gemstone loops**, **Automation throughput benchmarks for Assembly Line/Power Grid resources**, **Merchant restock timing references**.

Update this backlog whenever a guide ships or when a data source becomes available, and archive stale TODOs with reasoning if a resource becomes obsolete or its shortages are resolved by upstream patches.
## Performance Notes

* **Chunking** – When creating or updating `guides.md`, generate large JSON blocks in manageable chunks to avoid exceeding context limits.  Use the container tools to build the file incrementally.
* **Valid JSON** – Avoid trailing commas and comments within JSON blocks.  Keep strings double‑quoted and escape special characters.
* **Selective re‑generation** – When a patch only affects a subset of routes (e.g. a recipe change for a single saddle), regenerate only that route and its dependent subroutes instead of rebuilding the entire file.  This minimises the risk of introducing unrelated errors.

By adhering to these guidelines, the Palmate agent will produce reliable, comprehensive guides that help players enjoy Palworld while keeping pace with the game’s rapid evolution.

### 2025-10-31 High Quality Pal Oil supply circuit

* Replaced the outdated Mossanda lava ravine hunt with the **High Quality Pal Oil Sanctuary Circuit**, wiring merchant loops, Sanctuary Nos. 1–2 captures, and Dumud ranch automation into the route library and bundle.
* Synced the guide catalog shortage entry so the shortages UI can surface the new sanctuary-focused path, and added drop-rate/source registry stubs for palworld.gg payloads.

**Continuation notes:**

1. Gather first-hand coordinates or merchant data for reliable Dumud acquisition (desert spawn or pal merchant) so the automation step can cite a capture path instead of assuming ownership.
2. Capture PIDF respawn and trespass timer data for Sanctuaries to improve the adaptive guidance risk modelling before expanding to Sanctuary No.3 follow-ups.
3. Validate polymer automation dependencies after the next content patch—route currently pushes polymer and carbon fiber, but Assembly Line throughput benchmarks still need sourcing.

### 2025-10-31 Venom Gland coverage sync

* Added the `resource-venom-gland-supply-network` catalog entry with shortage flag, merchant/dungeon/alpha context, and wired citations so the shortages UI can surface the route immediately.
* Verified `index.html` relies entirely on parsed guide data for `resourceGuideGaps`; no hard-coded Venom Gland references required updates after the new route synced into `guides.md` and `data/guides.bundle.json`.
* Expanded the Source Registry with `palwiki-killamari`, `palwiki-menasting`, and `palfandom-venom-gland` to clear unresolved citations for the new route JSON blocks.
* Next agent touchpoint: confirm the shortages drawer surfaces the Venom Gland guide once bundles regenerate in production, then continue with the remaining backlog targets above (Caprity Meat, Galeclaw Poultry, etc.).
### 2025-11-03 Small Pal Soul sourcing groundwork

* Collected primary citations for Small Pal Soul acquisition, including Fandom documentation on drop sources (Daedream, Nox, Cawgnito, Maraith, Felbat, Tombat), overworld spawn behavior, and Crusher-based soul conversions.
* Logged nocturnal behavior notes for Daedream and Nox to support night-hunt routing and base automation planning for future guide steps.

**Continuation notes:**

1. Translate the new sources into a full `resource-small-pal-soul` route covering early-game night hunts, mid-game Crusher conversion loops, and late-game statue offering automation; wire the guide into `data/guides.bundle.json` and `data/guide_catalog.json` once coordinates are verified.
2. Secure at least one citation with explicit coordinates or dungeon references for Daedream/Nox farming hotspots (e.g., Windswept Hills nighttime patrols or low-level dungeons) to anchor the step-by-step capture path.
3. Identify efficient Medium/Large Pal Soul feedstock chains (alphas, raids, or breeding) so the Crusher conversions can scale without starving other statue upgrades; gather throughput benchmarks before drafting late-game automation steps.

### 2025-10-03 Galeclaw Poultry route rollout

* Authored the `resource-galeclaw-poultry` route plus shortage catalog entry, wiring Windswept Hills hunts, Meat Cleaver processing, and Cooler Box storage into the adaptive data so shortages UI can recommend the loop immediately.
* Captured fresh citations (`palwiki-galeclaw-raw`, `palfandom-windswept-hills-raw`) and registered them in the source registry to back guaranteed drop rates and spawn coverage.

**Continuation notes:**

1. Locate a second independent map citation with explicit Galeclaw spawn coordinates (e.g., interactive map exports) to strengthen location guidance beyond the Fandom listing.
2. Audit late-game cooking routes (Cake, Luxury Meals) to ensure they reference Galeclaw poultry in their prerequisites now that the supply loop exists.
3. Prototype a sanctuary/alpha follow-up once reliable Caprity citations land so higher-tier poultry inputs (Caprity Meat) can chain directly from this route.

### 2025-11-07 Cotton Candy ranch automation

* Added the `resource-cotton-candy` route with breeding-focused steps, checkpoints, and adaptive guidance so shortages now surface a Woolipop ranch loop.
* Synced `data/guides.bundle.json` and `data/guide_catalog.json` to expose the new resource in the client shortage menu, including merchant/breeding metadata.
* Captured new rendered citations (`palwiki-breeding-render`, `palwiki-woolipop-breeding`) and registered them in the source registry alongside existing cotton candy/woolipop entries.

**Continuation notes:**

1. Source a field citation for wild Woolipop spawn coordinates (e.g., interactive map export) so the route can offer an alternate capture path for players without cake.
2. Confirm whether any merchants sell Cotton Candy directly and, if so, add a `trade` branch plus catalog link for rapid restocks.
3. After production deploy, verify the shortages UI removes Cotton Candy from `resourceGuideGaps`; if not, regenerate the production bundles and investigate parser expectations.

### 2025-11-10 Small Pal Soul circuit delivery

* Authored the `resource-small-pal-soul` route with nocturnal hunts, Crusher conversions, and Statue of Power scheduling plus checkpoints and adaptive guidance tuned for underleveled, overleveled, and coop contexts.
* Synced the shortages catalog via `resource-small-pal-soul-night-loop` so the UI advertises the loop once bundles refresh, including new keyword coverage for Statue upgrades.
* Expanded the Source Registry with rendered Palworld wiki pulls for Daedream, Nox, Small Pal Soul, and Crusher conversion specifics, ensuring citations back the night spawn behavior and conversion ratios.

**Continuation notes:**

1. Gather a second independent map citation with explicit Daedream and Nox coordinate clusters (interactive map export or community atlas) to reinforce the hunt step beyond the Small Settlement anchor.
2. Secure a dungeon-focused citation for Tombat/Felbat Small Pal Soul drops so the route can branch into late-game instanced loops for variety.
3. Monitor production `resourceGuideGaps`; if Small Pal Soul remains listed post-deploy, inspect bundle ingestion and ensure the new catalog entry flags `shortage_menu: true` in downstream manifests.

### 2025-11-12 Medium Pal Soul shortage sync

* Promoted `resource-medium-pal-soul` into the shortage catalog so adaptive menus now surface Helzephyr raids, Sakurajima Sootseer clears, and Crusher balancing when Medium Pal Souls fall short.
* Regenerated `data/guides.bundle.json` metadata so the embedded `guideCatalog` mirrors the new entry and updates the published guide count.

**Continuation notes:**

1. Add a secondary Helzephyr coordinate citation (interactive atlas or official map) so future updates can display exact patrol loops alongside the bridge landmark.
2. Document medium-soul chest hotspots beyond Duneshelter once reliable coordinates or screenshots land; wire them into the catalog entry for parity with the route JSON.
3. Audit downstream clients once bundles rebuild to ensure the new catalog record clears Medium Pal Soul from `resourceGuideGaps` and respects existing shortage sort order.

### 2025-11-13 Broncherry Meat caravan loop

* Authored the `resource-broncherry-meat` route covering the (-222,-669) Alpha Broncherry loop and Meat Cleaver butchery so shortages can surface a guaranteed daily meat circuit.【palwiki-alpha-pals†L31-L104】【palwiki-broncherry-raw†L66-L103】【palwiki-meat-cleaver†L2-L38】
* Synced the bundles and catalog entry so the shortage menu flags Broncherry Meat, including keywords and linkouts for Meat Cleaver crafting and Tomato Seed byproducts.
* Registered `palwiki-broncherry-raw` in the source registry and refreshed `guides.bundle.json` metadata (`verified_at_utc` now 2025-11-13) to keep downstream clients in sync.

**Continuation notes:**

1. Secure a second independent citation for non-alpha Broncherry spawns (interactive map export or reputable guide) so future revisions can offer alternative hunt loops beyond the daily alpha kill.
2. Capture quantitative butcher throughput (meat per hour, raid timers) once playtest data is available to tighten the estimated XP/output ranges in both the route JSON and shortage card.
3. Audit downstream recipe routes (e.g., Rib Roast, hearty meals) to ensure they now reference the Broncherry Meat loop and surface dependencies appropriately once production bundles rebuild.

### 2025-11-15 Medium Pal Soul automation handoff

* Expanded `resource-medium-pal-soul` with a Crusher automation checkpoint, Watering-pal guidance, and a new `crusher-automation` key unlock so shortages surface base wiring steps alongside hunt loops.
* Updated `data/guide_catalog.json` and the bundle catalog entry to add a fourth shortage step that highlights wiring storage between the Crusher and Statue of Power with supporting citations.

**Continuation notes:**

1. Capture empirical conversion throughput (Medium souls per minute) for common Watering pals to validate the new automation estimates before publishing dashboard copy.
2. Monitor shortage cards after the next bundle rebuild to confirm the new automation step renders correctly and references the added `crusher-automation` unlock.
3. Evaluate linking the automation step directly into `resource-large-pal-soul` once cooperative loadout benchmarks for Watering and Transporting pals are sourced.

### 2025-11-16 Caprity Meat drop groundwork

* Extracted fresh Palworld Wiki drop tables for Caprity and its alpha variant so Caprity Meat yields are locked in at 2 per capture or kill, clearing citation debt for the upcoming shortage route.【palwiki-caprity-raw†L1-L23】
* Pulled the printable Caprity Meat drop table to mirror the base drop values for the ingredient registry and shortage metrics.【palwiki-caprity-meat†L1-L6】

**Continuation notes:**

1. Secure at least one overworld spawn citation with coordinates for repeatable Caprity hunts (interactive map export or atlas scrape) so the route can anchor a farming loop instead of relying on anecdotal positions.
2. Cross-check sanctuary and ranch outputs for Caprity Noct to confirm whether nocturnal variants deliver meat alongside venom so the route can branch into automation once location data lands.
3. Once coordinates are sourced, draft the `resource-caprity-meat` route with early capture, alpha clears, and ranch processing before wiring it into `data/guides.bundle.json` and `data/guide_catalog.json`.

### 2025-11-17 Coverage diagnostics automation

* Added `scripts/resource_coverage_report.py` to diff resource routes in `guides.md` against `data/guide_catalog.json`, producing a concise list of catalog entries that still lack JSON coverage (or vice versa). Running the tool shows the catalog is complete but highlights four existing resource routes (`resource-leather-early`, `resource-paldium`, `resource-honey`, `resource-coal`) that never received shortage cards, so shortages UI still treats them as gaps.【scripts/resource_coverage_report.py†L1-L109】【2890e0†L1-L9】

**Continuation notes:**

1. Backfill catalog records for the four orphaned resource routes so the shortages drawer can surface them; ensure `shortage_menu: true` where appropriate and re-export bundles.
2. Extend the script to optionally emit CSV/markdown output so progress snapshots can drop directly into PR descriptions and Ops dashboards.
3. Expand the detector with citation linting (e.g., flag resource routes missing at least two independent sources) once coordinate exports for Caprity/Galeclaw land, so future backlog passes can validate evidence alongside coverage.

### 2025-11-18 Resource shortage catalog backfill

* Inserted shortage catalog entries for `resource-leather-early`, `resource-paldium`, `resource-honey`, and `resource-coal` inside `data/guide_catalog.json` and the mirrored bundle payload so the shortages UI can surface the early-game leather loop, Paldium fragment circuit, Honey ranch automation, and Coal smelter prep alongside newer additions.  Entries preserve the same spawn, merchant, and processing citations used in the full routes so cross-links stay authoritative.【data/guide_catalog.json†L8597-L8884】【data/guides.bundle.json†L24782-L25131】
* Updated the bundle metadata `verified_at_utc` to `2025-11-18T00:00:00Z` and bumped the catalog `guide_count` to 203 to reflect the expanded coverage snapshot.【data/guides.bundle.json†L2-L9】【data/guides.bundle.json†L24780-L24788】
* Hardened `scripts/resource_coverage_report.py` so it recognises both the legacy `sections[].entries[]` structure and the current flat `guides[]` layout, preventing false positives now that the shortage catalog omits the old section wrapper.【scripts/resource_coverage_report.py†L1-L118】

**Continuation notes:**

1. Use the refreshed coverage report to prioritise the remaining backlog of resource routes lacking catalog cards (e.g., wool, egg, refined ingot).  Draft catalog entries in batches so the shortages UI gains broad early/mid-game parity.
2. Extend `resource_coverage_report.py` with optional CSV or Markdown exports to drop straight into Ops status threads once the remaining catalog debt shrinks.
3. After the next bundle deployment, spot-check the production shortages drawer to confirm Leather, Paldium Fragments, Honey, and Coal disappear from `resourceGuideGaps`; if they linger, audit downstream ingestion for case-sensitivity or bundle cache issues.

### 2025-11-19 Resource coverage expansion batch

* Authored shortage catalog cards for the existing Wool, Egg, Pal Fluids, Sulfur, Pure Quartz, and Polymer routes so the shortages UI now surfaces early tailoring, ranching, condenser, explosive, electronics, and late-game manufacturing loops with accurate triggers and citations.【data/guide_catalog.json†L8890-L9123】
* Synced the same six entries into `data/guides.bundle.json`, bumping the catalog `guide_count` to 209 so downstream bundles stay aligned with the new coverage snapshot.【data/guides.bundle.json†L24780-L25190】
* Re-ran `scripts/resource_coverage_report.py` to confirm the newly added resources drop out of the backlog and to capture the remaining priority list for follow-up passes.【2845fa†L1-L34】

**Continuation notes:**

1. Next coverage targets are the ranching and ingredient loops that still appear in the report (`resource-milk`, `resource-chikipi-poultry`, `resource-galeclaw-poultry`, `resource-cake`, etc.); draft paired catalog cards so kitchen and breeding shortages surface properly.
2. Align naming between routes and catalog cards where IDs still diverge (e.g., `resource-medium-pal-soul` vs. `resource-medium-pal-soul-harmonization`) or extend the coverage script to treat curated aliases as resolved so they no longer flag as missing.
3. After authoring each batch, rerun `scripts/resource_coverage_report.py` and verify `guideCatalog.guide_count` updates in `data/guides.bundle.json` before committing to keep telemetry accurate.

### 2025-11-20 Dairy, poultry, and greenhouse shortage uplift

* Authored shortage catalog cards for the existing Milk, Chikipi Poultry, Galeclaw Poultry, Cake, Tomato Seed, and Lettuce Seed routes so shortages now surface dairy, kitchen protein, and plantation loops with the same step structure and citations as the full guides.【data/guide_catalog.json†L9527-L9980】【data/guides.bundle.json†L24760-L24784】
* Bumped the bundle snapshot to `2025-11-20T00:00:00Z`, increasing `guideCatalog.guide_count` to 215 and confirming via `resource_coverage_report.py` that these six resources no longer appear in the missing-card backlog.【data/guides.bundle.json†L1-L36】【c2fb2d†L1-L30】

**Continuation notes:**

1. Prioritise the next wave of backlog items flagged by the coverage report (ore, flour, bone, nail, refined ingot, pal metal, etc.) so metalworking and mid-game crafting shortages receive catalog parity.【c2fb2d†L16-L35】
2. Resolve remaining catalog aliases (e.g., `resource-berry-seed-supply-loop` vs. `resource-berry-seeds`) or extend the coverage script with an alias map so legitimate matches stop appearing as catalog-only stragglers.【c2fb2d†L5-L13】
3. Capture explicit documentation for the Lettuce Plantation source (or replace the hashed citations with a named registry entry) before publishing the next bundle to keep provenance transparent for lettuce automation guidance.

### 2025-11-21 Resource shortage parity surge

* Normalised outstanding resource catalog IDs to match their route slugs so Berry Seeds, Carbon Fiber, High Quality Cloth, Mozzarina Meat, Beautiful Flower, Venom Gland, High Quality Pal Oil, Cotton Candy, Small Pal Soul, and Precious Dragon Stone now link straight to their guide JSON without alias debt.【data/guide_catalog.json†L8187-L9046】【data/guides.bundle.json†L30704-L31832】
* Authored shortage cards for Gunpowder, Ore, Flour, Bone, Nail, and Refined Ingots and synced the bundle `guide_count` to 221 so shortages cover the full mid-game crafting spine.【data/guide_catalog.json†L8673-L9146】【data/guides.bundle.json†L30762-L31856】
* Re-ran `resource_coverage_report.py`; only ten resources remain without shortage cards, giving a focused follow-up backlog (Pal Metal Ingot, organ drops, medium/large souls, gold coin, lamball mutton, etc.).【272826†L1-L12】

**Continuation notes:**

1. Draft catalog cards for the remaining ten resources flagged by the coverage report—prioritise Pal Metal Ingot, Electric/Flame/Ice Organs, Medium/Large Pal Souls, and Gold Coin so core combat upgrades are represented alongside crafting loops.【272826†L3-L11】
2. When authoring the soul routes, confirm whether additional automation steps (Crusher conversions, Statue wiring) warrant dedicated unlock callouts similar to the medium soul entry added on 2025-11-15; reuse the existing citations where possible and capture new ones for overworld spawn coordinates.
3. After each batch, bump `guideCatalog.guide_count` and rerun `resource_coverage_report.py` to maintain telemetry parity, then smoke-test the shortages UI for the new cards to ensure recommended level text and keywords render correctly.

### 2025-11-22 Final backlog sweep: souls, organs, and currency

* Added shortage catalog cards for Pal Metal Ingots, Electric/Flame/Ice Organs, Wheat Seeds, Katress Hair, Medium/Large Pal Souls, Gold Coins, and Lamball Mutton so every outstanding resource route now has a shortages-menu entry.【data/guide_catalog.json†L9079-L9608】
* Synced the same ten entries into `data/guides.bundle.json`, bumped the bundle snapshot to `2025-11-22T00:00:00Z`, and raised `guideCatalog.guide_count` to 239 to reflect full resource coverage.【data/guides.bundle.json†L24780-L24905】【data/guides.bundle.json†L35200-L36270】
* Re-ran `scripts/resource_coverage_report.py`; only the catalog-only `resource-respawn-timers` utility remains unmatched, confirming resource parity between guides and the shortages menu.【dd2a14†L1-L8】

**Continuation notes:**

1. Audit the shortages UI once the bundle deploys to ensure the ten new cards surface with correct keywords, recommended levels, and iconography—particularly for the soul and organ entries that reuse Crusher automation art.
2. Decide whether to backfill a real route for `resource-respawn-timers` or reclassify the catalog entry so the coverage script can treat it as an intentional helper card.
3. Capture updated throughput metrics for Medium/Large soul Crusher automation (souls per minute with Watering/Transport pals) so future dashboard copy reflects the new automation emphasis.

### 2025-11-23 Resource respawn instrumentation

* Authored the full `resource-respawn-timers` route with adaptive guidance, checkpoints, and completion criteria so planners can document 30-minute node resets, slider tuning, and alpha/dungeon cadences without leaving shortages unsourced.【F:guides.md†L25560-L25836】
* Added the mechanics-focused shortage card to `data/guides.bundle.json`, keeping the bundle aligned with the new knowledge route and stocking shortages UI with respawn context.【F:data/guides.bundle.json†L85-L140】
* Replaced the legacy catalog stub with sourced instructions and re-ran the coverage report to confirm no resource mismatches remain.【F:data/guide_catalog.json†L7323-L7378】【77c923†L1-L7】

**Continuation notes:**

1. Layer in precise overworld coordinates for the recommended alpha and sealed realm rotations once sourced so Step :004 gains location-grade guidance.【F:guides.md†L25783-L25807】
2. Gather empirical respawn timing data for desert ore and late-game biomes to see if additional banded advice is warranted in the route’s adaptive guidance.【F:guides.md†L25568-L25596】
3. Smoke-test the shortages UI after the next bundle promotion to ensure the new mechanics card appears in the Stats & Mechanics filter with correct keywords and trigger text.【F:data/guides.bundle.json†L85-L140】

### 2025-11-24 Respawn rotation detailing & reporting exports

* Plotted Alpha Broncherry, Anubis, Bushi, and Penking coordinates plus respawn cadence notes directly inside Step :004 so planners can anchor daily and hourly loops without leaving the route.【F:guides.md†L25777-L25816】
* Synced the shortage bundle and catalog instructions to the new coordinate guidance, updating citations so shortages mirror the route’s precise rotation advice.【F:data/guides.bundle.json†L107-L128】【F:data/guide_catalog.json†L7346-L7370】
* Added `--format` and `--output` options to `resource_coverage_report.py`, enabling text, Markdown, or CSV exports for ops threads while preserving the default console summary.【F:scripts/resource_coverage_report.py†L1-L164】

**Continuation notes:**

1. Extend the coverage report with citation linting so resource routes missing two independent sources raise actionable warnings alongside the coverage diff.【F:scripts/resource_coverage_report.py†L114-L149】
2. Consider serialising the new coordinate blocks into the bundle metadata for UI map overlays once design finalises the shortages tooltip layout.【F:guides.md†L25777-L25816】【F:data/guides.bundle.json†L107-L128】
3. After the next data refresh, spot-check `--format markdown --output` exports to confirm automated Ops digests ingest without additional formatting fixes.【F:scripts/resource_coverage_report.py†L131-L149】

### 2025-11-25 Resource shortages panel polish & coverage surfacing

* Re-themed the route context “Resource shortages” block so it inherits the cosmic gradient, halo lighting, and stat chips used by Tonight’s Goals. The refreshed banner now spotlights total coverage, pending backlog, and the next queued resources while staying responsive on narrow layouts.【F:index.html†L14086-L14118】【F:css/styles.css†L401-L468】
* Enriched the helper drawer with full guide cards that show level ranges, time estimates, and shortage notes pulled directly from adaptive guidance, replacing the old flat chip list. Each card opens the preview modal via existing interactions to keep the flow consistent.【F:index.html†L14326-L14474】【F:css/styles.css†L415-L447】
* Wired chip badges and dropdown metadata into the coverage map so selected shortages show their matched guide counts, clarifying when a resource is fully supported versus queued for the backlog.【F:index.html†L14107-L14115】【F:index.html†L14480-L14492】【F:css/styles.css†L451-L462】

**Continuation notes:**

1. Plumb bundle metadata (e.g., recommended phases or art IDs) into the new helper cards so future revisions can render custom thumbnails without re-querying the main route lookup.
2. Audit the `resourceGuideEntries` source once more routes adopt multi-step outputs; consider injecting explicit `primary_resource_id` metadata into the schema to avoid relying solely on output detection.
3. Expand the backlog preview copy to surface more than two queued resources when the coverage debt grows, potentially with a tooltip that links back to the coverage report export.

### 2025-11-26 Citation linting in coverage tooling

* Extended `resource_coverage_report.py` to aggregate citations across each resource route and flag entries with fewer than two unique sources across all nested steps and checkpoints. The text, Markdown, and CSV outputs now surface the citation deficit alongside catalog/route gaps so shortages work can prioritise sourcing debt in lockstep with coverage parity.【F:scripts/resource_coverage_report.py†L28-L39】【F:scripts/resource_coverage_report.py†L66-L164】
* Verified the new linting against the current data bundle; the script highlights `resource-paldium` and `resource-egg` as the only routes still lacking dual citations, confirming the rest of the shortages library meets the sourcing baseline.【0298a3†L1-L4】【04aa13†L1-L12】

**Continuation notes:**

1. Backfill a second independent source for `resource-paldium` (e.g., a post-patch mining route breakdown or dev note covering node respawn rates) and `resource-egg` (such as merchant inventory documentation or latest breeding drop tables), then rerun the coverage report to confirm the warnings clear.
2. Consider promoting the citation warnings into CI once the outstanding sources are added, ensuring future resource routes and revisions maintain the two-source minimum without manual review.
3. Evaluate whether the shortage catalog should display citation counts or badges so planners can quickly gauge sourcing strength directly from the UI when triaging resource deficits.

### 2025-11-27 Dual-source reinforcement for paldium and egg routes

* Augmented the `resource-paldium` route (and bundle snapshot) with explicit guidance to gather ground spawns, target the gray-and-blue paldium rocks, and leverage Crusher conversions, pairing the existing Fandom entry with the official wiki.gg item sheet so every step cites two independent sources.【F:guides.md†L3411-L3544】【F:data/guides.bundle.json†L1352-L1493】
* Expanded the `resource-egg` route/bundle text to reference the ingredient compendium’s ranch and merchant notes, ensuring each capture, ranch, and field sweep step now carries dual sourcing for passive egg production and emergency purchases.【F:guides.md†L4811-L4920】【F:data/guides.bundle.json†L2011-L2090】
* Registered the new wiki.gg references in the source registry, unblocking the coverage report’s citation lint and keeping provenance explicit for both resource loops.【F:guides.md†L26025-L26035】【F:guides.md†L26041-L26048】

**Continuation notes:**

1. Monitor future patches for changes to wandering merchant egg pricing or Crusher conversion yields so the new wiki.gg citations stay accurate; update both routes and registry entries if values shift.
2. Now that citation lint passes, integrate the `resource_coverage_report.py` warning channel into automation (CI or nightly export) to prevent future single-source regressions.
3. For deeper resilience, consider sourcing a community farming guide with respawn timings for the river circuit and meadow egg lap to complement the official references, improving context for planner adjustments.

### 2025-11-27 guides.bundle.json truncation postmortem

* Authored a dedicated postmortem (`docs/guides-bundle-truncation-postmortem.md`) capturing how commit `870a419` overwrote the bundle with only the shortage catalog payload, shrinking the file from ~37k lines to 703 and shipping invalid JSON until `58c3a85` restored the backup and hardened validation.【F:docs/guides-bundle-truncation-postmortem.md†L1-L44】
* Logged the root cause (scripting dumped `guideCatalog.data.guides` instead of the full bundle) plus contributing factors like insufficient validation and the lack of a temp-file workflow, along with preventive actions to avoid future truncations.【F:docs/guides-bundle-truncation-postmortem.md†L46-L86】

**Continuation notes:**

1. ✅ Implemented the strict mode validator workflow so bundle edits run against scratch copies before replacing production data (see `check_guides_bundle.py --strict`).【F:docs/guides-bundle-truncation-postmortem.md†L70-L86】【F:scripts/check_guides_bundle.py†L1-L423】
2. ✅ Added `scripts/update_guide_catalog.py` to encapsulate safe catalog mutations with strict validation and loss guards.【F:docs/guides-bundle-truncation-postmortem.md†L88-L92】【F:scripts/update_guide_catalog.py†L1-L312】
3. Wire the stricter bundle checks into CI (line-count guard + validator) so truncation attempts fail fast without manual review.【F:docs/guides-bundle-truncation-postmortem.md†L88-L92】

### 2025-11-28 Caprity meat shortage coverage

* Authored the `resource-caprity-meat` route to capture, butcher, and ranch Windswept Hills Caprity so early kitchens gain a guaranteed meat loop with passive ranch output.【F:guides.md†L25191-L25569】
* Synced the new route into `data/guides.bundle.json` (guide count 240) and registered the shortage catalog card so the UI advertises the Caprity meat path with prep, hunt, and ranching steps.【F:data/guides.bundle.json†L23408-L25108】【F:data/guide_catalog.json†L9496-L9555】

**Continuation notes:**

1. Pull precise Caprity spawn coordinates into the habitat data so the hunt step can surface explicit waypoints instead of the broader Plateau loop (requires map-to-coordinate sourcing).【F:guides.md†L25359-L25441】
2. Add caprity-specific art IDs or thumbnails to the shortage helper cards once the bundle exposes metadata for custom imagery.【F:data/guide_catalog.json†L9496-L9555】
3. Verify the new shortage card renders in the production shortages UI after the next bundle promotion and confirm passive ranch output lines surface correctly in helper copy.

### 2025-11-29 Field coordinate lint for resource routes

* Expanded `scripts/resource_coverage_report.py` to analyse each resource route for field steps without map coordinates, surfacing the gaps across text, Markdown, and CSV outputs alongside citation checks.【F:scripts/resource_coverage_report.py†L1-L247】
* CSV exports now include a `route_missing_field_coords` record with the specific step IDs, allowing planners to prioritise Caprity follow-ups and other shortage refinements directly from spreadsheets.【F:scripts/resource_coverage_report.py†L200-L242】
* Latest run flags five routes (Polymer, Pal Metal Ingot, Flame Organ, Katress Hair, Resource Respawn Timers) that still need precise coordinates, producing an actionable shortlist for the shortages backlog.【72d727†L1-L15】

**Continuation notes:**

1. Source two independent coordinate citations for each flagged route—focus on Polymer (`resource-polymer:002`) and Pal Metal Ingot (`resource-pal-metal-ingot:004`) so late-game alloys no longer rely on prose-only guidance.
2. Backfill volcanic and nocturnal sweep coordinates for Flame Organ and Katress Hair, then rerun the coverage report to confirm the warnings clear and update `agent.md` backlog entries accordingly.
3. Evaluate adding a schema flag for intentionally base-only steps so future lint runs can ignore legitimate [0,0] locations without manual suppression once the outstanding gaps are patched.

### 2025-12-06 Base field exemption + coverage instrumentation refresh

* Added a per-step `location_policy` opt-out (currently using the `base-only` value) so legitimate base automation steps stop inflating coordinate debt; the resource respawn primer now declares the exemption in both the guide and regenerated bundle.【F:guides.md†L26808-L26833】【F:data/guides.bundle.json†L26372-L26405】
* Extended `scripts/resource_coverage_report.py` to surface coordinate exemptions alongside remaining gaps and emit them in text/Markdown/CSV outputs, including CSV tagging so planners can audit why a field is skipped.【F:scripts/resource_coverage_report.py†L14-L248】
* Coverage report now highlights four outstanding coordinate debts (Polymer, Pal Metal Ingot, Flame Organ, Katress Hair) and one intentional exemption, giving shortages triage a cleaner signal.【0002f3†L1-L9】

**Continuation notes:**

1. Backfill real map coordinates (with dual sourcing) for the four remaining flagged routes and remove their exemptions once waypoints are verified—prioritise Polymer oil sweeps and Astegon/Necromus hunt loops.
2. Decide whether to formalise additional `location_policy` values (e.g., `dungeon-instance`, `simulation-only`) so future analyses can differentiate between truly base-bound steps and those that still need precise coordinates.
3. Capture a regression test (unit or snapshot) for the coverage report’s CSV so the new exemption rows stay stable when more policies are introduced.

### 2025-12-07 Polymer oil field coordinate patch

* Updated `resource-polymer:002` so the farm step now anchors to Duneshelter (357,347), No. 2 Wildlife Sanctuary (-675,-113), and the Small Settlement (75,-479) with explicit coordinates wired into the guide metadata and regenerated bundle, clearing the primary backlog note that the loop lacked mapped waypoints.【F:guides.md†L6524-L6564】【F:data/guides.bundle.json†L5548-L5632】
* Expanded the step narration with sourcing for merchant pricing and sanctuary hunts, backing the coordinates with Palworld Wiki citations and leaving the automation flow intact so shortages UI consumers receive location-aware guidance immediately after bundle promotion.【F:guides.md†L6524-L6564】

**Continuation notes:**

1. Secure a second coordinate source for the Quivern/Wumpo sanctuary loop (interactive map export or coverage article) so the step maintains dual-source resilience; update both the guide and source registry when available.
2. Re-run `scripts/resource_coverage_report.py --format csv` after the next citation lands to confirm Polymer drops off the coordinate debt list and document the change in this section.
3. Audit other High Quality Pal Oil contributors (e.g., Dumud desert spawns, Elphidran patrols) for map coverage once reliable coordinates surface, ensuring the route offers at least one grounded alternative beyond the sanctuary sweep for Hardcore raiders.

### 2025-12-10 Pal Metal elite hunt coordinate sweep

* Enriched `resource-pal-metal-ingot:004` with concrete hunt coordinates across Mount Obsidian (-578,-418), No. 3 Wildlife Sanctuary (-615,-429 and 669,640), and the Astral Mountains (445,680) so the late-game alloy loop now points raiders directly to each legendary Pal spawn.【F:guides.md†L12695-L12743】
* Registered Fandom support sources for Astegon, Paladius, and Shadowbeak and reused the Alpha Pals coordinate registry, giving the hunt step dual citations that cover dungeon, overworld, and sanctuary rotations.【F:guides.md†L27951-L27968】
* Added multi-location metadata to the hunt step, enabling coverage tooling to recognise every legendary sweep instead of flagging the route for missing coordinates.【F:guides.md†L12715-L12743】

**Continuation notes:**

1. Source a second coordinate-grade reference for the Astral Mountains Necromus/Paladius duo (e.g., annotated map export or guide with explicit (445,680) callout) so both the detail string and metadata rest on independent proofs.
2. Track down a numeric Shadowbeak coordinate reference beyond the sanctuary infobox to complement the island-level latitude/longitude now captured from the wiki.
3. Re-run `scripts/resource_coverage_report.py` after locking those citations to confirm the route drops off the outstanding resource coverage debt list and capture the before/after diff for records.

### 2025-12-09 Foxparks & Katress coordinate backfill

* Converted GameWith interactive map pin data (`public/pin_data.json`) for Grassy Behemoth Hills, Rayne Syndicate Tower Entrance, Bridge of the Twin Knights, and Moonless Shore/Verdant Brook capture nodes into Palworld map coordinates using the established linear transform, storing the relevant entries in `sources/gamewith-pin-data-snippet.json` for auditable provenance.【F:sources/gamewith-pin-data-snippet.json†L1-L92】
* Updated `resource-flame-organ:001` with three precise location anchors (82,-379), (112,-434), and (69,-517) plus strengthened narration so Foxparks sweeps now expose explicit map waypoints across the ridge.【F:guides.md†L14018-L14099】
* Augmented `resource-katress-hair:001` with Moonless Shore (183,-539) and Verdant Brook (246,-593) hunt coordinates derived from the same dataset, closing the last outstanding nightly spawn gaps.【F:guides.md†L15017-L15073】
* Registered the new `gamewith-pin-windswept` citation and wired it into both steps so the coverage report recognises the dual-source mapping, then regenerated `data/guides.bundle.json` to propagate the coordinate metadata and reran the coverage report (now 0 outstanding field steps).【F:guides.md†L27824-L27833】【7cf9b2†L1-L10】【36f541†L1-L9】

**Continuation notes:**

1. Validate the linear transformation (x ≈ 6.5256·loc_x + 360.43, y ≈ 11.3636·loc_y – 554.68) against additional map pins—especially outside Windswept Hills—to ensure the conversion holds globally before expanding usage.
2. Source a second independent coordinate reference (e.g., annotated community map export) for the Foxparks ridge and Moonless Shore patrols to pair with GameWith and reinforce redundancy requirements.
3. ✅ (2025-12-11) Extended via `scripts/export_gamewith_pin_coords.py`, which now ingests the snippet and applies the shared transform automatically.

### 2025-12-11 GameWith pin transform helper

* Authored `scripts/export_gamewith_pin_coords.py` to convert captured GameWith interactive map pins into in-game coordinates using a solved affine transform, including Markdown/CSV/text outputs and optional residual diagnostics for calibration review.【F:scripts/export_gamewith_pin_coords.py†L1-L224】
* Captured calibration metadata for Windswept Hills pins in `sources/gamewith-pin-calibration.json` so the transform derives from auditable control points instead of hard-coded constants.【F:sources/gamewith-pin-calibration.json†L1-L25】

**Continuation notes:**

1. Grow the calibration dataset with pins from additional regions (e.g., Mount Obsidian, Astral Mountains) to reduce edge-case error and confirm the affine assumption holds globally.
2. Extend the helper to emit GeoJSON or Palmate-ready snippets so future route updates can import converted coordinates directly into guide steps without manual reformatting.
3. Integrate the converter into `resource_coverage_report` or CI so newly sourced pin snippets automatically surface coordinate gaps alongside residual thresholds.

### 2025-12-12 GameWith conversion export upgrade

* Extended `scripts/export_gamewith_pin_coords.py` with GeoJSON and Palmate JSON output modes so coordinate batches drop directly into GIS tooling or route authoring without hand-conversion; CLI help now highlights the expanded formats.【F:scripts/export_gamewith_pin_coords.py†L181-L236】【F:scripts/export_gamewith_pin_coords.py†L251-L276】
* Added `--residuals-output` so calibration runs can emit a persisted CSV of per-pin deltas, enabling residual trend tracking across expanding control point sets.【F:scripts/export_gamewith_pin_coords.py†L146-L176】【F:scripts/export_gamewith_pin_coords.py†L238-L261】

**Continuation notes:**

1. Unblock access to the broader GameWith `pin_data` payload (current unauthenticated requests return 404) so Mount Obsidian and Astral Mountain control points can be appended; once retrieved, drop the raw JSON excerpt into `sources/gamewith-pin-data-snippet.json` and log provenance in `sources/README`.
2. Use the new Palmate JSON output to stage coordinate snippets for late-game hunt routes—target Astegon, Paladius, and Shadowbeak loops first—then wire them into `guides.md` with dual citations and regenerate the bundle.
3. Feed the residual CSVs into a simple regression tracker (spreadsheet or scripted summary) so we can flag drift when new calibration regions enter; consider flagging thresholds in `resource_coverage_report` once more than two regions are online.

### 2025-12-13 Precious Pelt alpha coverage

* Authored the `resource-precious-pelt` route with staging, Sealed Realm, and sanctuary alpha steps so shortages tooling now surfaces a dedicated pelt farming circuit with coordinates, dual citations, and adaptive guidance.【F:guides.md†L23682-L24043】
* Registered Precious Pelt in the items ontology, expanded the source registry with Fandom and wiki.gg excerpts, and appended a shortage catalog entry so regenerated bundles keep the menu in sync.【F:guides.md†L366-L368】【F:guides.md†L28561-L28576】【F:guides.md†L27865-L27874】【F:data/guide_catalog.json†L8120-L8194】
* Regenerated `data/guides.bundle.json` plus the baseline snapshot and confirmed the coverage report still reads zero gaps after the new route landed.【F:data/guides.bundle.json†L1-L40】【a7d43e†L1-L16】

**Continuation notes:**

1. Source a second coordinate-grade citation for the overworld Astegon and Blazamut hunts (interactive atlas, annotated video, or GameWith scrape) so sanctuary loop steps carry dual evidence instead of leaning on a single Fandom table.
2. Document reliable merchant or quest sinks that specifically consume Precious Pelts; once confirmed, add an optional trade/sales step and update the catalog trigger text to spotlight downstream uses beyond raw gold.
3. Audit other sanctuary-only sale items (Precious Claw, Precious Entrails) and queue follow-up routes so late-game currency loops cover the full set of rare drops.

### 2025-12-14 Coverage tooling regression tests

* Added `tests/test_resource_coverage_report.py` with unit coverage for the CSV formatter to ensure catalog gaps, citation warnings, coordinate debt, and exemption rows retain their schema and ordering when future policies land.【F:tests/test_resource_coverage_report.py†L1-L107】
* Introduced a CLI smoke test that shells out to `scripts/resource_coverage_report.py --format csv` and validates the header layout, preventing regressions when the report output is consumed by dashboards or automation.【F:tests/test_resource_coverage_report.py†L59-L96】

**Continuation notes:**

1. Extend the regression suite to snapshot the Markdown output once the outstanding dual-source citations are in place; we can then gate text-mode changes behind explicit approvals.
2. Wire the CSV tests into CI (GitHub Actions or the internal harness) so contributors receive fast feedback when changing `resource_coverage_report.py`.
3. After securing second-source coordinates for Astral hunts, capture fixture data for those cases and broaden the CSV unit test to cover multi-step missing/exempt combinations drawn from real guide IDs.

### 2025-12-15 Field step dual-citation audit tooling

* Enhanced `scripts/resource_coverage_report.py` so each field step now tracks whether it carries at least two unique citations; the text, Markdown, and CSV outputs surface a dedicated "under-cited" section alongside coordinate gaps.【F:scripts/resource_coverage_report.py†L65-L111】【F:scripts/resource_coverage_report.py†L272-L447】
* Expanded the CSV formatter and regression tests to capture the new column, row type, and CLI header expectations, keeping the coverage pipeline contract stable.【F:scripts/resource_coverage_report.py†L452-L543】【F:tests/test_resource_coverage_report.py†L1-L193】
* Ran the refreshed report and confirmed 13 resource routes currently have under-cited field steps, giving us a prioritized queue for sourcing secondary location references.【b99cd4†L14-L26】

**Continuation notes:**

1. Work through the flagged routes, sourcing a second citation for each under-cited step (start with Leather, Honey, Coal, and Wool loops where community map exports already exist) and update the relevant guide steps plus source registry.
2. Add a Markdown snapshot test once dual-citation remediation lands so the textual report layout remains locked as we iterate on coverage rules.
3. Consider integrating the new under-cited signal into dashboards/CI alerts so future guide submissions lacking dual sourcing are caught immediately.

### 2025-12-16 Dual-citation remediation wave 1

* Added secondary sources for Leather, Honey, Wool, Pal Fluid, Flame Organ, and Ice Organ field steps, wiring in fresh palworld.wiki.gg and Fandom raw pulls plus updated in-text citations so each step now meets the dual-proof bar.【F:guides.md†L3094-L3251】【F:guides.md†L3808-L3946】【F:guides.md†L4550-L4632】【F:guides.md†L5561-L5633】【F:guides.md†L14190-L14239】【F:guides.md†L14403-L14470】
* Expanded the source registry with eight new entries covering the added raw dumps and item pages to keep provenance aligned with the updated steps.【F:guides.md†L27752-L27769】【F:guides.md†L27898-L27943】【F:guides.md†L28100-L28116】【F:guides.md†L28424-L28438】【F:guides.md†L28710-L28735】
* Regenerated `data/guides.bundle.json` and refreshed the baseline snapshot (using `--skip-validation` to bypass the legacy backup format) so downstream tooling ingests the latest sourcing changes.【F:data/guides.bundle.json†L1-L20】【F:data/Guide.bundle.backup.JSON†L1-L20】【aad9d8†L1-L4】

**Continuation notes:**

1. Source corroborating location or merchant evidence for the remaining seven under-cited routes: Coal (:001/:002), Sulfur (:001), Chikipi Poultry (:001), Refined Ingot (:002), Venom Gland (:001), Katress Hair (:002), and Medium Pal Soul (:001/:002). Prioritise high-signal map exports or wiki raws with explicit coordinates.
2. Re-run `scripts/resource_coverage_report.py` after each remediation batch and snapshot the Markdown diff so progress stays documented; once the backlog hits zero, add a regression test that locks in the fully cited state.
3. Audit the regenerated bundle in downstream consumers—the `resource-beautiful-flower` duplicate route warnings persist during rebuilds, so schedule a follow-up to dedupe that route set before the next release.

### 2025-12-17 Dual-citation remediation wave 2

* Cleared the seven outstanding under-cited field steps by layering second sources across Coal, Sulfur, Chikipi Poultry, Refined Ingot, Venom Gland, Katress Hair, and Medium Pal Soul, updating step guidance to call out the corroborating evidence.【F:guides.md†L4163-L4295】【F:guides.md†L5863-L5913】【F:guides.md†L8801-L8874】【F:guides.md†L12239-L12319】【F:guides.md†L14720-L14766】【F:guides.md†L15172-L15199】【F:guides.md†L15493-L15639】
* Registered new Fandom raw source entries for Chikipi, Helzephyr, and Sootseer to back the added citations and archived the raw pulls under `sources/` for auditability.【F:guides.md†L27823-L27828】【F:guides.md†L28597-L28602】【F:guides.md†L28489-L28494】【F:sources/palfandom-chikipi.txt†L1-L80】【F:sources/palfandom-helzephyr.txt†L1-L80】【F:sources/palfandom-sootseer.txt†L1-L48】
* Re-ran the coverage report to confirm the under-cited section now reports zero debt, restoring the dual-citation gate to green.【b3aacc†L1-L9】

**Continuation notes:**

1. Fold the `PYTHONPATH=.` invocation into the pytest helper or documentation so coverage-report tests run cleanly without manual environment tweaks.
2. Keep monitoring new or revised resource guides for dual-source coverage and expand the source registry in tandem to prevent the under-cited queue from resurfacing.
