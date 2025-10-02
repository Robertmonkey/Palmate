const fs = require('fs');
const path = require('path');

const catalogPath = path.join(__dirname, '..', 'data', 'guide_catalog.json');
const palDataPath = path.join(__dirname, '..', 'data', 'palworld_complete_data_final.json');
const itemDetailsPath = path.join(__dirname, '..', 'data', 'item_details.json');

const PALWORLD_MAP_URL = 'https://palworld.gg/map';
const MANUAL_LINKS = [
  {
    regex: /\bgreat eagle statues?\b/i,
    link: { type: 'location', id: 'great-eagle-statue', name: 'Great Eagle Statue', region: 'Fast Travel Network', url: PALWORLD_MAP_URL }
  },
  {
    regex: /\bsmall settlement\b/i,
    link: { type: 'location', id: 'small-settlement', name: 'Small Settlement', region: 'Windswept Hills', url: PALWORLD_MAP_URL }
  },
  {
    regex: /\bcinnamoth forest\b/i,
    link: { type: 'location', id: 'cinnamoth-forest', name: 'Cinnamoth Forest', region: 'Windswept Hills', url: PALWORLD_MAP_URL }
  },
  {
    regex: /\bsealed realm(?: of the guardian)?\b/i,
    link: { type: 'location', id: 'sealed-realm-of-the-guardian', name: 'Sealed Realm of the Guardian', region: 'Windswept Hills', url: PALWORLD_MAP_URL }
  },
  {
    regex: /\bsakurajima(?: island)?\b/i,
    link: { type: 'location', id: 'sakurajima-island', name: 'Sakurajima Island', region: 'Sakurajima', url: PALWORLD_MAP_URL }
  },
  {
    regex: /\bastral mountains\b/i,
    link: { type: 'location', id: 'astral-mountains', name: 'Astral Mountains', region: 'Astral Mountains', url: PALWORLD_MAP_URL }
  }
];

function readJson(file){
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function slugify(text){
  if(!text) return '';
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function normaliseLabel(value){
  if(!value) return '';
  return String(value)
    .replace(/[\u2019\u2018']/g, '')
    .replace(/[\u2013\u2014-]/g, ' ')
    .replace(/[^a-zA-Z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function buildPatterns(name){
  const cleaned = normaliseLabel(name).toLowerCase();
  if(!cleaned) return [];
  const tokens = cleaned.split(/\s+/).filter(Boolean);
  if(!tokens.length) return [];
  if(tokens.length === 1 && tokens[0].length < 3) return [];
  const pattern = new RegExp(`\\b${tokens.join('\\s+')}\\b`, 'i');
  return [{ pattern, phrase: tokens.join(' ') }];
}

function createEntity({ type, id, name, image, synonyms = [] }){
  const display = name || id;
  const slug = slugify(id || name);
  const synonymSet = new Set();
  [name, id, display, slug, ...synonyms].forEach(value => {
    if(!value) return;
    const normalized = normaliseLabel(value);
    if(!normalized) return;
    synonymSet.add(normalized);
  });
  const patterns = [];
  synonymSet.forEach(value => {
    buildPatterns(value).forEach(entry => {
      patterns.push(entry.pattern);
    });
  });
  if(!patterns.length){
    return null;
  }
  return { type, id, slug, name: display, image: image || null, patterns };
}

function buildDictionary({ palData, itemDetails }){
  const entities = [];
  const techMap = new Map();
  (palData.tech || []).forEach(level => {
    (level.items || []).forEach(entry => {
      if(!entry || !entry.id) return;
      if(techMap.has(entry.id)) return;
      const entity = createEntity({ type: 'tech', id: entry.id, name: entry.name, image: entry.image });
      if(entity){
        techMap.set(entry.id, entity);
        entities.push(entity);
      }
    });
  });
  const itemMap = new Map();
  Object.entries(itemDetails || {}).forEach(([id, detail]) => {
    if(itemMap.has(id)) return;
    const entity = createEntity({ type: 'item', id, name: detail && detail.name });
    if(entity){
      itemMap.set(id, entity);
      entities.push(entity);
    }
  });
  Object.entries(palData.items || {}).forEach(([id, detail]) => {
    if(itemMap.has(id)) return;
    if(!/-|_/.test(id)) return;
    const fallbackName = String(id)
      .replace(/[_-]+/g, ' ')
      .replace(/\b\w/g, char => char.toUpperCase());
    const displayName = (detail && detail.name) || fallbackName;
    const entity = createEntity({ type: 'item', id, name: displayName });
    if(entity){
      itemMap.set(id, entity);
      entities.push(entity);
    }
  });
  const palMap = new Map();
  Object.values(palData.pals || {}).forEach(pal => {
    if(!pal || palMap.has(pal.id)) return;
    const entity = createEntity({ type: 'pal', id: String(pal.id), name: pal.name, image: pal.localImage || pal.image });
    if(entity){
      palMap.set(pal.id, entity);
      entities.push(entity);
    }
  });
  return entities;
}

function findMatches(text, entities, existingLinks){
  if(!text) return [];
  const lower = text.toLowerCase();
  const normalised = normaliseLabel(text).toLowerCase();
  const seen = new Set((existingLinks || []).map(link => `${link.type}:${link.id || link.slug || link.name || ''}`));
  const matches = [];
  entities.forEach(entity => {
    if(seen.has(`${entity.type}:${entity.id}`)) return;
    const matched = entity.patterns.some(pattern => pattern.test(lower) || pattern.test(normalised));
    if(matched){
      seen.add(`${entity.type}:${entity.id}`);
      const link = { type: entity.type, id: entity.id };
      if(entity.slug) link.slug = entity.slug;
      if(entity.name) link.name = entity.name;
      if(entity.image) link.image = entity.image;
      matches.push(link);
    }
  });
  MANUAL_LINKS.forEach(entry => {
    if(!entry || !entry.link || !entry.regex) return;
    if(entry.regex.test(text) || entry.regex.test(normalised)){
      const manual = { ...entry.link };
      const key = `${manual.type}:${manual.id || manual.slug || manual.name || ''}`;
      if(seen.has(key)) return;
      seen.add(key);
      matches.push(manual);
    }
  });
  return matches;
}

function sortLinks(links){
  return links.slice().sort((a, b) => {
    const order = { pal: 0, tech: 1, item: 2, tower: 3, location: 4, npc: 5 };
    const aOrder = order[a.type] ?? 99;
    const bOrder = order[b.type] ?? 99;
    if(aOrder !== bOrder) return aOrder - bOrder;
    const aId = (a.id || a.slug || '').toString();
    const bId = (b.id || b.slug || '').toString();
    return aId.localeCompare(bId, undefined, { sensitivity: 'base' });
  });
}

function mergeLinks(existing, additions){
  const byKey = new Map();
  existing.forEach(link => {
    if(!link || !link.type) return;
    const key = `${link.type}:${link.id || link.slug || link.name || ''}`;
    if(!byKey.has(key)){
      byKey.set(key, { ...link });
    }
  });
  additions.forEach(link => {
    if(!link || !link.type) return;
    const key = `${link.type}:${link.id || link.slug || link.name || ''}`;
    if(byKey.has(key)) return;
    byKey.set(key, { ...link });
  });
  return sortLinks(Array.from(byKey.values()));
}

function enhanceGuideCatalog(){
  const catalog = readJson(catalogPath);
  const palData = readJson(palDataPath);
  const itemDetails = readJson(itemDetailsPath);
  const entities = buildDictionary({ palData, itemDetails });
  let updatedSteps = 0;
  catalog.guides.forEach(guide => {
    if(!Array.isArray(guide.steps)) return;
    guide.steps.forEach(step => {
      const existingLinks = Array.isArray(step.links) ? step.links.filter(link => link && link.type) : [];
      const matches = findMatches(step.instruction || '', entities, existingLinks);
      if(matches.length){
        step.links = mergeLinks(existingLinks, matches);
        updatedSteps += 1;
      } else if(existingLinks.length){
        step.links = sortLinks(existingLinks);
      } else if(step.links){
        delete step.links;
      }
    });
  });
  fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2) + '\n');
  console.log(`Enhanced guide catalog with link chips for ${updatedSteps} steps.`);
}

enhanceGuideCatalog();
