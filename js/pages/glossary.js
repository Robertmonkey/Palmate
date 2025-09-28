import passives from '../../data/passives.sample.json' assert { type:'json' };

const escapeHTML = (value) => String(value ?? '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;');

export function renderGlossary(node){
  if(!node) return;

  const passiveButtons = passives.map((p) => {
    const id = p?.id ?? '';
    const name = p?.name ?? id;
    const payload = escapeHTML(JSON.stringify({ id, name }));
    return `<button id="passive-${escapeHTML(id)}" class="chip passive" data-passive='${payload}'>${escapeHTML(name)}</button>`;
  }).join('');

  node.innerHTML = `<h2>Glossary</h2>
  <div class="card"><h3>Passives</h3>
    <div class="badges">
      ${passiveButtons}
    </div>
  </div>
  <div class="card"><h3>Elements</h3><p>Fire, Water, Ice, Electric, Ground, Grass, Dark, Dragon, Neutral.</p></div>`;

  node.querySelectorAll('.chip.passive').forEach((btn) => {
    btn.addEventListener('click', () => {
      let info = null;
      const raw = btn.getAttribute('data-passive');
      if(raw){
        try { info = JSON.parse(raw); }
        catch (err) { info = null; }
      }
      const traitName = info?.name || btn.textContent.trim();
      const traitId = info?.id || traitName;
      if(typeof window.showTraitDetail === 'function'){
        window.showTraitDetail(traitName);
      } else if(typeof window.showGlossaryDetail === 'function'){
        window.showGlossaryDetail(traitId);
      } else if(typeof window.focusSearch === 'function'){
        window.focusSearch(traitName);
      }
    });
  });
}
