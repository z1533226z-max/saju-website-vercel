/** The server supplies the next KST midnight; fortune content stays server-rendered. */
(function () {
    'use strict';

    var refreshAt = Date.parse(document.body.dataset.dailyRefreshAt);
    if (!Number.isFinite(refreshAt)) return;
    var refreshKey = 'daily-refresh:' + refreshAt;
    var lastReloadKey = 'daily-refresh:last-reload';
    var reloading = false;
    var timer;
    var cooldownUntil = 0;
    // Choose once per page so restore events cannot bypass or redraw the jitter.
    var dueAt = refreshAt + Math.floor(Math.random() * 30001);
    try {
        if (window.sessionStorage.getItem(refreshKey)) return;
        var lastReload = Number(window.sessionStorage.getItem(lastReloadKey));
        if (lastReload > 0) {
            cooldownUntil = performance.now() + Math.max(0, 30000 - Math.max(0, Date.now() - lastReload));
        }
    } catch (_) {
        // Storage may be disabled; the in-memory guard still permits only one reload per page.
    }

    function refreshIfDue() {
        if (reloading) return;
        window.clearTimeout(timer);
        var remaining = Math.max(dueAt - Date.now(), cooldownUntil - performance.now());
        if (remaining > 0) {
            // Timers may wake early, and suspended tabs may resume before the jitter ends.
            timer = window.setTimeout(refreshIfDue, Math.max(1000, remaining));
            return;
        }
        reloading = true;
        try {
            window.sessionStorage.setItem(refreshKey, '1');
            window.sessionStorage.setItem(lastReloadKey, String(Date.now()));
        } catch (_) {
            // Keep the page-local guard even when a write fails (quota/privacy mode).
        }
        window.location.reload();
    }

    timer = window.setTimeout(refreshIfDue, Math.max(0, dueAt - Date.now(), cooldownUntil - performance.now()));
    // Sleeping tabs and browser history snapshots may not run their midnight timer.
    document.addEventListener('visibilitychange', function () {
        if (!document.hidden) refreshIfDue();
    });
    window.addEventListener('pageshow', refreshIfDue);
}());
