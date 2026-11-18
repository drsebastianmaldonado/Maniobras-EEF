// Animaciones de maniobras: esquema del circuito + trazado intracavitario, sincronizados con un mismo reloj.
// Cada animación tiene dos paneles (una alternativa contra la otra). Los tiempos son ilustrativos.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const mk = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };

  // Puntos del esquema (viewBox 0 0 310 400; el esquema ocupa y 0–255 y el trazado y 265–395)
  const G = { hra: [70, 44], aSep: [150, 80], apA: [264, 80], node: [150, 102], his: [150, 128], apex: [124, 222], base: [264, 152], rva: [118, 228], focus: [74, 44] };

  // ---------- Escenarios ----------
  // Cada uno devuelve { ev: eventos del trazado, wv: frentes que se mueven, flA / flV: activaciones para iluminar cámaras, ... }
  function travVop() {
    const LC = 340, VA = 110, AH = 185, HV = 45, SC = 300, ev = [], wv = [], flA = [], flV = [];
    const ante = (a, ah, stop) => { const h = a + ah; ev.push({ ch: 'His', t: h, l: 'H' }); wv.push({ c: 'ante', pts: stop ? [[G.aSep, a], [G.node, a + 30], [G.his, h]] : [[G.aSep, a], [G.node, a + 30], [G.his, h], [G.apex, h + HV]] }); if (!stop) { ev.push({ ch: 'VD', t: h + HV, l: 'V' }); flV.push(h + HV); } return h + HV; };
    const retro = (v, sa, from) => { const a = v + sa; wv.push({ c: 'retro', pts: [[from, v], [G.base, v + (sa - 70)], [G.apA, a]] }); ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a); return a; };
    // taquicardia
    let a = 170; ev.push({ ch: 'VD', t: 60, l: 'V' }); flV.push(60); wv.push({ c: 'retro', pts: [[G.apex, 60], [G.base, 100], [G.apA, a]] }); ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a);
    let v = ante(a, AH); a = retro(v, VA, G.apex);
    ante(a, AH, true);                             // la A siguiente baja hasta el His y choca con la estimulación
    const S = [700, 1000, 1300, 1600, 1900];
    S.forEach((s, i) => {
      ev.push({ ch: 'VD', t: s, l: 'E', stim: true }); flV.push(s);
      a = retro(s, 150, G.rva);
      if (i < S.length - 1) ante(a, AH + 5, true);
    });
    const lastA = a;
    ev.find(e => e.t === lastA && e.ch === 'AD').tag = 'última A acelerada';
    v = ante(lastA, AH + 10);                     // el último A conduce al V: A-V
    a = retro(v, VA, G.apex); v = ante(a, AH); retro(v, VA, G.apex);
    return { title: 'TRAV (o TRNAV): respuesta A-V', ap: true, ev, wv, flA, flV, stimEnd: 1900, verdictT: lastA + AH + 10 + HV,
      verdict: 'Después de la última A acelerada viene un V: <b>A-V</b>. Excluye la TA.',
      why: 'La A estimulada viajó por el circuito (V → vía → A) y sigue bajando por el nodo: la taquicardia continúa con el V.' };
  }

  function taVop() {
    const LC = 340, AH = 120, HV = 45, ev = [], wv = [], flA = [], flV = [];
    const focusBeat = (a, stop) => {
      ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a);
      wv.push({ c: 'focus', pts: [[G.focus, a], [G.aSep, a + 35]] });
      const h = a + AH; ev.push({ ch: 'His', t: h, l: 'H' });
      wv.push({ c: 'ante', pts: stop ? [[G.aSep, a + 35], [G.node, a + 60], [G.his, h]] : [[G.aSep, a + 35], [G.node, a + 60], [G.his, h], [G.apex, h + HV]] });
      if (!stop) { ev.push({ ch: 'VD', t: h + HV, l: 'V' }); flV.push(h + HV); }
    };
    focusBeat(60); focusBeat(400); focusBeat(740, true);
    const S = [860, 1160, 1460, 1760, 2060];
    let lastA = 0;
    S.forEach(s => {
      ev.push({ ch: 'VD', t: s, l: 'E', stim: true }); flV.push(s);
      const h = s + 60, a = s + 160;
      ev.push({ ch: 'His', t: h, l: 'H' }); ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a);
      wv.push({ c: 'retro', pts: [[G.rva, s], [G.his, h], [G.node, a - 25], [G.aSep, a]] });
      lastA = a;
    });
    ev.find(e => e.t === lastA && e.ch === 'AD').tag = 'última A acelerada';
    const f1 = lastA + 360;                       // el foco vuelve a disparar: A-A
    focusBeat(f1); focusBeat(f1 + LC);
    Object.assign(ev.find(e => e.t === f1 && e.ch === 'AD'), { tag: 'otra A (foco)', tagUp: true });
    return { title: 'TA: respuesta A-A-V', focus: true, ev, wv, flA, flV, stimEnd: 2060, verdictT: f1 + AH + HV,
      verdict: 'Después de la última A acelerada viene <b>otra A</b> y recién después el V: <b>A-A-V</b>. Es TA.',
      why: 'La A estimulada subió por el nodo y no puede volver a bajar. La taquicardia sigue porque el foco auricular dispara de nuevo.' };
  }

  const ANIMS = {
    vop: { t: 'Sobreestimulación ventricular: A-V vs A-A-V', dur: 3250, panels: [travVop, taVop],
      fases: [[0, 'Taquicardia (LC 340 ms). Mirá el circuito en el esquema y las A, H y V en el trazado.'],
              [690, 'Estimulación del VD a 300 ms (E): cada estímulo llega a la aurícula y las A se aceleran a 300.'],
              [2100, 'Se corta la estimulación. Mirá qué sigue a la <b>última A acelerada</b>.']] }
  };

  // ---------- Dibujo ----------
  const COL = { ante: 'var(--orange)', retro: 'var(--violet)', focus: 'var(--rose)' };
  function drawHeart(svg, sc) {
    const g = mk('g', {}, svg);
    const atr = mk('rect', { x: 20, y: 16, width: 272, height: 78, rx: 30, fill: 'var(--blue-soft)', stroke: 'var(--line)', 'stroke-width': 1.5 }, g);
    mk('text', { x: 30, y: 88, 'font-size': 11, fill: 'var(--ink2)' }, g).textContent = 'Aurículas';
    const ven = mk('path', { d: 'M30 142 Q34 252 156 254 Q284 252 292 142 Z', fill: 'var(--blue-soft)', stroke: 'var(--line)', 'stroke-width': 1.5 }, g);
    mk('text', { x: 200, y: 240, 'font-size': 11, fill: 'var(--ink2)' }, g).textContent = 'Ventrículos';
    mk('line', { x1: 20, y1: 116, x2: 292, y2: 116, stroke: 'var(--line)', 'stroke-dasharray': '4 4' }, g);
    // nodo, His y ramas
    mk('path', { d: `M150 102 L150 136 M150 136 L124 222 M150 136 L190 222`, stroke: 'var(--ink2)', 'stroke-width': 2, fill: 'none' }, g);
    mk('circle', { cx: 150, cy: 102, r: 6, fill: 'var(--card)', stroke: 'var(--ink2)', 'stroke-width': 2 }, g);
    mk('text', { x: 160, y: 106, 'font-size': 10, fill: 'var(--ink2)' }, g).textContent = 'nodo AV';
    mk('text', { x: 156, y: 134, 'font-size': 10, fill: 'var(--ink2)' }, g).textContent = 'His';
    if (sc.ap) {
      mk('line', { x1: 264, y1: 80, x2: 264, y2: 152, stroke: 'var(--rose)', 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
      mk('text', { x: 240, y: 128, 'font-size': 10, fill: 'var(--rose)', 'text-anchor': 'end' }, g).textContent = 'vía';
    }
    if (sc.focus) {
      mk('circle', { cx: G.focus[0], cy: G.focus[1], r: 7, fill: 'var(--rose)' }, g);
      mk('text', { x: G.focus[0] + 12, y: G.focus[1] + 4, 'font-size': 10, fill: 'var(--rose)' }, g).textContent = 'foco';
    }
    mk('circle', { cx: G.rva[0], cy: G.rva[1], r: 4, fill: 'var(--red)' }, g);
    mk('text', { x: G.rva[0] - 8, y: G.rva[1] + 4, 'font-size': 10, fill: 'var(--red)', 'text-anchor': 'end' }, g).textContent = 'catéter VD';
    return { atr, ven };
  }

  const LANES = [['AD', 'AD alta', 292], ['His', 'His', 332], ['VD', 'VD', 372]];
  const W = 1500, X0 = 46, X1 = 300;        // ventana del trazado (ms) y su ubicación
  function spike(t, y, big) { const h = big ? 12 : 9; return `M${t - 2} ${y} L${t} ${y - h} L${t + 2} ${y + h * 0.7} L${t + 4} ${y}`; }

  function mount(root) {
    if (root.dataset.on) return; root.dataset.on = 1;
    const A = ANIMS[root.dataset.anim]; if (!A) return;
    root.innerHTML = `<div class="bl">Animación: ${A.t}</div>
      <div class="anc"><button class="btn anplay" type="button">▶ Reproducir</button><button class="btn anre" type="button">↺ Reiniciar</button>
      <label class="small">Velocidad <select class="anv"><option value="0.12">muy lenta</option><option value="0.25" selected>lenta</option><option value="0.5">normal</option></select></label></div>
      <input class="ant" type="range" min="0" max="${A.dur}" value="0" step="10" aria-label="Momento de la animación">
      <p class="anf small"></p>
      <div class="anp"></div>
      <p class="small" style="margin:4px 0 0;opacity:.7">Animación didáctica: tiempos ilustrativos. Naranja: conducción anterógrada · violeta: retrógrada · rosa: vía o foco · rojo: estímulo.</p>`;
    const panels = A.panels.map(f => {
      const sc = f();
      const wrap = document.createElement('div'); wrap.className = 'anpanel';
      wrap.innerHTML = `<div class="ant2">${sc.title}</div>`;
      const svg = mk('svg', { viewBox: '0 0 310 400', role: 'img', 'aria-label': sc.title }, wrap);
      const h = drawHeart(svg, sc);
      LANES.forEach(([, lab, y]) => { mk('line', { x1: X0, y1: y, x2: X1, y2: y, stroke: 'var(--line)' }, svg); mk('text', { x: 4, y: y + 4, 'font-size': 10, fill: 'var(--ink2)' }, svg).textContent = lab; });
      const tr = mk('path', { d: '', stroke: 'var(--ink)', 'stroke-width': 1.3, fill: 'none' }, svg);
      const st = mk('path', { d: '', stroke: 'var(--red)', 'stroke-width': 1.6, fill: 'none' }, svg);
      const tg = mk('path', { d: '', stroke: 'var(--blue)', 'stroke-width': 2.2, fill: 'none' }, svg);
      const lab = mk('g', { 'font-size': 9, fill: 'var(--ink2)', 'text-anchor': 'middle' }, svg);
      const cur = mk('line', { x1: 0, y1: 270, x2: 0, y2: 392, stroke: 'var(--blue)', 'stroke-width': 1 }, svg);
      const dots = mk('g', {}, svg);
      const ver = document.createElement('div'); ver.className = 'anver'; wrap.appendChild(ver);
      root.querySelector('.anp').appendChild(wrap);
      return { sc, h, tr, st, tg, lab, cur, dots, ver };
    });
    const fas = root.querySelector('.anf'), btn = root.querySelector('.anplay'), rng = root.querySelector('.ant'), vel = root.querySelector('.anv');
    let t = 0, play = false, last = 0;

    function frame(T) {
      for (const p of panels) {
        const { sc } = p;
        // cámaras que se activan
        const lit = (arr, d) => arr.some(x => T >= x && T < x + d);
        p.h.atr.setAttribute('fill', lit(sc.flA, 70) ? 'var(--violet)' : 'var(--blue-soft)');
        p.h.atr.setAttribute('fill-opacity', lit(sc.flA, 70) ? 0.35 : 1);
        p.h.ven.setAttribute('fill', lit(sc.flV, 90) ? 'var(--orange)' : 'var(--blue-soft)');
        p.h.ven.setAttribute('fill-opacity', lit(sc.flV, 90) ? 0.3 : 1);
        // frentes que viajan
        let dh = '';
        for (const w of sc.wv) {
          const t0 = w.pts[0][1], t1 = w.pts[w.pts.length - 1][1];
          if (T < t0 || T > t1 + 40) continue;
          let k = 0; while (k < w.pts.length - 2 && T > w.pts[k + 1][1]) k++;
          const [p0, a0] = w.pts[k], [p1, a1] = w.pts[k + 1];
          const f = Math.max(0, Math.min(1, (T - a0) / Math.max(1, a1 - a0)));
          const x = p0[0] + (p1[0] - p0[0]) * f, y = p0[1] + (p1[1] - p0[1]) * f;
          const trail = w.pts.slice(0, k + 1).map(q => q[0].join(' ')).join(' L') + ` L${x} ${y}`;
          dh += `<path d="M${trail}" stroke="${COL[w.c]}" stroke-width="3" fill="none" opacity=".45"/><circle cx="${x}" cy="${y}" r="6" fill="${COL[w.c]}"/>`;
        }
        p.dots.innerHTML = dh;
        // trazado con ventana móvil
        const tStart = Math.max(0, T - W * 0.85), k = (X1 - X0) / W, xOf = tt => X0 + (tt - tStart) * k;
        let d = '', ds = '', dt = '', lh = '';
        LANES.forEach(([ch, , y]) => { d += `M${X0} ${y} L${xOf(Math.min(T, tStart + W))} ${y} `; });
        for (const e of sc.ev) {
          if (e.t > T || e.t < tStart) continue;
          const y = LANES.find(l => l[0] === e.ch)[2], x = xOf(e.t);
          if (e.stim) { ds += `M${x} ${y - 16} L${x} ${y + 12} `; lh += `<text x="${x}" y="${y - 18}" fill="var(--red)">E</text>`; continue; }
          const hot = e.tag && T > sc.stimEnd;
          if (hot) dt += spike(x, y, false); else d += spike(x, y, e.l === 'V');
          lh += `<text x="${x}" y="${y - 14}">${e.l}</text>`;
          if (hot) { const yy = y - (e.tagUp ? 36 : 24); lh += `<text x="${x}" y="${yy}" fill="var(--blue)" font-weight="700">${e.tag}</text><line x1="${x}" y1="${yy + 2}" x2="${x}" y2="${y - 22}" stroke="var(--blue)"/>`; }
        }
        p.tr.setAttribute('d', d); p.st.setAttribute('d', ds); p.tg.setAttribute('d', dt); p.lab.innerHTML = lh;
        const xc = xOf(T); p.cur.setAttribute('x1', xc); p.cur.setAttribute('x2', xc);
        p.ver.innerHTML = T >= sc.verdictT ? `<p>${sc.verdict}</p><p class="small" style="margin:0">${sc.why}</p>` : '';
        p.ver.classList.toggle('on', T >= sc.verdictT);
      }
      let txt = ''; for (const [ti, tx] of A.fases) if (T >= ti) txt = tx;
      fas.innerHTML = txt; rng.value = T;
    }
    function loop(now) {
      if (!play) return;
      const dt = Math.min(100, now - last); last = now;
      t += dt * parseFloat(vel.value);
      if (t >= A.dur) { t = A.dur; play = false; btn.textContent = '▶ Reproducir'; }
      frame(t);
      if (play) requestAnimationFrame(loop);
    }
    btn.onclick = () => { play = !play; btn.textContent = play ? '❚❚ Pausa' : '▶ Reproducir'; if (play) { if (t >= A.dur) t = 0; last = performance.now(); requestAnimationFrame(loop); } };
    root.querySelector('.anre').onclick = () => { t = 0; frame(t); };
    rng.oninput = () => { t = +rng.value; frame(t); };
    frame(0);
  }

  window.ANIM_IDS = Object.keys(ANIMS);
  window.mountAnims = r => r.querySelectorAll('.anim[data-anim]').forEach(mount);
})();
