const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext(devices['iPhone 13'])).newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/'); await p.waitForTimeout(600); await p.evaluate(() => tab('algo'));
  const pick = async t => { const ok = await p.evaluate(t => { const b = [...document.querySelectorAll('#cur .opt')].find(x => x.textContent.startsWith(t)); if (b) b.click(); return !!b; }, t); await p.waitForTimeout(120); if (!ok) console.log('  no encontré', t); };
  const cur = () => p.evaluate(() => document.querySelector('#cur').innerText.split('\n').slice(0, 2).join(' | '));
  const runs = [
    ['Angosto', '1:1', 'Concéntrica', '≤ 70 ms', 'Las A no se aceleran', 'Sí'], ['Angosto', '1:1', 'Concéntrica', '≤ 70 ms', 'Las A no se aceleran', 'No', 'VA linking'],
    ['Angosto', '1:1', 'Concéntrica', '≤ 70 ms', 'Las A no se aceleran', 'No', 'Ninguna'], ['Angosto', '1:1', 'Concéntrica', '≤ 70 ms', 'La TSV se corta', 'Se corta con bloqueo VA'],
    ['Angosto', '1:1', 'Concéntrica', '> 70 ms', 'RP corto', 'Las A no se aceleran', 'Sí'], ['Angosto', '1:1', 'Concéntrica', '> 70 ms', 'RP corto', 'Las A no se aceleran', 'No'],
    ['Angosto', '1:1', 'Excéntrica', 'Las A no se aceleran', 'Sí'], ['Angosto', '1:1', 'Excéntrica', 'Las A no se aceleran', 'No'],
    ['Angosto', '1:1', 'Concéntrica', '> 70 ms', 'RP largo', 'Las A no se aceleran', 'Sí'], ['Angosto', '1:1', 'Excéntrica', 'La TSV se corta', 'Se corta con bloqueo VA']];
  for (const r of runs) { if (await p.$('#reset')) await p.click('#reset'); for (const t of r) await pick(t); console.log(r.slice(2).join(' > '), '→', await cur()); }
  console.log('errs', errs); await b.close(); })();
