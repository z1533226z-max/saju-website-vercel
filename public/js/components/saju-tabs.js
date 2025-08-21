/**
 * Saju Tabs Component
 * Handles tab navigation for different Saju views
 */

class SajuTabs {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.activeTab = 'basic';
        this.tabs = {
            basic: '기본정보',
            detail: '상세분석',
            tenGods: '십성분석',
            majorFortune: '대운분석',
            compatibility: '궁합분석'
        };
        
        this.init();
    }
    
    init() {
        if (!this.container) return;
        
        this.renderTabs();
        this.bindEvents();
        this.showTab(this.activeTab);
    }
    
    renderTabs() {
        const tabsHTML = `
            <div class="saju-tabs-container">
                <div class="tabs-header">
                    ${Object.entries(this.tabs).map(([key, label]) => `
                        <button class="tab-button" data-tab="${key}">
                            <span class="tab-icon ${this.getTabIcon(key)}"></span>
                            <span class="tab-label">${label}</span>
                        </button>
                    `).join('')}
                </div>
                <div class="tabs-content">
                    ${Object.keys(this.tabs).map(key => `
                        <div class="tab-panel" id="tab-${key}" data-tab-content="${key}">
                            <!-- Content will be loaded dynamically -->
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        this.container.innerHTML = tabsHTML;
    }
    
    getTabIcon(tab) {
        const icons = {
            basic: 'icon-basic',
            detail: 'icon-detail',
            tenGods: 'icon-tengods',
            majorFortune: 'icon-fortune',
            compatibility: 'icon-compatibility'
        };
        return icons[tab] || '';
    }
    
    bindEvents() {
        const buttons = this.container.querySelectorAll('.tab-button');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                this.showTab(tab);
            });
        });
    }
    
    showTab(tabName) {
        // Update active button
        const buttons = this.container.querySelectorAll('.tab-button');
        buttons.forEach(button => {
            if (button.dataset.tab === tabName) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
        
        // Update active panel
        const panels = this.container.querySelectorAll('.tab-panel');
        panels.forEach(panel => {
            if (panel.dataset.tabContent === tabName) {
                panel.classList.add('active');
                panel.style.display = 'block';
                this.loadTabContent(tabName, panel);
            } else {
                panel.classList.remove('active');
                panel.style.display = 'none';
            }
        });
        
        this.activeTab = tabName;
        
        // Track tab change in analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'tab_change', {
                'event_category': 'engagement',
                'event_label': tabName
            });
        }
    }
    
    loadTabContent(tabName, panel) {
        // Check if content already loaded
        if (panel.dataset.loaded === 'true') return;
        
        switch(tabName) {
            case 'basic':
                this.loadBasicInfo(panel);
                break;
            case 'detail':
                this.loadDetailAnalysis(panel);
                break;
            case 'tenGods':
                this.loadTenGodsAnalysis(panel);
                break;
            case 'majorFortune':
                this.loadMajorFortune(panel);
                break;
            case 'compatibility':
                this.loadCompatibility(panel);
                break;
        }
        
        panel.dataset.loaded = 'true';
    }
    
    loadBasicInfo(panel) {
        panel.innerHTML = `
            <div class="basic-info-content">
                <h3>사주 기본 정보</h3>
                
                <!-- Four Pillars Table -->
                <div class="saju-pillars-table">
                    <div class="pillar-column year-pillar">
                        <div class="pillar-header">년주 (年柱)</div>
                        <div class="stem-branch">
                            <div class="heavenly-stem" id="year-stem">甲</div>
                            <div class="earthly-branch" id="year-branch">子</div>
                        </div>
                        <div class="pillar-element">木水</div>
                    </div>
                    
                    <div class="pillar-column month-pillar">
                        <div class="pillar-header">월주 (月柱)</div>
                        <div class="stem-branch">
                            <div class="heavenly-stem" id="month-stem">乙</div>
                            <div class="earthly-branch" id="month-branch">丑</div>
                        </div>
                        <div class="pillar-element">木土</div>
                    </div>
                    
                    <div class="pillar-column day-pillar">
                        <div class="pillar-header">일주 (日柱)</div>
                        <div class="stem-branch">
                            <div class="heavenly-stem" id="day-stem">丙</div>
                            <div class="earthly-branch" id="day-branch">寅</div>
                        </div>
                        <div class="pillar-element">火木</div>
                    </div>
                    
                    <div class="pillar-column hour-pillar">
                        <div class="pillar-header">시주 (時柱)</div>
                        <div class="stem-branch">
                            <div class="heavenly-stem" id="hour-stem">丁</div>
                            <div class="earthly-branch" id="hour-branch">卯</div>
                        </div>
                        <div class="pillar-element">火木</div>
                    </div>
                </div>
                
                <!-- Five Elements Summary -->
                <div class="five-elements-summary">
                    <h4>오행 분포</h4>
                    <canvas id="fiveElementsChart"></canvas>
                </div>
                
                <!-- Basic Interpretation -->
                <div class="basic-interpretation">
                    <h4>기본 해석</h4>
                    <div id="basic-interpretation-text">
                        <!-- Interpretation will be loaded here -->
                    </div>
                </div>
            </div>
        `;
        
        // Initialize Five Elements chart
        setTimeout(() => this.initFiveElementsChart(), 100);
    }
    
    loadDetailAnalysis(panel) {
        panel.innerHTML = `
            <div class="detail-analysis-content">
                <h3>상세 분석</h3>
                
                <div class="analysis-sections">
                    <div class="analysis-section">
                        <h4>일간 분석</h4>
                        <div id="day-master-analysis">
                            <p>일간의 강약과 용신 분석 내용이 표시됩니다.</p>
                        </div>
                    </div>
                    
                    <div class="analysis-section">
                        <h4>격국 판단</h4>
                        <div id="structure-analysis">
                            <p>사주의 격국과 특별 격국 여부를 분석합니다.</p>
                        </div>
                    </div>
                    
                    <div class="analysis-section">
                        <h4>용신 · 희신 · 기신</h4>
                        <div id="useful-gods-analysis">
                            <p>용신과 희신, 기신을 판단하여 운의 흐름을 파악합니다.</p>
                        </div>
                    </div>
                    
                    <div class="analysis-section">
                        <h4>신살 분석</h4>
                        <div id="shinshal-analysis">
                            <p>사주에 있는 신살과 그 영향을 분석합니다.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    loadTenGodsAnalysis(panel) {
        panel.innerHTML = `
            <div class="ten-gods-content">
                <h3>십성 분석</h3>
                
                <!-- Ten Gods Distribution Chart -->
                <div class="ten-gods-chart-container">
                    <h4>십성 분포도</h4>
                    <canvas id="tenGodsChart"></canvas>
                </div>
                
                <!-- Ten Gods Details -->
                <div class="ten-gods-details">
                    <div class="ten-god-item">
                        <span class="god-name">정관 (正官)</span>
                        <div class="god-bar">
                            <div class="god-fill" style="width: 20%"></div>
                        </div>
                        <span class="god-count">2개</span>
                    </div>
                    
                    <div class="ten-god-item">
                        <span class="god-name">편관 (偏官)</span>
                        <div class="god-bar">
                            <div class="god-fill" style="width: 10%"></div>
                        </div>
                        <span class="god-count">1개</span>
                    </div>
                    
                    <div class="ten-god-item">
                        <span class="god-name">정인 (正印)</span>
                        <div class="god-bar">
                            <div class="god-fill" style="width: 30%"></div>
                        </div>
                        <span class="god-count">3개</span>
                    </div>
                    
                    <div class="ten-god-item">
                        <span class="god-name">편인 (偏印)</span>
                        <div class="god-bar">
                            <div class="god-fill" style="width: 10%"></div>
                        </div>
                        <span class="god-count">1개</span>
                    </div>
                    
                    <div class="ten-god-item">
                        <span class="god-name">정재 (正財)</span>
                        <div class="god-bar">
                            <div class="god-fill" style="width: 20%"></div>
                        </div>
                        <span class="god-count">2개</span>
                    </div>
                </div>
                
                <!-- Ten Gods Interpretation -->
                <div class="ten-gods-interpretation">
                    <h4>십성 해석</h4>
                    <div id="ten-gods-interpretation-text">
                        <p>십성의 분포와 상호 관계를 통한 성격과 운명 분석</p>
                    </div>
                </div>
            </div>
        `;
        
        // Initialize Ten Gods chart
        setTimeout(() => this.initTenGodsChart(), 100);
    }
    
    loadMajorFortune(panel) {
        panel.innerHTML = `
            <div class="major-fortune-content">
                <h3>대운 분석</h3>
                
                <!-- Fortune Timeline -->
                <div class="fortune-timeline">
                    <h4>대운 흐름도</h4>
                    <div class="timeline-container">
                        <canvas id="fortuneTimeline"></canvas>
                    </div>
                </div>
                
                <!-- Current Major Fortune -->
                <div class="current-fortune">
                    <h4>현재 대운</h4>
                    <div class="fortune-period">
                        <span class="period-age">31-40세</span>
                        <span class="period-stems">戊申 대운</span>
                        <span class="period-element">土金</span>
                    </div>
                    <div class="fortune-description">
                        <p>현재 대운의 특징과 주의사항이 표시됩니다.</p>
                    </div>
                </div>
                
                <!-- Yearly Fortune -->
                <div class="yearly-fortune">
                    <h4>연운 (세운)</h4>
                    <div class="year-grid">
                        <div class="year-item current">
                            <span class="year">2024</span>
                            <span class="stems">甲辰</span>
                            <span class="element">木土</span>
                        </div>
                        <div class="year-item">
                            <span class="year">2025</span>
                            <span class="stems">乙巳</span>
                            <span class="element">木火</span>
                        </div>
                        <div class="year-item">
                            <span class="year">2026</span>
                            <span class="stems">丙午</span>
                            <span class="element">火火</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Initialize Fortune Timeline
        setTimeout(() => this.initFortuneTimeline(), 100);
    }
    
    loadCompatibility(panel) {
        panel.innerHTML = `
            <div class="compatibility-content">
                <h3>궁합 분석</h3>
                
                <div class="compatibility-input">
                    <h4>상대방 정보 입력</h4>
                    <form id="compatibility-form">
                        <div class="form-group">
                            <label>생년월일</label>
                            <input type="date" id="partner-birthdate" required>
                        </div>
                        <div class="form-group">
                            <label>출생시간</label>
                            <select id="partner-birthtime">
                                <option value="">모름</option>
                                <option value="00:00">자시 (23:00-01:00)</option>
                                <option value="02:00">축시 (01:00-03:00)</option>
                                <option value="04:00">인시 (03:00-05:00)</option>
                                <option value="06:00">묘시 (05:00-07:00)</option>
                                <option value="08:00">진시 (07:00-09:00)</option>
                                <option value="10:00">사시 (09:00-11:00)</option>
                                <option value="12:00">오시 (11:00-13:00)</option>
                                <option value="14:00">미시 (13:00-15:00)</option>
                                <option value="16:00">신시 (15:00-17:00)</option>
                                <option value="18:00">유시 (17:00-19:00)</option>
                                <option value="20:00">술시 (19:00-21:00)</option>
                                <option value="22:00">해시 (21:00-23:00)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>성별</label>
                            <select id="partner-gender" required>
                                <option value="남">남성</option>
                                <option value="여">여성</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>관계 유형</label>
                            <select id="relationship-type">
                                <option value="lover">연인</option>
                                <option value="marriage">부부</option>
                                <option value="business">사업 파트너</option>
                                <option value="family">가족</option>
                            </select>
                        </div>
                        <button type="submit" class="btn-calculate-compatibility">
                            궁합 계산하기
                        </button>
                    </form>
                </div>
                
                <div class="compatibility-result" id="compatibility-result" style="display: none;">
                    <!-- Compatibility results will be displayed here -->
                </div>
            </div>
        `;
        
        // Bind compatibility form events
        this.bindCompatibilityEvents();
    }
    
    initFiveElementsChart() {
        const ctx = document.getElementById('fiveElementsChart');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['목(木)', '화(火)', '토(土)', '금(金)', '수(水)'],
                datasets: [{
                    label: '오행 분포',
                    data: [3, 2, 1, 2, 2],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 5,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    initTenGodsChart() {
        const ctx = document.getElementById('tenGodsChart');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['정관', '편관', '정인', '편인', '정재', '편재', '비견', '겁재', '식신', '상관'],
                datasets: [{
                    data: [2, 1, 3, 1, 2, 1, 1, 0, 1, 0],
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40',
                        '#FF6384',
                        '#C9CBCF',
                        '#4BC0C0',
                        '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
    
    initFortuneTimeline() {
        const ctx = document.getElementById('fortuneTimeline');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80'],
                datasets: [{
                    label: '운세 흐름',
                    data: [60, 65, 70, 85, 75, 80, 70, 65],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    bindCompatibilityEvents() {
        const form = document.getElementById('compatibility-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // Get form values
                const partnerData = {
                    birthdate: document.getElementById('partner-birthdate').value,
                    birthtime: document.getElementById('partner-birthtime').value,
                    gender: document.getElementById('partner-gender').value,
                    relationshipType: document.getElementById('relationship-type').value
                };
                
                // Calculate compatibility (would call API in real implementation)
                await this.calculateCompatibility(partnerData);
            });
        }
    }
    
    async calculateCompatibility(partnerData) {
        // Show loading state
        const resultDiv = document.getElementById('compatibility-result');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<p>궁합을 계산하고 있습니다...</p>';
        
        // Simulate API call
        setTimeout(() => {
            resultDiv.innerHTML = `
                <h4>궁합 결과</h4>
                <div class="compatibility-score">
                    <div class="score-circle">
                        <span class="score-value">78</span>
                        <span class="score-label">점</span>
                    </div>
                    <div class="score-description">
                        <p class="score-level">좋은 궁합</p>
                        <p class="score-text">서로를 이해하고 보완하는 좋은 관계입니다.</p>
                    </div>
                </div>
                <div class="compatibility-details">
                    <h5>세부 분석</h5>
                    <ul>
                        <li>오행 균형: ★★★★☆</li>
                        <li>십성 조화: ★★★☆☆</li>
                        <li>일간 궁합: ★★★★☆</li>
                        <li>지지 관계: ★★★★★</li>
                    </ul>
                </div>
            `;
        }, 1500);
    }
    
    updateWithSajuData(sajuData) {
        // Update the displayed data with actual Saju calculation results
        if (!sajuData) return;
        
        // Update basic info
        if (this.activeTab === 'basic') {
            // Update pillars
            if (sajuData.year) {
                document.querySelector('#year-stem').textContent = sajuData.year.heavenly_hanja || sajuData.year.heavenly;
                document.querySelector('#year-branch').textContent = sajuData.year.earthly_hanja || sajuData.year.earthly;
            }
            // ... update other pillars
            
            // Update five elements chart
            if (sajuData.elements && sajuData.elements.distribution) {
                this.updateFiveElementsChart(sajuData.elements.distribution);
            }
        }
    }
    
    updateFiveElementsChart(distribution) {
        const chart = Chart.getChart('fiveElementsChart');
        if (chart && distribution) {
            chart.data.datasets[0].data = [
                distribution['목'] || 0,
                distribution['화'] || 0,
                distribution['토'] || 0,
                distribution['금'] || 0,
                distribution['수'] || 0
            ];
            chart.update();
        }
    }
}

// Export for use
window.SajuTabs = SajuTabs;