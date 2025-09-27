import tech from '../../data/tech.sample.json' assert { type:'json' };
export function renderTech(node){
  node.innerHTML = `<h2>Technology</h2>` + tech.map(t=>`
    <div class="card" id="tech-${t.id}">
      <strong>Lv ${t.level}</strong> — ${t.name}
    </div>
  `).join('');
}
