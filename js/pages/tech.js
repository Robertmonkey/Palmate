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

function isKidMode() {
  if (typeof document === 'undefined') return false;
  const { body } = document;
  return !!(body && typeof body.classList !== 'undefined' && body.classList.contains('kid-mode'));
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

function isGenericTechDescription(text) {
  if (typeof text !== 'string') return true;
  const normalised = text.trim().toLowerCase();
  if (!normalised) return true;
  return (
    normalised.startsWith('unlocks the') ||
    normalised.startsWith('unlock the') ||
    normalised.startsWith('unlocks ') ||
    normalised.startsWith('unlock ')
  );
}

function buildDefaultTechDescription(item, { kid = false } = {}) {
  const name = item?.name || 'this unlock';
  const group = String(item?.group || '').toLowerCase();
  const category = String(item?.category || '').toLowerCase();
  const ancient = !!item?.isAncient;
  if (category.includes('base') || group.includes('structure') || group.includes('building')) {
    return kid ? `Adds the ${name} building to your base.` : `Adds the ${name} structure to your base build menu.`;
  }
  if (category.includes('weapon')) {
    return kid ? `Lets you craft the ${name} weapon.` : `Unlocks crafting for the ${name} weapon.`;
  }
  if (category.includes('armor') || category.includes('gear') || group.includes('armor')) {
    return kid ? `Lets you make the ${name} gear to wear.` : `Unlocks the ${name} gear recipe.`;
  }
  if (category.includes('vehicle') || group.includes('mount')) {
    return kid ? `Lets you ride with the ${name}.` : `Unlocks the ${name} mount blueprint.`;
  }
  if (ancient) {
    return kid ? `Restores the ancient ${name} so you can use it again.` : `Restores the ancient ${name} blueprint.`;
  }
  return kid ? `Lets you make ${name}.` : `Unlocks crafting for ${name}.`;
}

function computeTechDescriptions(item) {
  const raw = typeof item?.description === 'string' ? item.description.trim() : '';
  const grown = raw && !isGenericTechDescription(raw) ? raw : buildDefaultTechDescription(item, { kid: false });
  const kidCopy = raw && !isGenericTechDescription(raw)
    ? raw.replace(/\bUnlocks\b/gi, 'Lets')
    : buildDefaultTechDescription(item, { kid: true });
  return {
    grown,
    kid: kidCopy || grown
  };
}

function formatTechCost(item, { kid = false, short = false } = {}) {
  if (!item || typeof item.techPoints !== 'number') {
    return kid ? 'Cost unknown' : 'Cost unknown';
  }
  const points = item.techPoints;
  if (points === 0) {
    return kid ? 'Free unlock' : 'Free unlock';
  }
  const isAncient = !!item.isAncient;
  if (short) {
    return `${points} ${isAncient ? 'AP' : 'TP'}`;
  }
  return `${points} ${isAncient ? 'Ancient Points' : 'Tech Points'}`;
}

function formatTechStatusText(isUnlocked, kidMode) {
  return isUnlocked
    ? (kidMode ? 'Already built!' : 'Unlocked')
    : (kidMode ? 'Still locked' : 'Locked');
}

function renderMaterialsSection(item, { kidMode }) {
  const entries = resolveMaterials(item);
  const note = typeof item?.note === 'string' && item.note.trim() ? item.note.trim() : null;
  if (!entries.length) {
    const fallback = kidMode
      ? 'No ingredients needed for this unlock.'
      : 'No crafting ingredients required for this unlock.';
    const message = note || fallback;
    return `<p class="tech-card__note">${escapeHtml(message)}</p>`;
  }
  const chips = entries.map(renderMaterialChip).join('');
  const list = `<ul class="tech-card__materials tech-materials" aria-label="Required materials" role="list">${chips}</ul>`;
  if (note) {
    return `${list}<p class="tech-card__note">${escapeHtml(note)}</p>`;
  }
  return list;
}

function renderBadges(item) {
  const chips = new Set();
  if (item.category) chips.add(item.category);
  if (item.group && item.group !== item.category) chips.add(item.group);
  if (item.branch && item.branch !== 'Technology') chips.add(item.branch);
  if (!chips.size) return '';
  return `
    <div class="tech-card__chips">
      ${Array.from(chips)
        .map(label => `<span class="tech-chip">${escapeHtml(label)}</span>`)
        .join('')}
    </div>
  `;
}

function renderImage(item) {
  if (!item.image) {
    return '<div class="tech-card__art tech-card__art--fallback" aria-hidden="true">⚙️</div>';
  }
  const alt = `${item.name} illustration`;
  return `
    <div class="tech-card__art">
      <img src="${escapeHtml(item.image)}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async" referrerpolicy="no-referrer">
    </div>
  `;
}

function renderDescription(item, kidMode) {
  const descriptions = computeTechDescriptions(item);
  const text = kidMode ? descriptions.kid : descriptions.grown;
  return `<p class="tech-card__description">${escapeHtml(text)}</p>`;
}

function renderItemCard(item, kidMode) {
  if (!item || !item.name) return '';
  const slug = typeof item.id === 'string' && item.id.trim()
    ? item.id.trim()
    : item.name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const techKey = slug || item.name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const unlocked = typeof window !== 'undefined' && typeof window.isTechUnlocked === 'function'
    ? window.isTechUnlocked(item.name)
    : false;
  const classes = ['tech-card'];
  if (unlocked) classes.push('tech-card--unlocked');
  const costLabel = formatTechCost(item, { kid: kidMode, short: true });
  const showCost = costLabel && costLabel !== 'Cost unknown';
  const statusText = formatTechStatusText(unlocked, kidMode);
  const costMarkup = showCost ? `<span class="tech-card__cost">${escapeHtml(costLabel)}</span>` : '';
  const ariaRole = kidMode ? 'Tech card' : 'Technology card';
  return `
    <article class="${classes.join(' ')}" id="tech-${escapeHtml(techKey)}" data-tech-key="${escapeHtml(techKey)}" data-tech-name="${escapeHtml(item.name)}" data-tech-branch="${escapeHtml(item.branch || '')}" tabindex="0" role="group" aria-roledescription="${escapeHtml(ariaRole)}">
      ${renderImage(item)}
      <div class="tech-card__info">
        <div class="tech-card__meta">
          <h5 class="tech-card__name">${escapeHtml(item.name)}</h5>
          ${costMarkup}
        </div>
        ${renderBadges(item)}
        ${renderDescription(item, kidMode)}
        ${renderMaterialsSection(item, { kidMode })}
        <div class="tech-card__footer">
          <span class="tech-card__status${unlocked ? ' tech-card__status--unlocked' : ''}" data-tech-status="${escapeHtml(techKey)}">${escapeHtml(statusText)}</span>
          <button type="button" class="unlock-btn${unlocked ? ' unlocked' : ''}" data-tech-key="${escapeHtml(techKey)}" data-tech-name="${escapeHtml(item.name)}" aria-pressed="${unlocked ? 'true' : 'false'}">${escapeHtml(unlocked ? 'Unlocked' : 'Unlock')}</button>
        </div>
      </div>
    </article>
  `;
}

function renderColumn(title, items, kidMode) {
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
      <div class="tech-card-grid tech-grid">
        ${items.map(item => renderItemCard(item, kidMode)).join('')}
      </div>
    </div>
  `;
}

function renderLevel(level, kidMode) {
  const standard = level.items.filter(item => !item?.isAncient);
  const ancient = level.items.filter(item => item?.isAncient);
  return `
    <section class="tech-tier" aria-labelledby="tech-tier-${level.level}">
      <header class="tech-tier__header">
        <span class="tech-tier__label">Level</span>
        <h3 id="tech-tier-${level.level}">${escapeHtml(level.level)}</h3>
      </header>
      <div class="tech-tier__columns">
        ${renderColumn('Technology', standard, kidMode)}
        ${renderColumn('Ancient Technology', ancient, kidMode)}
      </div>
    </section>
  `;
}

export function renderTech(node) {
  if (!node) return;
  const kidMode = isKidMode();
  if (!techLevels.length) {
    node.innerHTML = '<p class="tech-empty">Technology data is unavailable.</p>';
    return;
  }
  node.innerHTML = `
    <h2>Technology Tree</h2>
    <div class="tech-tiers">
      ${techLevels.map(level => renderLevel(level, kidMode)).join('')}
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
  const buttons = node.querySelectorAll('.unlock-btn');
  buttons.forEach(button => {
    button.addEventListener('click', event => {
      event.stopPropagation();
      const techKey = button.getAttribute('data-tech-key');
      const techName = button.getAttribute('data-tech-name') || '';
      const current = typeof window !== 'undefined' && typeof window.isTechUnlocked === 'function'
        ? window.isTechUnlocked(techName)
        : button.classList.contains('unlocked');
      let desired = !current;
      if (typeof window !== 'undefined' && typeof window.setTechUnlocked === 'function') {
        const result = window.setTechUnlocked(techName, desired, { techKey });
        if (typeof result === 'boolean') {
          desired = result;
        }
      }
      button.classList.toggle('unlocked', desired);
      button.textContent = desired ? 'Unlocked' : 'Unlock';
      button.setAttribute('aria-pressed', desired ? 'true' : 'false');
      const card = button.closest('.tech-card');
      if (card) {
        card.classList.toggle('tech-card--unlocked', desired);
        const status = card.querySelector('[data-tech-status]');
        if (status) {
          status.textContent = formatTechStatusText(desired, kidMode);
          status.classList.toggle('tech-card__status--unlocked', desired);
        }
      }
    });
  });
  const cards = node.querySelectorAll('.tech-card[data-tech-key]');
  cards.forEach(card => {
    card.addEventListener('click', event => {
      const origin = event.target;
      if (typeof Element !== 'undefined' && origin instanceof Element) {
        if (origin.closest('a') || origin.closest('button')) return;
      }
      const techKey = card.getAttribute('data-tech-key');
      if (techKey && typeof window !== 'undefined' && typeof window.showTechDetail === 'function') {
        window.showTechDetail(techKey);
      }
    });
    card.addEventListener('keydown', event => {
      if (event.key !== 'Enter' && event.key !== ' ' && event.key !== 'Spacebar') {
        return;
      }
      const origin = event.target;
      if (typeof Element !== 'undefined' && origin instanceof Element && (origin.closest('a') || origin.closest('button'))) {
        return;
      }
      event.preventDefault();
      const techKey = card.getAttribute('data-tech-key');
      if (techKey && typeof window !== 'undefined' && typeof window.showTechDetail === 'function') {
        window.showTechDetail(techKey);
      }
    });
  });
}
