Agent Guidelines for Pal Marathon

This document is intended for AI agents (such as ChatGPT Codex) that interact with the Pal Marathon project. It outlines the project’s structure, conventions and best practices so that automated tools can navigate and modify the codebase effectively.

Project Overview

Pal Marathon is an offline‑first, single‑page web application that serves as a comprehensive guide for Palworld. It is designed to run entirely within the browser using HTML, CSS and JavaScript, and is best hosted on GitHub Pages. The app provides cross‑linked information about pals, moves, passives, items, technologies, routes and more, with separate presentation modes for children and adults.

Repository Structure

palmate.html – The primary HTML document containing inline CSS and JavaScript. This file bootstraps the app, loads the JSON data and renders all pages (Home, Pals, Map, Route, Tech, Items, Glossary, Breeding and Progress). Navigation is handled via JavaScript by toggling the visibility of <section> elements.

data/ – Contains JSON data files. The main file, palworld_complete_data_final.json, holds structured data for pals, items, tech tree, route steps, skills and passives. Each pal record includes stats, work suitability, drops, breeding data, image paths, spawn areas and pre‑computed breeding combos.

assets/ – Holds all static assets:

assets/pals/ – Menu images for each pal.

assets/icons/ – Element type icons.

assets/images/ – Shared images (e.g. static world map, background).

assets/sounds/ – Placeholder audio files for UI interactions.

scripts/ (optional) – Python or Node scripts for processing or enriching the dataset. For example, you might add a script to download new pal images or update spawn areas.

Data Model

The pals object in the JSON file is keyed by string IDs and contains fields such as:

id, key, name, wiki, image, localImage – identification and art assets.

genus, rarity, price, size – basic info.

stats – numerical stats like HP, attack, defense, speed, stamina, etc.

work – work suitability levels for roles like Kindling, Mining, etc.

skills – list of active skill keys.

drops – items this pal drops upon defeat or harvesting.

breeding – breeding power and types used in breeding calculations.

types – primary and secondary elemental types.

spawnAreas – list of biome names where the pal typically spawns.

breedingCombos – array of parent pairs that can produce this pal.

Other top‑level keys include:

items – dictionary of items with categories, the pals that drop them and any crafting use.

tech – array of tech levels with their recipes or unlocks and required materials.

route – array of tower boss encounters with elements, weaknesses, HP, location, tips and steps lists for a narrative walkthrough.

skillsDetails – dictionary of active skills describing damage category, type and a short description.

passiveDetails – dictionary of passive traits with concise descriptions.

Agents should never hard‑code data into the HTML; instead, update the JSON and adjust the rendering functions to accommodate new fields. This ensures data remains decoupled from presentation.

Guidelines for Agents

Loading Data – Use the fetch() call in palmate.html to read the JSON file. When adding new data fields, update the parsing logic accordingly.

Adding Content – When new pals, items or tech appear in the game, append them to the JSON with appropriate keys and structure. Maintain alphabetical or numerical ordering where possible. Be sure to assign spawnAreas and breedingCombos for new pals.

UI Enhancements – All UI changes should preserve responsiveness and the distinction between Kid Mode and Grown‑up Mode. Use the existing CSS variables for colours and spacing to maintain visual coherence. Make sure navigation remains intuitive and that new pages or modals are cross‑linked.

Map Integration – Do not embed or scrape third‑party map tiles. The current approach uses an iframe to load palworld.gg for full interactivity and a static image as fallback. If embedding fails due to CORS, provide clear instructions for users to open the map in a new tab.

Data Enrichment – If research yields new spawn locations, tech items or patch changes, update the JSON data and include citations as comments in the commit message or relevant script. Avoid duplicating information across multiple files.

Accessibility – Ensure new content supports keyboard navigation, screen readers (consider aria-labels) and includes alt text for images. Provide simplified descriptions in Kid Mode and more detailed information in Grown‑up Mode.

Testing – Always serve the app through a local HTTP server (e.g. python -m http.server) before testing, as browser security restrictions prevent file:// fetches.

Source Attribution – When adding factual data (spawn areas, skill descriptions, etc.), cite reliable sources such as Palworld wiki pages, Game8 guides or Polygon articles. Include these citations in pull request descriptions or code comments where appropriate.

By following these guidelines, AI agents can safely extend and maintain the Pal Marathon project while preserving its overall quality and usability.
