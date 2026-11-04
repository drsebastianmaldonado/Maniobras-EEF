const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const dir = process.argv[2]; const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.svg'))) {
    await p.goto('file://' + dir + '/' + f); const el = await p.$('svg');
    const bb = await el.boundingBox(); await p.setViewportSize({ width: Math.ceil(bb.width) + 4, height: Math.ceil(bb.height) + 4 });
    await el.screenshot({ path: dir + '/' + f.replace('.svg', '.png') }); }
  await b.close(); })();
