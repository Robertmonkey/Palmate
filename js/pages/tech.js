import dataset from '../../data/palworld_complete_data_final.json' assert { type: 'json' };

const techLevels = Array.isArray(dataset?.tech)
  ? dataset.tech
      .filter(level => level && typeof level.level === 'number')
      .map(level => ({
        level: level.level,
        items: Array.isArray(level.items) ? level.items.filter(Boolean) : []
      }))
      .sort((a, b) => a.level - b.level)
  : [];

const htmlEscapes = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;'
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => htmlEscapes[character] || character);
}

function normaliseMaterials(materials) {
  if (!materials || typeof materials !== 'object') return [];
  return Object.entries(materials)
    .filter(([, qty]) => qty !== null && qty !== undefined)
    .map(([name, qty]) => ({
      name: String(name),
      quantity: Number(qty)
    }))
    .filter(entry => entry.name.trim().length && Number.isFinite(entry.quantity) && entry.quantity >= 0);
}

function renderMaterials(materials) {
  const entries = normaliseMaterials(materials);
  if (!entries.length) return '';
  const rows = entries
    .map(entry => `<li><span>${escapeHtml(entry.name)}</span><span>${entry.quantity}</span></li>`)
    .join('');
  return `<ul class="tech-materials" aria-label="Required materials">${rows}</ul>`;
}

function renderBadges(item) {
  const badges = [];
  if (item.category) badges.push(item.category);
  if (item.group && item.group !== item.category) badges.push(item.group);
  if (item.branch && item.branch !== 'Technology') badges.push(item.branch);
  if (!badges.length) return '';
  return `
    <div class="tech-badges">
      ${badges
        .map(label => `<span class="tech-badge">${escapeHtml(label)}</span>`)
        .join('')}
    </div>
  `;
}

function formatCost(item) {
  const points = typeof item.techPoints === 'number' ? item.techPoints : null;
  if (points === null) return '';
  if (points === 0) {
    return `<p class="tech-cost">Free unlock</p>`;
  }
  const label = item.isAncient ? 'Ancient Points' : 'Tech Points';
  return `<p class="tech-cost">${escapeHtml(points)} ${label}</p>`;
}

function renderImage(item) {
  if (!item.image) {
    return '<div class="tech-image tech-image--placeholder" aria-hidden="true">⚙️</div>';
  }
  const alt = `${item.name} illustration`;
  return `
    <div class="tech-image">
      <img src="${escapeHtml(item.image)}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async" referrerpolicy="no-referrer">
    </div>
  `;
}

function renderDescription(item) {
  const description = item.description
    ? escapeHtml(item.description)
    : `Unlocks the ${escapeHtml(item.name)} blueprint.`;
  return `<p class="tech-description">${description}</p>`;
}

function renderItemCard(item) {
  if (!item || !item.name) return '';
  const techId = item.id || item.name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  return `
    <article class="tech-card" id="tech-${escapeHtml(techId)}">
      ${renderImage(item)}
      <div class="tech-body">
        <h5 class="tech-name">${escapeHtml(item.name)}</h5>
        ${renderBadges(item)}
        ${formatCost(item)}
        ${renderDescription(item)}
        ${renderMaterials(item.materials)}
      </div>
    </article>
  `;
}

function renderColumn(title, items) {
  const safeTitle = escapeHtml(title);
  if (!items.length) {
    return `
      <div class="tech-column">
        <h4>${safeTitle}</h4>
        <p class="tech-empty">No unlocks at this tier.</p>
      </div>
    `;
  }
  return `
    <div class="tech-column">
      <h4>${safeTitle}</h4>
      <div class="tech-grid">
        ${items.map(renderItemCard).join('')}
      </div>
    </div>
  `;
}

function renderLevel(level) {
  const standard = level.items.filter(item => !item?.isAncient);
  const ancient = level.items.filter(item => item?.isAncient);
  return `
    <section class="tech-tier" aria-labelledby="tech-tier-${level.level}">
      <header class="tech-tier__header">
        <span class="tech-tier__label">Level</span>
        <h3 id="tech-tier-${level.level}">${escapeHtml(level.level)}</h3>
      </header>
      <div class="tech-tier__columns">
        ${renderColumn('Technology', standard)}
        ${renderColumn('Ancient Technology', ancient)}
      </div>
    </section>
  `;
}

export function renderTech(node) {
  if (!node) return;
  if (!techLevels.length) {
    node.innerHTML = '<p class="tech-empty">Technology data is unavailable.</p>';
    return;
  }
  node.innerHTML = `
    <h2>Technology Tree</h2>
    <div class="tech-tiers">
      ${techLevels.map(renderLevel).join('')}
    </div>
  `;
}
