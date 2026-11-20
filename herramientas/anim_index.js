// Genera anim-index.js: la lista de animaciones (ids, fichas y nombres) que la app necesita al abrir,
// para cargar anim.js (≈ 145 KB) recién cuando se muestra una animación.
// Correlo después de cambiar anim.js:  node herramientas/anim_index.js
const fs = require('fs'), path = require('path');
const raiz = path.join(__dirname, '..');
global.window = {}; global.document = {};
require(path.join(raiz, 'anim.js'));
const W = global.window, label = {};
for (const k of W.ANIM_IDS) label[k] = W.animLabel(k);
const out = `// Generado por herramientas/anim_index.js a partir de anim.js: no editar a mano.
window.ANIM_IDS = ${JSON.stringify(W.ANIM_IDS)};
window.ANIM_FOR = ${JSON.stringify(W.ANIM_FOR)};
window.ANIM_LABEL = ${JSON.stringify(label)};
window.animLabel = k => window.ANIM_LABEL[k] || k;
// anim.js se carga la primera vez que hay que mostrar una animación y reemplaza esta función por la real
(function () {
  let carga = null;
  const cargar = () => carga || (carga = new Promise((ok, mal) => { const s = document.createElement('script'); s.src = 'anim.js'; s.onload = ok; s.onerror = () => { carga = null; mal(); }; document.head.appendChild(s); }));
  window.mountAnims = r => { if (!r || !r.querySelector('.anim[data-anim]')) return; cargar().then(() => window.mountAnims(r)).catch(() => {}); };
})();
`;
fs.writeFileSync(path.join(raiz, 'anim-index.js'), out);
console.log(W.ANIM_IDS.length + ' animaciones; anim-index.js ' + Math.round(out.length / 1024) + ' KB');
