Pal Marathon – An Interactive Companion Guide for Palworld

Pal Marathon is an open‑source, offline‑first web application designed as the ultimate companion for exploring and conquering the world of Palworld. Built for families to play together, it offers two modes—Kid Mode and Grown‑up Mode—and features a complete Paldex, interactive map integration, route planner, tech tree, item index, glossary, breeding calculator and progress tracker. The project runs entirely in your browser and can be hosted on GitHub Pages without any backend.

Features

Kid Mode / Grown‑up Mode – The interface adapts to its audience. Kid Mode uses larger buttons and simplified descriptions with optional text‑to‑speech, while Grown‑up Mode displays full stats, breeding power, sortable tables and patch notes.

Comprehensive Paldex – Browse all pals, filter by element or work role, and view detailed pages including stats, moves, passives, work suitabilities, gear, breeding combos and spawn hints. Every term (move, passive, item) is cross‑linked, making exploration intuitive.

Interactive Map Integration – The map page embeds the official Palworld.gg interactive map in an <iframe> so you can explore spawn locations, towers, dungeons, effigies, skill fruit trees and fast travel points without leaving the app. A static map fallback is provided for offline viewing.

Route Planner – Follow a step‑by‑step route through the seven tower bosses. Each entry includes element, weakness, HP, location and climate, plus preparation tips and detailed instructions on how to tackle the encounter.

Technology Tree – See all Pal gear and ancient technology recipes with level requirements, cost and material lists. Unlocks are tracked in your browser’s local storage.

Items & Glossary – Search through pal gear, general items, passive skills, active moves, element strengths/weaknesses and work suitabilities. Clicking any entry opens a modal with concise explanations and additional links.

Breeding Calculator – Select two parent pals to predict their offspring. The app uses breeding power averages to provide likely results and lists known parent combinations.

Progress Tracking – Mark pals as caught, items as collected, tech recipes as unlocked and route steps as completed. All progress is saved in your browser (no account needed).

Directory Structure
├── index.html                     # Main application file (HTML, CSS, JS in one)
├── data/
│   ├── palworld_complete_data_final.json       # Comprehensive data file for pals, items, tech, route, skills and passives
│   └── palworld_complete_data_fallback.js      # Auto-generated JS fallback when fetch() is blocked
├── assets/
│   ├── pals/                     # Pal menu images
│   ├── icons/                    # Element icons
│   ├── images/                   # Map, background and other images
│   └── sounds/                   # Placeholder audio files for UI interactions
├── agent.md                      # Guidelines for AI agents working on this project
├── README.md                     # This document
└── scripts/                      # (optional) Data processing or enrichment scripts

Running Locally

Because browsers restrict file:// fetch requests, you need to serve the project via an HTTP server. A quick way is using Python:

cd palmarathon    # change into the project directory
python3 -m http.server 8000


Then open http://localhost:8000/index.html in your browser. The app will load the data file and all assets correctly.

If you cannot run a local server (for example, when double-clicking the HTML file), the app falls back to `data/palworld_complete_data_fallback.js`. The fallback mirrors the JSON payload in JavaScript so it can be loaded even when browsers block `fetch()` on the `file://` protocol. Regenerate it whenever the JSON changes:

```
python scripts/generate_embedded_dataset.py
```

Contributing

Contributions are welcome! Here are some guidelines:

Keep Data Centralised – Always update the JSON files in data/ rather than embedding data in HTML. Maintain consistent keys and structures.

Respect Mode Distinctions – When adding new features, ensure they work for both Kid Mode and Grown‑up Mode. Provide simplified text and bigger hit targets for Kid Mode.

No External Tile Hosting – Do not copy or host third‑party map tiles. The interactive map is provided via an iframe pointing to Palworld.gg. Use the static image for offline fallback.

Test Thoroughly – Serve the site locally and verify that new additions don’t break existing functionality. Check cross‑linking between pals, items, moves and passives.

Cite Your Sources – When adding new spawn areas, tech recipes or trait descriptions, include a link to a reliable source (e.g., Palworld wiki, Game8, Polygon) in your commit message or in a code comment.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements

Pal Marathon is a community fan project and is not affiliated with Pocketpair Inc., Palworld.gg or Game8.co. Data and descriptions are adapted from open community resources, including Palworld.gg, Game8 guides and official Palworld API CSVs.
