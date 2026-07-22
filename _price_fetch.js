const { chromium } = require('playwright');
const URLS = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' });
  for (const u of URLS) {
    try {
      await page.goto(u, { waitUntil: 'networkidle', timeout: 25000 });
      await page.waitForTimeout(1500);
      const txt = await page.evaluate(() => document.body.innerText);
      const prices = [...txt.matchAll(/\$[\d,]+(?:\.\d+)?(?:\s?\/\s?(?:mo|month|yr|year|user|seat|member))?/gi)].map(m=>m[0]);
      const title = await page.title();
      const isChallenge = /just a moment|enable javascript/i.test(txt.slice(0,200));
      console.log(`\n=== ${u} ===`);
      console.log('TITLE:', title, '| CHALLENGE:', isChallenge);
      console.log('PRICES:', [...new Set(prices)].slice(0,30).join('  '));
    } catch (e) {
      console.log(`\n=== ${u} ===\nERROR: ${e.message}`);
    }
  }
  await browser.close();
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
