import guide from '../../data/route.chapters.json' assert { type: 'json' };
import dataset from '../../data/palworld_complete_data_final.json' assert { type: 'json' };
import itemDetails from '../../data/item_details.json' assert { type: 'json' };

const STORAGE_KEY = 'palmarathon:route:v1';
const PREFERENCES_KEY = 'palmarathon:route:prefs:v1';
const LINK_IMAGE_INDEX = buildLinkImageIndex(dataset, itemDetails);

export function renderRoute(node){
  const kidMode = isKidMode();
  const state = loadState();
  const preferences = loadPreferences();
  let hideOptional = !!preferences.hideOptional;
  const overview = calculateGuideOverview(guide.chapters, state);
  const openChapterIndex = (() => {
    if(overview.nextChapterId){
      const idx = guide.chapters.findIndex(ch => ch.id === overview.nextChapterId);
      if(idx >= 0) return idx;
    }
    if(overview.clearedChapters && overview.clearedChapters >= guide.chapters.length){
      return guide.chapters.length ? guide.chapters.length - 1 : 0;
    }
    return 0;
  })();
  const heroTitle = kidMode ? 'Family Adventure Route' : 'Adaptive Boss & Story Command Center';
  const heroLead = kidMode
    ? 'Track every big step together, highlight bonus adventures, and jump straight to the next win.'
    : 'Monitor chapter momentum, surface optional clean-up, and hop directly to the next required task.';

  node.innerHTML = `
    <div class="route-page route-page--modern">
      <section class="card route-dashboard" id="routeDashboard">
        <div class="route-dashboard__header">
          <div class="route-dashboard__titles">
            <span class="route-dashboard__eyebrow">${escapeHTML(kidMode ? 'Adventure campaign' : 'Boss & story route')}</span>
            <h2>${escapeHTML(heroTitle)}</h2>
            <p class="route-dashboard__lead">${escapeHTML(heroLead)}</p>
          </div>
          <div class="route-dashboard__actions">
            <button class="btn route-dashboard__action" id="toggleOptional">${optionalToggleLabel(hideOptional, kidMode)}</button>
          </div>
        </div>
        <div class="route-dashboard__stats">
          <div class="route-dashboard__stat">
            <span class="route-dashboard__stat-label">${escapeHTML(kidMode ? 'Chapters cleared' : 'Chapters complete')}</span>
            <strong class="route-dashboard__stat-value" data-route-overview="chapters">${overview.clearedChapters}/${overview.totalChapters}</strong>
            <p class="route-dashboard__stat-meta">${escapeHTML(kidMode ? 'Finish the required steps in a chapter to mark it as cleared.' : 'Complete every required step to finish a chapter.')}</p>
          </div>
          <div class="route-dashboard__stat">
            <span class="route-dashboard__stat-label">${escapeHTML(kidMode ? 'Required progress' : 'Required steps')}</span>
            <strong class="route-dashboard__stat-value" data-route-overview="required-count">${overview.requiredChecked}/${overview.requiredTotal}</strong>
            <div class="route-dashboard__progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${overview.requiredPct}">
              <span class="route-dashboard__progress-fill" data-route-overview="required-fill" style="width:${overview.requiredPct}%"></span>
            </div>
            <p class="route-dashboard__stat-meta" data-route-overview="required-summary">${escapeHTML(overview.requiredSummary)}</p>
          </div>
          <div class="route-dashboard__stat">
            <span class="route-dashboard__stat-label">${escapeHTML(kidMode ? 'Bonus progress' : 'Optional steps')}</span>
            <strong class="route-dashboard__stat-value" data-route-overview="optional-count">${overview.optionalChecked}/${overview.optionalTotal}</strong>
            <div class="route-dashboard__progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${overview.optionalPct}">
              <span class="route-dashboard__progress-fill route-dashboard__progress-fill--optional" data-route-overview="optional-fill" style="width:${overview.optionalPct}%"></span>
            </div>
            <p class="route-dashboard__stat-meta" data-route-overview="optional-summary">${escapeHTML(overview.optionalSummary)}</p>
          </div>
        </div>
        <div class="route-dashboard__next" data-route-overview="next">${escapeHTML(overview.nextLabel)}</div>
      </section>
      <div class="route-layout">
        <section class="card route-timeline" id="routeTimeline">
          <div class="route-timeline__header">
            <h3>${escapeHTML(kidMode ? 'Tonight’s roadmap' : 'Route timeline')}</h3>
            <p>${escapeHTML(kidMode ? 'Tap any chapter to jump to its checklist.' : 'Jump to a chapter or skim completion at a glance.')}</p>
          </div>
          <ol class="route-timeline__list" id="routeTimelineList"></ol>
        </section>
        <section class="route-chapter-stack" id="chapters"></section>
      </div>
    </div>
  `;

  const wrap = node.querySelector('#chapters');
  guide.chapters.forEach((ch, idx) => {
    const chapterEl = document.createElement('article');
    chapterEl.className = 'card route-chapter';
    chapterEl.id = `chapter-${ch.id}`;
    chapterEl.dataset.chapter = ch.id;
    chapterEl.dataset.index = String(idx);
    chapterEl.innerHTML = renderChapterInner(ch, idx, state, hideOptional, idx === openChapterIndex);
    wrap.appendChild(chapterEl);
  });

  const timeline = node.querySelector('#routeTimeline');
  if(timeline){
    timeline.addEventListener('click', (event) => {
      const origin = event.target;
      if(!(origin instanceof Element)) return;
      const anchor = origin.closest('[data-scroll-target]');
      if(!anchor) return;
      event.preventDefault();
      const targetId = anchor.dataset.scrollTarget;
      if(!targetId) return;
      const chapter = node.querySelector(`#${targetId}`);
      if(chapter){
        const details = chapter.querySelector('.route-chapter__details');
        if(details) details.open = true;
        chapter.scrollIntoView({ behavior: 'smooth', block: 'start' });
        pulse(chapter);
      }
    });
  }

  wrap.addEventListener('change', (e) => {
    if(e.target.matches('input[type=checkbox][data-step]')){
      const stepId = e.target.dataset.step;
      const checked = e.target.checked;
      state[stepId] = checked;
      saveState(state);
      const chapterNode = e.target.closest('.route-chapter');
      const chId = chapterNode ? chapterNode.dataset.chapter : null;
      const ch = guide.chapters.find(c => c.id === chId);
      if(ch){
        rerenderChapter(ch, state, node, hideOptional);
      }
      refreshGuideAnalytics(node, guide.chapters, state);
    }
  });

  wrap.addEventListener('click', (e) => {
    const origin = e.target;
    if(!(origin instanceof Element)) return;
    const stepAnchor = origin.closest('[data-link]');
    if(stepAnchor){
      const payload = JSON.parse(stepAnchor.dataset.link);
      navigateLink(payload);
      e.preventDefault();
    }
    const btn = e.target.closest('button[data-action]');
    if(!btn) return;
    const chId = btn.dataset.ch;
    const ch = guide.chapters.find(c=>c.id===chId);
    if(!ch) return;
    if(btn.dataset.action==='markRequired'){
      ch.steps.filter(s=>!s.optional).forEach(s=> state[s.id] = true);
      saveState(state);
      rerenderChapter(ch, state, node, hideOptional);
      refreshGuideAnalytics(node, guide.chapters, state);
    } else if(btn.dataset.action==='resetChapter'){
      ch.steps.forEach(s=> delete state[s.id]);
      saveState(state);
      rerenderChapter(ch, state, node, hideOptional);
      refreshGuideAnalytics(node, guide.chapters, state);
    }
  });

  const optionalButton = node.querySelector('#toggleOptional');
  if(optionalButton){
    optionalButton.addEventListener('click', () => {
      hideOptional = !hideOptional;
      preferences.hideOptional = hideOptional;
      savePreferences(preferences);
      optionalButton.textContent = optionalToggleLabel(hideOptional, isKidMode());
      optionalButton.setAttribute('aria-pressed', hideOptional ? 'true' : 'false');
      guide.chapters.forEach(ch => rerenderChapter(ch, state, node, hideOptional));
      refreshGuideAnalytics(node, guide.chapters, state);
    });
  }
  if(optionalButton){
    optionalButton.setAttribute('aria-pressed', hideOptional ? 'true' : 'false');
  }
  refreshGuideAnalytics(node, guide.chapters, state);
}

function renderChapterInner(ch, index, state, hideOptional, open){
  const kid = isKidMode();
  const progress = chapterProgress(ch, state);
  const optionalStats = chapterOptionalProgress(ch, state);
  const nextRequired = ch.steps.find(step => !step.optional && !state[step.id]);
  const nextOptional = ch.steps.find(step => step.optional && !state[step.id]);
  let summaryMeta;
  if(nextRequired){
    summaryMeta = kid
      ? `Next big step: ${stepText(nextRequired)}`
      : `Next required: ${stepText(nextRequired)}`;
  } else if(nextOptional && !hideOptional){
    summaryMeta = kid
      ? `Bonus idea: ${stepText(nextOptional)}`
      : `Next optional: ${stepText(nextOptional)}`;
  } else if(nextOptional && hideOptional){
    summaryMeta = kid ? 'Bonus steps hidden' : 'Optional steps hidden';
  } else {
    summaryMeta = kid ? 'Chapter complete' : 'Chapter complete';
  }
  const requiredLabel = kid
    ? `${progress.requiredChecked}/${progress.requiredCount} big step${progress.requiredCount === 1 ? '' : 's'} done`
    : `${progress.requiredChecked}/${progress.requiredCount} required complete`;
  const optionalLabel = optionalStats.optionalCount
    ? (kid
      ? `${optionalStats.optionalChecked}/${optionalStats.optionalCount} bonus cleared`
      : `${optionalStats.optionalChecked}/${optionalStats.optionalCount} optional complete`)
    : (kid ? 'No bonus steps' : 'No optional steps');
  const stepsHtml = renderSteps(ch, state, hideOptional);
  const stepsContent = stepsHtml || `<p class="route-steps-empty">${escapeHTML(kid ? 'All bonus steps are hidden.' : 'Optional steps are hidden. Show them to revisit bonus content.')}</p>`;
  return `
    <header class="route-chapter__header">
      <div class="route-chapter__titles">
        <span class="route-chapter__number">${String(index + 1).padStart(2, '0')}</span>
        <div class="route-chapter__text">
          <h3 class="route-chapter__title">${escapeHTML(chapterTitle(ch))}</h3>
          <p class="route-chapter__subtitle">${escapeHTML(chapterWhy(ch))}</p>
        </div>
      </div>
      <div class="route-chapter__progress">${renderProgress(progress)}</div>
    </header>
    <details class="route-chapter__details" ${open ? 'open' : ''}>
      <summary class="route-chapter__summary">
        <div class="route-chapter__summary-text">
          <span>${escapeHTML(kid ? 'Chapter checklist' : 'Chapter checklist')}</span>
          <span class="route-chapter__summary-meta">${escapeHTML(summaryMeta)}</span>
        </div>
        <span class="route-chapter__summary-toggle"><i class="fa-solid fa-chevron-down"></i></span>
      </summary>
      <div class="route-chapter__body">${stepsContent}</div>
      <footer class="route-chapter__footer">
        <div class="route-chapter__footer-meta">
          <span>${escapeHTML(requiredLabel)}</span>
          <span>${escapeHTML(optionalLabel)}</span>
        </div>
        <div class="route-chapter__footer-actions">
          <button class="btn" data-action="markRequired" data-ch="${ch.id}">${escapeHTML(kid ? 'Mark big steps done' : 'Mark required complete')}</button>
          <button class="btn btn--ghost" data-action="resetChapter" data-ch="${ch.id}">${escapeHTML(kid ? 'Restart chapter' : 'Reset chapter')}</button>
          ${progress.requiredDone ? `<span class="route-chapter__badge">${escapeHTML(kid ? 'Chapter complete!' : 'Chapter complete')}</span>` : ''}
        </div>
      </footer>
    </details>
  `;
}

function rerenderChapter(ch, state, node, hideOptional){
  const sec = node.querySelector(`#chapter-${ch.id}`);
  if(!sec) return;
  const details = sec.querySelector('.route-chapter__details');
  const wasOpen = details ? details.open : false;
  const index = Number(sec.dataset.index) || 0;
  sec.innerHTML = renderChapterInner(ch, index, state, hideOptional, wasOpen);
  if(wasOpen){
    const nextDetails = sec.querySelector('.route-chapter__details');
    if(nextDetails) nextDetails.open = true;
  }
}

function renderSteps(ch, state, hideOptional){
  const fragments = [];
  const kid = isKidMode();
  ch.steps.forEach(step=>{
    if(hideOptional && step.optional) return;
    const checked = !!state[step.id];
    const category = step.category || 'Task';
    const categorySlug = category.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'') || 'task';
    const optionalFlag = step.optional
      ? `<span class="step-flag">${escapeHTML(kid ? 'Bonus' : 'Optional')}</span>`
      : '';
    const links = renderLinks(step.links || []);
    const classes = ['step'];
    if(step.optional) classes.push('optional');
    if(checked) classes.push('step--checked');
    fragments.push(`
      <label class="${classes.join(' ')}">
        <input type="checkbox" data-step="${step.id}" ${checked ? 'checked' : ''} />
        <div class="step-content">
          <div class="step-header">
            <span class="step-category step-category--${categorySlug}">${escapeHTML(category)}</span>
            ${optionalFlag}
          </div>
          <p class="step-text">${escapeHTML(stepText(step))}</p>
          ${links}
        </div>
      </label>
    `);
  });
  if(!fragments.length) return '';
  return `<div class="step-list">${fragments.join('')}</div>`;
}

function renderProgress({requiredDone, requiredCount, requiredChecked}){
  const kid = isKidMode();
  const pct = requiredCount ? Math.round((requiredChecked / requiredCount) * 100) : 0;
  let label;
  if(requiredCount === 0){
    label = kid ? 'No big steps required' : 'No required steps';
  } else if(requiredDone){
    label = kid ? 'Big steps finished' : 'All required steps complete';
  } else {
    const noun = requiredCount === 1 ? (kid ? 'big step' : 'required step') : (kid ? 'big steps' : 'required steps');
    label = kid
      ? `${requiredChecked}/${requiredCount} ${noun} done`
      : `${requiredChecked}/${requiredCount} ${noun} complete`;
  }
  return `
    <div class="route-progress" data-role="chapter-progress">
      <div class="route-progress__bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}">
        <span class="route-progress__fill" style="width:${pct}%"></span>
      </div>
      <span class="route-progress__label">${escapeHTML(label)}</span>
    </div>
  `;
}

function chapterProgress(ch, state){
  const required = ch.steps.filter(s=>!s.optional);
  const requiredChecked = required.filter(s=> state[s.id]).length;
  return { requiredCount: required.length, requiredChecked, requiredDone: requiredChecked === required.length };
}

function chapterOptionalProgress(ch, state){
  const optional = ch.steps.filter(step => step.optional);
  const optionalChecked = optional.filter(step => state[step.id]).length;
  return { optionalCount: optional.length, optionalChecked };
}

function calculateGuideOverview(chapters, state){
  const kid = isKidMode();
  const totalChapters = Array.isArray(chapters) ? chapters.length : 0;
  let clearedChapters = 0;
  let requiredTotal = 0;
  let requiredChecked = 0;
  let optionalTotal = 0;
  let optionalChecked = 0;
  let nextChapter = null;
  let nextChapterOptionalFallback = null;
  let nextRequiredStep = null;
  let nextRequiredChapter = null;
  let nextOptionalStep = null;
  let nextOptionalChapter = null;

  if(Array.isArray(chapters)){
    chapters.forEach(ch => {
      if(!ch || !Array.isArray(ch.steps)) return;
      const progress = chapterProgress(ch, state);
      const optional = chapterOptionalProgress(ch, state);
      requiredTotal += progress.requiredCount;
      requiredChecked += progress.requiredChecked;
      optionalTotal += optional.optionalCount;
      optionalChecked += optional.optionalChecked;
      const hasOptionalRemaining = optional.optionalCount > optional.optionalChecked;
      if(!progress.requiredDone){
        if(!nextChapter){
          nextChapter = ch;
        }
      } else {
        clearedChapters += 1;
        if(hasOptionalRemaining && !nextChapterOptionalFallback){
          nextChapterOptionalFallback = ch;
        }
      }
      if(!nextRequiredStep){
        const candidate = ch.steps.find(step => !step.optional && !state[step.id]);
        if(candidate){
          nextRequiredStep = candidate;
          nextRequiredChapter = ch;
        }
      }
      if(!nextOptionalStep){
        const candidate = ch.steps.find(step => step.optional && !state[step.id]);
        if(candidate){
          nextOptionalStep = candidate;
          nextOptionalChapter = ch;
        }
      }
    });
  }

  const requiredPct = requiredTotal ? Math.round((requiredChecked / requiredTotal) * 100) : 0;
  const optionalPct = optionalTotal ? Math.round((optionalChecked / optionalTotal) * 100) : 0;

  const remainingRequired = Math.max(requiredTotal - requiredChecked, 0);
  const remainingOptional = Math.max(optionalTotal - optionalChecked, 0);

  let requiredSummary;
  if(requiredTotal === 0){
    requiredSummary = kid ? 'No big steps to track yet.' : 'No required steps to track yet.';
  } else if(remainingRequired === 0){
    requiredSummary = kid ? 'All big steps are complete.' : 'Every required step is complete.';
  } else {
    const noun = remainingRequired === 1 ? (kid ? 'big step' : 'required step') : (kid ? 'big steps' : 'required steps');
    requiredSummary = kid
      ? `${remainingRequired} ${noun} left`
      : `${remainingRequired} ${noun} remaining`;
  }

  let optionalSummary;
  if(optionalTotal === 0){
    optionalSummary = kid ? 'Bonus chores appear as you unlock them.' : 'Optional tasks appear when available.';
  } else if(remainingOptional === 0){
    optionalSummary = kid ? 'All bonus fun complete.' : 'Optional clean-up complete.';
  } else {
    const noun = remainingOptional === 1 ? (kid ? 'bonus step' : 'optional step') : (kid ? 'bonus steps' : 'optional steps');
    optionalSummary = kid
      ? `${remainingOptional} ${noun} to explore`
      : `${remainingOptional} ${noun} remaining`;
  }

  if(!nextChapter && nextChapterOptionalFallback){
    nextChapter = nextChapterOptionalFallback;
  }

  let nextLabel;
  let nextChapterId = nextChapter?.id || null;
  const nextStep = nextRequiredStep || nextOptionalStep;
  if(nextStep && nextStep.optional && nextOptionalChapter && !nextChapterId){
    nextChapterId = nextOptionalChapter.id || null;
  }
  if(nextStep && !nextStep.optional && nextRequiredChapter){
    nextChapterId = nextRequiredChapter.id || nextChapterId;
  }
  if(totalChapters === 0){
    nextLabel = kid ? 'No chapters available yet.' : 'No chapters available yet.';
  } else if(nextStep){
    const prefix = nextStep.optional
      ? (kid ? 'Bonus idea' : 'Next optional step')
      : (kid ? 'Next big step' : 'Next required step');
    nextLabel = `${prefix}: ${stepText(nextStep)}`;
    if(nextChapter && nextChapter.id){
      nextChapterId = nextChapter.id;
    }
  } else if(clearedChapters === totalChapters){
    nextLabel = kid ? 'All chapters complete! Celebrate with your crew.' : 'All chapters complete—legendary work.';
  } else if(nextChapter && nextChapter.id){
    nextChapterId = nextChapter.id;
    nextLabel = kid
      ? `Begin ${chapterTitle(nextChapter)}`
      : `Begin ${chapterTitle(nextChapter)}`;
  } else {
    nextLabel = kid ? 'Pick a chapter to begin.' : 'Choose a chapter to begin.';
  }

  return {
    totalChapters,
    clearedChapters,
    requiredTotal,
    requiredChecked,
    optionalTotal,
    optionalChecked,
    requiredPct,
    optionalPct,
    requiredSummary,
    optionalSummary,
    nextLabel,
    nextChapterId
  };
}

function refreshGuideAnalytics(node, chapters, state){
  const overview = calculateGuideOverview(chapters, state);
  updateOverview(node, overview);
  renderTimeline(node, chapters, state, overview.nextChapterId);
  return overview;
}

function updateOverview(node, overview){
  const setText = (key, value) => {
    const el = node.querySelector(`[data-route-overview="${key}"]`);
    if(el) el.textContent = value;
  };
  setText('chapters', `${overview.clearedChapters}/${overview.totalChapters}`);
  setText('required-count', `${overview.requiredChecked}/${overview.requiredTotal}`);
  setText('optional-count', `${overview.optionalChecked}/${overview.optionalTotal}`);
  setText('required-summary', overview.requiredSummary);
  setText('optional-summary', overview.optionalSummary);
  setText('next', overview.nextLabel);
  const requiredFill = node.querySelector('[data-route-overview="required-fill"]');
  if(requiredFill){
    requiredFill.style.width = `${overview.requiredPct}%`;
    const bar = requiredFill.parentElement;
    if(bar && bar.setAttribute){
      bar.setAttribute('aria-valuenow', String(overview.requiredPct));
    }
  }
  const optionalFill = node.querySelector('[data-route-overview="optional-fill"]');
  if(optionalFill){
    optionalFill.style.width = `${overview.optionalPct}%`;
    const bar = optionalFill.parentElement;
    if(bar && bar.setAttribute){
      bar.setAttribute('aria-valuenow', String(overview.optionalPct));
    }
  }
}

function renderTimeline(node, chapters, state, activeChapterId){
  const list = node.querySelector('#routeTimelineList');
  if(!list) return;
  if(!Array.isArray(chapters) || !chapters.length){
    list.innerHTML = `<li class="route-timeline__empty">${escapeHTML(isKidMode() ? 'Routes will appear here soon.' : 'Routes will appear here soon.')}</li>`;
    return;
  }
  list.innerHTML = chapters.map((ch, idx) => renderTimelineEntry(ch, idx, state, activeChapterId)).join('');
}

function renderTimelineEntry(ch, index, state, activeChapterId){
  const classes = ['route-timeline__item'];
  const progress = chapterProgress(ch, state);
  const optional = chapterOptionalProgress(ch, state);
  if(progress.requiredDone) classes.push('route-timeline__item--complete');
  if(activeChapterId && activeChapterId === ch.id) classes.push('route-timeline__item--active');
  const kid = isKidMode();
  const requiredStatus = progress.requiredDone
    ? (kid ? 'Complete' : 'Complete')
    : `${progress.requiredChecked}/${progress.requiredCount || 0} ${kid ? 'big' : 'required'}`;
  const optionalStatus = optional.optionalCount
    ? `${optional.optionalChecked}/${optional.optionalCount} ${kid ? 'bonus' : 'optional'}`
    : '';
  const meta = optionalStatus ? `${requiredStatus} • ${optionalStatus}` : requiredStatus;
  const pct = progress.requiredCount
    ? Math.round((progress.requiredChecked / progress.requiredCount) * 100)
    : 0;
  return `
    <li class="${classes.join(' ')}">
      <button type="button" class="route-timeline__anchor" data-scroll-target="chapter-${ch.id}">
        <span class="route-timeline__step">${String(index + 1).padStart(2, '0')}</span>
        <span class="route-timeline__title">${escapeHTML(chapterTitle(ch))}</span>
        <span class="route-timeline__meta">${escapeHTML(meta)}</span>
        <span class="route-timeline__progress" aria-hidden="true">
          <span class="route-timeline__progress-fill" style="width:${pct}%"></span>
        </span>
      </button>
    </li>
  `;
}

function renderLinks(links){
  if(!links || !links.length) return '';
  return `<div class="step-links badges">${links.map(l=>{
    const label = linkLabel(l);
    const safeLabel = escapeHTML(label);
    const payload = escapeHTML(JSON.stringify(l));
    const typeToken = linkTypeToken(l?.type);
    const typeAttr = typeToken ? ` data-link-type="${typeToken}"` : '';
    const titleAttr = label ? ` title="${safeLabel}"` : '';
    const image = findLinkImage(l);
    const classes = ['chip', 'link'];
    if(image) classes.push('link--with-thumb');
    const thumb = image
      ? `<span class="chip__thumb"><img src="${escapeHTML(image)}" alt="${safeLabel}" loading="lazy" decoding="async" referrerpolicy="no-referrer"></span>`
      : '';
    return `<a href="#" class="${classes.join(' ')}" data-link="${payload}"${typeAttr}${titleAttr} role="button">${thumb}<span class="chip__label">${safeLabel}</span></a>`;
  }).join('')}</div>`;
}

function optionalToggleLabel(hidden, kid){
  if(kid) return hidden ? 'Show bonus steps' : 'Hide bonus steps';
  return hidden ? 'Show Optional' : 'Hide Optional';
}

function chapterTitle(ch){
  const kid = isKidMode();
  if(kid) return ch.titleKid || ch.title || '';
  if(ch.title) return ch.title;
  return ch.titleKid || '';
}

function chapterWhy(ch){
  const kid = isKidMode();
  if(kid) return ch.whyKid || ch.why || '';
  if(ch.why) return ch.why;
  return ch.whyKid || '';
}

function stepText(step){
  const kid = isKidMode();
  if(!kid && step.textAdult) return step.textAdult;
  if(kid) return step.textKid || step.text || '';
  return step.text || step.textKid || '';
}

function isKidMode(){
  return document.body.classList.contains('kid-mode');
}

function linkLabel(l){
  if(!l) return 'Open';
  if(l.label) return String(l.label);
  const id = l.id || l.slug || l.name;
  if(l.type==='pal'){
    const source = l.name || l.slug || id;
    return capitalize(source);
  }
  if(l.type==='item') return niceName(id || l.label || 'item');
  if(l.type==='tech') return techName(id || l.label || 'tech');
  if(l.type==='passive') return capitalize(id || l.label || 'passive');
  if(l.type==='move') return niceName(id || l.label || 'move');
  if(l.type==='glossary') return niceName(id || l.label || 'entry');
  if(l.type==='tower'){
    if(l.map && l.map.title) return l.map.title;
    return niceName(id || 'tower');
  }
  if(id) return niceName(id);
  return 'Open';
}

function findLinkImage(link){
  if(!link) return null;
  if(link.image && typeof link.image === 'string') return link.image;
  const candidates = [];
  if(link.id != null) candidates.push(link.id);
  if(link.slug != null) candidates.push(link.slug);
  if(link.name) candidates.push(link.name);
  if(link.label) candidates.push(link.label);
  if(link.type === 'pal' && link.key) candidates.push(link.key);
  const seen = new Set();
  for(const candidate of candidates){
    if(candidate == null) continue;
    const raw = String(candidate);
    if(!raw) continue;
    if(!seen.has(raw)){
      seen.add(raw);
      const direct = LINK_IMAGE_INDEX.get(raw);
      if(direct) return direct;
    }
    const normalized = normalizeLinkKey(raw);
    if(normalized && !seen.has(normalized)){
      seen.add(normalized);
      const mapped = LINK_IMAGE_INDEX.get(normalized);
      if(mapped) return mapped;
    }
  }
  return null;
}

function normalizeLinkKey(value){
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

function buildLinkImageIndex(primaryDataset, detailDataset){
  const map = new Map();
  const register = (key, url) => {
    if(!key || !url) return;
    const raw = String(key);
    if(raw && !map.has(raw)){
      map.set(raw, url);
    }
    const normalized = normalizeLinkKey(raw);
    if(normalized && !map.has(normalized)){
      map.set(normalized, url);
    }
  };
  const stack = [];
  if(primaryDataset) stack.push(primaryDataset);
  if(detailDataset) stack.push(detailDataset);
  while(stack.length){
    const current = stack.pop();
    if(!current) continue;
    if(Array.isArray(current)){
      for(let i = 0; i < current.length; i += 1){
        stack.push(current[i]);
      }
      continue;
    }
    if(typeof current === 'object'){
      const image = typeof current.image === 'string' && current.image
        ? current.image
        : (typeof current.icon === 'string' ? current.icon : null);
      if(image){
        if(current.id != null) register(current.id, image);
        if(current.key != null) register(current.key, image);
        if(current.slug) register(current.slug, image);
        if(current.name) register(current.name, image);
      }
      for(const key of Object.keys(current)){
        const child = current[key];
        if(child && typeof child === 'object'){
          stack.push(child);
        }
      }
    }
  }
  return map;
}

// --- Navigation glue to existing pages/modals ---
function navigateLink(l){
  if(!l) return;
  if(l.type==='pal'){
    const target = l.slug || l.id || l.name;
    if(target && typeof window.viewPal === 'function') window.viewPal(target);
    else if(target) focusSearch(target, { target: 'pals' });
  } else if(l.type==='tech'){
    const techId = l.id || l.slug || l.name;
    if(techId && typeof window.showTechDetail === 'function') window.showTechDetail(techId);
    else if(l.url) window.open(l.url, '_blank', 'noopener');
    else if(techId) focusSearch(niceName(techId), { target: 'items' });
  } else if(l.type==='item'){
    const itemKey = normalizeItemKey(l);
    const searchTerm = l.name || l.label || (itemKey ? niceName(itemKey) : '');
    if(itemKey && typeof window.openItemDetail === 'function'){
      window.openItemDetail(itemKey);
    } else if(itemKey){
      focusSearch(searchTerm || itemKey, { target: 'items' });
    } else if(l.url){
      window.open(l.url, '_blank', 'noopener');
    } else if(searchTerm){
      focusSearch(searchTerm, { target: 'items' });
    }
  } else if(l.type==='passive'){
    const trait = capitalize(l.id || l.slug || '');
    if(typeof window.showTraitDetail === 'function') window.showTraitDetail(trait);
    else if(trait) focusSearch(trait, { target: 'pals' });
  } else if(l.type==='move'){
    if(typeof window.showSkillDetail === 'function') window.showSkillDetail(l.id);
    else if(l.id) focusSearch(niceName(l.id), { target: 'pals' });
  } else if(l.type==='glossary'){
    const key = l.id || l.slug;
    if(typeof window.showGlossaryDetail === 'function' && key) window.showGlossaryDetail(key);
    else if(l.url) window.open(l.url, '_blank', 'noopener');
    else if(key) focusSearch(niceName(key), { target: 'items' });
  } else if(l.type==='tower'){
    if(typeof window.openTowerMap === 'function') window.openTowerMap(l);
    else if(l.url) window.open(l.url, '_blank', 'noopener');
    else if(l.map && l.map.url) window.open(l.map.url, '_blank', 'noopener');
  } else if(l.url){
    window.open(l.url, '_blank', 'noopener');
  }
}

function linkTypeToken(type){
  if(!type) return '';
  return String(type).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'');
}

function normalizeItemKey(link){
  if(!link) return '';
  const candidates = [];
  if(link.id != null) candidates.push(link.id);
  if(link.slug != null) candidates.push(link.slug);
  if(link.name) candidates.push(link.name);
  if(link.label) candidates.push(link.label);
  for(const candidate of candidates){
    if(candidate == null) continue;
    const raw = String(candidate).trim();
    if(!raw) continue;
    const normalized = raw
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/(^_|_$)/g, '');
    if(normalized) return normalized;
  }
  return '';
}

function pulse(el){
  el.classList.add('pulse');
  setTimeout(()=>el.classList.remove('pulse'), 1500);
}

function focusSearch(q, options){
  if(typeof window.focusSearch === 'function'){
    window.focusSearch(q, options);
    return;
  }
  const target = options?.target === 'items' ? 'items' : 'pals';
  const input = document.getElementById(target === 'items' ? 'itemSearch' : 'palSearch');
  if(input){
    input.value = q;
    input.dispatchEvent(new Event('input', {bubbles:true}));
  }
}

// --- Storage helpers ---
function loadState(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
  catch(e){ return {}; }
}
function saveState(s){ localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); }

function loadPreferences(){
  try {
    const stored = JSON.parse(localStorage.getItem(PREFERENCES_KEY));
    if(stored && typeof stored === 'object'){
      return { hideOptional: !!stored.hideOptional };
    }
  } catch(e){ /* ignore */ }
  return { hideOptional: false };
}

function savePreferences(prefs){
  try {
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify({ hideOptional: !!prefs.hideOptional }));
  } catch(e){ /* ignore */ }
}

// --- Small helpers ---
function escapeHTML(s){ return (s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function capitalize(s){ return (s||'').replace(/(^|-|_)\w/g, m=>m.toUpperCase()).replace(/[-_]/g,' '); }
function niceName(id){ return capitalize(String(id).replace(/_/g,' ')); }
function techName(id){ return niceName(id); }
export function resetRouteProgress(node){
  if(!node) return;
  if(confirm('Reset all guide progress?')){
    localStorage.removeItem(STORAGE_KEY);
    renderRoute(node);
  }
}
