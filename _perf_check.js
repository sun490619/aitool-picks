const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const PORT = 8137;
const MIME = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.png':'image/png', '.jpg':'image/jpeg', '.svg':'image/svg+xml', '.json':'application/json', '.xml':'application/xml', '.txt':'text/plain' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/index.html';
  let fp = path.join(ROOT, p);
  if (!fs.existsSync(fp) || fs.statSync(fp).isDirectory()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(fp)] || 'application/octet-stream' });
  fs.createReadStream(fp).pipe(res);
});

const URLS = ['/index.html', '/posts/best-ai-seo-tools-2026.html', '/tools/grammarly.html', '/category/writing.html'];

(async () => {
  console.error('starting server...');
  await new Promise(r => server.listen(PORT, r));
  console.error('launching browser...');
  const browser = await chromium.launch();
  console.error('browser ok');
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  for (const u of URLS) {
    const transfers = {};
    const imgSizes = [];
    const onResp = (r) => {
      const len = parseInt(r.headers()['content-length'] || '0', 10);
      const ct = r.headers()['content-type'] || '';
      transfers[ct] = (transfers[ct] || 0) + (isNaN(len) ? 0 : len);
      if (ct.startsWith('image/')) imgSizes.push({ url: r.url(), len });
    };
    page.on('response', onResp);
    console.error('goto', u);
    const t0 = Date.now();
    await page.goto(`http://localhost:${PORT}${u}`, { waitUntil: 'load', timeout: 30000 });
    const nav = await page.evaluate(() => {
      const e = performance.getEntriesByType('navigation')[0];
      const paint = performance.getEntriesByType('paint');
      return { dcl: Math.round(e.domContentLoadedEventEnd), load: Math.round(e.loadEventEnd) };
    });
    const lcpVal = await page.evaluate(() => new Promise((res) => {
      try {
        const po = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          res(Math.round(entries[entries.length - 1].startTime));
        });
        po.observe({ type: 'largest-contentful-paint', buffered: true });
      } catch (e) { res('n/a'); }
      setTimeout(() => res('timeout'), 6000);
    }));
    page.off('response', onResp);
    const totalBytes = Object.values(transfers).reduce((a, b) => a + b, 0);
    imgSizes.sort((a, b) => b.len - a.len);
    console.log(`\n=== ${u} ===`);
    console.log(`DOMContentLoaded: ${nav.dcl}ms | Load: ${nav.load}ms | LCP: ${lcpVal}ms`);
    console.log(`Total transfer: ${(totalBytes / 1024).toFixed(1)} KB`);
    console.log(`Images: ${imgSizes.length}, top5:`);
    imgSizes.slice(0, 5).forEach(i => console.log(`  ${(i.len / 1024).toFixed(1)} KB  ${i.url.split('/').slice(-1)[0]}`));
  }
  await browser.close();
  server.close();
  console.error('done');
})().catch(e => { console.error('FATAL', e); process.exit(1); });
