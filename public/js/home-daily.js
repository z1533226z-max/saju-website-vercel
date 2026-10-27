/* Reuse the daily page's server-rendered fortunes; never generate homepage predictions. */
(function () {
    'use strict';

    const choices = document.getElementById('zodiac-choices');
    if (!choices) return;
    const preview = document.getElementById('daily-preview');
    const date = document.getElementById('home-date');
    const name = document.getElementById('daily-preview-name');
    const relation = document.getElementById('daily-preview-relation');
    const message = document.getElementById('daily-preview-message');
    const score = document.getElementById('daily-preview-score');
    const link = document.getElementById('daily-preview-link');
    const retry = document.getElementById('daily-preview-retry');
    const formatter = new Intl.DateTimeFormat('ko-KR', { timeZone: 'Asia/Seoul', year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' });
    let fortunes;
    let refreshAt = 0;
    let timer;
    let loading = false;

    function selectFortune() {
        const selected = choices.querySelector('input:checked');
        const fortune = fortunes && fortunes.querySelector(`a.zodiac-summary-card[href="/daily/${selected.value}/"]`);
        name.textContent = selected.nextElementSibling.textContent + '의 오늘';
        link.href = '/daily/' + selected.value + '/';
        if (!fortune) return;
        relation.textContent = fortune.querySelector('.zsc-rel-chip').textContent.trim();
        message.textContent = fortune.querySelector('.zsc-msg').textContent.trim();
        score.textContent = fortune.querySelector('.zsc-val').textContent.trim() + '점';
    }

    async function loadFortunes() {
        if (loading) return;
        loading = true;
        fortunes = null;
        clearTimeout(timer);
        preview.dataset.state = 'loading';
        preview.setAttribute('aria-busy', 'true');
        relation.textContent = '오늘의 운세를 불러오고 있어요.';
        message.textContent = '';
        score.textContent = '—';
        retry.hidden = true;
        date.textContent = formatter.format(new Date());
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 10000);
        try {
            const response = await fetch('/daily/', { signal: controller.signal, cache: 'no-store' });
            if (!response.ok) throw new Error('Daily page unavailable');
            const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
            const day = doc.body.dataset.dailyDate;
            const next = Date.parse(doc.body.dataset.dailyRefreshAt);
            if (!/^\d{4}-\d{2}-\d{2}$/.test(day || '') || !Number.isFinite(next)) throw new Error('Missing daily date');
            for (const input of choices.querySelectorAll('input')) {
                const card = doc.querySelector(`a.zodiac-summary-card[href="/daily/${input.value}/"]`);
                if (!card || !['.zsc-rel-chip', '.zsc-msg', '.zsc-val'].every(selector => card.querySelector(selector)?.textContent.trim())) throw new Error('Incomplete daily data');
            }
            fortunes = doc;
            refreshAt = next;
            date.dateTime = day;
            date.textContent = formatter.format(new Date(day + 'T12:00:00+09:00'));
            selectFortune();
            preview.dataset.state = 'ready';
            // An inaccurate device clock must not cause an endless request loop.
            const remaining = refreshAt - Date.now();
            timer = setTimeout(loadFortunes, remaining > 0 ? remaining : 60000);
        } catch (_) {
            preview.dataset.state = 'error';
            relation.textContent = '운세를 불러오지 못했어요.';
            message.textContent = '다시 불러오거나, 오늘 운세 페이지에서 확인해 주세요.';
            retry.hidden = false;
        } finally {
            clearTimeout(timeout);
            preview.setAttribute('aria-busy', 'false');
            loading = false;
        }
    }

    choices.addEventListener('change', selectFortune);
    retry.addEventListener('click', loadFortunes);
    document.addEventListener('visibilitychange', function () {
        if (!document.hidden && Date.now() >= refreshAt) loadFortunes();
    });
    document.getElementById('home-saju-link').addEventListener('click', function (event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        document.getElementById('input-section').scrollIntoView({ behavior: 'instant', block: 'start' });
        document.getElementById('birth-year').focus({ preventScroll: true });
    });
    document.querySelector('.home-menu').addEventListener('click', function (event) {
        if (event.target.closest('a')) this.open = false;
    });
    document.querySelector('.home-menu').addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            this.open = false;
            this.querySelector('summary').focus();
        }
    });
    loadFortunes();
}());
