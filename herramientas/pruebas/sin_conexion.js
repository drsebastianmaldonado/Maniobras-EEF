const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const c = await b.newContext(Object.assign({}, devices['iPhone 13'], { serviceWorkers: 'allow' })); const p = await c.newPage();
  await p.goto('http://localhost:8765/'); await p.waitForTimeout(2000);
  console.log('sw', await p.evaluate(async () => { const r = await navigator.serviceWorker.getRegistration(); return [!!r, !!navigator.serviceWorker.controller, r && r.active && r.active.state]; }));
  await p.reload(); await p.waitForTimeout(1500);
  console.log('controller tras recarga', await p.evaluate(() => !!navigator.serviceWorker.controller));
  await p.click('#offBtn'); await p.waitForFunction(() => !document.querySelector('#offBtn').disabled, null, { timeout: 120000 });
  console.log(await p.textContent('#offEst'));
  console.log('caches', await p.evaluate(async () => { const o = {}; for (const k of await caches.keys()) o[k] = (await (await caches.open(k)).keys()).length; return o; }));
  await c.setOffline(true);
  try { await p.reload({ waitUntil: 'domcontentloaded' }); await p.waitForTimeout(1500); console.log('recarga offline OK', await p.title()); } catch (e) { console.log('recarga offline FALLÓ', e.message.split('\n')[0]); }
  const r = await p.evaluate(async () => { const urls = ['figs/sim/casos/c17_vbasal.jpg', 'figs/esq/ppi.jpg', 'localizar/via-accesoria.html']; const out = []; for (const u of urls) { try { const x = await fetch(u); out.push(u + ' ' + x.status); } catch (e) { out.push(u + ' ERROR'); } } return out; });
  console.log(r);
  const r2 = await p.evaluate(async () => { tab('prac'); startCase(16); await new Promise(r => setTimeout(r, 800)); const im = [...document.querySelectorAll('#p-prac img')]; im.forEach(i => { i.loading = 'eager'; i.src = i.src; }); await new Promise(r => setTimeout(r, 2000)); return im.length + ' imgs, ' + im.filter(i => i.complete && i.naturalWidth > 0).length + ' cargadas'; });
  console.log('caso 17 sin conexión:', r2);
  await b.close(); })();
