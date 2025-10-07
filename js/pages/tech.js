import dataset from '../../data/palworld_complete_data_final.json' assert { type: 'json' };
import itemDetails from '../../data/item_details.json' assert { type: 'json' };

const itemDetailEntries = itemDetails && typeof itemDetails === 'object'
  ? Object.entries(itemDetails).map(([key, value]) => {
      const slug = String(key);
      if (!value || typeof value !== 'object') {
        return [slug, { slug, id: slug }];
      }
      const detail = { ...value };
      if (!detail.slug) detail.slug = slug;
      if (!detail.id) detail.id = slug;
      if (!detail.name && detail.title) detail.name = detail.title;
      return [slug, detail];
    })
  : [];

const itemDetailsBySlug = Object.fromEntries(
  itemDetailEntries.map(([key, value]) => [String(key), value])
);

const itemDetailsByName = new Map(
  itemDetailEntries
    .map(([, detail]) => {
      const name = detail && typeof detail === 'object' ? detail.name : null;
      return typeof name === 'string' && name.trim() ? [name.trim().toLowerCase(), detail] : null;
    })
    .filter(Boolean)
);

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

function findItemDetail(item) {
  if (!item || typeof item !== 'object') return null;
  const id = typeof item.id === 'string' ? item.id : '';
  const name = typeof item.name === 'string' ? item.name : '';
  const slugKey = id ? id.replace(/[^a-z0-9]+/gi, '_').toLowerCase() : '';
  if (slugKey && itemDetailsBySlug[slugKey]) return itemDetailsBySlug[slugKey];
  if (name) {
    const detail = itemDetailsByName.get(name.trim().toLowerCase());
    if (detail) return detail;
  }
  if (name) {
    const fallbackSlug = name.trim().toLowerCase().replace(/[^a-z0-9]+/g, '_');
    if (itemDetailsBySlug[fallbackSlug]) return itemDetailsBySlug[fallbackSlug];
  }
  return null;
}

function resolveMaterials(item) {
  const direct = normaliseMaterials(item?.materials);
  if (direct.length) {
    return direct.map(entry => ({ ...entry, icon: null }));
  }
  const detail = findItemDetail(item);
  if (!detail || typeof detail !== 'object' || !Array.isArray(detail.recipe)) return [];
  return detail.recipe
    .map(ingredient => {
      if (!ingredient || typeof ingredient !== 'object') return null;
      const name = typeof ingredient.name === 'string' ? ingredient.name : '';
      if (!name.trim()) return null;
      const quantityRaw = ingredient.quantity;
      const numberValue =
        typeof quantityRaw === 'number'
          ? quantityRaw
          : quantityRaw !== undefined
          ? Number(quantityRaw)
          : NaN;
      const quantity = Number.isFinite(numberValue) && numberValue >= 0 ? numberValue : null;
      const icon = typeof ingredient.icon === 'string' && ingredient.icon.trim() ? ingredient.icon : null;
      return { name, quantity, icon };
    })
    .filter(Boolean);
}

function lookupMaterialDetail(name) {
  if (!name) return null;
  const normalized = String(name).trim().toLowerCase();
  if (!normalized) return null;
  const fromName = itemDetailsByName.get(normalized);
  if (fromName) return fromName;
  const slugKey = normalized.replace(/[^a-z0-9]+/g, '_');
  return itemDetailsBySlug[slugKey] || null;
}

function renderMaterialChip(entry) {
  if (!entry || !entry.name) return '';
  const name = String(entry.name).trim();
  if (!name) return '';
  const detail = lookupMaterialDetail(name);
  const iconCandidate = entry.icon || (detail && typeof detail === 'object' && (detail.image || detail.icon));
  const icon = iconCandidate && String(iconCandidate).trim() ? String(iconCandidate).trim() : null;
  const quantity = Number.isFinite(entry.quantity) ? entry.quantity : null;
  const qtyLabel = quantity !== null ? `×${quantity}` : '×?';
  const ariaLabel = quantity !== null
    ? `${detail?.name || name}, quantity ${quantity}`
    : `${detail?.name || name}, quantity unknown`;
  const displayName = detail?.name ? detail.name : name;
  const slug = detail?.slug || detail?.id || displayName.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const payload = {
    type: 'item',
    id: slug,
    slug,
    name: displayName
  };
  const payloadAttr = escapeHtml(JSON.stringify(payload));
  const thumb = icon
    ? `<span class="chip__thumb"><img src="${escapeHtml(icon)}" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer"></span>`
    : '<span class="chip__thumb tech-material-chip__thumb--placeholder" aria-hidden="true">⚙️</span>';
  return `
    <li class="tech-material">
      <a href="#" class="chip link tech-material-chip link--with-thumb" data-link="${payloadAttr}" data-link-type="item" role="button" aria-label="${escapeHtml(ariaLabel)}">
        ${thumb}
        <span class="chip__body">
          <span class="chip__label">${escapeHtml(displayName)}</span>
          <span class="chip__meta">${escapeHtml(qtyLabel)}</span>
        </span>
      </a>
    </li>
  `;
}

function renderMaterials(item) {
  const entries = resolveMaterials(item);
  if (!entries.length) return '';
  const chips = entries.map(renderMaterialChip).join('');
  return `<ul class="tech-materials" aria-label="Required materials" role="list">${chips}</ul>`;
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
        ${renderMaterials(item)}
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
  const links = node.querySelectorAll('a[data-link]');
  links.forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      const raw = link.getAttribute('data-link');
      if (!raw) return;
      let payload = null;
      try {
        payload = JSON.parse(raw);
      } catch (error) {
        payload = null;
      }
      if (!payload) return;
      if (typeof window.navigateLink === 'function') {
        window.navigateLink(payload);
        return;
      }
      if (payload.type === 'item' && typeof window.openItemDetail === 'function') {
        window.openItemDetail(payload.id || payload.slug || payload.name);
      }
    });
  });
}
