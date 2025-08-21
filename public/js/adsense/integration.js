/**
 * AdSense Integration Module
 * Coordinates AdLoader, Performance Tracker, and A/B Testing
 */

class AdSenseIntegration {
    constructor(config = {}) {
        this.config = {
            enabled: config.enabled !== false,
            debugMode: config.debugMode || false,
            ...config
        };

        // Component references
        this.adLoader = null;
        this.performanceTracker = null;
        this.abTesting = null;

        // Integration state
        this.initialized = false;
        this.activeExperiments = [];

        // Initialize
        this.init();
    }

    /**
     * Initialize AdSense integration
     */
    async init() {
        if (!this.config.enabled) {
            console.log('AdSense integration disabled');
            return;
        }

        try {
            // Initialize components
            await this.initializeComponents();

            // Setup integrations
            this.setupIntegrations();

            // Apply A/B test variants
            this.applyExperimentVariants();

            // Start monitoring
            this.startMonitoring();

            this.initialized = true;
            console.log('AdSense integration initialized successfully');

            // Dispatch ready event
            window.dispatchEvent(new CustomEvent('adsense-ready', {
                detail: { integration: this }
            }));

        } catch (error) {
            console.error('Failed to initialize AdSense integration:', error);
            this.handleInitializationError(error);
        }
    }

    /**
     * Initialize all components
     */
    async initializeComponents() {
        // Get or create AdLoader instance
        if (window.adLoader) {
            this.adLoader = window.adLoader;
        } else {
            const AdLoader = window.AdLoader || (await import('./ad-loader.js')).default;
            this.adLoader = new AdLoader({
                clientId: this.config.clientId || APP_CONFIG?.ADSENSE?.CLIENT_ID,
                slots: this.config.slots || APP_CONFIG?.ADSENSE?.SLOTS,
                enableTracking: true,
                enableAutoRefresh: false, // Will be controlled by A/B test
                enableExperiments: false // Handled by abTesting
            });
            window.adLoader = this.adLoader;
        }

        // Get or create Performance Tracker
        if (window.adPerformanceTracker) {
            this.performanceTracker = window.adPerformanceTracker;
        } else {
            const AdPerformanceTracker = window.AdPerformanceTracker || 
                (await import('./performance-tracker.js')).default;
            this.performanceTracker = new AdPerformanceTracker({
                trackingEnabled: true,
                analyticsEnabled: APP_CONFIG?.FEATURES?.ENABLE_ANALYTICS,
                debugMode: this.config.debugMode
            });
            window.adPerformanceTracker = this.performanceTracker;
        }

        // Get or create A/B Testing Framework
        if (window.abTesting) {
            this.abTesting = window.abTesting;
        } else {
            const ABTestingFramework = window.ABTestingFramework || 
                (await import('./ab-testing.js')).default;
            this.abTesting = new ABTestingFramework({
                enabled: true,
                analyticsEnabled: APP_CONFIG?.FEATURES?.ENABLE_ANALYTICS,
                debugMode: this.config.debugMode
            });
            window.abTesting = this.abTesting;
        }
    }

    /**
     * Setup integrations between components
     */
    setupIntegrations() {
        // Connect AdLoader events to Performance Tracker
        this.setupAdLoaderTracking();

        // Connect A/B Testing to Performance Tracker
        this.setupExperimentTracking();

        // Setup cross-component error handling
        this.setupErrorHandling();
    }

    /**
     * Setup AdLoader event tracking
     */
    setupAdLoaderTracking() {
        // Track ad load events
        window.addEventListener('ad_loaded', (event) => {
            const { adId, loadTime, adUnit, adSize } = event.detail;
            
            // Track in performance tracker
            this.performanceTracker.trackImpression(adId);
            this.performanceTracker.trackLoadTime(adId, loadTime);

            // Track in A/B testing
            this.activeExperiments.forEach(expId => {
                this.abTesting.trackMetric(expId, 'ad_loads', 1);
                this.abTesting.trackMetric(expId, 'load_time', loadTime);
            });

            if (this.config.debugMode) {
                console.log('Ad loaded and tracked:', adId, loadTime);
            }
        });

        // Track viewable impressions
        window.addEventListener('viewable_impression', (event) => {
            const { adId } = event.detail;
            
            // Track in A/B testing
            this.activeExperiments.forEach(expId => {
                this.abTesting.trackMetric(expId, 'viewability', 1);
            });
        });

        // Track clicks
        window.addEventListener('ad_click', (event) => {
            const { adId } = event.detail;
            
            // Track conversions in A/B testing
            this.activeExperiments.forEach(expId => {
                this.abTesting.trackConversion(expId);
                this.abTesting.trackMetric(expId, 'ctr', 1);
            });
        });

        // Track errors
        window.addEventListener('ad_error', (event) => {
            const { adId, errorType } = event.detail;
            
            // Track in A/B testing
            this.activeExperiments.forEach(expId => {
                this.abTesting.trackMetric(expId, 'errors', 1);
            });
        });
    }

    /**
     * Setup experiment tracking
     */
    setupExperimentTracking() {
        // Get active experiments
        this.activeExperiments = this.abTesting.getActiveExperiments()
            .map(exp => exp.id);

        // Track experiment participation
        window.addEventListener('experiment_participation', (event) => {
            const { experiment, variant } = event.detail;
            
            if (this.config.debugMode) {
                console.log(`User assigned to ${variant} variant of ${experiment}`);
            }
        });

        // Track experiment metrics
        window.addEventListener('experiment_metric', (event) => {
            const { experiment, metric, value } = event.detail;
            
            // Also track in performance tracker for correlation
            this.performanceTracker.trackExperiment(
                experiment,
                this.abTesting.userAssignments[experiment],
                metric,
                value
            );
        });
    }

    /**
     * Apply experiment variants
     */
    applyExperimentVariants() {
        // Apply placement experiment
        const placementVariant = this.abTesting.getUserVariant('ad_placement');
        if (placementVariant) {
            const config = this.abTesting.getVariantConfig('ad_placement', placementVariant);
            if (config) {
                this.applyPlacementConfig(config);
            }
        }

        // Apply size experiment
        const sizeVariant = this.abTesting.getUserVariant('ad_size');
        if (sizeVariant) {
            const config = this.abTesting.getVariantConfig('ad_size', sizeVariant);
            if (config) {
                this.applySizeConfig(config);
            }
        }

        // Apply format experiment
        const formatVariant = this.abTesting.getUserVariant('ad_format');
        if (formatVariant) {
            const config = this.abTesting.getVariantConfig('ad_format', formatVariant);
            if (config) {
                this.applyFormatConfig(config);
            }
        }

        // Apply refresh experiment
        const refreshVariant = this.abTesting.getUserVariant('refresh_strategy');
        if (refreshVariant) {
            const config = this.abTesting.getVariantConfig('refresh_strategy', refreshVariant);
            if (config) {
                this.applyRefreshConfig(config);
            }
        }

        // Apply lazy loading experiment
        const lazyVariant = this.abTesting.getUserVariant('lazy_loading');
        if (lazyVariant) {
            const config = this.abTesting.getVariantConfig('lazy_loading', lazyVariant);
            if (config) {
                this.applyLazyLoadConfig(config);
            }
        }
    }

    /**
     * Apply placement configuration
     */
    applyPlacementConfig(config) {
        // Update ad container positions
        Object.entries(config).forEach(([adUnit, position]) => {
            const container = document.querySelector(`[data-ad-unit="${adUnit}"]`);
            if (container) {
                container.dataset.position = position;
            }
        });
    }

    /**
     * Apply size configuration
     */
    applySizeConfig(config) {
        const device = this.adLoader.detectDevice();
        const sizes = config[device];
        
        if (sizes) {
            Object.entries(sizes).forEach(([type, size]) => {
                const containers = document.querySelectorAll(`[data-ad-type="${type}"]`);
                containers.forEach(container => {
                    container.dataset.adSize = size;
                });
            });
        }
    }

    /**
     * Apply format configuration
     */
    applyFormatConfig(config) {
        if (config.format === 'mixed') {
            // Enable native ads for in-feed positions
            document.querySelectorAll('[data-position*="feed"]').forEach(container => {
                container.dataset.adType = 'in-feed';
                container.classList.add('native-ad');
            });
        }
    }

    /**
     * Apply refresh configuration
     */
    applyRefreshConfig(config) {
        if (config.refreshEnabled) {
            this.adLoader.config.enableAutoRefresh = true;
            this.adLoader.config.refreshInterval = config.refreshInterval;
            
            if (config.viewableOnly) {
                // Modify refresh logic to only refresh viewable ads
                this.adLoader.refreshAds = () => {
                    const viewableAds = Array.from(this.adLoader.loadedAds).filter(adId => {
                        const element = document.getElementById(adId);
                        return element && element.dataset.viewTracked === 'true';
                    });
                    
                    viewableAds.forEach(adId => {
                        const element = document.getElementById(adId);
                        if (element) {
                            element.innerHTML = '';
                            this.adLoader.loadedAds.delete(adId);
                            delete element.dataset.viewTracked;
                            this.adLoader.loadAd(element);
                        }
                    });
                };
            }
            
            this.adLoader.setupAutoRefresh();
        }
    }

    /**
     * Apply lazy loading configuration
     */
    applyLazyLoadConfig(config) {
        if (config.lazyLoad === false) {
            // Load all ads immediately
            document.querySelectorAll('.ad-container').forEach(container => {
                this.adLoader.forceLoadAd(container);
            });
        } else {
            // Update lazy loading margin
            this.adLoader.config.rootMargin = config.rootMargin;
            // Recreate observer with new config
            this.adLoader.setupObserver();
        }
    }

    /**
     * Setup error handling
     */
    setupErrorHandling() {
        // Global error handler for ad-related errors
        window.addEventListener('error', (event) => {
            if (event.message && event.message.includes('adsbygoogle')) {
                this.handleAdError(event);
            }
        });

        // Handle ad load failures
        window.addEventListener('ad_load_failed', (event) => {
            this.handleAdLoadFailure(event.detail);
        });
    }

    /**
     * Handle ad error
     */
    handleAdError(error) {
        console.error('Ad error detected:', error);
        
        // Track error
        this.performanceTracker.trackError('global', error);
        
        // Notify A/B testing
        this.activeExperiments.forEach(expId => {
            this.abTesting.trackMetric(expId, 'errors', 1);
        });
    }

    /**
     * Handle ad load failure
     */
    handleAdLoadFailure(detail) {
        const { adId, error } = detail;
        
        console.error(`Ad load failed for ${adId}:`, error);
        
        // Attempt recovery
        setTimeout(() => {
            const element = document.getElementById(adId);
            if (element && !element.querySelector('.ad-fallback')) {
                this.adLoader.forceLoadAd(element);
            }
        }, 5000);
    }

    /**
     * Handle initialization error
     */
    handleInitializationError(error) {
        // Fallback to basic ad loading
        console.warn('Falling back to basic ad loading');
        
        // Load AdSense script directly
        const script = document.createElement('script');
        script.async = true;
        script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js';
        script.setAttribute('data-ad-client', this.config.clientId || APP_CONFIG?.ADSENSE?.CLIENT_ID);
        document.head.appendChild(script);
        
        // Initialize ads manually
        script.onload = () => {
            document.querySelectorAll('.ad-container').forEach(container => {
                try {
                    (window.adsbygoogle = window.adsbygoogle || []).push({});
                } catch (e) {
                    console.error('Failed to initialize ad:', e);
                }
            });
        };
    }

    /**
     * Start monitoring
     */
    startMonitoring() {
        // Monitor performance every minute
        setInterval(() => {
            this.checkPerformance();
        }, 60000);

        // Monitor experiments
        setInterval(() => {
            this.checkExperiments();
        }, 300000); // Every 5 minutes
    }

    /**
     * Check performance
     */
    checkPerformance() {
        const summary = this.performanceTracker.getPerformanceSummary();
        
        if (this.config.debugMode) {
            console.log('Performance Summary:', summary);
        }

        // Alert if performance is poor
        if (summary.score < 50) {
            console.warn('Poor ad performance detected:', summary.score);
            this.optimizePerformance();
        }

        // Track in A/B testing
        this.activeExperiments.forEach(expId => {
            this.abTesting.trackMetric(expId, 'performance_score', summary.score);
        });
    }

    /**
     * Check experiments
     */
    checkExperiments() {
        this.activeExperiments.forEach(expId => {
            const status = this.abTesting.getExperimentStatus(expId);
            
            if (status && status.results && status.results.winner) {
                if (status.results.winner.status === 'winner') {
                    console.log(`Experiment ${expId} has a winner:`, status.results.winner);
                    
                    // Auto-apply winner if confidence is high
                    if (status.results.significance && status.results.significance.confidence >= 95) {
                        this.abTesting.applyWinningVariant(expId);
                        console.log(`Applied winning variant for ${expId}`);
                    }
                }
            }
        });
    }

    /**
     * Optimize performance
     */
    optimizePerformance() {
        // Pause auto-refresh if enabled
        if (this.adLoader.config.enableAutoRefresh) {
            this.adLoader.pauseAutoRefresh();
            
            // Resume after 5 minutes
            setTimeout(() => {
                this.adLoader.resumeAutoRefresh();
            }, 300000);
        }

        // Reduce number of ads if too many
        if (this.adLoader.loadedAds.size > 3) {
            // Remove least viewable ads
            const summary = this.performanceTracker.getPerformanceSummary();
            const leastViewable = Object.entries(summary.metrics.viewableImpressions)
                .sort((a, b) => a[1] - b[1])
                .slice(0, 2)
                .map(([adId]) => adId);
            
            leastViewable.forEach(adId => {
                const element = document.getElementById(adId);
                if (element) {
                    element.innerHTML = '';
                    this.adLoader.loadedAds.delete(adId);
                }
            });
        }
    }

    /**
     * Get integration status
     */
    getStatus() {
        return {
            initialized: this.initialized,
            components: {
                adLoader: !!this.adLoader,
                performanceTracker: !!this.performanceTracker,
                abTesting: !!this.abTesting
            },
            performance: this.performanceTracker ? 
                this.performanceTracker.getPerformanceSummary() : null,
            experiments: this.activeExperiments.map(expId => 
                this.abTesting.getExperimentStatus(expId)
            ),
            adsLoaded: this.adLoader ? this.adLoader.loadedAds.size : 0
        };
    }

    /**
     * Export all data
     */
    exportData() {
        const data = {
            timestamp: Date.now(),
            status: this.getStatus(),
            performance: this.performanceTracker ? 
                this.performanceTracker.getPerformanceSummary() : null,
            experiments: this.abTesting ? 
                Object.keys(this.abTesting.experiments).map(expId => 
                    this.abTesting.calculateResults(expId)
                ) : []
        };

        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `adsense-data-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Destroy integration
     */
    destroy() {
        // Stop monitoring
        clearInterval(this.monitoringInterval);
        clearInterval(this.experimentInterval);

        // Destroy components
        if (this.adLoader) {
            this.adLoader.destroy();
        }

        // Reset state
        this.initialized = false;
        this.activeExperiments = [];

        console.log('AdSense integration destroyed');
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdSenseIntegration;
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.adSenseIntegration = new AdSenseIntegration({
            enabled: APP_CONFIG?.FEATURES?.ENABLE_ADS,
            clientId: APP_CONFIG?.ADSENSE?.CLIENT_ID,
            slots: APP_CONFIG?.ADSENSE?.SLOTS,
            debugMode: APP_CONFIG?.APP?.DEBUG_MODE
        });
    });
} else {
    // DOM already loaded
    window.adSenseIntegration = new AdSenseIntegration({
        enabled: APP_CONFIG?.FEATURES?.ENABLE_ADS,
        clientId: APP_CONFIG?.ADSENSE?.CLIENT_ID,
        slots: APP_CONFIG?.ADSENSE?.SLOTS,
        debugMode: APP_CONFIG?.APP?.DEBUG_MODE
    });
}