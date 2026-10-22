/** The server supplies the next KST midnight; fortune content stays server-rendered. */
(function () {
    'use strict';

    var refreshAt = Date.parse(document.body.dataset.dailyRefreshAt);
    if (!Number.isFinite(refreshAt)) return;
    var reloading = false;

    function refreshIfDue() {
        if (!reloading && Date.now() >= refreshAt) {
            reloading = true;
            window.location.reload();
        }
    }

    window.setTimeout(refreshIfDue, Math.max(0, refreshAt - Date.now()));
    // Sleeping tabs and browser history snapshots may not run their midnight timer.
    document.addEventListener('visibilitychange', function () {
        if (!document.hidden) refreshIfDue();
    });
    window.addEventListener('pageshow', refreshIfDue);
}());
