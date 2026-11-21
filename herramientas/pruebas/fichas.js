const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
  const p = await b.newPage({ viewport: { width: 1100, height: 1500 } }); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/'); await p.waitForTimeout(800);
  for (const id of ['vop', 'ppi', 'sava', 'dha', 'hisorto', 'diff', 'ehr', 'parahis', 'vai', 'aop', 'eha', 'preex', 'ado']) {
    await p.evaluate(id => openFicha(id), id); await p.waitForTimeout(300);
    const r = await p.evaluate(() => [...document.querySelectorAll('#dlgB .anim')].map(a => {
      const rg = a.querySelector('.ant'); rg.value = rg.max; rg.dispatchEvent(new Event('input'));
      return a.querySelector('.bl').textContent + ' [' + a.querySelectorAll('.anpanel').length + '] ' + (a.querySelector('.anver').textContent.slice(0, 60)); }));
    console.log(id, '\n  ' + r.join('\n  '));
  }
  await p.evaluate(() => openFicha('hisorto')); await p.waitForTimeout(300);
  await p.evaluate(() => { const r = document.querySelectorAll('#dlgB .anim')[0].querySelector('.ant'); r.value = 2050; r.dispatchEvent(new Event('input')); });
  const el = (await p.$$('#dlgB .anim'))[0]; await el.scrollIntoViewIfNeeded(); await el.screenshot({ path: process.argv[2] + '/a_single_hisorto.png' });
  console.log('errs', errs); await b.close(); })();
