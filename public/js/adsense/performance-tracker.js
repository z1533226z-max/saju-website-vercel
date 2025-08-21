/**
 * AdSense Performance Tracker
 * Monitors and reports ad performance metrics for optimization
 */

class AdPerformanceTracker {
    constructor(config = {}) {
        this.config = {
            trackingEnabled: config.trackingEnabled !== false,
            reportInterval: config.reportInterval || 60000, // 1 minute
            analyticsEnabled: config.analyticsEnabled !== false,
            debugMode: config.debugMode || false,
            storageKey: config.storageKey || 'adPerformanceMetrics'
        };

        // Performance metrics
        this.metrics = {
            pageViews: 0,
            adImpressions: {},
            viewableImpressions: {},
            clicks: {},
            hoverTime: {},
            loadTimes: {},
            errorCount: {},
            revenue: 0,
            sessionStart: Date.now(),
            lastUpdate: Date.now()
        };

        // Core Web Vitals related to ads
        this.webVitals = {
            cls: 0,
            fid: 0,
            lcp: 0,
            fcp: 0,
            ttfb: 0
        };

        // A/B test results
        this.experiments = {};

        // Session data
        this.session = {
            id: this.generateSessionId(),
            startTime: Date.now(),
            device: this.detectDevice(),
            referrer: document.referrer,
            pageUrl: window.location.href
        };

        // Initialize
        this.init();
    }

    /**
     * Initialize the performance tracker
     */
    init() {
        if (!this.config.trackingEnabled) return;

        // Load previous metrics from storage
        this.loadMetrics();

        // Setup tracking
        this.setupImpressionTracking();
        this.setupViewabilityTracking();
        this.setupClickTracking();
        this.setupEngagementTracking();
        this.setupErrorTracking();
        this.setupWebVitalsTracking();

        // Start reporting
        this.startReporting();

        // Track page view
        this.trackPageView();

        console.log('AdPerformanceTracker initialized');
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Detect device type
     */
    detectDevice() {
        const width = window.innerWidth;
        if (width < 768) return 'mobile';
        if (width < 1024) return 'tablet';
        return 'desktop';
    }

    /**
     * Load metrics from localStorage
     */
    loadMetrics() {
        try {
            const stored = localStorage.getItem(this.config.storageKey);
            if (stored) {
                const data = JSON.parse(stored);
                // Only load today's metrics
                if (this.isSameDay(data.lastUpdate)) {
                    this.metrics = { ...this.metrics, ...data };
                }
            }
        } catch (error) {
            console.error('Failed to load metrics:', error);
        }
    }

    /**
     * Save metrics to localStorage
     */
    saveMetrics() {
        try {
            localStorage.setItem(this.config.storageKey, JSON.stringify({
                ...this.metrics,
                lastUpdate: Date.now()
            }));
        } catch (error) {
            console.error('Failed to save metrics:', error);
        }
    }

    /**
     * Check if two timestamps are on the same day
     */
    isSameDay(timestamp) {
        const date1 = new Date(timestamp);
        const date2 = new Date();
        return date1.toDateString() === date2.toDateString();
    }

    /**
     * Track page view
     */
    trackPageView() {
        this.metrics.pageViews++;
        this.sendEvent('page_view', {
            url: window.location.href,
            referrer: document.referrer,
            device: this.session.device
        });
    }

    /**
     * Setup impression tracking
     */
    setupImpressionTracking() {
        // Listen for ad load events
        window.addEventListener('adloaded', (event) => {
            const adId = event.detail?.adId;
            if (adId) {
                this.trackImpression(adId);
            }
        });

        // Monitor ad containers
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.classList?.contains('adsbygoogle')) {
                            const container = node.closest('.ad-container');
                            if (container) {
                                this.trackImpression(container.id);
                            }
                        }
                    });
                }
            });
        });

        // Observe all ad containers
        document.querySelectorAll('.ad-container').forEach(container => {
            observer.observe(container, { childList: true, subtree: true });
        });
    }

    /**
     * Track ad impression
     */
    trackImpression(adId) {
        if (!this.metrics.adImpressions[adId]) {
            this.metrics.adImpressions[adId] = 0;
        }
        this.metrics.adImpressions[adId]++;

        this.sendEvent('ad_impression', {
            adId: adId,
            timestamp: Date.now(),
            device: this.session.device
        });

        if (this.config.debugMode) {
            console.log(`Ad impression tracked: ${adId}`);
        }
    }

    /**
     * Setup viewability tracking
     */
    setupViewabilityTracking() {
        const viewabilityObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const adId = entry.target.id;
                
                // Track when 50% or more is visible for at least 1 second
                if (entry.intersectionRatio >= 0.5) {
                    if (!entry.target.dataset.viewTimer) {
                        entry.target.dataset.viewTimer = setTimeout(() => {
                            this.trackViewableImpression(adId);
                            delete entry.target.dataset.viewTimer;
                        }, 1000);
                    }
                } else {
                    // Clear timer if ad goes out of view
                    if (entry.target.dataset.viewTimer) {
                        clearTimeout(entry.target.dataset.viewTimer);
                        delete entry.target.dataset.viewTimer;
                    }
                }

                // Track visibility percentage
                this.trackVisibility(adId, entry.intersectionRatio);
            });
        }, {
            threshold: [0, 0.25, 0.5, 0.75, 1.0]
        });

        // Observe all ad containers
        document.querySelectorAll('.ad-container').forEach(container => {
            viewabilityObserver.observe(container);
        });
    }

    /**
     * Track viewable impression
     */
    trackViewableImpression(adId) {
        if (!this.metrics.viewableImpressions[adId]) {
            this.metrics.viewableImpressions[adId] = 0;
        }
        this.metrics.viewableImpressions[adId]++;

        this.sendEvent('viewable_impression', {
            adId: adId,
            timestamp: Date.now(),
            device: this.session.device
        });

        if (this.config.debugMode) {
            console.log(`Viewable impression tracked: ${adId}`);
        }
    }

    /**
     * Track ad visibility
     */
    trackVisibility(adId, ratio) {
        this.sendEvent('ad_visibility', {
            adId: adId,
            visibilityRatio: ratio,
            timestamp: Date.now()
        });
    }

    /**
     * Setup click tracking
     */
    setupClickTracking() {
        document.addEventListener('click', (event) => {
            const adContainer = event.target.closest('.ad-container');
            if (adContainer) {
                this.trackClick(adContainer.id, event);
            }
        }, true);
    }

    /**
     * Track ad click
     */
    trackClick(adId, event) {
        if (!this.metrics.clicks[adId]) {
            this.metrics.clicks[adId] = 0;
        }
        this.metrics.clicks[adId]++;

        const clickData = {
            adId: adId,
            x: event.clientX,
            y: event.clientY,
            timestamp: Date.now(),
            device: this.session.device
        };

        this.sendEvent('ad_click', clickData);

        // Calculate CTR
        const impressions = this.metrics.adImpressions[adId] || 1;
        const ctr = (this.metrics.clicks[adId] / impressions) * 100;

        this.sendEvent('ctr_calculated', {
            adId: adId,
            ctr: ctr.toFixed(2),
            clicks: this.metrics.clicks[adId],
            impressions: impressions
        });

        if (this.config.debugMode) {
            console.log(`Ad click tracked: ${adId}, CTR: ${ctr.toFixed(2)}%`);
        }
    }

    /**
     * Setup engagement tracking
     */
    setupEngagementTracking() {
        let hoverStart = null;
        let currentAdId = null;

        // Track hover time
        document.addEventListener('mouseenter', (event) => {
            const adContainer = event.target.closest('.ad-container');
            if (adContainer) {
                hoverStart = Date.now();
                currentAdId = adContainer.id;
            }
        }, true);

        document.addEventListener('mouseleave', (event) => {
            const adContainer = event.target.closest('.ad-container');
            if (adContainer && hoverStart && currentAdId === adContainer.id) {
                const hoverDuration = Date.now() - hoverStart;
                this.trackHoverTime(currentAdId, hoverDuration);
                hoverStart = null;
                currentAdId = null;
            }
        }, true);

        // Track scroll depth
        this.trackScrollDepth();
    }

    /**
     * Track hover time on ads
     */
    trackHoverTime(adId, duration) {
        if (!this.metrics.hoverTime[adId]) {
            this.metrics.hoverTime[adId] = [];
        }
        this.metrics.hoverTime[adId].push(duration);

        // Calculate average hover time
        const avgHoverTime = this.metrics.hoverTime[adId].reduce((a, b) => a + b, 0) / 
                            this.metrics.hoverTime[adId].length;

        this.sendEvent('ad_hover', {
            adId: adId,
            duration: duration,
            avgHoverTime: avgHoverTime,
            timestamp: Date.now()
        });
    }

    /**
     * Track scroll depth
     */
    trackScrollDepth() {
        let maxScrollDepth = 0;
        let scrollTimeout;

        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
                const scrolled = window.scrollY;
                const scrollDepth = Math.round((scrolled / scrollHeight) * 100);

                if (scrollDepth > maxScrollDepth) {
                    maxScrollDepth = scrollDepth;
                    
                    // Track milestones
                    if ([25, 50, 75, 90, 100].includes(scrollDepth)) {
                        this.sendEvent('scroll_depth', {
                            depth: scrollDepth,
                            timestamp: Date.now()
                        });
                    }
                }
            }, 100);
        });
    }

    /**
     * Setup error tracking
     */
    setupErrorTracking() {
        window.addEventListener('aderror', (event) => {
            const adId = event.detail?.adId;
            const error = event.detail?.error;
            
            if (adId) {
                this.trackError(adId, error);
            }
        });
    }

    /**
     * Track ad error
     */
    trackError(adId, error) {
        if (!this.metrics.errorCount[adId]) {
            this.metrics.errorCount[adId] = 0;
        }
        this.metrics.errorCount[adId]++;

        this.sendEvent('ad_error', {
            adId: adId,
            error: error?.message || 'Unknown error',
            timestamp: Date.now(),
            device: this.session.device
        });

        if (this.config.debugMode) {
            console.error(`Ad error tracked: ${adId}`, error);
        }
    }

    /**
     * Setup Core Web Vitals tracking
     */
    setupWebVitalsTracking() {
        // Cumulative Layout Shift (CLS)
        let clsValue = 0;
        const clsObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (!entry.hadRecentInput) {
                    clsValue += entry.value;
                    this.webVitals.cls = clsValue;
                }
            }
        });
        
        try {
            clsObserver.observe({ type: 'layout-shift', buffered: true });
        } catch (e) {
            // Layout shift observation not supported
        }

        // First Input Delay (FID)
        const fidObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                this.webVitals.fid = entry.processingStart - entry.startTime;
            }
        });
        
        try {
            fidObserver.observe({ type: 'first-input', buffered: true });
        } catch (e) {
            // First input observation not supported
        }

        // Largest Contentful Paint (LCP)
        const lcpObserver = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            this.webVitals.lcp = lastEntry.renderTime || lastEntry.loadTime;
        });
        
        try {
            lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
        } catch (e) {
            // LCP observation not supported
        }

        // Track navigation timing
        if (window.performance && window.performance.timing) {
            const timing = window.performance.timing;
            this.webVitals.ttfb = timing.responseStart - timing.navigationStart;
            this.webVitals.fcp = timing.domContentLoadedEventEnd - timing.navigationStart;
        }
    }

    /**
     * Track ad load time
     */
    trackLoadTime(adId, loadTime) {
        if (!this.metrics.loadTimes[adId]) {
            this.metrics.loadTimes[adId] = [];
        }
        this.metrics.loadTimes[adId].push(loadTime);

        const avgLoadTime = this.metrics.loadTimes[adId].reduce((a, b) => a + b, 0) / 
                           this.metrics.loadTimes[adId].length;

        this.sendEvent('ad_load_time', {
            adId: adId,
            loadTime: loadTime,
            avgLoadTime: avgLoadTime,
            timestamp: Date.now()
        });
    }

    /**
     * Track experiment result
     */
    trackExperiment(experimentName, variant, metric, value) {
        if (!this.experiments[experimentName]) {
            this.experiments[experimentName] = {};
        }
        
        if (!this.experiments[experimentName][variant]) {
            this.experiments[experimentName][variant] = {
                impressions: 0,
                clicks: 0,
                revenue: 0,
                customMetrics: {}
            };
        }

        const experiment = this.experiments[experimentName][variant];
        
        switch (metric) {
            case 'impression':
                experiment.impressions++;
                break;
            case 'click':
                experiment.clicks++;
                break;
            case 'revenue':
                experiment.revenue += value;
                break;
            default:
                if (!experiment.customMetrics[metric]) {
                    experiment.customMetrics[metric] = [];
                }
                experiment.customMetrics[metric].push(value);
        }

        this.sendEvent('experiment_tracked', {
            experiment: experimentName,
            variant: variant,
            metric: metric,
            value: value,
            timestamp: Date.now()
        });
    }

    /**
     * Calculate performance score
     */
    calculatePerformanceScore() {
        const weights = {
            viewability: 0.3,
            ctr: 0.25,
            engagement: 0.2,
            errors: 0.15,
            webVitals: 0.1
        };

        let score = 0;

        // Viewability score (viewable/total impressions)
        const totalImpressions = Object.values(this.metrics.adImpressions).reduce((a, b) => a + b, 0);
        const totalViewable = Object.values(this.metrics.viewableImpressions).reduce((a, b) => a + b, 0);
        const viewabilityRate = totalImpressions > 0 ? (totalViewable / totalImpressions) : 0;
        score += viewabilityRate * weights.viewability * 100;

        // CTR score
        const totalClicks = Object.values(this.metrics.clicks).reduce((a, b) => a + b, 0);
        const ctr = totalImpressions > 0 ? (totalClicks / totalImpressions) : 0;
        score += Math.min(ctr * 10, 1) * weights.ctr * 100; // Cap at 10% CTR

        // Engagement score (based on hover time)
        const hasHoverData = Object.keys(this.metrics.hoverTime).length > 0;
        const avgHoverTime = hasHoverData ? 
            Object.values(this.metrics.hoverTime)
                .flat()
                .reduce((a, b) => a + b, 0) / 
            Object.values(this.metrics.hoverTime)
                .flat()
                .length : 0;
        const engagementScore = Math.min(avgHoverTime / 3000, 1); // 3 seconds = perfect
        score += engagementScore * weights.engagement * 100;

        // Error score (inverse - fewer errors = higher score)
        const totalErrors = Object.values(this.metrics.errorCount).reduce((a, b) => a + b, 0);
        const errorRate = totalImpressions > 0 ? (totalErrors / totalImpressions) : 0;
        score += (1 - Math.min(errorRate * 10, 1)) * weights.errors * 100;

        // Web Vitals score
        const clsScore = this.webVitals.cls < 0.1 ? 1 : (this.webVitals.cls < 0.25 ? 0.5 : 0);
        const fidScore = this.webVitals.fid < 100 ? 1 : (this.webVitals.fid < 300 ? 0.5 : 0);
        const lcpScore = this.webVitals.lcp < 2500 ? 1 : (this.webVitals.lcp < 4000 ? 0.5 : 0);
        const vitalsScore = (clsScore + fidScore + lcpScore) / 3;
        score += vitalsScore * weights.webVitals * 100;

        return Math.round(score);
    }

    /**
     * Get performance summary
     */
    getPerformanceSummary() {
        const totalImpressions = Object.values(this.metrics.adImpressions).reduce((a, b) => a + b, 0);
        const totalViewable = Object.values(this.metrics.viewableImpressions).reduce((a, b) => a + b, 0);
        const totalClicks = Object.values(this.metrics.clicks).reduce((a, b) => a + b, 0);
        const totalErrors = Object.values(this.metrics.errorCount).reduce((a, b) => a + b, 0);

        return {
            score: this.calculatePerformanceScore(),
            metrics: {
                pageViews: this.metrics.pageViews,
                impressions: totalImpressions,
                viewableImpressions: totalViewable,
                clicks: totalClicks,
                errors: totalErrors,
                viewabilityRate: totalImpressions > 0 ? 
                    ((totalViewable / totalImpressions) * 100).toFixed(2) + '%' : '0%',
                ctr: totalImpressions > 0 ? 
                    ((totalClicks / totalImpressions) * 100).toFixed(2) + '%' : '0%',
                errorRate: totalImpressions > 0 ? 
                    ((totalErrors / totalImpressions) * 100).toFixed(2) + '%' : '0%'
            },
            webVitals: this.webVitals,
            experiments: this.experiments,
            session: {
                ...this.session,
                duration: Date.now() - this.session.startTime
            }
        };
    }

    /**
     * Start automatic reporting
     */
    startReporting() {
        // Report periodically
        setInterval(() => {
            this.reportMetrics();
        }, this.config.reportInterval);

        // Report on page unload
        window.addEventListener('beforeunload', () => {
            this.reportMetrics();
            this.saveMetrics();
        });
    }

    /**
     * Report metrics
     */
    reportMetrics() {
        const summary = this.getPerformanceSummary();
        
        this.sendEvent('performance_report', summary);

        if (this.config.debugMode) {
            console.log('Performance Report:', summary);
        }

        // Save to localStorage
        this.saveMetrics();
    }

    /**
     * Send event to analytics
     */
    sendEvent(eventName, data) {
        if (!this.config.analyticsEnabled) return;

        // Send to Google Analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'Ad_Performance',
                event_label: data.adId || 'general',
                value: data.value || 1,
                custom_data: JSON.stringify(data)
            });
        }

        // Custom event for other tracking systems
        window.dispatchEvent(new CustomEvent('adperformance', {
            detail: {
                event: eventName,
                data: data
            }
        }));
    }

    /**
     * Reset metrics
     */
    resetMetrics() {
        this.metrics = {
            pageViews: 0,
            adImpressions: {},
            viewableImpressions: {},
            clicks: {},
            hoverTime: {},
            loadTimes: {},
            errorCount: {},
            revenue: 0,
            sessionStart: Date.now(),
            lastUpdate: Date.now()
        };
        
        this.experiments = {};
        this.saveMetrics();
    }

    /**
     * Export metrics as CSV
     */
    exportMetricsAsCSV() {
        const summary = this.getPerformanceSummary();
        const rows = [
            ['Metric', 'Value'],
            ['Performance Score', summary.score],
            ['Page Views', summary.metrics.pageViews],
            ['Total Impressions', summary.metrics.impressions],
            ['Viewable Impressions', summary.metrics.viewableImpressions],
            ['Total Clicks', summary.metrics.clicks],
            ['Total Errors', summary.metrics.errors],
            ['Viewability Rate', summary.metrics.viewabilityRate],
            ['CTR', summary.metrics.ctr],
            ['Error Rate', summary.metrics.errorRate],
            ['CLS', summary.webVitals.cls],
            ['FID', summary.webVitals.fid],
            ['LCP', summary.webVitals.lcp],
            ['Session Duration', summary.session.duration + 'ms'],
            ['Device', summary.session.device]
        ];

        const csv = rows.map(row => row.join(',')).join('\n');
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ad-performance-${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdPerformanceTracker;
}

// Auto-initialize if config is available
if (typeof APP_CONFIG !== 'undefined') {
    window.adPerformanceTracker = new AdPerformanceTracker({
        trackingEnabled: APP_CONFIG.FEATURES?.ENABLE_ANALYTICS,
        analyticsEnabled: APP_CONFIG.FEATURES?.ENABLE_ANALYTICS,
        debugMode: APP_CONFIG.APP?.DEBUG_MODE
    });
}