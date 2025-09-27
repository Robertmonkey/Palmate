import passives from '../../data/passives.sample.json' assert { type:'json' };
export function renderGlossary(node){
  node.innerHTML = `<h2>Glossary</h2>
  <div class="card"><h3>Passives</h3>
    <div class="badges">
      ${passives.map(p=>`<button id="passive-${p.id}" class="chip passive" onclick='window.passive("${p.id}")'>${p.name}</button>`).join('')}
    </div>
  </div>
  <div class="card"><h3>Elements</h3><p>Fire, Water, Ice, Electric, Ground, Grass, Dark, Dragon, Neutral.</p></div>`;
}
