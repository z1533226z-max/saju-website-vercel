import { chromium } from '@playwright/test';

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

    // Collect ALL console messages
    const errors = [];
    const logs = [];
    page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
        else logs.push(`[${msg.type()}] ${msg.text()}`);
    });
    page.on('pageerror', err => errors.push(`PAGE ERROR: ${err.message}`));

    // Track network failures
    page.on('response', response => {
        if (response.status() >= 400) {
            logs.push(`HTTP ${response.status()}: ${response.url()}`);
        }
    });

    console.log('1. Navigating to site...');
    await page.goto('https://saju-website-vercel.vercel.app/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(2000);

    // Fill in the form
    console.log('2. Filling form...');

    // Select year 1990
    await page.selectOption('#birth-year', '1990');
    await page.waitForTimeout(300);

    // Select month 5
    await page.selectOption('#birth-month', '5');
    await page.waitForTimeout(300);

    // Select day 15
    await page.selectOption('#birth-day', '15');
    await page.waitForTimeout(300);

    // Select time (오시 11:00-13:00)
    const timeButtons = await page.locator('.time-grid button').all();
    if (timeButtons.length > 6) {
        await timeButtons[6].click(); // 오시
    }
    await page.waitForTimeout(300);

    // Select gender (남성) - click the label, not the hidden radio
    await page.locator('.gender-card', { hasText: '남성' }).click({ force: true });
    await page.waitForTimeout(300);

    // Screenshot form filled
    await page.screenshot({ path: '/tmp/saju-form-filled.png', fullPage: false });
    console.log('   Form filled screenshot saved');

    // Submit form
    console.log('3. Submitting form...');
    await page.locator('.submit-button').click();

    // Wait for API response
    await page.waitForTimeout(8000);

    // Screenshot basic results tab
    console.log('4. Capturing basic results...');
    await page.screenshot({ path: '/tmp/saju-result-basic.png', fullPage: false });

    // Scroll down to see more of basic results
    await page.evaluate(() => window.scrollBy(0, 600));
    await page.waitForTimeout(500);
    await page.screenshot({ path: '/tmp/saju-result-basic-2.png', fullPage: false });

    // Click 심화 분석 tab
    console.log('5. Clicking 심화 분석 tab...');
    const advancedTab = page.locator('.result-tab-btn', { hasText: '심화 분석' });
    if (await advancedTab.isVisible()) {
        await advancedTab.click();
        await page.waitForTimeout(1000);
        await page.screenshot({ path: '/tmp/saju-result-advanced.png', fullPage: false });

        // Scroll to see more
        await page.evaluate(() => window.scrollBy(0, 600));
        await page.waitForTimeout(500);
        await page.screenshot({ path: '/tmp/saju-result-advanced-2.png', fullPage: false });
    } else {
        console.log('   심화 분석 tab NOT visible!');
    }

    // Click 운세 흐름 tab
    console.log('6. Clicking 운세 흐름 tab...');
    const fortuneTab = page.locator('.result-tab-btn', { hasText: '운세 흐름' });
    if (await fortuneTab.isVisible()) {
        await fortuneTab.click();
        await page.waitForTimeout(1000);
        await page.screenshot({ path: '/tmp/saju-result-fortune.png', fullPage: false });

        // Scroll to see chart
        await page.evaluate(() => window.scrollBy(0, 600));
        await page.waitForTimeout(500);
        await page.screenshot({ path: '/tmp/saju-result-fortune-2.png', fullPage: false });
    } else {
        console.log('   운세 흐름 tab NOT visible!');
    }

    // Check Alpine.js data state
    console.log('\n7. Checking Alpine.js state...');
    const alpineState = await page.evaluate(() => {
        const el = document.querySelector('[x-data]');
        if (!el && !el.__x) return 'No Alpine data found';
        try {
            const data = Alpine.$data(el);
            return {
                showResults: data.showResults,
                resultTab: data.resultTab,
                hasInterpretation: !!data.interpretation,
                interpretationKeys: Object.keys(data.interpretation || {}),
                hasTenGods: !!data.interpretation?.ten_gods,
                tenGodsKeys: Object.keys(data.interpretation?.ten_gods || {}),
                hasMajorFortune: !!data.interpretation?.major_fortune,
                majorFortuneKeys: Object.keys(data.interpretation?.major_fortune || {}),
                hasFortuneTimeline: !!data.interpretation?.fortune_timeline,
                fortuneTimelineKeys: Object.keys(data.interpretation?.fortune_timeline || {}),
                hasPattern: !!data.pattern,
                hasShinshal: !!data.shinshal,
                hasYongshin: !!data.yongshin,
                sajuYear: data.saju?.year,
            };
        } catch (e) {
            return 'Error: ' + e.message;
        }
    });
    console.log('Alpine state:', JSON.stringify(alpineState, null, 2));

    // Print errors
    console.log('\n=== Console Errors ===');
    if (errors.length > 0) {
        // Deduplicate
        const unique = [...new Set(errors)];
        unique.forEach(e => console.log('ERROR:', e));
    } else {
        console.log('No errors');
    }

    // Print relevant logs
    console.log('\n=== Relevant Logs ===');
    logs.filter(l => l.includes('HTTP') || l.includes('error') || l.includes('Error') || l.includes('saju') || l.includes('API'))
        .forEach(l => console.log(l));

    await browser.close();
})();
