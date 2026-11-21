const { chromium, devices } = require('playwright');
const dir = process.argv[2];
(async () => { const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext(devices['iPhone 13'])).newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/'); await p.waitForTimeout(600); await p.evaluate(() => tab('algo'));
  const pick = async t => { const ok = await p.evaluate(t => { const b = [...document.querySelectorAll('#cur .opt')].find(x => x.textContent.startsWith(t)); if (b) b.click(); return !!b; }, t); await p.waitForTimeout(150); if (!ok) console.log('  no encontré', t); };
  const cur = () => p.evaluate(() => document.querySelector('#cur').innerText.split('\n').slice(0, 2).join(' | '));
  for (const [path, tail] of [[['Angosto', '1:1', 'Concéntrica', '≤ 70 ms', 'A-A-V'], ['Sigo sospechando', 'Fijo']], [['Angosto', '1:1', 'Excéntrica', 'A-A-V'], ['Sigo sospechando', 'Varía']], [['Angosto', '1:1', 'Concéntrica', '> 70 ms', 'RP corto', 'A-A-V'], ['Sigo sospechando', 'Fijo']], [['Ancho con His', 'Más V que A', 'Sí'], ['Sigo sospechando', '≤ 30']]]) {
    if (await p.$('#reset')) await p.click('#reset');
    for (const t of path) await pick(t); console.log(path.slice(-2).join(' > '), '→', await cur());
    if (path[0] === 'Angosto' && path[2] === 'Concéntrica' && path[3] === '≤ 70 ms') await p.screenshot({ path: dir + '/pre_ta.png' });
    if (path[0].startsWith('Ancho')) await p.screenshot({ path: dir + '/pre_bbr.png' });
    for (const t of tail) { await pick(t); console.log('   ', t, '→', await cur()); }
  }
  console.log('errs', errs); await b.close(); })();
