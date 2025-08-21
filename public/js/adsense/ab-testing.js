/**
 * A/B Testing Framework for AdSense Optimization
 * Manages experiments for ad placement, size, and format optimization
 */

class ABTestingFramework {
    constructor(config = {}) {
        this.config = {
            enabled: config.enabled !== false,
            cookieName: config.cookieName || 'ab_experiments',
            cookieDuration: config.cookieDuration || 30, // days
            debugMode: config.debugMode || false,
            analyticsEnabled: config.analyticsEnabled !== false
        };

        // Active experiments
        this.experiments = {};

        // User assignments
        this.userAssignments = {};

        // Results storage
        this.results = {
            experiments: {},
            timestamp: Date.now()
        };

        // Initialize
        this.init();
    }

    /**
     * Initialize the A/B testing framework
     */
    init() {
        if (!this.config.enabled) return;

        // Load user assignments from cookie
        this.loadUserAssignments();

        // Setup default experiments
        this.setupDefaultExperiments();

        // Load previous results
        this.loadResults();

        console.log('A/B Testing Framework initialized');
    }

    /**
     * Setup default experiments
     */
    setupDefaultExperiments() {
        // Ad placement experiment
        this.createExperiment('ad_placement', {
            name: 'Ad Placement Optimization',
            description: 'Test different ad placements for better engagement',
            variants: [
                {
                    id: 'control',
                    name: 'Standard Placement',
                    weight: 0.5,
                    config: {
                        topBanner: 'header-bottom',
                        inContent: 'results-middle',
                        sidebar: 'sidebar-top'
                    }
                },
                {
                    id: 'above_fold',
                    name: 'Above Fold Focus',
                    weight: 0.5,
                    config: {
                        topBanner: 'header-top',
                        inContent: 'input-bottom',
                        sidebar: 'hero-side'
                    }
                }
            ],
            metrics: ['viewability', 'ctr', 'revenue'],
            duration: 7 // days
        });

        // Ad size experiment
        this.createExperiment('ad_size', {
            name: 'Ad Size Optimization',
            description: 'Test different ad sizes for better performance',
            variants: [
                {
                    id: 'standard',
                    name: 'Standard Sizes',
                    weight: 0.34,
                    config: {
                        desktop: { banner: '728x90', display: '336x280' },
                        mobile: { banner: '320x50', display: '300x250' }
                    }
                },
                {
                    id: 'responsive',
                    name: 'Responsive Ads',
                    weight: 0.33,
                    config: {
                        desktop: { banner: 'fluid', display: 'fluid' },
                        mobile: { banner: 'fluid', display: 'fluid' }
                    }
                },
                {
                    id: 'large',
                    name: 'Large Format',
                    weight: 0.33,
                    config: {
                        desktop: { banner: '970x90', display: '300x600' },
                        mobile: { banner: '320x100', display: '336x280' }
                    }
                }
            ],
            metrics: ['viewability', 'ctr', 'revenue', 'cls'],
            duration: 14 // days
        });

        // Ad format experiment
        this.createExperiment('ad_format', {
            name: 'Ad Format Testing',
            description: 'Test display vs native ad formats',
            variants: [
                {
                    id: 'display_only',
                    name: 'Display Ads Only',
                    weight: 0.5,
                    config: {
                        format: 'display',
                        style: 'standard'
                    }
                },
                {
                    id: 'native_mix',
                    name: 'Native + Display Mix',
                    weight: 0.5,
                    config: {
                        format: 'mixed',
                        style: 'native-infeed'
                    }
                }
            ],
            metrics: ['engagement', 'ctr', 'bounce_rate'],
            duration: 7 // days
        });

        // Refresh strategy experiment
        this.createExperiment('refresh_strategy', {
            name: 'Ad Refresh Strategy',
            description: 'Test different refresh intervals',
            variants: [
                {
                    id: 'no_refresh',
                    name: 'No Refresh',
                    weight: 0.25,
                    config: {
                        refreshEnabled: false
                    }
                },
                {
                    id: 'refresh_30s',
                    name: '30 Second Refresh',
                    weight: 0.25,
                    config: {
                        refreshEnabled: true,
                        refreshInterval: 30000
                    }
                },
                {
                    id: 'refresh_60s',
                    name: '60 Second Refresh',
                    weight: 0.25,
                    config: {
                        refreshEnabled: true,
                        refreshInterval: 60000
                    }
                },
                {
                    id: 'smart_refresh',
                    name: 'Smart Refresh (Viewable Only)',
                    weight: 0.25,
                    config: {
                        refreshEnabled: true,
                        refreshInterval: 45000,
                        viewableOnly: true
                    }
                }
            ],
            metrics: ['revenue', 'viewability', 'user_experience'],
            duration: 7 // days
        });

        // Lazy loading experiment
        this.createExperiment('lazy_loading', {
            name: 'Lazy Loading Strategy',
            description: 'Test different lazy loading thresholds',
            variants: [
                {
                    id: 'eager',
                    name: 'Eager Loading',
                    weight: 0.33,
                    config: {
                        lazyLoad: false
                    }
                },
                {
                    id: 'standard_lazy',
                    name: 'Standard Lazy (200px)',
                    weight: 0.34,
                    config: {
                        lazyLoad: true,
                        rootMargin: '200px'
                    }
                },
                {
                    id: 'aggressive_lazy',
                    name: 'Aggressive Lazy (500px)',
                    weight: 0.33,
                    config: {
                        lazyLoad: true,
                        rootMargin: '500px'
                    }
                }
            ],
            metrics: ['page_speed', 'viewability', 'revenue'],
            duration: 7 // days
        });
    }

    /**
     * Create a new experiment
     */
    createExperiment(id, config) {
        if (this.experiments[id]) {
            console.warn(`Experiment ${id} already exists`);
            return;
        }

        this.experiments[id] = {
            id: id,
            ...config,
            status: 'active',
            startDate: Date.now(),
            endDate: Date.now() + (config.duration * 24 * 60 * 60 * 1000),
            participants: 0,
            results: {}
        };

        // Initialize results for each variant
        config.variants.forEach(variant => {
            this.experiments[id].results[variant.id] = {
                participants: 0,
                conversions: 0,
                metrics: {}
            };

            // Initialize metrics
            config.metrics.forEach(metric => {
                this.experiments[id].results[variant.id].metrics[metric] = {
                    count: 0,
                    sum: 0,
                    min: null,
                    max: null
                };
            });
        });

        if (this.config.debugMode) {
            console.log(`Experiment created: ${id}`, this.experiments[id]);
        }
    }

    /**
     * Get user's variant for an experiment
     */
    getUserVariant(experimentId) {
        const experiment = this.experiments[experimentId];
        if (!experiment || experiment.status !== 'active') {
            return null;
        }

        // Check if experiment has ended
        if (Date.now() > experiment.endDate) {
            this.endExperiment(experimentId);
            return null;
        }

        // Check if user already assigned
        if (this.userAssignments[experimentId]) {
            return this.userAssignments[experimentId];
        }

        // Assign user to variant
        const variant = this.assignUserToVariant(experiment);
        this.userAssignments[experimentId] = variant.id;
        this.saveUserAssignments();

        // Track participation
        experiment.participants++;
        experiment.results[variant.id].participants++;

        // Send event
        this.trackEvent('experiment_participation', {
            experiment: experimentId,
            variant: variant.id,
            timestamp: Date.now()
        });

        return variant.id;
    }

    /**
     * Assign user to variant based on weights
     */
    assignUserToVariant(experiment) {
        const random = Math.random();
        let cumulative = 0;

        for (const variant of experiment.variants) {
            cumulative += variant.weight;
            if (random < cumulative) {
                return variant;
            }
        }

        // Fallback to last variant
        return experiment.variants[experiment.variants.length - 1];
    }

    /**
     * Get variant configuration
     */
    getVariantConfig(experimentId, variantId) {
        const experiment = this.experiments[experimentId];
        if (!experiment) return null;

        const variant = experiment.variants.find(v => v.id === variantId);
        return variant ? variant.config : null;
    }

    /**
     * Track metric for an experiment
     */
    trackMetric(experimentId, metric, value = 1) {
        const experiment = this.experiments[experimentId];
        if (!experiment || experiment.status !== 'active') return;

        const variantId = this.userAssignments[experimentId];
        if (!variantId) return;

        const result = experiment.results[variantId];
        if (!result || !result.metrics[metric]) return;

        // Update metric
        const metricData = result.metrics[metric];
        metricData.count++;
        metricData.sum += value;
        metricData.min = metricData.min === null ? value : Math.min(metricData.min, value);
        metricData.max = metricData.max === null ? value : Math.max(metricData.max, value);

        // Send event
        this.trackEvent('experiment_metric', {
            experiment: experimentId,
            variant: variantId,
            metric: metric,
            value: value,
            timestamp: Date.now()
        });

        // Save results periodically
        if (metricData.count % 10 === 0) {
            this.saveResults();
        }
    }

    /**
     * Track conversion for an experiment
     */
    trackConversion(experimentId, value = 1) {
        const experiment = this.experiments[experimentId];
        if (!experiment || experiment.status !== 'active') return;

        const variantId = this.userAssignments[experimentId];
        if (!variantId) return;

        const result = experiment.results[variantId];
        if (!result) return;

        result.conversions++;

        // Track as revenue if value provided
        if (value > 0) {
            this.trackMetric(experimentId, 'revenue', value);
        }

        // Send event
        this.trackEvent('experiment_conversion', {
            experiment: experimentId,
            variant: variantId,
            value: value,
            timestamp: Date.now()
        });
    }

    /**
     * Calculate experiment results
     */
    calculateResults(experimentId) {
        const experiment = this.experiments[experimentId];
        if (!experiment) return null;

        const results = {
            experiment: experimentId,
            name: experiment.name,
            status: experiment.status,
            duration: Date.now() - experiment.startDate,
            participants: experiment.participants,
            variants: []
        };

        // Calculate stats for each variant
        experiment.variants.forEach(variant => {
            const variantResult = experiment.results[variant.id];
            const stats = {
                id: variant.id,
                name: variant.name,
                participants: variantResult.participants,
                conversions: variantResult.conversions,
                conversionRate: variantResult.participants > 0 ? 
                    (variantResult.conversions / variantResult.participants * 100).toFixed(2) : 0,
                metrics: {}
            };

            // Calculate metric averages
            Object.entries(variantResult.metrics).forEach(([metric, data]) => {
                stats.metrics[metric] = {
                    average: data.count > 0 ? (data.sum / data.count).toFixed(2) : 0,
                    total: data.sum,
                    min: data.min,
                    max: data.max,
                    count: data.count
                };
            });

            results.variants.push(stats);
        });

        // Determine winner
        results.winner = this.determineWinner(results.variants);

        // Calculate statistical significance
        if (results.variants.length === 2) {
            results.significance = this.calculateSignificance(
                results.variants[0],
                results.variants[1]
            );
        }

        return results;
    }

    /**
     * Determine winner of experiment
     */
    determineWinner(variants) {
        if (variants.length === 0) return null;

        // Sort by conversion rate
        const sorted = [...variants].sort((a, b) => 
            parseFloat(b.conversionRate) - parseFloat(a.conversionRate)
        );

        const winner = sorted[0];
        const second = sorted[1];

        // Only declare winner if there's sufficient data and difference
        if (winner.participants < 100) {
            return {
                status: 'insufficient_data',
                message: 'Need more participants for reliable results'
            };
        }

        if (second && parseFloat(winner.conversionRate) - parseFloat(second.conversionRate) < 1) {
            return {
                status: 'no_clear_winner',
                message: 'Variants performing similarly'
            };
        }

        return {
            status: 'winner',
            variant: winner.id,
            conversionRate: winner.conversionRate,
            improvement: second ? 
                ((parseFloat(winner.conversionRate) - parseFloat(second.conversionRate)) / 
                 parseFloat(second.conversionRate) * 100).toFixed(2) : 0
        };
    }

    /**
     * Calculate statistical significance (simplified)
     */
    calculateSignificance(variant1, variant2) {
        const n1 = variant1.participants;
        const n2 = variant2.participants;
        const p1 = variant1.conversions / n1;
        const p2 = variant2.conversions / n2;

        if (n1 < 30 || n2 < 30) {
            return {
                significant: false,
                confidence: 0,
                message: 'Insufficient sample size'
            };
        }

        // Pooled proportion
        const p = (variant1.conversions + variant2.conversions) / (n1 + n2);
        
        // Standard error
        const se = Math.sqrt(p * (1 - p) * (1/n1 + 1/n2));
        
        // Z-score
        const z = Math.abs(p1 - p2) / se;
        
        // Simplified confidence calculation
        let confidence = 0;
        if (z > 2.58) confidence = 99;
        else if (z > 1.96) confidence = 95;
        else if (z > 1.64) confidence = 90;
        else confidence = Math.min(z * 40, 89);

        return {
            significant: confidence >= 95,
            confidence: confidence,
            zScore: z.toFixed(2),
            message: confidence >= 95 ? 'Statistically significant' : 'Not significant'
        };
    }

    /**
     * End an experiment
     */
    endExperiment(experimentId) {
        const experiment = this.experiments[experimentId];
        if (!experiment) return;

        experiment.status = 'ended';
        experiment.endDate = Date.now();

        // Calculate final results
        const results = this.calculateResults(experimentId);

        // Send event
        this.trackEvent('experiment_ended', {
            experiment: experimentId,
            results: results,
            timestamp: Date.now()
        });

        // Save results
        this.saveResults();

        if (this.config.debugMode) {
            console.log(`Experiment ended: ${experimentId}`, results);
        }

        return results;
    }

    /**
     * Apply winning variant
     */
    applyWinningVariant(experimentId) {
        const results = this.calculateResults(experimentId);
        if (!results || !results.winner || results.winner.status !== 'winner') {
            return false;
        }

        const experiment = this.experiments[experimentId];
        const winningVariant = experiment.variants.find(v => v.id === results.winner.variant);
        
        if (!winningVariant) return false;

        // Apply winning configuration
        this.applyConfiguration(winningVariant.config);

        // Send event
        this.trackEvent('variant_applied', {
            experiment: experimentId,
            variant: winningVariant.id,
            timestamp: Date.now()
        });

        return true;
    }

    /**
     * Apply configuration
     */
    applyConfiguration(config) {
        // This would integrate with AdLoader to apply the configuration
        if (window.adLoader) {
            Object.entries(config).forEach(([key, value]) => {
                if (window.adLoader.config.hasOwnProperty(key)) {
                    window.adLoader.config[key] = value;
                }
            });
        }
    }

    /**
     * Get all active experiments
     */
    getActiveExperiments() {
        return Object.values(this.experiments)
            .filter(exp => exp.status === 'active' && Date.now() < exp.endDate);
    }

    /**
     * Get experiment status
     */
    getExperimentStatus(experimentId) {
        const experiment = this.experiments[experimentId];
        if (!experiment) return null;

        return {
            id: experimentId,
            name: experiment.name,
            status: experiment.status,
            variant: this.userAssignments[experimentId] || null,
            daysRemaining: Math.ceil((experiment.endDate - Date.now()) / (24 * 60 * 60 * 1000)),
            results: this.calculateResults(experimentId)
        };
    }

    /**
     * Load user assignments from cookie
     */
    loadUserAssignments() {
        const cookie = this.getCookie(this.config.cookieName);
        if (cookie) {
            try {
                this.userAssignments = JSON.parse(decodeURIComponent(cookie));
            } catch (e) {
                this.userAssignments = {};
            }
        }
    }

    /**
     * Save user assignments to cookie
     */
    saveUserAssignments() {
        this.setCookie(
            this.config.cookieName,
            encodeURIComponent(JSON.stringify(this.userAssignments)),
            this.config.cookieDuration
        );
    }

    /**
     * Load results from localStorage
     */
    loadResults() {
        try {
            const stored = localStorage.getItem('ab_test_results');
            if (stored) {
                const data = JSON.parse(stored);
                // Merge with current results
                Object.entries(data.experiments).forEach(([id, results]) => {
                    if (this.experiments[id]) {
                        this.experiments[id].results = results;
                    }
                });
            }
        } catch (e) {
            console.error('Failed to load A/B test results:', e);
        }
    }

    /**
     * Save results to localStorage
     */
    saveResults() {
        try {
            const data = {
                experiments: {},
                timestamp: Date.now()
            };

            Object.entries(this.experiments).forEach(([id, experiment]) => {
                data.experiments[id] = experiment.results;
            });

            localStorage.setItem('ab_test_results', JSON.stringify(data));
        } catch (e) {
            console.error('Failed to save A/B test results:', e);
        }
    }

    /**
     * Get cookie value
     */
    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return null;
    }

    /**
     * Set cookie
     */
    setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    /**
     * Track event
     */
    trackEvent(eventName, data) {
        if (!this.config.analyticsEnabled) return;

        // Send to Google Analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'AB_Testing',
                event_label: data.experiment || 'general',
                value: data.value || 1,
                custom_data: JSON.stringify(data)
            });
        }

        // Custom event
        window.dispatchEvent(new CustomEvent('abtest', {
            detail: {
                event: eventName,
                data: data
            }
        }));
    }

    /**
     * Export results as CSV
     */
    exportResultsAsCSV() {
        const rows = [['Experiment', 'Variant', 'Participants', 'Conversions', 'Conversion Rate', 'Status']];

        Object.entries(this.experiments).forEach(([id, experiment]) => {
            const results = this.calculateResults(id);
            results.variants.forEach(variant => {
                rows.push([
                    experiment.name,
                    variant.name,
                    variant.participants,
                    variant.conversions,
                    variant.conversionRate + '%',
                    experiment.status
                ]);
            });
        });

        const csv = rows.map(row => row.join(',')).join('\n');
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ab-test-results-${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ABTestingFramework;
}

// Auto-initialize if config is available
if (typeof APP_CONFIG !== 'undefined') {
    window.abTesting = new ABTestingFramework({
        enabled: APP_CONFIG.FEATURES?.ENABLE_ADS,
        analyticsEnabled: APP_CONFIG.FEATURES?.ENABLE_ANALYTICS,
        debugMode: APP_CONFIG.APP?.DEBUG_MODE
    });
}