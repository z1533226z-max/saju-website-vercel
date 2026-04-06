import { chromium } from 'playwright';

const URL = 'https://saju-website-vercel.vercel.app/';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  // Collect console errors
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });

  console.log('1. Loading page...');
  await page.goto(URL, { waitUntil: 'networkidle' });

  // Verify dark theme
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  console.log(`   Body background: ${bg}`);

  // Take hero screenshot
  await page.screenshot({ path: '/tmp/verify-01-hero.png' });
  console.log('   Hero screenshot saved');

  // Fill form
  console.log('2. Filling form...');
  await page.selectOption('select[x-model="birthYear"]', '1990');
  await page.selectOption('select[x-model="birthMonth"]', '5');
  await page.selectOption('select[x-model="birthDay"]', '15');

  // Select time (오시)
  const timeBtn = page.locator('.time-grid button', { hasText: '오시' });
  await timeBtn.click();

  // Select gender
  await page.locator('.gender-card').first().click({ force: true });

  // Submit
  console.log('3. Submitting form...');
  await page.click('#submit-btn');

  // Wait for results
  await page.waitForSelector('.result-tab-btn', { timeout: 30000 });
  await page.waitForTimeout(2000);

  // Screenshot Tab 1: 기본 분석
  console.log('4. Tab 1: 기본 분석');
  await page.screenshot({ path: '/tmp/verify-02-basic.png', fullPage: true });

  // Check elements chart
  const elemChart = await page.evaluate(() => {
    const canvas = document.getElementById('elements-chart');
    return canvas ? { width: canvas.width, height: canvas.height } : null;
  });
  console.log(`   Elements chart: ${JSON.stringify(elemChart)}`);

  // Click Tab 2: 심화 분석
  console.log('5. Tab 2: 심화 분석');
  await page.click('button:has-text("심화 분석")');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/tmp/verify-03-advanced.png', fullPage: true });

  // Check ten gods width
  const tenGodsWidth = await page.evaluate(() => {
    const card = document.querySelector('.interpretation--full .interpretation-card');
    return card ? card.getBoundingClientRect().width : 0;
  });
  console.log(`   Ten gods card width: ${tenGodsWidth}px`);

  // Click Tab 3: 운세 흐름
  console.log('6. Tab 3: 운세 흐름');
  await page.click('button:has-text("운세 흐름")');
  await page.waitForTimeout(2000);  // Wait for chart to render
  await page.screenshot({ path: '/tmp/verify-04-fortune.png', fullPage: true });

  // Check fortune chart
  const fortuneChart = await page.evaluate(() => {
    const canvas = document.getElementById('fortune-chart');
    if (!canvas) return { exists: false };
    const ctx = canvas.getContext('2d');
    // Check if anything is drawn by sampling a few pixels
    const imageData = ctx.getImageData(canvas.width / 2, canvas.height / 2, 1, 1);
    const [r, g, b, a] = imageData.data;
    return {
      exists: true,
      width: canvas.width,
      height: canvas.height,
      centerPixel: `rgba(${r},${g},${b},${a})`,
      hasContent: a > 0
    };
  });
  console.log(`   Fortune chart: ${JSON.stringify(fortuneChart)}`);

  // Check fortune stats
  const fortuneStats = await page.evaluate(() => {
    const bestYear = document.querySelector('.stat-item.best-year');
    const cautionYear = document.querySelector('.stat-item.caution-year');
    return {
      bestYear: bestYear ? bestYear.innerText.trim().substring(0, 50) : 'not found',
      cautionYear: cautionYear ? cautionYear.innerText.trim().substring(0, 50) : 'not found'
    };
  });
  console.log(`   Fortune stats: ${JSON.stringify(fortuneStats)}`);

  // Summary
  console.log('\n=== SUMMARY ===');
  console.log(`Dark theme: ${bg.includes('12, 11, 16') || bg.includes('0C0B10') ? 'YES' : 'NO'} (${bg})`);
  console.log(`Elements chart rendered: ${elemChart ? 'YES' : 'NO'}`);
  console.log(`Ten gods full width: ${tenGodsWidth > 600 ? 'YES' : 'NO'} (${tenGodsWidth}px)`);
  console.log(`Fortune chart rendered: ${fortuneChart.hasContent ? 'YES' : 'NO'}`);
  console.log(`Console errors: ${errors.length}`);
  if (errors.length > 0) {
    errors.forEach(e => console.log(`  - ${e}`));
  }

  await browser.close();
})();
