/**
 * Saju Enhanced Integration
 * Integrates all new components (tabs, charts, timeline, print)
 */

// Initialize enhanced features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeEnhancedFeatures();
});

/**
 * Initialize all enhanced features
 */
function initializeEnhancedFeatures() {
    console.log('Initializing Saju Enhanced Features...');
    
    // Initialize components
    const components = {
        tabs: null,
        charts: null,
        timeline: null,
        printView: null
    };
    
    // Check if results section exists
    const resultsSection = document.getElementById('results-section');
    if (resultsSection) {
        // Add enhanced container
        const enhancedContainer = document.createElement('div');
        enhancedContainer.id = 'saju-enhanced-container';
        enhancedContainer.className = 'saju-enhanced';
        resultsSection.appendChild(enhancedContainer);
        
        // Initialize tabs
        if (typeof SajuTabs !== 'undefined') {
            components.tabs = new SajuTabs('saju-enhanced-container');
            console.log('✓ Tabs initialized');
        }
        
        // Initialize charts
        if (typeof SajuCharts !== 'undefined') {
            components.charts = new SajuCharts();
            console.log('✓ Charts initialized');
        }
        
        // Initialize timeline
        if (typeof FortuneTimeline !== 'undefined') {
            // Create timeline container
            const timelineContainer = document.createElement('div');
            timelineContainer.id = 'fortune-timeline-container';
            resultsSection.appendChild(timelineContainer);
            
            components.timeline = new FortuneTimeline('fortune-timeline-container');
            console.log('✓ Timeline initialized');
        }
        
        // Initialize print view
        if (typeof PrintView !== 'undefined') {
            components.printView = new PrintView();
            console.log('✓ Print view initialized');
        }
    }
    
    // Store components globally
    window.sajuComponents = components;
    
    // Listen for Saju calculation results
    window.addEventListener('sajuCalculated', handleSajuResults);
    
    // Add sample data button for testing
    addTestButton();
}

/**
 * Handle Saju calculation results
 */
function handleSajuResults(event) {
    const sajuData = event.detail;
    
    console.log('Saju results received:', sajuData);
    
    // Update all components with new data
    if (window.sajuComponents) {
        if (window.sajuComponents.tabs) {
            window.sajuComponents.tabs.updateWithSajuData(sajuData);
        }
        
        if (window.sajuComponents.charts) {
            // Update charts with element data
            if (sajuData.elements) {
                const distribution = sajuData.elements.distribution || sajuData.elements;
                window.sajuComponents.charts.initFiveElementsRadar('fiveElementsChart', distribution);
                window.sajuComponents.charts.initFiveElementsBar('fiveElementsBarChart', distribution);
            }
            
            // Update ten gods chart
            if (sajuData.ten_gods) {
                window.sajuComponents.charts.initTenGodsDoughnut('tenGodsChart', sajuData.ten_gods);
            }
        }
        
        if (window.sajuComponents.timeline) {
            window.sajuComponents.timeline.updateWithSajuData(sajuData);
        }
        
        if (window.sajuComponents.printView) {
            window.sajuComponents.printView.updateWithSajuData(sajuData);
        }
    }
}

/**
 * Add test button for development
 */
function addTestButton() {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        const testButton = document.createElement('button');
        testButton.id = 'test-enhanced-features';
        testButton.textContent = '테스트 데이터 로드';
        testButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 10px 20px;
            background: #D4AF37;
            color: #0C0B10;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            z-index: 9999;
        `;
        
        testButton.onclick = loadTestData;
        document.body.appendChild(testButton);
    }
}

/**
 * Load test data for development
 */
function loadTestData() {
    const testData = {
        year: {
            heavenly: '갑',
            earthly: '자',
            heavenly_hanja: '甲',
            earthly_hanja: '子',
            heavenly_element: '목',
            earthly_element: '수'
        },
        month: {
            heavenly: '을',
            earthly: '축',
            heavenly_hanja: '乙',
            earthly_hanja: '丑',
            heavenly_element: '목',
            earthly_element: '토'
        },
        day: {
            heavenly: '병',
            earthly: '인',
            heavenly_hanja: '丙',
            earthly_hanja: '寅',
            heavenly_element: '화',
            earthly_element: '목'
        },
        hour: {
            heavenly: '정',
            earthly: '묘',
            heavenly_hanja: '丁',
            earthly_hanja: '卯',
            heavenly_element: '화',
            earthly_element: '목'
        },
        elements: {
            distribution: {
                '목': 4,
                '화': 2,
                '토': 1,
                '금': 0,
                '수': 1
            },
            total: 8
        },
        ten_gods: {
            '정관': 2,
            '편관': 1,
            '정인': 3,
            '편인': 1,
            '정재': 2,
            '편재': 1,
            '비견': 1,
            '겁재': 0,
            '식신': 1,
            '상관': 0
        },
        interpretation: {
            personality: '일간 병화(丙火)는 태양과 같은 성격으로 밝고 활발하며 리더십이 강합니다.',
            career: '창의적이고 표현력이 뛰어나 예술, 교육, 미디어 분야에 적성이 있습니다.',
            wealth: '정재가 안정적으로 있어 꾸준한 재물운이 예상됩니다.',
            relationship: '정인이 많아 타인에게 도움을 받는 운이 강합니다.',
            health: '화(火)가 다소 강하므로 심장과 혈액순환에 주의가 필요합니다.'
        },
        birthDate: '1990-05-15',
        currentAge: 34
    };
    
    // Dispatch custom event with test data
    const event = new CustomEvent('sajuCalculated', { detail: testData });
    window.dispatchEvent(event);
    
    // Show results section
    const resultsSection = document.getElementById('results-section');
    if (resultsSection) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    console.log('Test data loaded successfully');
}

/**
 * API Integration for real data
 */
async function calculateSaju(formData) {
    try {
        // Show loading state
        showLoading();
        
        // Call API
        const response = await fetch('/api/saju/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const sajuData = await response.json();
        
        // Save to localStorage
        localStorage.setItem('lastSajuResult', JSON.stringify(sajuData));
        localStorage.setItem('sajuFormData', JSON.stringify(formData));
        
        // Dispatch event with results
        const event = new CustomEvent('sajuCalculated', { detail: sajuData });
        window.dispatchEvent(event);
        
        // Show results
        showResults();
        
        return sajuData;
        
    } catch (error) {
        console.error('Error calculating Saju:', error);
        showError('사주 계산 중 오류가 발생했습니다. 다시 시도해주세요.');
        throw error;
    } finally {
        hideLoading();
    }
}

/**
 * UI Helper functions
 */
function showLoading() {
    const loader = document.getElementById('loading-indicator');
    if (loader) loader.style.display = 'block';
}

function hideLoading() {
    const loader = document.getElementById('loading-indicator');
    if (loader) loader.style.display = 'none';
}

function showResults() {
    const resultsSection = document.getElementById('results-section');
    if (resultsSection) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function showError(message) {
    if (typeof showToast === 'function') {
        showToast(message, 5000);
    } else {
        alert(message);
    }
}

// Export functions for external use
window.calculateSaju = calculateSaju;
window.loadTestData = loadTestData;

// CSS files are now loaded directly in index.html with cache-bust params

console.log('Saju Enhanced Features loaded successfully');