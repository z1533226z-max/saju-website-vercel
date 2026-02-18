/**
 * AdLoader - Optimized Google AdSense Loading System
 * Implements lazy loading, performance tracking, and revenue optimization
 */

class AdLoader {
    constructor(config = {}) {
        // Configuration
        this.config = {
            clientId: config.clientId || APP_CONFIG?.ADSENSE?.CLIENT_ID || 'ca-pub-XXXXXXXXXXXXXXXX',
            rootMargin: config.rootMargin || '200px',
            threshold: config.threshold || 0.01,
            maxAdsPerPage: config.maxAdsPerPage || 5,
            refreshInterval: config.refreshInterval || 30000, // 30 seconds
            enableAutoRefresh: config.enableAutoRefresh || false,
            enableTracking: config.enableTracking !== false,
            enableExperiments: config.enableExperiments || false
        };

        // State management
        this.loadedAds = new Set();
        this.adQueue = [];
        this.isScriptLoaded = false;
        this.observer = null;
        this.refreshTimer = null;
        this.performanceMetrics = {
            totalLoaded: 0,
            totalFailed: 0,
            averageLoadTime: 0,
            viewableImpressions: 0
        };

        // Ad unit configurations
        this.adUnits = {
            desktop: {
                topBanner: {
                    size: '728x90',
                    slot: config.slots?.topBanner || 'XXXXXXXXXX',
                    position: 'header-bottom',
                    type: 'display',
                    priority: 1
                },
                inContent: {
                    size: '336x280',
                    slot: config.slots?.inContent || 'XXXXXXXXXX',
                    position: 'results-middle',
                    type: 'display',
                    priority: 2
                },
                sidebar: {
                    size: '300x600',
                    slot: config.slots?.sidebar || 'XXXXXXXXXX',
                    position: 'sidebar-top',
                    type: 'display',
                    priority: 3
                }
            },
            mobile: {
                topBanner: {
                    size: '320x50',
                    slot: config.slots?.mobileBanner || 'XXXXXXXXXX',
                    position: 'header-bottom',
                    type: 'banner',
                    priority: 1
                },
                inFeed: {
                    size: 'fluid',
                    slot: config.slots?.inFeed || 'XXXXXXXXXX',
                    position: 'after-input',
                    type: 'in-feed',
                    priority: 2
                },
                anchor: {
                    size: '320x50',
                    slot: config.slots?.anchor || 'XXXXXXXXXX',
                    position: 'bottom-fixed',
                    type: 'anchor',
                    priority: 3
                }
            },
            tablet: {
                topBanner: {
                    size: '468x60',
                    slot: config.slots?.tabletBanner || 'XXXXXXXXXX',
                    position: 'header-bottom',
                    type: 'display',
                    priority: 1
                },
                inContent: {
                    size: '300x250',
                    slot: config.slots?.tabletContent || 'XXXXXXXXXX',
                    position: 'results-middle',
                    type: 'display',
                    priority: 2
                }
            }
        };

        // Initialize
        this.init();
    }

    /**
     * Initialize the AdLoader
     */
    async init() {
        try {
            // Load AdSense script if not already loaded
            await this.loadAdSenseScript();
            
            // Setup intersection observer for lazy loading
            this.setupObserver();
            
            // Setup device detection and responsive handling
            this.setupResponsiveHandling();
            
            // Setup performance tracking
            if (this.config.enableTracking) {
                this.setupPerformanceTracking();
            }
            
            // Setup experiments if enabled
            if (this.config.enableExperiments) {
                this.setupExperiments();
            }
            
            // Register existing ad containers
            this.registerExistingAds();
            
            // Setup auto-refresh if enabled
            if (this.config.enableAutoRefresh) {
                this.setupAutoRefresh();
            }
            
            console.log('AdLoader initialized successfully');
        } catch (error) {
            console.error('Failed to initialize AdLoader:', error);
            this.trackError('initialization_failed', error);
        }
    }

    /**
     * Load Google AdSense script
     */
    async loadAdSenseScript() {
        if (this.isScriptLoaded || window.adsbygoogle) {
            this.isScriptLoaded = true;
            return Promise.resolve();
        }

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.async = true;
            script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js';
            script.setAttribute('data-ad-client', this.config.clientId);
            
            script.onload = () => {
                this.isScriptLoaded = true;
                console.log('AdSense script loaded');
                resolve();
            };
            
            script.onerror = (error) => {
                console.error('Failed to load AdSense script:', error);
                reject(error);
            };
            
            document.head.appendChild(script);
        });
    }

    /**
     * Setup Intersection Observer for lazy loading
     */
    setupObserver() {
        const observerOptions = {
            rootMargin: this.config.rootMargin,
            threshold: this.config.threshold
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.loadedAds.has(entry.target.id)) {
                    this.loadAd(entry.target);
                }
            });
        }, observerOptions);
    }

    /**
     * Setup responsive handling
     */
    setupResponsiveHandling() {
        this.currentDevice = this.detectDevice();
        
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                const newDevice = this.detectDevice();
                if (newDevice !== this.currentDevice) {
                    this.currentDevice = newDevice;
                    this.handleDeviceChange();
                }
            }, 250);
        });
    }

    /**
     * Detect current device type
     */
    detectDevice() {
        const width = window.innerWidth;
        if (width < 768) return 'mobile';
        if (width < 1024) return 'tablet';
        return 'desktop';
    }

    /**
     * Handle device change
     */
    handleDeviceChange() {
        console.log(`Device changed to: ${this.currentDevice}`);
        
        // Update ad sizes for new device
        document.querySelectorAll('.ad-container').forEach(container => {
            if (!this.loadedAds.has(container.id)) {
                this.updateAdConfiguration(container);
            }
        });
        
        // Track device change
        this.trackEvent('device_change', {
            from: this.previousDevice,
            to: this.currentDevice
        });
        
        this.previousDevice = this.currentDevice;
    }

    /**
     * Update ad configuration for current device
     */
    updateAdConfiguration(container) {
        const adUnit = container.dataset.adUnit;
        const deviceConfig = this.adUnits[this.currentDevice];
        
        if (deviceConfig && deviceConfig[adUnit]) {
            const config = deviceConfig[adUnit];
            container.dataset.adSize = config.size;
            container.dataset.adSlot = config.slot;
            container.dataset.adType = config.type;
            
            // Reserve space to prevent CLS
            this.reserveAdSpace(container, config.size);
        }
    }

    /**
     * Reserve ad space to prevent Cumulative Layout Shift
     */
    reserveAdSpace(container, size) {
        if (size && size !== 'fluid') {
            const [width, height] = size.split('x');
            container.style.minHeight = `${height}px`;
            container.style.minWidth = `${width}px`;
            container.style.backgroundColor = 'var(--color-bg-secondary, #13121A)';
            container.style.display = 'flex';
            container.style.alignItems = 'center';
            container.style.justifyContent = 'center';
            
            // Add loading placeholder
            if (!container.querySelector('.ad-placeholder')) {
                const placeholder = document.createElement('div');
                placeholder.className = 'ad-placeholder';
                placeholder.textContent = '� \)...';
                placeholder.style.color = 'var(--color-text-muted, #666)';
                placeholder.style.fontSize = '12px';
                container.appendChild(placeholder);
            }
        }
    }

    /**
     * Register existing ad containers
     */
    registerExistingAds() {
        const adContainers = document.querySelectorAll('.ad-container');
        adContainers.forEach(container => {
            this.registerAd(container);
        });
    }

    /**
     * Register an ad container for lazy loading
     */
    registerAd(element) {
        if (!element.id) {
            element.id = `ad-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        }
        
        // Update configuration for current device
        this.updateAdConfiguration(element);
        
        // Check if we've reached max ads limit
        if (this.loadedAds.size >= this.config.maxAdsPerPage) {
            this.adQueue.push(element);
            return;
        }
        
        // Observe for lazy loading
        if (this.observer) {
            this.observer.observe(element);
        }
    }

    /**
     * Load an ad
     */
    async loadAd(element) {
        const startTime = performance.now();
        
        try {
            // Mark as loaded to prevent duplicate loading
            this.loadedAds.add(element.id);
            
            // Get ad configuration
            const adConfig = this.getAdConfig(element);
            
            // Remove placeholder
            const placeholder = element.querySelector('.ad-placeholder');
            if (placeholder) {
                placeholder.remove();
            }
            
            // Create ad element
            const ins = document.createElement('ins');
            ins.className = 'adsbygoogle';
            ins.style.display = 'block';
            
            // Set ad parameters
            ins.setAttribute('data-ad-client', this.config.clientId);
            ins.setAttribute('data-ad-slot', adConfig.slot);
            
            // Set size based on type
            if (adConfig.size === 'fluid') {
                ins.setAttribute('data-ad-format', 'fluid');
                ins.setAttribute('data-ad-layout-key', '-fb+5w+4e-db+86');
            } else if (adConfig.type === 'in-feed') {
                ins.setAttribute('data-ad-format', 'auto');
                ins.setAttribute('data-full-width-responsive', 'true');
            } else {
                const [width, height] = adConfig.size.split('x');
                ins.style.width = `${width}px`;
                ins.style.height = `${height}px`;
            }
            
            // Append to container
            element.appendChild(ins);
            
            // Push to AdSense
            (window.adsbygoogle = window.adsbygoogle || []).push({});
            
            // Track success
            const loadTime = performance.now() - startTime;
            this.trackAdLoad(element.id, adConfig, loadTime);
            
            // Update metrics
            this.performanceMetrics.totalLoaded++;
            this.updateAverageLoadTime(loadTime);
            
            // Stop observing
            if (this.observer) {
                this.observer.unobserve(element);
            }
            
            // Process queue if any
            this.processQueue();
            
        } catch (error) {
            console.error('Failed to load ad:', error);
            this.performanceMetrics.totalFailed++;
            this.trackError('ad_load_failed', {
                adId: element.id,
                error: error.message
            });
            
            // Retry logic
            this.handleLoadFailure(element);
        }
    }

    /**
     * Get ad configuration for element
     */
    getAdConfig(element) {
        const adUnit = element.dataset.adUnit || 'default';
        const deviceConfig = this.adUnits[this.currentDevice];
        
        return {
            slot: element.dataset.adSlot || deviceConfig[adUnit]?.slot || 'XXXXXXXXXX',
            size: element.dataset.adSize || deviceConfig[adUnit]?.size || '300x250',
            type: element.dataset.adType || deviceConfig[adUnit]?.type || 'display',
            unit: adUnit
        };
    }

    /**
     * Process queued ads
     */
    processQueue() {
        if (this.adQueue.length > 0 && this.loadedAds.size < this.config.maxAdsPerPage) {
            const nextAd = this.adQueue.shift();
            this.registerAd(nextAd);
        }
    }

    /**
     * Handle ad load failure
     */
    handleLoadFailure(element) {
        const retryCount = parseInt(element.dataset.retryCount || '0');
        
        if (retryCount < 3) {
            element.dataset.retryCount = (retryCount + 1).toString();
            
            // Retry after delay
            setTimeout(() => {
                this.loadedAds.delete(element.id);
                this.loadAd(element);
            }, 5000 * (retryCount + 1)); // Exponential backoff
        } else {
            // Show fallback content
            this.showFallbackContent(element);
        }
    }

    /**
     * Show fallback content for failed ads
     */
    showFallbackContent(element) {
        element.innerHTML = `
            <div class="ad-fallback" style="
                padding: 20px;
                text-align: center;
                background: var(--color-bg-secondary, #13121A);
                border: 1px solid var(--color-border, #2A2940);
                border-radius: 4px;
            ">
                <p style="color: var(--color-text-muted, #666); margin: 0;">�| ��,  Ƶ��</p>
            </div>
        `;
    }

    /**
     * Setup performance tracking
     */
    setupPerformanceTracking() {
        // Track viewability
        this.setupViewabilityTracking();
        
        // Track clicks
        this.setupClickTracking();
        
        // Track revenue events
        this.setupRevenueTracking();
        
        // Send metrics periodically
        setInterval(() => {
            this.sendPerformanceMetrics();
        }, 60000); // Every minute
    }

    /**
     * Setup viewability tracking
     */
    setupViewabilityTracking() {
        const viewabilityObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.intersectionRatio >= 0.5) {
                    const adId = entry.target.id;
                    
                    if (!entry.target.dataset.viewTracked) {
                        entry.target.dataset.viewTracked = 'true';
                        this.performanceMetrics.viewableImpressions++;
                        
                        this.trackEvent('viewable_impression', {
                            adId: adId,
                            viewTime: entry.time,
                            intersectionRatio: entry.intersectionRatio
                        });
                    }
                }
            });
        }, { threshold: [0.5] });
        
        // Observe loaded ads
        setInterval(() => {
            this.loadedAds.forEach(adId => {
                const element = document.getElementById(adId);
                if (element && !element.dataset.viewObserved) {
                    viewabilityObserver.observe(element);
                    element.dataset.viewObserved = 'true';
                }
            });
        }, 1000);
    }

    /**
     * Setup click tracking
     */
    setupClickTracking() {
        document.addEventListener('click', (event) => {
            const adContainer = event.target.closest('.ad-container');
            
            if (adContainer && this.loadedAds.has(adContainer.id)) {
                this.trackEvent('ad_click', {
                    adId: adContainer.id,
                    adUnit: adContainer.dataset.adUnit,
                    x: event.clientX,
                    y: event.clientY
                });
            }
        }, true);
    }

    /**
     * Setup revenue tracking
     */
    setupRevenueTracking() {
        // Listen for AdSense events (if available)
        window.addEventListener('adsense-loaded', (event) => {
            this.trackEvent('ad_revenue', {
                adId: event.detail.adId,
                revenue: event.detail.revenue
            });
        });
    }

    /**
     * Setup auto-refresh for ads
     */
    setupAutoRefresh() {
        this.refreshTimer = setInterval(() => {
            this.refreshAds();
        }, this.config.refreshInterval);
    }

    /**
     * Refresh ads
     */
    refreshAds() {
        // Only refresh viewable ads
        const viewableAds = Array.from(this.loadedAds).filter(adId => {
            const element = document.getElementById(adId);
            return element && element.dataset.viewTracked === 'true';
        });
        
        viewableAds.forEach(adId => {
            const element = document.getElementById(adId);
            if (element) {
                // Clear and reload
                element.innerHTML = '';
                this.loadedAds.delete(adId);
                delete element.dataset.viewTracked;
                this.loadAd(element);
            }
        });
        
        this.trackEvent('ads_refreshed', {
            count: viewableAds.length
        });
    }

    /**
     * Setup A/B testing experiments
     */
    setupExperiments() {
        this.experiments = {
            placementTest: {
                name: 'ad_placement_optimization',
                variants: ['control', 'above_fold', 'sticky'],
                allocation: [0.34, 0.33, 0.33]
            },
            sizeTest: {
                name: 'ad_size_optimization',
                variants: ['standard', 'responsive', 'native'],
                allocation: [0.34, 0.33, 0.33]
            }
        };
        
        // Run experiments
        this.runExperiments();
    }

    /**
     * Run A/B testing experiments
     */
    runExperiments() {
        Object.values(this.experiments).forEach(experiment => {
            const variant = this.selectVariant(experiment);
            this.applyExperimentVariant(experiment.name, variant);
            
            // Track experiment
            this.trackEvent('experiment_activated', {
                experiment: experiment.name,
                variant: variant
            });
        });
    }

    /**
     * Select experiment variant
     */
    selectVariant(experiment) {
        const random = Math.random();
        let cumulative = 0;
        
        for (let i = 0; i < experiment.variants.length; i++) {
            cumulative += experiment.allocation[i];
            if (random < cumulative) {
                return experiment.variants[i];
            }
        }
        
        return experiment.variants[0];
    }

    /**
     * Apply experiment variant
     */
    applyExperimentVariant(experimentName, variant) {
        // Apply variant-specific changes
        switch (experimentName) {
            case 'ad_placement_optimization':
                this.applyPlacementVariant(variant);
                break;
            case 'ad_size_optimization':
                this.applySizeVariant(variant);
                break;
        }
    }

    /**
     * Apply placement variant
     */
    applyPlacementVariant(variant) {
        switch (variant) {
            case 'above_fold':
                // Prioritize above-fold ads
                this.config.rootMargin = '500px';
                break;
            case 'sticky':
                // Make certain ads sticky
                document.querySelectorAll('.ad-container[data-position="sidebar"]').forEach(ad => {
                    ad.style.position = 'sticky';
                    ad.style.top = '100px';
                });
                break;
        }
    }

    /**
     * Apply size variant
     */
    applySizeVariant(variant) {
        switch (variant) {
            case 'responsive':
                // Use responsive ad sizes
                document.querySelectorAll('.ad-container').forEach(ad => {
                    ad.dataset.adSize = 'fluid';
                });
                break;
            case 'native':
                // Use native ad formats
                document.querySelectorAll('.ad-container').forEach(ad => {
                    ad.dataset.adType = 'in-feed';
                });
                break;
        }
    }

    /**
     * Track ad load event
     */
    trackAdLoad(adId, config, loadTime) {
        this.trackEvent('ad_loaded', {
            adId: adId,
            adUnit: config.unit,
            adSize: config.size,
            adType: config.type,
            loadTime: Math.round(loadTime),
            device: this.currentDevice
        });
    }

    /**
     * Track event
     */
    trackEvent(eventName, data = {}) {
        if (!this.config.enableTracking) return;
        
        // Send to Google Analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'Advertising',
                event_label: data.adId || data.adUnit || 'unknown',
                value: data.value || 1,
                custom_data: JSON.stringify(data)
            });
        }
        
        // Log to console in debug mode
        if (APP_CONFIG?.APP?.DEBUG_MODE) {
            console.log(`[AdLoader Event] ${eventName}:`, data);
        }
    }

    /**
     * Track error
     */
    trackError(errorType, data = {}) {
        this.trackEvent('ad_error', {
            errorType: errorType,
            ...data
        });
    }

    /**
     * Update average load time
     */
    updateAverageLoadTime(loadTime) {
        const totalLoads = this.performanceMetrics.totalLoaded;
        const currentAverage = this.performanceMetrics.averageLoadTime;
        
        this.performanceMetrics.averageLoadTime = 
            (currentAverage * (totalLoads - 1) + loadTime) / totalLoads;
    }

    /**
     * Send performance metrics
     */
    sendPerformanceMetrics() {
        this.trackEvent('performance_metrics', {
            ...this.performanceMetrics,
            timestamp: Date.now()
        });
    }

    /**
     * Get current performance metrics
     */
    getMetrics() {
        return {
            ...this.performanceMetrics,
            loadedAds: this.loadedAds.size,
            queuedAds: this.adQueue.length,
            device: this.currentDevice
        };
    }

    /**
     * Manually trigger ad loading for specific element
     */
    forceLoadAd(elementOrId) {
        const element = typeof elementOrId === 'string' 
            ? document.getElementById(elementOrId)
            : elementOrId;
            
        if (element) {
            this.loadAd(element);
        }
    }

    /**
     * Pause auto-refresh
     */
    pauseAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    /**
     * Resume auto-refresh
     */
    resumeAutoRefresh() {
        if (!this.refreshTimer && this.config.enableAutoRefresh) {
            this.setupAutoRefresh();
        }
    }

    /**
     * Destroy the AdLoader instance
     */
    destroy() {
        // Stop observers
        if (this.observer) {
            this.observer.disconnect();
        }
        
        // Clear timers
        this.pauseAutoRefresh();
        
        // Clear state
        this.loadedAds.clear();
        this.adQueue = [];
        
        console.log('AdLoader destroyed');
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdLoader;
}

// Auto-initialize if config is available
if (typeof APP_CONFIG !== 'undefined' && APP_CONFIG.FEATURES?.ENABLE_ADS) {
    window.adLoader = new AdLoader({
        clientId: APP_CONFIG.ADSENSE.CLIENT_ID,
        slots: APP_CONFIG.ADSENSE.SLOTS,
        enableTracking: APP_CONFIG.FEATURES.ENABLE_ANALYTICS,
        enableAutoRefresh: true,
        enableExperiments: true
    });
}