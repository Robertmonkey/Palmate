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

* High-priority shortages still missing guides: **Caprity Meat**, **Galeclaw Poultry**, **Broncherry Meat**, **Cotton Candy**, **High Quality Pal Oil**, **Small Pal Soul**, **Medium Pal Soul follow-ups (Crusher automation variants)**, **Sanctuary-exclusive drops (e.g., Lyleen Noct hair, Sibelyx Ignis cloth)**, **Merchant restock timing references**.
* Secondary targets once two independent citations are secured: **Milk auxiliary spawns**, **Seed restock timers (Tomato/Lettuce/Berry)**, **Elite alpha respawn timers for gemstone loops**, **Automation throughput benchmarks for Assembly Line/Power Grid resources**.

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
