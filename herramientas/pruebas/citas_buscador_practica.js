const { chromium, devices } = require('playwright');
const dir = process.argv[2];
(async () => { const b = await chromium.launch(); const errs = [];
  const c = await b.newContext(devices['iPhone 13']); const p = await c.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/'); await p.waitForTimeout(700);
  // 1) citas
  await p.evaluate(() => openFicha('ppi')); await p.waitForTimeout(300);
  await p.click('#dlgB .fnav [data-jump="interp"]'); await p.waitForTimeout(900);
  await p.click('#dlgB .cit[data-ref="michaud01"]'); await p.waitForTimeout(300);
  console.log('popup', await p.evaluate(() => [document.querySelector('#refpop').open, document.querySelector('#rpT').textContent.slice(0, 60), [...document.querySelectorAll('#rpL a')].map(a => a.href)]));
  await p.screenshot({ path: dir + '/x_cite.png' });
  await p.click('#rpX'); await p.evaluate(() => $('#dlg').close());
  console.log('refs sin link', await p.evaluate(() => Object.keys(REFS).filter(k => !REFLINK[k]).join(', ')));
  // 2) buscador
  await p.click('#srchBtn');
  for (const q of ['enriquez', 'kistler', 'tracto de salida', 'cuspide', 'wpw', 'calcular', 'crista']) { await p.fill('#sq', q); await p.waitForTimeout(120);
    console.log(q, '→', await p.evaluate(() => [...document.querySelectorAll('#sres .sg')].map(e => e.textContent).join(', ')), '| 1º', await p.evaluate(() => document.querySelector('#sres button b')?.textContent)); }
  await p.fill('#sq', 'tracto de salida'); await p.waitForTimeout(150); await p.screenshot({ path: dir + '/x_search.png' });
  await p.click('#sres .sg:has-text("Localizadores") + button'); await p.waitForTimeout(400);
  console.log('abre', await p.evaluate(() => [document.querySelector('.seg .on').textContent, !document.querySelector('#loc-enr').hidden]));
  // 3) práctica
  await p.evaluate(() => { tab('prac'); startCase(10); pDone = PCASOS[10].dx[0]; renderCase(); }); await p.waitForTimeout(300);
  console.log('práctica caso 11', await p.evaluate(() => [...document.querySelectorAll('#pracBody .anlink')].map(b => b.textContent).join(' / ')));
  await p.evaluate(() => document.querySelector('#pracBody .anlink').scrollIntoView({ block: 'center' })); await p.waitForTimeout(200);
  await p.screenshot({ path: dir + '/x_prac.png' });
  await p.click('#pracBody .anlink'); await p.waitForTimeout(500);
  console.log('abrió', await p.evaluate(() => document.querySelector('#dlgT').textContent));
  const all = await p.evaluate(() => PCASOS.map((c, i) => (i + 1) + ':' + (((d => { d.innerHTML = caseAnims(c); return d.querySelectorAll('.anlink').length; })(document.createElement('div'))))).join(' '));
  console.log('anims por caso', all);
  console.log('errs', errs); await b.close(); })();
