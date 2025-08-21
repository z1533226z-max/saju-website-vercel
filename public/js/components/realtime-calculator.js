/**
 * Real-time Saju Calculator
 * Automatically calculates and displays results as user inputs data
 */

class RealtimeCalculator {
    constructor() {
        this.debounceTimer = null;
        this.debounceDelay = 500; // milliseconds
        this.isCalculating = false;
        this.lastCalculation = null;
        this.requiredFields = ['year', 'month', 'day', 'hour', 'gender'];
        this.init();
    }
    
    init() {
        this.attachEventListeners();
        this.createRealtimeIndicator();
    }
    
    createRealtimeIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'realtime-indicator';
        indicator.className = 'realtime-indicator';
        indicator.innerHTML = `
            <div class="indicator-content">
                <span class="indicator-icon">⚡</span>
                <span class="indicator-text">실시간 계산 활성화</span>
                <label class="realtime-toggle">
                    <input type="checkbox" id="realtime-toggle" checked>
                    <span class="toggle-slider-mini"></span>
                </label>
            </div>
            <div class="calculation-status" id="calculation-status"></div>
        `;
        
        // Add to form or appropriate container
        const formContainer = document.querySelector('.form-container, #input-form, .saju-form');
        if (formContainer) {
            formContainer.insertBefore(indicator, formContainer.firstChild);
        }
        
        // Add toggle listener
        const toggle = document.getElementById('realtime-toggle');
        if (toggle) {
            toggle.addEventListener('change', (e) => {
                this.enabled = e.target.checked;
                this.updateIndicatorStatus();
            });
        }
        
        this.enabled = true;
    }
    
    attachEventListeners() {
        // Listen for date changes from enhanced date picker
        window.addEventListener('dateChanged', (e) => {
            if (this.enabled) {
                this.handleInputChange(e.detail);
            }
        });
        
        // Attach to existing form inputs
        const formInputs = [
            'input[name="birthYear"]',
            'select[name="birthYear"]',
            'input[name="birthMonth"]',
            'select[name="birthMonth"]',
            'input[name="birthDay"]',
            'select[name="birthDay"]',
            'select[name="birthHour"]',
            'input[name="birthTime"]',
            'input[name="gender"]',
            'select[name="gender"]',
            '#year-input',
            '#month-input',
            '#day-input',
            '#hour-input',
            '#gender-input'
        ];
        
        formInputs.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.addEventListener('change', () => {
                    if (this.enabled) {
                        this.handleInputChange();
                    }
                });
                
                // For text inputs, also listen to input event
                if (element.type === 'text' || element.type === 'number') {
                    element.addEventListener('input', () => {
                        if (this.enabled) {
                            this.handleInputChange();
                        }
                    });
                }
            });
        });
        
        // Listen for radio buttons (gender)
        const genderRadios = document.querySelectorAll('input[type="radio"][name="gender"]');
        genderRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                if (this.enabled) {
                    this.handleInputChange();
                }
            });
        });
    }
    
    handleInputChange(eventData = null) {
        // Clear existing timer
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // Show calculating status
        this.showStatus('입력 중...', 'typing');
        
        // Set new timer
        this.debounceTimer = setTimeout(() => {
            this.checkAndCalculate();
        }, this.debounceDelay);
    }
    
    checkAndCalculate() {
        // Collect form data
        const formData = this.collectFormData();
        
        // Check if all required fields are filled
        const isComplete = this.validateFormData(formData);
        
        if (isComplete) {
            // Check if data has changed since last calculation
            if (this.hasDataChanged(formData)) {
                this.performCalculation(formData);
            } else {
                this.showStatus('이미 계산됨', 'completed');
            }
        } else {
            // Show which fields are missing
            const missingFields = this.getMissingFields(formData);
            this.showStatus(`필요 항목: ${missingFields.join(', ')}`, 'incomplete');
            
            // Clear results if incomplete
            this.clearResults();
        }
    }
    
    collectFormData() {
        const data = {};
        
        // Try different possible input selectors
        data.year = this.getInputValue(['#year-input', 'input[name="birthYear"]', 'select[name="birthYear"]']);
        data.month = this.getInputValue(['#month-input', 'input[name="birthMonth"]', 'select[name="birthMonth"]']);
        data.day = this.getInputValue(['#day-input', 'input[name="birthDay"]', 'select[name="birthDay"]']);
        data.hour = this.getInputValue(['#hour-input', '#selectedHour', 'select[name="birthHour"]', 'input[name="birthTime"]']);
        
        // Gender (could be radio buttons or select)
        const genderRadio = document.querySelector('input[type="radio"][name="gender"]:checked');
        if (genderRadio) {
            data.gender = genderRadio.value;
        } else {
            data.gender = this.getInputValue(['#gender-input', 'select[name="gender"]']);
        }
        
        // Calendar type
        const calendarToggle = document.getElementById('calendar-type-toggle');
        const calendarRadio = document.querySelector('input[type="radio"][name="calendarType"]:checked');
        
        if (calendarToggle) {
            data.isLunar = calendarToggle.checked;
        } else if (calendarRadio) {
            data.isLunar = calendarRadio.value === 'lunar';
        } else {
            data.isLunar = false;
        }
        
        return data;
    }
    
    getInputValue(selectors) {
        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element && element.value) {
                return element.value;
            }
        }
        return null;
    }
    
    validateFormData(data) {
        return this.requiredFields.every(field => {
            return data[field] && data[field].toString().trim() !== '';
        });
    }
    
    getMissingFields(data) {
        const fieldNames = {
            year: '년도',
            month: '월',
            day: '일',
            hour: '시간',
            gender: '성별'
        };
        
        return this.requiredFields
            .filter(field => !data[field] || data[field].toString().trim() === '')
            .map(field => fieldNames[field] || field);
    }
    
    hasDataChanged(data) {
        if (!this.lastCalculation) return true;
        
        return JSON.stringify(data) !== JSON.stringify(this.lastCalculation);
    }
    
    async performCalculation(formData) {
        if (this.isCalculating) return;
        
        this.isCalculating = true;
        this.showStatus('계산 중...', 'calculating');
        
        try {
            // Prepare request data
            const requestData = {
                birthDate: `${formData.year}-${String(formData.month).padStart(2, '0')}-${String(formData.day).padStart(2, '0')}`,
                birthTime: formData.hour,
                gender: formData.gender,
                isLunar: formData.isLunar || false
            };
            
            // Call API
            const response = await fetch('/api/saju/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success || result.data) {
                // Update results
                this.updateResults(result.data || result);
                this.lastCalculation = formData;
                this.showStatus('계산 완료!', 'completed');
                
                // Trigger custom event
                const event = new CustomEvent('sajuCalculated', { 
                    detail: result.data || result 
                });
                window.dispatchEvent(event);
                
                // Show results section with smooth animation
                this.showResultsSection();
            } else {
                this.showStatus('계산 오류', 'error');
                console.error('Calculation error:', result.message);
            }
        } catch (error) {
            console.error('Real-time calculation error:', error);
            this.showStatus('연결 오류', 'error');
            
            // Try to use mock data for development
            if (window.location.hostname === 'localhost') {
                this.useMockData(formData);
            }
        } finally {
            this.isCalculating = false;
        }
    }
    
    updateResults(data) {
        // Update basic Saju display
        if (data.year) {
            this.updatePillar('year', data.year);
        }
        if (data.month) {
            this.updatePillar('month', data.month);
        }
        if (data.day) {
            this.updatePillar('day', data.day);
        }
        if (data.hour) {
            this.updatePillar('hour', data.hour);
        }
        
        // Update elements if available
        if (data.elements) {
            this.updateElements(data.elements);
        }
        
        // Update interpretation if available
        if (data.interpretation) {
            this.updateInterpretation(data.interpretation);
        }
        
        // Update any enhanced components
        if (window.sajuComponents) {
            Object.values(window.sajuComponents).forEach(component => {
                if (component && typeof component.updateWithSajuData === 'function') {
                    component.updateWithSajuData(data);
                }
            });
        }
    }
    
    updatePillar(pillar, data) {
        const heavenlyElement = document.querySelector(`#${pillar}-heavenly, .${pillar}-heavenly`);
        const earthlyElement = document.querySelector(`#${pillar}-earthly, .${pillar}-earthly`);
        
        if (heavenlyElement && data.heavenly) {
            heavenlyElement.textContent = data.heavenly_hanja || data.heavenly;
        }
        if (earthlyElement && data.earthly) {
            earthlyElement.textContent = data.earthly_hanja || data.earthly;
        }
    }
    
    updateElements(elements) {
        // Update element distribution display
        const distribution = elements.distribution || elements;
        
        Object.entries(distribution).forEach(([element, count]) => {
            const countElement = document.querySelector(`#element-${element}-count, .element-${element}-count`);
            if (countElement) {
                countElement.textContent = count;
            }
        });
        
        // Update charts if available
        if (window.sajuComponents && window.sajuComponents.charts) {
            window.sajuComponents.charts.updateWithElementData(distribution);
        }
    }
    
    updateInterpretation(interpretation) {
        Object.entries(interpretation).forEach(([key, value]) => {
            const element = document.querySelector(`#interpretation-${key}, .interpretation-${key}`);
            if (element) {
                element.textContent = value;
            }
        });
    }
    
    showResultsSection() {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            // Add animation class
            resultsSection.classList.add('results-appearing');
            resultsSection.style.display = 'block';
            
            // Smooth scroll to results
            setTimeout(() => {
                resultsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 100);
            
            // Remove animation class after animation completes
            setTimeout(() => {
                resultsSection.classList.remove('results-appearing');
            }, 500);
        }
    }
    
    clearResults() {
        // Hide results section if no valid input
        const resultsSection = document.getElementById('results-section');
        if (resultsSection && this.enabled) {
            resultsSection.style.display = 'none';
        }
    }
    
    showStatus(message, type) {
        const statusElement = document.getElementById('calculation-status');
        if (!statusElement) return;
        
        statusElement.textContent = message;
        statusElement.className = `calculation-status ${type}`;
        
        // Add appropriate icon
        let icon = '';
        switch(type) {
            case 'typing': icon = '✏️'; break;
            case 'calculating': icon = '⚙️'; break;
            case 'completed': icon = '✅'; break;
            case 'error': icon = '❌'; break;
            case 'incomplete': icon = 'ℹ️'; break;
        }
        
        if (icon) {
            statusElement.innerHTML = `${icon} ${message}`;
        }
    }
    
    updateIndicatorStatus() {
        const indicator = document.getElementById('realtime-indicator');
        if (indicator) {
            if (this.enabled) {
                indicator.classList.add('active');
                this.showStatus('실시간 계산 활성화', 'completed');
            } else {
                indicator.classList.remove('active');
                this.showStatus('실시간 계산 비활성화', 'incomplete');
            }
        }
    }
    
    useMockData(formData) {
        // Generate mock data for development
        const mockData = {
            year: {
                heavenly: '갑',
                earthly: '자',
                heavenly_hanja: '甲',
                earthly_hanja: '子'
            },
            month: {
                heavenly: '병',
                earthly: '인',
                heavenly_hanja: '丙',
                earthly_hanja: '寅'
            },
            day: {
                heavenly: '무',
                earthly: '진',
                heavenly_hanja: '戊',
                earthly_hanja: '辰'
            },
            hour: {
                heavenly: '경',
                earthly: '신',
                heavenly_hanja: '庚',
                earthly_hanja: '申'
            },
            elements: {
                distribution: {
                    '목': Math.floor(Math.random() * 3) + 1,
                    '화': Math.floor(Math.random() * 3) + 1,
                    '토': Math.floor(Math.random() * 3) + 1,
                    '금': Math.floor(Math.random() * 3) + 1,
                    '수': Math.floor(Math.random() * 3) + 1
                }
            },
            interpretation: {
                personality: '실시간 계산 테스트 - 성격 분석',
                career: '실시간 계산 테스트 - 직업 적성',
                wealth: '실시간 계산 테스트 - 재물운',
                relationship: '실시간 계산 테스트 - 인간관계',
                health: '실시간 계산 테스트 - 건강운'
            }
        };
        
        this.updateResults(mockData);
        this.lastCalculation = formData;
        this.showStatus('테스트 데이터 로드', 'completed');
        this.showResultsSection();
    }
}

// Export for use
window.RealtimeCalculator = RealtimeCalculator;