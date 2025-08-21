/**
 * API Integration for Saju Website
 */

class SajuAPI {
    constructor(config = APP_CONFIG) {
        this.config = config;
        this.baseURL = config.API.BASE_URL;
        this.endpoints = config.API.ENDPOINTS;
        this.timeout = config.API.TIMEOUT;
        this.retryAttempts = config.API.RETRY_ATTEMPTS;
    }

    /**
     * Make API request with retry logic
     * @param {string} url - API endpoint URL
     * @param {object} options - Fetch options
     * @param {number} retries - Number of retry attempts
     * @returns {Promise} - API response
     */
    async makeRequest(url, options = {}, retries = this.retryAttempts) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);

            if (retries > 0 && !error.name.includes('Abort')) {
                console.log(`Retrying... (${this.retryAttempts - retries + 1}/${this.retryAttempts})`);
                await this.delay(1000 * (this.retryAttempts - retries + 1));
                return this.makeRequest(url, options, retries - 1);
            }

            throw error;
        }
    }

    /**
     * Delay helper for retry logic
     * @param {number} ms - Milliseconds to delay
     * @returns {Promise}
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Calculate Saju
     * @param {object} data - Birth data
     * @returns {Promise} - Saju calculation result
     */
    async calculateSaju(data) {
        const url = `${this.baseURL}${this.endpoints.CALCULATE}`;
        
        // Track with Google Analytics
        if (typeof gtag !== 'undefined' && this.config.FEATURES.ENABLE_ANALYTICS) {
            gtag('event', this.config.ANALYTICS.EVENTS.CALCULATE, {
                calendar_type: data.calendarType,
                year: data.year,
                gender: data.gender
            });
        }

        try {
            const result = await this.makeRequest(url, {
                method: 'POST',
                body: JSON.stringify(data)
            });

            // Save to localStorage if enabled
            if (this.config.FEATURES.ENABLE_HISTORY) {
                this.saveToHistory(data, result);
            }

            return result;
        } catch (error) {
            console.error('Failed to calculate Saju:', error);
            
            // Try to use cached result if available
            const cachedResult = this.getCachedResult(data);
            if (cachedResult) {
                console.log('Using cached result');
                return cachedResult;
            }
            
            throw error;
        }
    }

    /**
     * Get history from localStorage
     * @returns {Array} - History items
     */
    getHistory() {
        try {
            const history = localStorage.getItem(this.config.STORAGE.HISTORY);
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Failed to get history:', error);
            return [];
        }
    }

    /**
     * Save to history
     * @param {object} input - Input data
     * @param {object} result - Calculation result
     */
    saveToHistory(input, result) {
        try {
            const history = this.getHistory();
            const historyItem = {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                input: input,
                result: result
            };
            
            // Keep only last 10 items
            history.unshift(historyItem);
            if (history.length > 10) {
                history.pop();
            }
            
            localStorage.setItem(this.config.STORAGE.HISTORY, JSON.stringify(history));
        } catch (error) {
            console.error('Failed to save history:', error);
        }
    }

    /**
     * Clear history
     */
    clearHistory() {
        try {
            localStorage.removeItem(this.config.STORAGE.HISTORY);
        } catch (error) {
            console.error('Failed to clear history:', error);
        }
    }

    /**
     * Get cached result for specific input
     * @param {object} data - Input data
     * @returns {object|null} - Cached result or null
     */
    getCachedResult(data) {
        const history = this.getHistory();
        const cacheKey = `${data.calendarType}-${data.year}-${data.month}-${data.day}-${data.hour}-${data.gender}`;
        
        for (const item of history) {
            const itemKey = `${item.input.calendarType}-${item.input.year}-${item.input.month}-${item.input.day}-${item.input.hour}-${item.input.gender}`;
            if (itemKey === cacheKey) {
                return item.result;
            }
        }
        
        return null;
    }

    /**
     * Calculate compatibility between two people
     * @param {object} person1 - First person's data
     * @param {object} person2 - Second person's data
     * @returns {Promise} - Compatibility result
     */
    async calculateCompatibility(person1, person2) {
        if (!this.config.FEATURES.ENABLE_COMPATIBILITY) {
            throw new Error('Compatibility feature is disabled');
        }
        
        const url = `${this.baseURL}${this.endpoints.COMPATIBILITY}`;
        
        try {
            const result = await this.makeRequest(url, {
                method: 'POST',
                body: JSON.stringify({ person1, person2 })
            });
            
            return result;
        } catch (error) {
            console.error('Failed to calculate compatibility:', error);
            throw error;
        }
    }

    /**
     * Export result as JSON
     * @param {object} result - Saju result
     * @returns {string} - JSON string
     */
    exportAsJSON(result) {
        try {
            return JSON.stringify(result, null, 2);
        } catch (error) {
            console.error('Failed to export as JSON:', error);
            throw error;
        }
    }

    /**
     * Export result as text
     * @param {object} result - Saju result
     * @returns {string} - Formatted text
     */
    exportAsText(result) {
        try {
            let text = '사주팔자 분석 결과\n';
            text += '==================\n\n';
            
            // Four Pillars
            text += '사주 구성:\n';
            text += `년주: ${result.fourPillars.year.heavenlyStem} ${result.fourPillars.year.earthlyBranch}\n`;
            text += `월주: ${result.fourPillars.month.heavenlyStem} ${result.fourPillars.month.earthlyBranch}\n`;
            text += `일주: ${result.fourPillars.day.heavenlyStem} ${result.fourPillars.day.earthlyBranch}\n`;
            text += `시주: ${result.fourPillars.hour.heavenlyStem} ${result.fourPillars.hour.earthlyBranch}\n\n`;
            
            // Five Elements
            text += '오행 분석:\n';
            for (const [element, count] of Object.entries(result.fiveElements)) {
                text += `${element}: ${count}\n`;
            }
            text += '\n';
            
            // Interpretation
            text += '해석:\n';
            text += `성격: ${result.interpretation.personality}\n`;
            text += `운세: ${result.interpretation.fortune}\n`;
            text += `건강: ${result.interpretation.health}\n`;
            text += `재물: ${result.interpretation.wealth}\n`;
            
            return text;
        } catch (error) {
            console.error('Failed to export as text:', error);
            throw error;
        }
    }

    /**
     * Share result URL
     * @param {object} result - Saju result
     * @returns {string} - Shareable URL
     */
    generateShareURL(result) {
        try {
            const baseURL = window.location.origin + window.location.pathname;
            const params = new URLSearchParams({
                y: result.input.year,
                m: result.input.month,
                d: result.input.day,
                h: result.input.hour,
                g: result.input.gender,
                c: result.input.calendarType
            });
            
            return `${baseURL}?${params.toString()}`;
        } catch (error) {
            console.error('Failed to generate share URL:', error);
            throw error;
        }
    }

    /**
     * Parse share URL parameters
     * @returns {object|null} - Parsed parameters or null
     */
    parseShareURL() {
        try {
            const params = new URLSearchParams(window.location.search);
            
            if (!params.has('y')) {
                return null;
            }
            
            return {
                year: parseInt(params.get('y')),
                month: parseInt(params.get('m')),
                day: parseInt(params.get('d')),
                hour: params.get('h'),
                gender: params.get('g'),
                calendarType: params.get('c') || 'solar'
            };
        } catch (error) {
            console.error('Failed to parse share URL:', error);
            return null;
        }
    }

    /**
     * Validate input data
     * @param {object} data - Input data to validate
     * @returns {object} - Validation result
     */
    validateInput(data) {
        const errors = [];
        
        // Validate year
        if (!data.year || data.year < this.config.VALIDATION.MIN_YEAR || data.year > this.config.VALIDATION.MAX_YEAR) {
            errors.push(`년도는 ${this.config.VALIDATION.MIN_YEAR}년부터 ${this.config.VALIDATION.MAX_YEAR}년 사이여야 합니다.`);
        }
        
        // Validate month
        if (!data.month || data.month < 1 || data.month > 12) {
            errors.push('올바른 월을 선택해주세요.');
        }
        
        // Validate day
        if (!data.day || data.day < 1 || data.day > 31) {
            errors.push('올바른 일을 선택해주세요.');
        }
        
        // Validate hour
        if (!data.hour) {
            errors.push('출생 시간을 선택해주세요.');
        }
        
        // Validate gender
        if (!data.gender || (data.gender !== 'male' && data.gender !== 'female')) {
            errors.push('성별을 선택해주세요.');
        }
        
        // Validate calendar type
        if (!data.calendarType || (data.calendarType !== 'solar' && data.calendarType !== 'lunar')) {
            errors.push('양력/음력을 선택해주세요.');
        }
        
        return {
            valid: errors.length === 0,
            errors: errors
        };
    }
}

// Create global instance
const sajuAPI = new SajuAPI();

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SajuAPI;
}