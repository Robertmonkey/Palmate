import guide from '../../data/route.chapters.json' assert { type: 'json' };

const STORAGE_KEY = 'palmarathon:route:v1';

export function renderRoute(node){
  node.innerHTML = `
    <section class="card">
      <h2>Boss Route & Progress</h2>
      <p>Work through each chapter. Check off steps as you do them. <em>Optional</em> steps don’t block completion.</p>
      <div class="badges" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
        <button class="btn" id="toggleOptional">Hide Optional</button>
        <button class="btn" id="resetAll">Reset All</button>
      </div>
    </section>
    <div id="chapters"></div>
  `;
  const wrap = node.querySelector('#chapters');
  const state = loadState();
  let hideOptional = false;

  // Build chapter accordions
  guide.chapters.forEach((ch, idx) => {
    const chapterEl = document.createElement('section');
    chapterEl.className = 'card';
    chapterEl.id = `chapter-${ch.id}`;
    const progress = chapterProgress(ch, state);
    chapterEl.innerHTML = `
      <div style="display:flex;align-items:center;gap:12px;justify-content:space-between;flex-wrap:wrap">
        <div>
          <h3 style="margin:0">${escapeHTML(ch.title)}</h3>
          <p style="margin:.25rem 0;color:var(--muted)">${escapeHTML(ch.why)}</p>
        </div>
        <div style="min-width:220px">
          ${renderProgress(progress)}
        </div>
      </div>
      <details ${idx===0 ? 'open' : ''}>
        <summary class="btn" style="margin-top:8px">Open steps</summary>
        ${renderSteps(ch, state, hideOptional)}
        <div style="display:flex;gap:8px;margin-top:12px">
          <button class="btn" data-action="markRequired" data-ch="${ch.id}">Mark Required Complete</button>
          <button class="btn" data-action="resetChapter" data-ch="${ch.id}">Reset Chapter</button>
          ${progress.requiredDone ? `<span style="margin-left:auto">✅ Chapter Complete</span>` : ''}
        </div>
      </details>
    `;
    wrap.appendChild(chapterEl);
  });

  // Delegated events
  wrap.addEventListener('change', (e) => {
    if(e.target.matches('input[type=checkbox][data-step]')){
      const stepId = e.target.dataset.step;
      const checked = e.target.checked;
      state[stepId] = checked;
      saveState(state);
      // Update chapter progress bar
      const chId = e.target.closest('section.card').id.replace('chapter-','');
      const ch = guide.chapters.find(c=>c.id===chId);
      const prog = chapterProgress(ch, state);
      e.target.closest('section.card').querySelector('.progress').outerHTML = renderProgress(prog);
    }
  });

  wrap.addEventListener('click', (e) => {
    const stepAnchor = e.target.closest('[data-link]');
    if(stepAnchor){
      const payload = JSON.parse(stepAnchor.dataset.link);
      navigateLink(payload);
      e.preventDefault();
    }
    const btn = e.target.closest('button[data-action]');
    if(!btn) return;
    const chId = btn.dataset.ch;
    const ch = guide.chapters.find(c=>c.id===chId);
    if(btn.dataset.action==='markRequired'){
      ch.steps.filter(s=>!s.optional).forEach(s=> state[s.id] = true);
      saveState(state);
      rerenderChapter(ch, state, node, hideOptional);
    } else if(btn.dataset.action==='resetChapter'){
      ch.steps.forEach(s=> delete state[s.id]);
      saveState(state);
      rerenderChapter(ch, state, node, hideOptional);
    }
  });

  node.querySelector('#toggleOptional').onclick = ()=>{
    hideOptional = !hideOptional;
    node.querySelector('#toggleOptional').textContent = hideOptional ? 'Show Optional' : 'Hide Optional';
    // Rerender all chapters with the new optional filter
    guide.chapters.forEach(ch => rerenderChapter(ch, state, node, hideOptional));
  };
  node.querySelector('#resetAll').onclick = ()=>{
    if(confirm('Reset ALL progress?')){
      localStorage.removeItem(STORAGE_KEY);
      renderRoute(node);
    }
  };
}

function rerenderChapter(ch, state, node, hideOptional){
  const sec = node.querySelector(`#chapter-${ch.id}`);
  const detailsWasOpen = sec.querySelector('details').open;
  const progress = chapterProgress(ch, state);
  sec.innerHTML = `
    <div style="display:flex;align-items:center;gap:12px;justify-content:space-between;flex-wrap:wrap">
      <div>
        <h3 style="margin:0">${escapeHTML(ch.title)}</h3>
        <p style="margin:.25rem 0;color:var(--muted)">${escapeHTML(ch.why)}</p>
      </div>
      <div style="min-width:220px">${renderProgress(progress)}</div>
    </div>
    <details ${detailsWasOpen ? 'open' : ''}>
      <summary class="btn" style="margin-top:8px">Open steps</summary>
      ${renderSteps(ch, state, hideOptional)}
      <div style="display:flex;gap:8px;margin-top:12px">
        <button class="btn" data-action="markRequired" data-ch="${ch.id}">Mark Required Complete</button>
        <button class="btn" data-action="resetChapter" data-ch="${ch.id}">Reset Chapter</button>
        ${progress.requiredDone ? `<span style="margin-left:auto">✅ Chapter Complete</span>` : ''}
      </div>
    </details>
  `;
}

function renderSteps(ch, state, hideOptional){
  const cats = ['Base','Gear','Tech','Catch','Prep','Explore','Boss'];
  const groups = {};
  cats.forEach(c=>groups[c]=[]);
  ch.steps.forEach(step=>{
    if(hideOptional && step.optional) return;
    const checked = !!state[step.id];
    groups[step.category] ??= [];
    groups[step.category].push(`
      <label class="step ${step.optional?'optional':''}">
        <input type="checkbox" data-step="${step.id}" ${checked?'checked':''} />
        <span class="step-text">${escapeHTML(step.text)} ${step.optional?'<em>(Optional)</em>':''}</span>
        ${renderLinks(step.links||[])}
      </label>
    `);
  });
  return Object.entries(groups).filter(([,items])=>items.length).map(([cat, items])=>`
    <div class="step-group">
      <h4>${cat}</h4>
      ${items.join('')}
    </div>
  `).join('');
}

function renderProgress({requiredDone, requiredCount, requiredChecked}){
  const pct = requiredCount ? Math.round((requiredChecked/requiredCount)*100) : 0;
  return `
    <div class="progress" aria-label="Chapter progress" style="display:grid;gap:6px">
      <div style="height:10px;border-radius:999px;background:#22314A;overflow:hidden">
        <div style="height:10px;width:${pct}%;background:var(--accent)"></div>
      </div>
      <div style="font-size:.9rem;color:var(--muted)">${requiredChecked}/${requiredCount} required done (${pct}%)</div>
    </div>
  `;
}

function chapterProgress(ch, state){
  const required = ch.steps.filter(s=>!s.optional);
  const requiredChecked = required.filter(s=> state[s.id]).length;
  return { requiredCount: required.length, requiredChecked, requiredDone: requiredChecked === required.length };
}

function renderLinks(links){
  if(!links || !links.length) return '';
  return `<span class="badges">${links.map(l=>{
    const label = linkLabel(l);
    const payload = JSON.stringify(l).replace(/"/g,'&quot;');
    return `<a href="#" class="chip link" data-link="${payload}" role="button">${escapeHTML(label)}</a>`;
  }).join('')}</span>`;
}

function linkLabel(l){
  if(l.type==='pal') return capitalize(l.slug);
  if(l.type==='passive') return capitalize(l.id);
  if(l.type==='move') return niceName(l.id);
  if(l.type==='tech') return techName(l.id);
  if(l.type==='glossary') return niceName(l.id);
  if(l.type==='tower') return niceName(l.id);
  return 'Open';
}

// --- Navigation glue to existing pages/modals ---
function navigateLink(l){
  if(l.type==='pal'){
    // Go to Pals page and try to open modal if available
    document.querySelector('[data-page="pals"]').click();
    if(window.viewPal) window.viewPal(l.slug);
    else focusSearch(l.slug);
  } else if(l.type==='tech'){
    document.querySelector('[data-page="tech"]').click();
    // try to scroll to a card with id `tech-${id}`
    setTimeout(()=>{
      const el = document.getElementById(`tech-${l.id}`);
      if(el){ pulse(el); el.scrollIntoView({behavior:'smooth', block:'center'}); }
    }, 60);
  } else if(l.type==='passive'){
    document.querySelector('[data-page="glossary"]').click();
    setTimeout(()=>{
      const el = document.getElementById(`passive-${l.id}`);
      if(el){ pulse(el); el.scrollIntoView({behavior:'smooth', block:'center'}); }
      else focusSearch(l.id);
    }, 60);
  } else if(l.type==='move'){
    document.querySelector('[data-page="glossary"]').click();
    setTimeout(()=>{
      const el = document.getElementById(`move-${l.id}`);
      if(el){ pulse(el); el.scrollIntoView({behavior:'smooth', block:'center'}); }
      else focusSearch(niceName(l.id));
    }, 60);
  } else if(l.type==='glossary'){
    document.querySelector('[data-page="glossary"]').click();
  } else if(l.type==='tower'){
    // External map (safe deep-link placeholder)
    window.open(l.url || 'https://palworld.gg/map', '_blank', 'noopener');
  }
}

function pulse(el){
  el.classList.add('pulse');
  setTimeout(()=>el.classList.remove('pulse'), 1500);
}

function focusSearch(q){
  const input = document.querySelector('#q');
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

// --- Small helpers ---
function escapeHTML(s){ return (s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function capitalize(s){ return (s||'').replace(/(^|-|_)\w/g, m=>m.toUpperCase()).replace(/[-_]/g,' '); }
function niceName(id){ return capitalize(String(id).replace(/_/g,' ')); }
function techName(id){ return niceName(id); }
