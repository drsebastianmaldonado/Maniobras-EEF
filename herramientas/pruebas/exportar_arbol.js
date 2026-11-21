const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('http://localhost:8765/'); await p.waitForTimeout(600);
  const t = await p.evaluate(() => { const strip = x => String(x || '').replace(/<[^>]+>/g, ''); const o = {};
    for (const [k, n] of Object.entries(N)) o[k] = n.leaf ? { leaf: 1, dx: n.fn ? 'Resultado según circuito inferior y superior (PJRT · NFRT · TRNAV atípica · zona gris)' : strip(n.dx), tone: n.tone || '' }
      : { q: strip(n.q), pre: !!n.pre, dx: strip(n.dx || ''), opts: n.opts.map(x => ({ t: strip(x.t), go: x.go })) };
    return o; });
  require('fs').writeFileSync(process.argv[2], JSON.stringify(t, null, 1)); await b.close(); })();
